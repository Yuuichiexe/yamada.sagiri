"""
MIT License

Copyright (c) 2022 Arsh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from NekoRobot.mongo import db
from typing import Dict, List, Union

karmadb = db.karma
karmaonoffdb = db.karmaonoff


def get_karmas_count() -> dict:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    karmas_count = 0
    for chat in chats.to_list(length=1000000):
        for i in chat['karma']:
            karma_ = chat['karma'][i]['karma']
            if karma_ > 0:
                karmas_count += karma_
        chats_count += 1
    return {"chats_count": chats_count, "karmas_count": karmas_count}


def user_global_karma(user_id) -> int:
    chats = karmadb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return 0
    total_karma = 0
    for chat in chats.to_list(length=1000000):
        karma = get_karma(
            chat["chat_id"], await int_to_alpha(user_id)
        )
        if karma and int(karma['karma']) > 0:
            total_karma += int(karma['karma'])
    return total_karma


def get_karmas(chat_id: int) -> Dict[str, int]:
    karma = karmadb.find_one({"chat_id": chat_id})
    if not karma:
        return {}
    return karma['karma']


def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    karmas = get_karmas(chat_id)
    if name in karmas:
        return karmas[name]


def update_karma(chat_id: int, name: str, karma: dict):
    name = name.lower().strip()
    karmas = get_karmas(chat_id)
    karmas[name] = karma
    karmadb.update_one(
        {"chat_id": chat_id}, {"$set": {"karma": karmas}}, upsert=True
    )


def is_karma_on(chat_id: int) -> bool:
    chat = karmadb.find_one({"chat_id_toggle": chat_id})
    return not chat


def karma_on(chat_id: int):
    is_karma = is_karma_on(chat_id)
    if is_karma:
        return
    return karmadb.delete_one({"chat_id_toggle": chat_id})


def karma_off(chat_id: int):
    is_karma = is_karma_on(chat_id)
    if not is_karma:
        return
    return karmadb.insert_one({"chat_id_toggle": chat_id})

def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = str(user_id)
    return "".join(alphabet[int(i)] for i in user_id)


def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id
