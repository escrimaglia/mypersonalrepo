# FastApi Main Proyect
# By Ed SCrimaglia

import datetime
import uuid
from pydantic import AfterValidator, BaseModel
from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import Field, SQLModel, create_engine, Session, select
import rabbitmq as rb
from oauth2 import User, DataBase, Token, Autenticator
import json
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import pytz
from typing import TypeVar, Annotated
from custom_validation import ValidateListToStr
from enum import Enum

local_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
# Annotated for ListToStr objects
T = TypeVar('T')
ValidList = Annotated[list[T], AfterValidator(ValidateListToStr.convert_list_to_str)]

class Estado(Enum):
    Confirmado = "CNF"
    Pendiente = "PND"
    Cancelado = "CAN"
class Producto(BaseModel):
    producto: str = Field(default=uuid.uuid4())
    cantidad: float = Field(..., gt=0)
class ProductoBase(BaseModel):
    producto: ValidList[Producto]
    estado: Estado | None = "CNF" 
    total: float | None = None
class PedidoBase(SQLModel):
    producto: str
    estado: Estado | None = "CNF" 
    total: float | None = None
class Pedido(PedidoBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    userid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    costo: float = Field(default=12.6)
    creacion: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(local_timezone))
class PedidoPrecio(PedidoBase):
    userid: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    costo: float = Field(default=12.6)

app = FastAPI(title="IAEW", description="FastApi & OAuth2 Integration - 2024", version="1.0.0")

# Dependencia para el esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

sqlite_file_name = "iaew.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)
    
@app.get("/api/v1/pedidos", tags=["Métodos principales"])
def read_pedidos():
    with Session(engine) as session:
        registros_pedidos = session.exec(select(Pedido)).all()
        return [
            {
                "pedidoId": reg.id,
                "userId": reg.userid,
                "producto": reg.producto,
                "creacion": reg.creacion,
                "total": reg.total
            }
            for reg in registros_pedidos
        ]

@app.get("/api/v1/pedidos/{id}", tags=["Métodos principales"])
async def pedidos_by_id(id: int):
    async with Session(engine) as session:
        stmt = select(Pedido).where(Pedido.id == id)
        result = await session.execute(stmt)
        pedido = result.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(status_code=404, detail="El pedido no existe")

    return {
        "pedidoId": pedido.id,
        "userId": pedido.userid,
        "producto": pedido.producto,
        "creacion": pedido.creacion,
        "total": pedido.total
    }

@app.post("/api/v1/producer", tags=["Métodos principales"])
def publish_pedido(body: str):
    try:
        msg = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Could not validate the JSON format")
    
    result = rb.send_message(msg=body)
    
    if not result[0]:
        return {"RabbitMQ": result[1]}
    
    return msg
    
@app.post("/api/v1/token", response_model=Token,tags=["Métodos principales"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Autenticator.authentication(DataBase.users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=Autenticator.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Autenticator.create_access_token({"sub": user['username']}, local_timezone, access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}

@app.get("/api/v1/costo", tags=["Sólo Documentación (user Postman con Auth2.0)"])
async def read_costo_pedidos(token: str = Depends(oauth2_scheme)):
    def raise_credentials_exception(detail: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, Autenticator.SECRET_KEY, algorithms=[Autenticator.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise_credentials_exception("Could not validate credentials")
        user = Autenticator.authentication(DataBase.users_db, username)
        if user is None:
            raise_credentials_exception("User not found")
    except (jwt.PyJWTError, jwt.ExpiredSignatureError) as error:
        raise_credentials_exception(str(error))

    list_pedidos = []
    
    with Session(engine) as session:
        registros_pedidos = session.exec(select(Pedido)).all()
        for reg in registros_pedidos:
            pedido_info = {
                "pedidoId": reg.id,
                "userId": reg.userid,
                "producto": reg.producto,
                "creacion": reg.creacion,
                "total": reg.total,
                "costo": reg.costo
            }
            list_pedidos.append(pedido_info)

    return list_pedidos