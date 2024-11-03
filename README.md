# Evaluacion-API-efh
Pasos para ejecutar el repositorio Evaluacion-API-efh

1) Ir al Github y selecionar el repositorio EdwinDavidFlores/Evaluacion-API-efh
2) Luego ir al apartado de "Code" luego selecionar el Codespace en uso.
3) Una vez cargada el Codespace, en la parte del terminal ingresar el codigo " uvicorn ,main:app --reload " para carga el proyecto en el FastAPI, el cual nos va a redireccionar a un navegador el mismo que tendra este link: "https://fearsome-spirit-pjpp4jp6rxrw36v5-8000.app.github.dev/docs"
4) Luego de cargado el proyecto se podra realizar las Operaciones CRUD (Create,Research ,Update, Delete) completas ,tanto para Proyectos como Usuarios.
5) La cuenta Azure de Cosmos DB es : "acdbefhdev" ,donde se encuentra la BD: "ProyectosDB" y contenedores: "Proyectos" y "Usuarios", el cual estan los registros que se encuentran listos para las validaciones y acciones segun se requiera tanto para los Proyectos como usuarios. https://portal.azure.com/#@dblearner.com/resource/subscriptions/253d6ed3-64b2-4fb0-957a-c81a3bd7781f/resourceGroups/AcademyNoSQL/providers/Microsoft.DocumentDb/databaseAccounts/acdbefhdev/dataExplorer