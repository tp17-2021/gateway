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

* <a href="/gateway/statevector">/gateway/statevector</a>

<h1 id="fastapi-default">Default</h1>

## hello__get

<a id="opIdhello__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/', headers = headers)

print(r.json())

```

`GET /`

*Hello*

Sample testing endpoint 

> Example responses

> 200 Response

```json
null
```

<h3 id="hello__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="hello__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_state_election_state_election_get

<a id="opIdget_state_election_state_election_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/state_election', headers = headers)

print(r.json())

```

`GET /state_election`

*Get State Election*

Get election state string 0 or 1 

> Example responses

> 200 Response

```json
null
```

<h3 id="get_state_election_state_election_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_state_election_state_election_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## set_state_election_state_election_post

<a id="opIdset_state_election_state_election_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/statevector/state_election', headers = headers)

print(r.json())

```

`POST /state_election`

*Set State Election*

Set election state string 0 or 1 

> Body parameter

```json
"string"
```

<h3 id="set_state_election_state_election_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="set_state_election_state_election_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="set_state_election_state_election_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_state_write_state_write_get

<a id="opIdget_state_write_state_write_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/state_write', headers = headers)

print(r.json())

```

`GET /state_write`

*Get State Write*

Get write state string 0 or 1 

> Example responses

> 200 Response

```json
null
```

<h3 id="get_state_write_state_write_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_state_write_state_write_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## set_state_write_state_write_post

<a id="opIdset_state_write_state_write_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/statevector/state_write', headers = headers)

print(r.json())

```

`POST /state_write`

*Set State Write*

Set write state string 0 or 1 

> Body parameter

```json
"string"
```

<h3 id="set_state_write_state_write_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="set_state_write_state_write_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="set_state_write_state_write_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## state_register_terminals_state_register_terminals_get

<a id="opIdstate_register_terminals_state_register_terminals_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/state_register_terminals', headers = headers)

print(r.json())

```

`GET /state_register_terminals`

*State Register Terminals*

Get terminals registration state string 0 or 1 

> Example responses

> 200 Response

```json
null
```

<h3 id="state_register_terminals_state_register_terminals_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="state_register_terminals_state_register_terminals_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## set_state_register_terminals_state_register_terminals_post

<a id="opIdset_state_register_terminals_state_register_terminals_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/statevector/state_register_terminals', headers = headers)

print(r.json())

```

`POST /state_register_terminals`

*Set State Register Terminals*

Set register terminals state string 0 or 1 

> Body parameter

```json
"string"
```

<h3 id="set_state_register_terminals_state_register_terminals_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="set_state_register_terminals_state_register_terminals_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="set_state_register_terminals_state_register_terminals_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_office_id_office_id_get

<a id="opIdget_office_id_office_id_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/office_id', headers = headers)

print(r.json())

```

`GET /office_id`

*Get Office Id*

Get office id 

> Example responses

> 200 Response

```json
null
```

<h3 id="get_office_id_office_id_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_office_id_office_id_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_pin_pin_get

<a id="opIdget_pin_pin_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/pin', headers = headers)

print(r.json())

```

`GET /pin`

*Get Pin*

Get pin 

> Example responses

> 200 Response

```json
null
```

<h3 id="get_pin_pin_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_pin_pin_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_server_key_server_key_get

<a id="opIdget_server_key_server_key_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/server_key', headers = headers)

print(r.json())

```

`GET /server_key`

*Get Server Key*

Get server key 

> Example responses

> 200 Response

```json
null
```

<h3 id="get_server_key_server_key_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_server_key_server_key_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_server_address_server_address_get

<a id="opIdget_server_address_server_address_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/statevector/server_address', headers = headers)

print(r.json())

```

`GET /server_address`

*Get Server Address*

Get server address 

> Example responses

> 200 Response

```json
null
```

<h3 id="get_server_address_server_address_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get_server_address_server_address_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

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

