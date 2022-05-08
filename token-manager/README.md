# Token manager

Service resposible for generating and validating tokens.

Token structure is `{uuid}` wihout `-` character for example `858c0eb798a8475dbcf67e29ddb4966e`.

## Communication with the frontend
The token manager communicates with the frontend application using websockets. Frontend informs the user about the status of the writer, about the successful or unsuccessful writing of the token, or about writing next token on tag. Websocket sends a `writer_status` event, which takes the values `off`, `idle`, ` success`, `error`.

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

### Activate NFC writer
Activate NFC writer machine. After turning on, machine's led will turn on and be able to write data to NFC tokens.

```http
POST /tokens/writer/activate
```

### Dectivate NFC writer
Deactivate NFC writer machine. Led on machine will turn off.

```http
POST /tokens/writer/deactivate
```

### Delete unwritten tokens
Delete unwritten NFC tokens from database.

```http
POST /tokens/writer/delete
```

### Update written token
Update NFC token state from unwritten to written

```http
POST /tokens/writer/update
```
```json
{
    "token": "token"
}
