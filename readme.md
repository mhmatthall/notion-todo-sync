# notion-todo-sync

> [!NOTE]
> I don't use this script anymore as I've restructured my Notion to-do system, so it likely won't be updated. I'd recommend restructuring your Notion databases so that you don't need this script; try using [roll-up properties](https://www.notion.so/help/relations-and-rollups) instead.

A script for keeping linked page properties synchronised in Notion databases. Notion doesn't currently support grouping databases by roll-ups but I really need this for how my to-do list is structured.

## What?

So each item in my to-do list belongs to a **Project**, and each Project belongs to a more general **Origin** (e.g. the to-do item 'Book the return flight' might belong to a **Project** called 'Amsterdam trip', which itself belongs to the 'Personal' **Origin**). This is implemented in my Notion as a database of to-do items, each of which with two properties: a Project relation and an Origin roll-up.

I want to be able to group my to-do items according to the general Origin that they belong to rather than by Project, because I want to separate out my to-do items at a high-level -- it's no use having a kanban board split into hundreds of sections for every single Project I've ever made. Notion doesn't support this right now though, since you can't group/subgroup by roll-up properties. Hence the need for this script to automatically sync the Origin property for to-do list items based on the value of their Project property.

## Setup

1. Clone this repo
2. Install dependencies:

   `conda env create -f environment.yml`

3. Create a [new Notion integration](https://notion.so/my-integrations) and copy your API key
4. Open Notion and copy the ID of the database you want the script to manage, making sure to _Share_ it with your newly created integration

   > [!NOTE]
   > You'll have to share any embedded database relations with your integration too, if you want to access any of their data

5. Create a `.env` file in the root of this repo with the following lines:

   ```dotenv
   NOTION_INTEGRATION_API_KEY=<your Notion integration API key>
   NOTION_TARGET_DB_ID=\<the ID of the database being synchronised>
   ```

6. Register a `cron` job to execute the `init.sh` script as often as required (e.g. every 10 minutes: `*/10 * * * *`)

## Dependencies

- `cron` to schedule automatic execution of the script
- `conda` for dependencies
- Python
  - tested on Python 3.10
  - requires `requests` and `dotenv`

---

## ~~To-do~~

> [!WARNING]
> No longer being updated

- Actually make reusable
- Containerise
- Allow custom property specification based on [JSONpath](https://restfulapi.net/json-jsonpath/) strings
