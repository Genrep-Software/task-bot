#!/usr/bin/python3

# task_bot.py
#
# Main file for the GroupMe Airtable task bot
#
# Copyright (c) 2020 Genrep Software, LLC.
# https://github.com/Genrep-Software/task-bot

import json
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

    for key in ["bot_id", "group_id"]:
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
    group_id: str

    POST_URL = "https://api.groupme.com/v3/bots/post"

    def send(self, msg: str) -> None:
        """
        Send a message from the bot in the group.
        :param msg: Message to send; only sends the first 998 characters of msg
        """
        data = {
            "bot_id": self.bot_id,
            "text": msg,
        }
        requests.post(GroupmeBot.POST_URL, json=data)


################################################################################
# Main Function
################################################################################

def main():
    keys = load_api_keys("api_keys.json")
    bot = GroupmeBot(keys.get("bot_id"), keys.get("group_id"))
    bot.send("Testy buddy!")


if __name__ == "__main__":
    main()
