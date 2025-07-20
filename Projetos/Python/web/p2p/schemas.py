# schemas.py
# schemas.py

from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    email: str
    password: str

    class Config:
        from_attributes = True  # substitui orm_mode


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    nickname: str  # Campo obrigatório
    
class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(UserBase):
    # Não é necessário incluir `id` novamente aqui, pois já está em UserBase
    class Config:
        from_attributes = True  # Substitui `orm_mode`


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    # O `id` geralmente não deve ser incluído no modelo de criação

class User(BaseModel):
    id: int
    model_config = {
        "from_attributes": True  # Substitui `orm_mode = True` no Pydantic v2
    }
 