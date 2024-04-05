from db_context import DBContext
from action import Action
from device import Device


class DataManager:
    db_context: DBContext
    devices: list[Device]

    def __init__(self, devices=[]):
        self.db_context = DBContext("./data/")
        self.devices = devices
            
    def get_device_by_id(self, id):
        for device in self.devices:
            if device.id == id:
                return device
        return None
         
    def get_action_by_id(self, id):
        for device in self.devices:
            for action in device.actions:
                if action.id == id:
                    return action
        return None
                
    def add_action(self, action):
        for device in self.devices:
            print(action.device_id, device.id)
            if action.device_id == device.id:
                device.actions.append(action)

    def load_data(self):
            actions = Action.read_actions_csv(self.db_context)
            self.devices = Device.read_devices_csv(self.db_context, actions)

    def save_data(self):
        global_actions = []
        for device in self.devices:
            for action in device.actions:
                global_actions.append(action)
                    
        Action.save_actions_csv(self.db_context, global_actions)
        Device.save_devices_csv(self.db_context, self.devices)
