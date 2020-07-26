#!/usr/bin/python3

# task_bot.py
#
# Main file for the GroupMe Airtable task bot
#
# Copyright (c) 2020 Genrep Software, LLC.
# https://github.com/Genrep-Software/task-bot

import json
import time
from dataclasses import dataclass
from typing import Dict

import requests


################################################################################
# Helper Functions
################################################################################

def load_api_keys(keyfile: str) -> Dict[str, str]:
    """
    Loads API keys from a JSON-serialized key file
    :param keyfile: Path to the JSON file to deserialize
    :return: Dictionary containing API keys
    """
    with open(keyfile, "r") as f:
        keys = json.load(f)

    for key in ["bot_id", "airtable_api_key", "airtable_api_url"]:
        if key not in keys or not keys.get(key):
            raise KeyError(f"\"{key}\" not in key file {keyfile}")

    return keys


################################################################################
# Classes
################################################################################

@dataclass
class GroupmeBot(object):
    """
    Represents a GroupMe bot that can handle sending and receiving messages.
    """
    bot_id: str

    POST_URL = "https://api.groupme.com/v3/bots/post"
    MAX_MSG_LEN = 998

    def send(self, msg: str) -> None:
        """
        Send a message from the bot in the group.
        :param msg: Message to send; cuts into substrings of length 998
        """
        for substr in [msg[i:(i + GroupmeBot.MAX_MSG_LEN)] for i in
                       range(0, len(msg), GroupmeBot.MAX_MSG_LEN)]:
            data = {
                "bot_id": self.bot_id,
                "text": substr,
            }
            requests.post(GroupmeBot.POST_URL, json=data)
            time.sleep(0.5)


class Airtable(object):
    """
    Represents the records in the Airtable tasks list.
    """
    def __init__(self, api_key: str, api_url: str):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })
        self.records = dict()
        self.get_records()

    def get_records(self, view: str = "Bot") -> None:
        # Get the first 100 records from the task list
        params = tuple({
            "view": view,
        }.items())
        with self.session.get(self.api_url, params=params) as r:
            records = map(lambda i: i.get("fields"), r.json().get("records"))

        # Add each of them to the object's dictionary of records
        for record in records:
            if record is None:
                continue

            assigned_to = record\
                .get("Assigned To", dict())\
                .get("name", "Unassigned")
            if assigned_to not in self.records:
                self.records[assigned_to] = []
            self.records.get(assigned_to).append(record)


################################################################################
# Main Function
################################################################################

def main():
    keys = load_api_keys("api_keys.json")
    bot = GroupmeBot(keys.get("bot_id"))
    # try:
    table = Airtable(keys.get("airtable_api_key"), keys.get("airtable_api_url"))
    print(json.dumps(table.records, indent=2))
    """
    except Exception as e:
        bot.send(str(e))
    """


if __name__ == "__main__":
    main()
