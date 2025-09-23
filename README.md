# Documentation for autolog
### fastAPI: A collection of APIs that expose CRUD operations around a postgreSQL Autolog database


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/autolog/info         | Basic description of the application and container     |
| GET    | /api/v1/autolog/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern                  | Description              | Example                    |
|--------|------------------------------|--------------------------|----------------------------|
| GET    | /api/v1/autolog/vehicle      | List all vehicles        | /api/v1/autolog/vehicle    |
| GET    | /api/v1/autolog/vehicle/{id} | Get vehicle by ID        | /api/v1/autolog/vehicle/42 |
| POST   | /api/v1/autolog/vehicle      | Create new vehicle       | /api/v1/autolog/vehicle    |
| PUT    | /api/v1/autolog/vehicle/{id} | Update vehicle (full)    | /api/v1/autolog/vehicle/42 |
| PATCH  | /api/v1/autolog/vehicle/{id} | Update vehicle (partial) | /api/v1/autolog/vehicle/42 |
| DELETE | /api/v1/autolog/vehicle/{id} | Delete vehicle           | /api/v1/autolog/vehicle/42 |


### Access the info endpoint
http://home.dev.com/api/v1/autolog/info

### View test page
http://home.dev.com/autolog/test/vehicle.html

### Swagger:
http://home.dev.com/api/v1/autolog/docs