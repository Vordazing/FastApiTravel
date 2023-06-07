import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    login: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id_account: int
    post: str

    class Config:
        orm_mode = True