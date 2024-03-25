class RemoteException(Exception):
    """Still an exception raised when uncommon things happen"""
    def __init__(self, status, message=None):
        self.status = status
        self.message = message # you could add more args

    def __str__(self):
        return str(self.message) # __str__() obviously expects a string to be returned, so make sure not to send any other data types