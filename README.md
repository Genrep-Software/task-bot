# Genrep Software Task Bot

Internally at Genrep, tasks are tracked and managed with a synchronized
Airtable. Many tasks have due dates. This bot sends a message once daily with
all of the tasks that have due dates.



# Installation

Clone the repository locally using

```.bash
git clone https://github.com/Genrep-Software/task-bot.git && cd task-bot
```

Before installing, create a file called `api_keys.json` in the same directory
as the `task_bot.py` file. Populate the file with the following JSON
dictionary, filling in your own values where appropriate:

```.json
{
  "bot_id": "[BOT ID]",
  "airtable_api_key": "[AIRTABLE API KEY]",
  "airtable_api_url": "[AIRTABLE API URL]"
}
```

To install, run `make install` from the command line. This will first use `pip`
in Python 3 to install the requirements. Then, it will add a line to the system
`crontab` to run the file daily at 9:00am.
