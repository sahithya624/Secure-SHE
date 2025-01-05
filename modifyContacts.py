import json


def addContact(phone: str) -> None:
    if phone[0:3] != "+91":
        phone = "+91" + phone

    with open("db\\contacts.json", "r") as f:
        data = json.load(f)

    if phone not in data['trusted']:
        data["trusted"].append(phone)

    with open("db\\contacts.json", "w") as f:
        json.dump(data, f, indent=4)


def removeContact(phone: str) -> None:
    if phone[0:3] != "+91":
        phone = "+91" + phone

    with open("db\\contacts.json", "r") as f:
        data = json.load(f)

    if phone in data['trusted']:
        data["trusted"].remove(phone)

    with open("db\\contacts.json", "w") as f:
        json.dump(data, f, indent=4)


def purgeContacts() -> None:
    with open("db\\contacts.json", "r") as f:
        data = json.load(f)

    data["trusted"].clear()

    with open("db\\contacts.json", "w") as f:
        json.dump(data, f, indent=4)