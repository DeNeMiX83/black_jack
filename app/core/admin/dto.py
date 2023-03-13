from app.common.dto import BaseDto


class AdminLogin(BaseDto):
    email: str
    password: str


class AdminCreate(AdminLogin):
    ...


class AdminAuth(BaseDto):
    id: int
    email: str
