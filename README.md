# General workflow and explanation
## Workflow
1. Write proto files
2. Compile proto files
3. Write implementation in views.py
4. Add service to server in asgi.py
5. Run service with docker compose
6. Test service <br/>
	6a. Expose port and check service with tools like postman and grpcurl <br/>
	6b. Use it with other service <br/>
