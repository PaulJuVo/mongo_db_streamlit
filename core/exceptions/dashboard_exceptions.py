class NoDataFound(Exception):
    def __init__(self, message : str, errorcode : int) -> None:
        self.message = message
        self.errorcode = errorcode
    
    def __str__(self):
        return f'{self.message}: ERRORCODE {self.errorcode}'