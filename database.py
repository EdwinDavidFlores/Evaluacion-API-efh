from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv
import os

# Obtener las variables de entorno


# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)

# Crear o obtener el contenedor_usuarios
try:
    usuarios_container = database.create_container_if_not_exists(
        id=CONTAINER_NAME1,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    usuarios_container = database.get_container_client(CONTAINER_NAME1)


    # Crear o obtener el contenedor_proyectos
try:
    proyectos_container = database.create_container_if_not_exists(
        id=CONTAINER_NAME2,
        partition_key={'paths': ['/id'], 'kind': 'Hash'},
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    proyectos_container = database.get_container_client(CONTAINER_NAME2)