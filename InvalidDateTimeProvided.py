class InvalidDateTimeProvidedException(Exception):
    def __init__(self, message="date provided is not available at the moment"):
        self.message = message
        super().__init__(self.message)