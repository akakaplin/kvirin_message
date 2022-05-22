# kvirin_message

Kvirin Message for DEMHACK 4

## Components

All components are parts of docker containers:

1. Database (redis) - `db`
2. API module - `api`
3. Signal bot module - `signal`

## API

API container endpoints:

1. User can request his bridges via *POST* request to `/bridge`.

Expected request body:

```json
  {
  proto: signal,
  cell: +7900100001001000,
  nickname: …,
  uid: …,
  }
```

2. Metrics are exposed over *GET* `/metrics` *prometheus* endpoint.

Supported metrics:
TODO

3. Admin can increase or decrease user *karma* using *POST* `/report` endpoint.

Expected request body:

```json
  {
  state: true,
  bridge: "bridge_txt",
  }
```

This request will increase or decrease *karma* counter for all users associated with the specific bridge.
It can be invokes when bridge availability is analyzed (ban detected).

## Configuration

An example configudation:

```yaml
pools:
  bad:
    features:
      - feature: is_bad
        value: true
    bridges:
      - bad_1
      - bad_2
      - bad_3
      - bad_4
```

Here we create a pool with 4 bridges inside & 1 predicate feature

## Anti-enumeration algo

1. *Different pools* - admin is able to configure different pools with different alighment mechanisms.
2. *Sticky sessions* - Inside pools, users are assigned randomly.
3. *User karma* - we can track users carma by IP (±1 per time interval) via `/report` endpoint.

```mermaid
  graph TD;
      A[Fresh new user] -->|Sticky session| B(Quarantine)
      B-->|Report OK| C(Good users);
      B-->|Report BAD| D(Bad users);
      C-->|Report BAD| D(Bad users);
```

### Potential improvements

1. Penalize for a specific vector. not for the whole world. Like "bad in China".
2. Right now, sticky sessions are reset on a service restart. Probably, they should not.

## Authors

* TODO
* TODO
* Aleksei Kaplin <aleksei.kaplin.2021@gmail.com>
* TODO

Special thanks:

* TODO
