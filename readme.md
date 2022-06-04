# notion-todo-sync
Currently a very niche Python script for synchronising page properties for pages in my [Notion](https://notion.so/) to-do list, because Notion does not currently allow sub-grouping kanban boards by roll-ups (the bastards). I should make it clear that this definitely isn't reusable right now, but I thought it might be helpful for peeps to look at if they want to steal this and do similar.

## Files
- `sandbox.ipynb` contains a sort of verbose version of the script that helps (me) understand what's going on
- `notionsync.py` is the script itself, which runs once on execution
- `init.sh` is a shell script used to repeatedly execute the Python script at a desired interval

## Setup
- Make a new Notion integration ([here's the link](https://notion.so/my-integrations)) and copy your API key.
- Go to your relevant Notion workspace, find the database you want, copy its ID, then *Share* it to your newly created integration. You'll have to share any embedded database relations with your integration too, if you want to access any of their data.
- Clone this project.
- Provide a `.env` file that has the following:
  - `NOTION_INTEGRATION_API_KEY=`\<your Notion integration API key>
  - `NOTION_TARGET_DB_ID=`\<the ID of the database being synchronised>

## Requirements
See included `env.yml` file for setting up the environment

---

## To-do
- Actually make reusable
- Add any kind of validation, error handling, exceptions, etc.
- Allow custom property specification based on [JSONpath](https://restfulapi.net/json-jsonpath/) strings

## If you have any issues
Bite me :)