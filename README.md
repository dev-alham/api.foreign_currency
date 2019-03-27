# Setup API Documentation
Run using Docker
```bash
docker-compose up
```

## Setup

- Create Django Admin

```bash
docker-compose run web python manage.py createsuperuser
```

- `input username`
- `input email`
- `input password`

###### Open Django Admin
`<publishe ip docker>:8000/admin`

## Setting Maintenance
insert into database id = 1, is_maintenance=1
- 1 for maintenance
- 0 for not maintenance

## Databse
- user db: `alhamsya`
- password db : `alhamsya`
- name db: `foreign_currency_test`

# Api
##### <method_request>   :   <url_request>
###### input daily exchange rate data
- POST: `<publishe ip docker>:8000/api/exchange`

```sh
# request data

{
	"date": "2018-07-3",
	"from_rate": "USD",
	"to_rate": "gbp",
	"rate": 0.75709
}
```
###### list all exchange rate
- GET: `<publishe ip docker>:8000/api/exchange/rate`

###### add an exchange rate to the list
- POST: `<publishe ip docker>:8000/api/exchange/rate`
```sh
# request data

{
	"from_rate": "usd",
	"to_rate": "gbp"
}
```

###### remove an exchange rate from the list
- DELETE: `<publishe ip docker>:8000/api/exchange/rate/<int: id_rate>`

###### exchange rate trend from the most recent 7 data points
- GET: `<publishe ip docker>:8000/api/exchange/rate/trend/<int: limit_data>`

###### exchange rates to be tracked
- GET: `<publishe ip docker>:8000/api/exchange/rate/date/<str: date_data>`

