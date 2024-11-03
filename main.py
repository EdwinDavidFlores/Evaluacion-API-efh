from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from database import usuarios_container
from database import proyectos_container
from models import Usuarios, Proyectos
from azure.cosmos import exceptions
from datetime import datetime

app = FastAPI(title='***API de Gestion de Proyectos y usuarios de sobre desarrollo de aplicaciones***')

###Endpoint de Eventos

@app.get("/")
def home():
	return "Hola Mundo Proyecto"


### Crear usuario
@app.post("/usuarios/",response_model=Usuarios,status_code=201)
def crear_usuario(usuarios: Usuarios):
	try:
		usuarios_container.create_item(body=usuarios.dict())
		return usuarios
	except exceptions.CosmosResourceExistsError:
		raise HTTPException(status_code=400, detail="El usuario con este ID ya existe")
	except exceptions.CosmosHttpResponseError as e:
		raise HTTPException(status_code=400, detail=str(e))

### Obtener usuario por id
@app.get("/usuarios/{usuario_id}", response_model=Usuarios)
def obtener_usuarios_por_ID(usuario_id: str= Path(...,description="ID del usuario a recuperar")):
	try:
		usuario=usuarios_container.read_item(item=usuario_id,partition_key=usuario_id)
		return usuario
	except exceptions.CosmosResourceNotFoundError:
		raise HTTPException(status_code=404, detail="Usuario no encontrado.")
	except exceptions.CosmosHttpResponseError as e:
		raise HTTPException(status_code=400, detail=str(e))


### Listar usuarios
@app.get("/usuarios/", response_model=List[Usuarios])
def listar_usuarios():
	query="SELECT * FROM c WHERE 1=1"
	items=list(usuarios_container.query_items(query=query,enable_cross_partition_query=True))
	return items

### Actualizar usuario

@app.put("/usuarios/{usuario_id}",response_model=Usuarios)
def actualizar_usuario(usuario_id: str, actualizar_usuario: Usuarios):
	try:
		existing_usuario = usuarios_container.read_item(item=usuario_id, partition_key=usuario_id)
	except Exception:
		raise HTTPException(status_code=404, detail="Usuario no encontrado.")
	try:
		existing_usuario.update(actualizar_usuario.dict(exclude_unset=True))
		usuarios_container.replace_item(item=usuario_id, body=existing_usuario)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {str(e)}")
	return existing_usuario


### Eliminar usuario

@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: str):
	try:
		existing_usuario = usuarios_container.read_item(item=id_usuario, partition_key=id_usuario)
	except Exception:
		raise HTTPException(status_code=404, detail="Usuario no existe")
	query=f"SELECT * FROM c where c.id_usuario= '{id_usuario}'"
	proyectos=proyectos_container.query_items(query=query,enable_cross_partition_query=True)
	proyectos_list = list(proyectos)
	if not proyectos_list:
		usuarios_container.delete_item(item=id_usuario, partition_key=id_usuario)
		return {"mensaje":"Usuario eliminado"}
	return {"mensaje":"Usuario no puede ser eliminado"}
	


 ### Crear proyecto
@app.post("/proyectos/",response_model=Proyectos,status_code=201)
async def crear_proyecto(proyecto: Proyectos):
	try:
		existing_usuario = usuarios_container.read_item(item=proyecto.id_usuario, partition_key=proyecto.id_usuario)
	except Exception:
		raise HTTPException(status_code=404, detail="Usuario no encontrado")
	try:
		proyectos_container.create_item(body=proyecto.dict())
		return proyecto
	except exceptions.CosmosResourceExistsError:
		raise HTTPException(status_code=400, detail="El proyecto con este ID ya existe")
	except exceptions.CosmosHttpResponseError as e:
		raise HTTPException(status_code=400, detail=str(e))



### Obtener proyecto por ID

@app.get("/proyectos/{proyecto_id}", response_model=Proyectos)
def obtener_proyectos_por_ID(proyecto_id: str= Path(...,description="ID del proyecto a recuperar")):
	try:
		proyecto=proyectos_container.read_item(item=proyecto_id,partition_key=proyecto_id)
		return proyecto
	except exceptions.CosmosResourceNotFoundError:
		raise HTTPException(status_code=404, detail="Proyecto no encontrado")
	except exceptions.CosmosHttpResponseError as e:
		raise HTTPException(status_code=400, detail=str(e))



### Obtener proyectos de usuario

@app.get("/usuarios/{id_usuario}/proyectos")
async def obtener_proyectos_usuario(id_usuario: str= Path(...,description="ID del usuario a recuperar sus proyectos")):
	try:
		existing_usuario = usuarios_container.read_item(item=id_usuario, partition_key=id_usuario)
	except Exception:
		raise HTTPException(status_code=404, detail="Usuario no encontrado.")
	query=f"SELECT * FROM c where c.id_usuario= '{id_usuario}'"
	proyectos=proyectos_container.query_items(query=query,enable_cross_partition_query=True)
	proyectos_list = list(proyectos)
	if not proyectos_list:
		raise HTTPException(status_code=404, detail="No se encontraron proyectos para el usuario")
	return proyectos_list



### Listar proyectos

@app.get("/proyectos/", response_model=List[Proyectos])
def listar_proyectos():
	query="SELECT * FROM c WHERE 1=1"
	items=list(proyectos_container.query_items(query=query,enable_cross_partition_query=True))
	return items


### Actualizar proyecto
@app.put("/proyectos/{proyecto_id}",response_model=Proyectos)
def actualizar_proyecto(proyecto_id: str, actualizar_proyecto: Proyectos):
	try:
		existing_usuario = usuarios_container.read_item(item=actualizar_proyecto.id_usuario, partition_key=actualizar_proyecto.id_usuario)
	except Exception:
		raise HTTPException(status_code=404, detail="Usuario no encontrado")
	try:
		existing_proyecto = proyectos_container.read_item(item=proyecto_id, partition_key=proyecto_id)
	except Exception:
		raise HTTPException(status_code=404, detail="Proyecto no encontrado")
	try:
		existing_proyecto.update(actualizar_proyecto.dict(exclude_unset=True))
		proyectos_container.replace_item(item=proyecto_id, body=existing_proyecto)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error al actualizar el proyecto: {str(e)}")
	return existing_proyecto



### Eliminar proyecto

@app.delete("/proyectos/{proyecto_id}")
def eliminar_proyecto(proyecto_id: str):
    try:
        proyectos_container.delete_item(item=proyecto_id, partition_key=proyecto_id)
        return {"mensaje":"Proyecto eliminado"}
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no existe')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))