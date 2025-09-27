# Documentation for autolog
### fastAPI: A collection of APIs that expose CRUD operations around a postgreSQL Autolog database


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/autolog/info         | Basic description of the application and container     |
| GET    | /api/v1/autolog/health    | Health check endpoint     |



## CRUD Endpoints for Vehicle:
| Method | URL Pattern                  | Description              | Example                    |
|--------|------------------------------|--------------------------|----------------------------|
| GET    | /api/v1/autolog/vehicle      | List all vehicles        | /api/v1/autolog/vehicle    |
| GET    | /api/v1/autolog/vehicle/{id} | Get vehicle by ID        | /api/v1/autolog/vehicle/12 |
| POST   | /api/v1/autolog/vehicle      | Create new vehicle       | /api/v1/autolog/vehicle    |
| PUT    | /api/v1/autolog/vehicle/{id} | Update vehicle (full)    | /api/v1/autolog/vehicle/12 |
| PATCH  | /api/v1/autolog/vehicle/{id} | Update vehicle (partial) | /api/v1/autolog/vehicle/12 |
| DELETE | /api/v1/autolog/vehicle/{id} | Delete vehicle           | /api/v1/autolog/vehicle/12 |


## CRUD Endpoints for Gas:
| Method | URL Pattern                           | Description                             | Example                           |
|--------|---------------------------------------|-----------------------------------------|-----------------------------------|
| GET    | /api/v1/autolog/vehicle/{id}/gas      | List all gas entries for vehicles       | /api/v1/autolog/vehicle/12/gas    |
| GET    | /api/v1/autolog/vehicle/{id}/gas/{id} | Get gas entry by ID for a given vehicle | /api/v1/autolog/vehicle/12/gas/42 |
| POST   | /api/v1/autolog/vehicle/{id}/gas      | Create new gas entry                    | /api/v1/autolog/vehicle/12/gas    |
| PUT    | /api/v1/autolog/vehicle/{id}/gas/{id} | Update gas entry (full)                 | /api/v1/autolog/vehicle/12/gas/42        |
| PATCH  | /api/v1/autolog/vehicle/{id}/gas/{id} | Update gas entry (partial)              | /api/v1/autolog/vehicle/12/gas/42        |
| DELETE | /api/v1/autolog/vehicle/{id}/gas/{id} | Delete gas entry                        | /api/v1/autolog/vehicle/12/gas/42        |

## CRUD Endpoints for Insurance:
| Method | URL Pattern                            | Description                             | Example                           |
|--------|----------------------------------------|-----------------------------------------|-----------------------------------|
| GET    | /api/v1/autolog/vehicle/{id}/insurance | List all insurances for a vehicles      | /api/v1/autolog/vehicle/12/insurance    |
| GET    | /api/v1/autolog/vehicle/{id}/insurance/{id}  | Get insurance by ID for a given vehicle | /api/v1/autolog/vehicle/12/insurance/42 |
| POST   | /api/v1/autolog/vehicle/{id}/insurance       | Create new insurance record             | /api/v1/autolog/vehicle/12/insurance    |
| PUT    | /api/v1/autolog/vehicle/{id}/insurance/{id}  | Update insurance record (full)          | /api/v1/autolog/vehicle/12/insurance/42        |
| PATCH  | /api/v1/autolog/vehicle/{id}/insurance/{id}  | Update insurance record (partial)       | /api/v1/autolog/vehicle/12/insurance/42        |
| DELETE | /api/v1/autolog/vehicle/{id}/insurance/{id}  | Delete insurance record                 | /api/v1/autolog/vehicle/12/insurance/42        |


### Access the info endpoint
http://home.dev.com/api/v1/autolog/info

### View test page
http://home.dev.com/autolog/test/vehicle.html

### Swagger:
http://home.dev.com/api/v1/autolog/docs