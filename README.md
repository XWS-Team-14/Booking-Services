# General workflow and explanation
## Workflow
1. Write proto files
2. Compile proto files <br/>
	Example: <br/>
		- Have python installed with grpcio and grpcio-tools <br/>
		- Position yourself in proto folder <br/>
		- Run code `python -m grpc_tools.protoc -I. --proto_path=. --python_out=. --grpc_python_out=. example.proto` <br/>
3. Edit grpc version of proto file import '**from .** import example_pb2 as example__pb2'
4. Add models to app/models
5. Add model classes that extend **document** class to db/mongodb.py -> near the bottom
6. Write servicers in app/core
7. Add servicers to server in app/manage/run_server.py
8. Run service <br/>
	8a. Locally -> edit config.yaml host ip to localhost and copy proto folder into service folder<br/>
	8b. With docker compose -> expose ports <br/>
9. Test service <br/>
	9a. Expose port and check service with tools like postman and grpcurl <br/>
	9b. Use it with other service <br/>
