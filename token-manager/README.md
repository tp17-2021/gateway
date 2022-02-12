# Token manager

Service resposible for generating and validating tokens.

Token structure is `{polling_place_id}_{uuid}` for example `1_858c0eb7-98a8-475d-bcf6-7e29ddb4966e`.

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


### Validate token
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