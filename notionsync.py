import os
import logging
import requests as req
from time import sleep
from dotenv import load_dotenv

# ---------------------------- CONFIG ----------------------------

# Setup logger
logging.basicConfig(format='%(asctime)s === %(levelname)s === %(message)s', level=logging.INFO)

# Import secrets from .env
load_dotenv()

HTTP_HEADER = {
    'Authorization': f"Bearer {os.environ.get('NOTION_INTEGRATION_API_KEY')}",
    'Notion-Version': '2022-02-22',
    'Content-Type': 'application/json'
}

# ---------------------------- FUNCTIONS ----------------------------

def get_origin_name(project_id):
    """ Get the name of the Origin for a given Project

    Args:
        project_id (str): The page UID of the Project

    Returns:
        str: The plaintext name of the Origin for the Project
    """
    # Fetch Project page
    r_project = req.get(
        f'https://api.notion.com/v1/pages/{project_id}',
        headers=HTTP_HEADER
    )

    # If HTTP error, raise exception
    r_project.raise_for_status()

    # Extract the UID of the given Project's Origin page
    origin_id = r_project.json().get('properties').get('Origin').get('relation')[0].get('id')

    # Fetch Origin page
    r_origin = req.get(
        f'https://api.notion.com/v1/pages/{origin_id}',
        headers=HTTP_HEADER
    )

    # If HTTP error, raise exception
    r_origin.raise_for_status()
    
    # Return the plaintext name of the Origin
    return r_origin.json().get('properties').get('Name').get('title')[0].get('plain_text')

def update_origin_name(page_id, origin_name):
    """Update the Origin property of a Project

    Args:
        page_id (str):  The UID of the Project
        origin_name (str): The new Origin name value in plaintext
    """
    r = req.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=HTTP_HEADER,
        json={
            "properties": {
                "Origin": {
                    "select": {
                        "name": origin_name
                    }
                }
            }
        }
    )
    
    # If HTTP error, raise exception
    r.raise_for_status()

def fetch_db(db_id):
    """Fetch a Notion database

    Returns:
        dict: The returned database as a JSON-serialisable dict (removes HTTP request guff)
    """
    r = req.post(
        f'https://api.notion.com/v1/databases/{db_id}/query',
        headers=HTTP_HEADER,
        # Notion filter payload; stops us getting 'Completed' tasks which don't appear in the todo list
        json={
            "filter": {
                "property": "Priority",
                "select": {
                    "does_not_equal": "Completed"
                }
            }
        }
    )

    # If HTTP error, raise exception
    r.raise_for_status()

    return r.json()['results']

def main():
    # Fetch the to-do database
    try:
        db = fetch_db(os.environ.get('NOTION_TARGET_DB_ID'))
        logging.debug(f"FETCH successful of database {os.environ.get('NOTION_TARGET_DB_ID')}")
    
    except req.HTTPError as e:
        logging.error(f"FETCH unsuccessful of database {os.environ.get('NOTION_TARGET_DB_ID')} (returned {e.response.status_code})")
        return

    # Iterate through every to-do item
    for item in db:
        # Read the item's Project property
        project = item.get('properties').get('Project').get('relation')

        # Only update the Origin property if the item has a Project property
        if project:
            # Get UID of item's current Origin
            current_origin_name = item.get('properties').get('Origin').get('select')

            # Ask Notion for the true Origin name for the given Project (plaintext)
            try:
                true_origin_name = get_origin_name(project[0].get('id'))

            except req.HTTPError as e:
                logging.error(f"FETCH unsuccessful of Project {project[0].get('id')} (returned {e.response.status_code})")
                continue

            # If the item has no Origin property, or if the Origin property is out-of-date, update it
            try:
                if not current_origin_name:
                    update_origin_name(item.get('id'), true_origin_name)
                    logging.info(f"PATCH successful to page {item.get('id')} ('{current_origin_name}' -> '{true_origin_name}')")

                elif (current_origin_name.get('name') != true_origin_name):
                    update_origin_name(item.get('id'), true_origin_name)
                    logging.info(f"PATCH successful to page {item.get('id')} ('{current_origin_name}' -> '{true_origin_name}')")

                
            except req.HTTPError as e:
                logging.error(f"PATCH unsuccessful for page {item.get('id')} (returned {e.response.status_code} when setting Origin to '{true_origin_name}')")
                continue

if __name__ == '__main__':
    logging.info('♥ notionsync by mhmatthall === sync started')

    # Print imported variables
    logging.debug(f"targeting notion db {os.environ.get('NOTION_TARGET_DB_ID')}")
    logging.debug(f"using api key {os.environ.get('NOTION_INTEGRATION_API_KEY')}")

    # Less go baybee
    try:
        main()
        logging.info('♥ notionsync by mhmatthall === sync completed')
    
    except:
        logging.exception('Fatal error:')
