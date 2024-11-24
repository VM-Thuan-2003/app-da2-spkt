from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# Example:
# r = Role.ADMIN
# print(r.value)  # 'admin'
# print(r.name)   # 'ADMIN'


class Authorization:
    def __init__(self, role: Role):
        self.role = role

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
