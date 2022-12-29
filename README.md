# Fampay Backend Assignment

### Requirements (Implemented)

☑️ Background service to load youtube video data periodically

☑️ A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.

☑️ Optimised search API that supports partial match on title and description

☑️ Dockerized the entire project

☑️ Support for multiple API keys implemented

☑️ Dashboard view available through django admin

### Setup Instructions

1.  The backend directory holds the code for the project , use the docker-compose.yml file to launch the project

```vhdl
docker compose build 
docker compose up
```

1.  Access the django admin at [localhost:3000/admin](http://localhost:3000/admin) , default username is _**ganesh**_ password is _**password.**_ You can add your api key in APIKey page for testing purpose.
2.  Make API requests to [localhost:3000/getvideos](http://localhost:3000/getvideos) and [localhost:3000/search](http://localhost:3000/search) by following the instructions here : [POSTMAN DOCS](https://documenter.getpostman.com/view/19494450/2s8Z6yXDSG)

### Design

![design.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7b963145-9db8-4ebf-9865-9770513967bc/Screenshot_2022-12-30_at_4.15.55_AM.png)