from app.common.dto import BaseDto
from uuid import UUID


class AdminLogin(BaseDto):
    email: str
    password: str


class AdminCreate(AdminLogin):
    ...


class AdminAuth(BaseDto):
    id: UUID
    email: str
