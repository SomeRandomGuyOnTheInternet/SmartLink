from __future__ import annotations
from db_context import DBContext
import ast


class Action:
    id: str
    device_id: str
    name: str
    description: str
    command: str
    is_toggle: bool
    current_state: int

    def __init__(self, id, device_id, name, description, command, is_toggle, current_state):
        self.id = id
        self.device_id = device_id
        self.name = name
        self.description = description
        self.command = command
        self.is_toggle = is_toggle
        self.current_state = current_state

    @staticmethod
    def read_actions_csv(db_context: DBContext):
        try:
            data = db_context.read_from_csv("actions.csv")
            actions = []
            for entry in data:
                try:
                    if "id" not in entry or "device_id" not in entry or "name" not in entry \
                            or "description" not in entry or "command" not in entry \
                            or "is_toggle" not in entry or "current_state" not in entry:
                        raise ValueError(
                            "Invalid entry found in the devices database.")

                    action = Action(
                        entry["id"],
                        entry["device_id"],
                        entry["name"],
                        entry["description"],
                        entry["command"],
                        ast.literal_eval(entry["is_toggle"]),
                        int(entry["current_state"])
                    )
                    actions.append(action)
                except Exception as e:
                    print(e)
                    continue
            return actions
        except IOError as e:
            print(e)
            raise ValueError("Something went wrong while reading actions.")

    @staticmethod
    def save_actions_csv(db_context: DBContext, actions: list[Action]):
        try:
            data = []
            headers = ["id", "device_id", "name", "description",
                       "command", "is_toggle", "current_state"]
            for action in actions:
                if not isinstance(action, Action):
                    raise ValueError(
                        "Tried to save an invalid list of actions.")
                data.append({headers[0]: action.id, headers[1]: action.device_id, headers[2]: action.name,
                            headers[3]: action.description, headers[4]: action.command, headers[5]: action.is_toggle, headers[6]: action.current_state})

            return db_context.write_to_csv("actions.csv", data, headers)
        except IOError as e:
            print(e)
            raise ValueError("Something went wrong while saving actions.")
