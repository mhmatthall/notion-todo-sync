# notion-todo-sync
A script for keeping linked page properties synchronised in Notion databases. Notion doesn't currently support grouping databases by roll-ups but I really need this for how my to-do list is structured.

## What?
So each item in my to-do list belongs to a **Project**, and each Project belongs to a more general **Origin** (e.g. the to-do item 'Book the return flight' might belong to a **Project** called 'Amsterdam trip', which itself belongs to the 'Personal' **Origin**). This is implemented in my Notion as a database of to-do items, each of which with two properties: a Project relation and an Origin roll-up.

I want to be able to group my to-do items according to the general Origin that they belong to rather than by Project, because I want to separate out my to-do items at a high-level -- it's no use having a kanban board split into hundreds of sections for every single Project I've ever made. Notion doesn't support this right now though, since you can't group/subgroup by roll-up properties. Hence the need for this script to automatically sync the Origin property for to-do list items based on the value of their Project property.

## Files
- `notionsync.py` is the script itself
- `init.sh` is a shell script used to repeatedly execute the Python script at a desired interval

## Setup
- [Make a new Notion integration](https://notion.so/my-integrations) and copy your API key.
- On Notion, copy the ID of the database you want the script to manage, making sure to *Share* it with your newly created integration. You'll have to share any embedded database relations with your integration too, if you want to access any of their data.
- Clone this project.
- Install dependencies with `conda env create -f environment.yml`
- Create a `.env` file that has the following lines:
  - `NOTION_INTEGRATION_API_KEY=`\<your Notion integration API key>
  - `NOTION_TARGET_DB_ID=`\<the ID of the database being synchronised>

## Dependencies
- Python
  - tested on Python 3.10
  - requires `requests` and `dotenv`
- Bash
  - ~~`cron` for automating the script~~

---

## To-do
- Actually make reusable
- Containerise
- Allow custom property specification based on [JSONpath](https://restfulapi.net/json-jsonpath/) strings
