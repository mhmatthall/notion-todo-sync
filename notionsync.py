import requests as req
from time import sleep
# For secrets:
from dotenv import load_dotenv
import os

def parse_project_origin_name(project_id):
    """ Request a Project page, get the ID of its Origin property, then request that and parse its plaintext name property

    Args:
        project_id (str): The ID of the target Project page

    Returns:
        str: The plaintext name of the page's correct Origin property
    """
    # Fetch project page from Notion and extract only its 'Origin' property's page ID
    r = req.get(
        f'https://api.notion.com/v1/pages/{project_id}',
        headers={
            'Authorization': f"Bearer {os.environ.get('NOTION_INTEGRATION_API_KEY')}",
            'Notion-Version': '2022-02-22'
        }
    )

    print(f"parsing of origin name from page '{project_id}' returned HTTP {r.status_code}")
    
    origin_id = r.json().get('properties').get('Origin').get('relation')[0].get('id')

    # Fetch origin page from Notion and extract only the page's plaintext name
    origin_name = req.get(
        f'https://api.notion.com/v1/pages/{origin_id}',
        headers={
            'Authorization': f"Bearer {os.environ.get('NOTION_INTEGRATION_API_KEY')}",
            'Notion-Version': '2022-02-22'
        }
    ).json().get('properties').get('Name').get('title')[0].get('plain_text')

    return origin_name


def push_origin_name(page_id, origin_name):
    """Update the Origin property of a page on Notion

    Args:
        page_id (str):  The ID of the target page
        origin_name (str): The new plaintext Origin name
    """
    r = req.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers={
            'Authorization': f"Bearer {os.environ.get('NOTION_INTEGRATION_API_KEY')}",
            'Notion-Version': '2022-02-22'
        },
        # Payload
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

    print(f"pushing of new origin name '{origin_name}' to page '{page_id}' returned HTTP {r.status_code}")


def fetch_db(db_id):
    """Fetch a Notion database

    Returns:
        dict: The returned database as a JSON-serialisable dict (removes HTTP request guff)
    """
    r = req.post(
        f'https://api.notion.com/v1/databases/{db_id}/query',
        headers={
            'Authorization': f"Bearer {os.environ.get('NOTION_INTEGRATION_API_KEY')}",
            'Notion-Version': '2022-02-22'
        },
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

    print(f"fetching of database '{db_id}' returned HTTP {r.status_code}")

    return r.json()['results']


def main():
    # Fetch the to-do list database from Notion
    db = fetch_db(os.environ.get('NOTION_TARGET_DB_ID'))

    for page in db:
        # If the page has a relation
        if page.get('properties').get('Project').get('relation'):
            project_id = page.get('properties').get('Project').get('relation')[0].get('id')

            if page.get('properties').get('Origin').get('select'):
                # Try and parse the JSON for the name
                current_origin_name = page.get('properties').get('Origin').get('select').get('name')
            else:
                # If the JSON doesn't exist to parse, then there's no current origin name
                current_origin_name = None

            # Fetch the correct origin name
            origin_name = parse_project_origin_name(project_id)

            # If the page's plaintext origin name doesn't match the project's plaintext origin name
            # OR the page has no plaintext origin name
            if (current_origin_name != origin_name or not current_origin_name):
                push_origin_name(page.get('id'), origin_name)


if __name__ == '__main__':
    # Import environment vars from ./.env
    load_dotenv()

    while True:
        # Less go baybee
        main()

        # I'm using sleep rather than cron because:
        #   - this is run in a Docker where it's the only foreground task
        #   - running the task 3 times a minute would require 3 cron instances since it only has minute-level granularity
        sleep(10)