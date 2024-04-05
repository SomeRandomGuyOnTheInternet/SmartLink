from __future__ import annotations
from action import Action
from db_context import DBContext

class Device:
    id: str
    name: str
    description: str
    actions: list[Action]

    def __init__(self, id: str, name: str, description: str, actions: list[Action]):
        self.id = id
        self.name = name
        self.description = description
        self.actions = actions

    @staticmethod
    def read_devices_csv(db_context: DBContext, all_actions: list[Action]):
        try:
            data = db_context.read_from_csv("devices.csv")
            devices = []

            for entry in data:
                try:
                    if "id" not in entry or "name" not in entry or "description" not in entry:
                        raise ValueError(
                            "Invalid entry found in the devices database.")
                    actions = []
                    for a in all_actions:
                        if a.device_id == entry["id"]:
                            actions.append(a)
                    device = Device(entry["id"], entry["name"],
                                    entry["description"], actions)
                    devices.append(device)
                except Exception as e:
                    print(e)
                    continue
            return devices
        except IOError as e:
            print(e)
            raise ValueError("Something went wrong while reading devices.")

    @staticmethod
    def save_devices_csv(db_context: DBContext, devices: list[Device]):
        try:
            data = []
            headers = ["id", "name", "description"]
            for device in devices:
                if not isinstance(device, Device):
                    raise ValueError(
                        "Tried to save an invalid list of devices.")
                data.append({headers[0]: device.id, headers[1]: device.name, headers[2]: device.description})
                

            return db_context.write_to_csv("devices.csv", data, headers)
        except IOError as e:
            print(e)
            raise ValueError("Something went wrong while saving devices.")
