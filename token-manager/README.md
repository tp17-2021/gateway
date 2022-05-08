# Token manager

Service resposible for generating and validating tokens.

Token structure is `{uuid}` wihout `-` character for example `858c0eb798a8475dbcf67e29ddb4966e`.

## API description


### Generate token
Generates new token and returns it.

#### Request
```http
POST /tokens/create
```

#### Response
```json
{
    "status": "success",
    "token": "token"
}
```


### Validate token
Validate if provided token is valid.

#### Request
```http
POST /tokens/validate
```
```json
{
    "token": "token"
}
```
#### Response
If token is invalid returns empty response with status `403` else status `200`.


### Deactivate token
Deactivate provided token.

#### Request
```http
POST /tokens/deactivate
```
```json
{
    "token": "token"
}
```
#### Response
If token is invalid returns empty response with status `403` else status `200`.


### Delete token
Delete provided token.

#### Request
```http
DELETE /tokens/delete
```
```json
{
    "token": "token"
}
```
#### Response
If token is invalid returns empty response with status `403` else status `200`.
