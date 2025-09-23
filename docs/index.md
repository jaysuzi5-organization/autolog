# Documentation for autolog
### fastAPI: A collection of APIs that expose CRUD operations around a postgreSQL Autolog database


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/autolog/info         | Basic description of the application and container     |
| GET    | /api/v1/autolog/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern           | Description             | Example             |
|--------|-----------------------|--------------------|---------------------|
| GET    | /api/v1/autolog         | List all autolog     | /api/v1/autolog       |
| GET    | /api/v1/autolog/{id}    | Get autolog by ID     | /api/v1/autolog/42    |
| POST   | /api/v1/autolog         | Create new autolog    | /api/v1/autolog       |
| PUT    | /api/v1/autolog/{id}    | Update autolog (full) | /api/v1/autolog/42    |
| PATCH  | /api/v1/autolog/{id}    | Update autolog (partial) | /api/v1/autolog/42 |
| DELETE | /api/v1/autolog/{id}    | Delete autolog        | /api/v1/autolog/42    |


### Access the info endpoint
http://home.dev.com/api/v1/autolog/info

### View test page
http://home.dev.com/autolog/test/autolog.html

### Swagger:
http://home.dev.com/api/v1/autolog/docs