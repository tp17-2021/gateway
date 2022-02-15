# Voting Service

Deployed as one of the microservices on Gateway. Provides voting public API which receives electronic votes and tokens from Voting Terminals in a voting room.


## How to run it

_Note: If you want to build and run the whole Gateway, reffer to [gateway repo](https://github.com/tp17-2021/gateway) and use docker-compose._

Clone the repo and navigate inside it. Build the image:

```bash
docker build -t voting-service-image .
```

Run the container:

```bash
docker run -d --name voting-service -p 8222:80 voting-service-image
```

Navigate to ```localhost:8222/docs``` and you should see FastAPI docs for the service.

---

## API description

In case of invalid token and `403 status` of response an error data in FastAPI-like format is provided:

```json
{
  "detail": [
    {
      "loc": [
        "token"
      ],
      "msg": "Invalid token provided",
      "type": "string"
    }
  ]
}
```

### vote

```http
POST /api/vote
```
```json
{
    "vote": {},
    "token": "string"
}
```
| Key | Description |
| --- | --- |
| vote | JSON object of received vote |
| token | Voting token in string format |

The request receives a vote from a Voting Terminal, checks validity of token, registers vote in Vote DB and deactivates the token to disallow it from being used with another vote.

#### Response

If the token is valid and whole operation completed successfully, `status 204` and no data is returned.

If token is not valid, `status 403` and corresponding error data is returned.

If request is in incorrect format, `status 422` and corresponding error data managed by FastAPI is returned.

If a problem occurs during request handling on the server side, `status 500` and no data is returned.


### token-validity

```http
POST /api/token-validity
```
```json
{
    "token": "string"
}
```
| Key | Description |
| --- | --- |
| token | Voting token in string format |

The request receives a token from VT, checks validity of the token and returns wether token is valid or not.

#### Response

If the token is valid and whole operation completed successfully, `status 204` and no data is returned.

If token is not valid, `status 403` and corresponding error data is returned.

If request is in incorrect format, `status 422` and corresponding error data managed by FastAPI is returned.

If a problem occurs during request handling on the server side, `status 500` and no data is returned.

