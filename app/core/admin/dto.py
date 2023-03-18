from pydantic import BaseModel


class AdminLogin(BaseModel):
    email: str
    password: str


class AdminCreate(AdminLogin):
    ...


class AdminAuth(BaseModel):
    id: int
    email: str
