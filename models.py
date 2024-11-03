from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Usuarios(BaseModel):
	id: str=Field(..., example='u1')
	nombre: str= Field(..., example='Saul')
	email: EmailStr= Field(..., example='edwinlflores@example.com')
	edad: int= Field(..., example=34)

class Proyectos(BaseModel):
	id: str=Field(..., example='p1')
	nombre: str= Field(..., example='Desarrollo de proyecto en Power BI')
	descripcion: Optional[str]= Field(None, example='Desarrollar una a')
	id_usuario: str = Field (..., example='u1')
	fecha_creacion: str = Field(..., example='2024-10-23T19:00:002')