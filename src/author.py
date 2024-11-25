from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Authorization:
    def __init__(self, role: Role):
        self.role = role

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
