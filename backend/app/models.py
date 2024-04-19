from sqlmodel import Field, Relationship, SQLModel


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = False
    is_superuser: bool = False
    real_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

class UserRegister(SQLModel):
    email: str
    password: str
    real_name: str | None = None

# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    password: str | None = None
    email: str | None = None

class UserUpdateMe(SQLModel):
    real_name: str | None = None
    email: str | None = None

class UserUpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None

# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str

# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None

# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User = Relationship(back_populates="items")

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str