# kvirin_message

Kvirin Message for DEMHACK 4

## Components

All components are parts of docker containers:

1. Database (redis) - `db`
2. API module - `api`
3. Signal bot module - `signal`

## Configuration

The api

## Metrics

Metrics are exposed over `/metrics` *prometheus* endpoint.

TODO: metrics list

## Anti-enumeration algo

1. Different pools.
2. Sticky sessions.
3. User karma (±1 per time interval)

TODO: better description

## Authors

* TODO
* TODO
* Aleksei Kaplin <aleksei.kaplin.2021@gmail.com>
* TODO

Special thanks:

* TODO
