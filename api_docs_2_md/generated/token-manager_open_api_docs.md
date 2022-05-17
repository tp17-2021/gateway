## API endpoints
---
title: FastAPI v0.1.0
language_tabs:
  - python: Python
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="fastapi">FastAPI v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Base URLs:

* <a href="/gateway/token-manager-api">/gateway/token-manager-api</a>

<h1 id="fastapi-default">Default</h1>

## root__get

<a id="opIdroot__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/token-manager-api/', headers = headers)

print(r.json())

```

`GET /`

*Root*

Simple hello message. 

> Example responses

> 200 Response

```json
null
```

<h3 id="root__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="root__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## activate_state_tokens_writer_activate_post

<a id="opIdactivate_state_tokens_writer_activate_post"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/writer/activate', headers = headers)

print(r.json())

```

`POST /tokens/writer/activate`

*Activate State*

Activate NFC writer machine. After turning on,
machine's LED will turn on and be able to write data to NFC tokens.

> Example responses

> 200 Response

```json
null
```

<h3 id="activate_state_tokens_writer_activate_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="activate_state_tokens_writer_activate_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## deactivate_state_tokens_writer_deactivate_post

<a id="opIddeactivate_state_tokens_writer_deactivate_post"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/writer/deactivate', headers = headers)

print(r.json())

```

`POST /tokens/writer/deactivate`

*Deactivate State*

Deactivate NFC writer machine. Led on machine will turn off.

> Example responses

> 200 Response

```json
null
```

<h3 id="deactivate_state_tokens_writer_deactivate_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="deactivate_state_tokens_writer_deactivate_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## delete_unwritten_tokens_writer_delete_post

<a id="opIddelete_unwritten_tokens_writer_delete_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/writer/delete', headers = headers)

print(r.json())

```

`POST /tokens/writer/delete`

*Delete Unwritten*

Delete unwritten NFC tokens from database. 

> Body parameter

```json
{
  "event": "string"
}
```

<h3 id="delete_unwritten_tokens_writer_delete_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_delete_unwritten_tokens_writer_delete_post](#schemabody_delete_unwritten_tokens_writer_delete_post)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete_unwritten_tokens_writer_delete_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete_unwritten_tokens_writer_delete_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## update_written_tokens_writer_update_post

<a id="opIdupdate_written_tokens_writer_update_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/writer/update', headers = headers)

print(r.json())

```

`POST /tokens/writer/update`

*Update Written*

Update NFC token state from unwritten to written.

> Body parameter

```json
{
  "token": "string"
}
```

<h3 id="update_written_tokens_writer_update_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_update_written_tokens_writer_update_post](#schemabody_update_written_tokens_writer_update_post)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="update_written_tokens_writer_update_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="update_written_tokens_writer_update_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## create_token_tokens_create_post

<a id="opIdcreate_token_tokens_create_post"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/create', headers = headers)

print(r.json())

```

`POST /tokens/create`

*Create Token*

Generates new token and returns it. 

> Example responses

> 200 Response

```json
null
```

<h3 id="create_token_tokens_create_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="create_token_tokens_create_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## validate_token_tokens_validate_post

<a id="opIdvalidate_token_tokens_validate_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/validate', headers = headers)

print(r.json())

```

`POST /tokens/validate`

*Validate Token*

Validate if provided token is valid.
If token is invalid returns empty response with status 403 else status 200.

> Body parameter

```json
{
  "token": "string"
}
```

<h3 id="validate_token_tokens_validate_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_validate_token_tokens_validate_post](#schemabody_validate_token_tokens_validate_post)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="validate_token_tokens_validate_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="validate_token_tokens_validate_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## deactivate_token_tokens_deactivate_post

<a id="opIddeactivate_token_tokens_deactivate_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/token-manager-api/tokens/deactivate', headers = headers)

print(r.json())

```

`POST /tokens/deactivate`

*Deactivate Token*

Deactivate provided token. Change active status to false.
If token is invalid returns empty response with status 403 else status 200.

> Body parameter

```json
{
  "token": "string"
}
```

<h3 id="deactivate_token_tokens_deactivate_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_deactivate_token_tokens_deactivate_post](#schemabody_deactivate_token_tokens_deactivate_post)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="deactivate_token_tokens_deactivate_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="deactivate_token_tokens_deactivate_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## delete_token_tokens_delete_delete

<a id="opIddelete_token_tokens_delete_delete"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.delete('/gateway/token-manager-api/tokens/delete', headers = headers)

print(r.json())

```

`DELETE /tokens/delete`

*Delete Token*

Delete provided token.
If token is invalid returns empty response with status 403 else status 200.

> Body parameter

```json
{
  "token": "string"
}
```

<h3 id="delete_token_tokens_delete_delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_delete_token_tokens_delete_delete](#schemabody_delete_token_tokens_delete_delete)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete_token_tokens_delete_delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete_token_tokens_delete_delete-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_Body_deactivate_token_tokens_deactivate_post">Body_deactivate_token_tokens_deactivate_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_deactivate_token_tokens_deactivate_post"></a>
<a id="schema_Body_deactivate_token_tokens_deactivate_post"></a>
<a id="tocSbody_deactivate_token_tokens_deactivate_post"></a>
<a id="tocsbody_deactivate_token_tokens_deactivate_post"></a>

```json
{
  "token": "string"
}

```

Body_deactivate_token_tokens_deactivate_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|token|string|true|none|none|

<h2 id="tocS_Body_delete_token_tokens_delete_delete">Body_delete_token_tokens_delete_delete</h2>
<!-- backwards compatibility -->
<a id="schemabody_delete_token_tokens_delete_delete"></a>
<a id="schema_Body_delete_token_tokens_delete_delete"></a>
<a id="tocSbody_delete_token_tokens_delete_delete"></a>
<a id="tocsbody_delete_token_tokens_delete_delete"></a>

```json
{
  "token": "string"
}

```

Body_delete_token_tokens_delete_delete

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|token|string|true|none|none|

<h2 id="tocS_Body_delete_unwritten_tokens_writer_delete_post">Body_delete_unwritten_tokens_writer_delete_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_delete_unwritten_tokens_writer_delete_post"></a>
<a id="schema_Body_delete_unwritten_tokens_writer_delete_post"></a>
<a id="tocSbody_delete_unwritten_tokens_writer_delete_post"></a>
<a id="tocsbody_delete_unwritten_tokens_writer_delete_post"></a>

```json
{
  "event": "string"
}

```

Body_delete_unwritten_tokens_writer_delete_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|event|string|true|none|none|

<h2 id="tocS_Body_update_written_tokens_writer_update_post">Body_update_written_tokens_writer_update_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_update_written_tokens_writer_update_post"></a>
<a id="schema_Body_update_written_tokens_writer_update_post"></a>
<a id="tocSbody_update_written_tokens_writer_update_post"></a>
<a id="tocsbody_update_written_tokens_writer_update_post"></a>

```json
{
  "token": "string"
}

```

Body_update_written_tokens_writer_update_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|token|string|true|none|none|

<h2 id="tocS_Body_validate_token_tokens_validate_post">Body_validate_token_tokens_validate_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_validate_token_tokens_validate_post"></a>
<a id="schema_Body_validate_token_tokens_validate_post"></a>
<a id="tocSbody_validate_token_tokens_validate_post"></a>
<a id="tocsbody_validate_token_tokens_validate_post"></a>

```json
{
  "token": "string"
}

```

Body_validate_token_tokens_validate_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|token|string|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[string]|true|none|none|
|msg|string|true|none|none|
|type|string|true|none|none|

