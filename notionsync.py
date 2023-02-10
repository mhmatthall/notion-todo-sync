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
        project_id (str): The page ID of the Project

    Returns:
        str: The plaintext name of the Origin for the Project
    """
    # Fetch Project page
    r_project = req.get(
        f'https://api.notion.com/v1/pages/{project_id}',
        headers=HTTP_HEADER
    )

    if (r_project.status_code == 200):
        logging.debug(f"FETCH successful of Project {project_id}")
    else:
        logging.error(f"FETCH unsuccessful of Project {project_id} (returned {r_project.status_code})")
    
    # Extract the ID of the given Project's Origin page
    origin_id = r_project.json().get('properties').get('Origin').get('relation')[0].get('id')

    # Fetch Origin page
    r_origin = req.get(
        f'https://api.notion.com/v1/pages/{origin_id}',
        headers=HTTP_HEADER
    )

    if (r_origin.status_code == 200):
        logging.debug(f"FETCH successful of Origin {origin_id}")
    else:
        logging.error(f"FETCH unsuccessful of Project {origin_id} (returned {r_origin.status_code})")
    
    # Extract the plaintext name of the Origin
    return r_origin.json().get('properties').get('Name').get('title')[0].get('plain_text')

def update_origin_name(page_id, origin_name):
    """Update the Origin property of a Project

    Args:
        page_id (str):  The ID of the Project
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

    if (r.status_code == 200):
        logging.info(f"PATCH successful to page {page_id} (set Origin to '{origin_name}')")
    else:
        logging.error(f"PATCH unsuccessful for page {page_id} (returned {r.status_code} when setting Origin to '{origin_name}')")

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

    if (r.status_code == 200):
        logging.debug(f"FETCH successful of database {db_id}")
    else:
        logging.error(f"FETCH unsuccessful of database {db_id} (returned {r.status_code})")

    return r.json()['results']

def main():
    # Fetch the to-do database
    db = fetch_db(
        os.environ.get('NOTION_TARGET_DB_ID')
    )

    # Iterate through every to-do item
    for item in db:
        project = item.get('properties').get('Project').get('relation')

        # Only if the item has a Project property
        if project:
            origin = item.get('properties').get('Origin').get('select')

            if origin:                
                # Item has an Origin property
                if (origin.get('name') != get_origin_name(project[0].get('id'))):
                    # Update only if out-of-date
                    update_origin_name(item.get('id'), get_origin_name(project[0].get('id')))
            else:
                # Item does not have an Origin property
                update_origin_name(item.get('id'), get_origin_name(project[0].get('id')))

if __name__ == '__main__':
    logging.info('♥ notionsync by mhmatthall')

    # Print imported variables
    logging.info(f"targeting notion db {os.environ.get('NOTION_TARGET_DB_ID')}")
    logging.debug(f"using api key {os.environ.get('NOTION_INTEGRATION_API_KEY')}")

    while True:
        # run every 30 seconds
        try:
            # Less go baybee
            main()
        except:
            logging.exception('Fatal error:')
        
        sleep(30)
