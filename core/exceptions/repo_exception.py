class RepoException(Exception):
    def __init__(self, msg : str) -> None:
        self.message = msg
    def __str__(self):
        return f'{self.message}'