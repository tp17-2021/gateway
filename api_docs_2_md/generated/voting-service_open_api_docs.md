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

* <a href="/gateway/voting-service-api">/gateway/voting-service-api</a>

<h1 id="fastapi-default">Default</h1>

## hello__get

<a id="opIdhello__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/voting-service-api/', headers = headers)

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

## vote_api_vote_post

<a id="opIdvote_api_vote_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/voting-service-api/api/vote', headers = headers)

print(r.json())

```

`POST /api/vote`

*Vote*

Receives vote with valid token, validates the token,
sotres the vote and invalidates the token.

Returns:
    200: Vote was successfully stored
    403: Token is invalid
    409: The election is not running at the moment
    422: Invalid request body

> Body parameter

```json
{
  "voting_terminal_id": "string",
  "payload": {
    "encrypted_message": "string",
    "encrypted_object": "string"
  }
}
```

<h3 id="vote_api_vote_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_vote_api_vote_post](#schemabody_vote_api_vote_post)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="vote_api_vote_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="vote_api_vote_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## token_validity_api_token_validity_post

<a id="opIdtoken_validity_api_token_validity_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/gateway/voting-service-api/api/token-validity', headers = headers)

print(r.json())

```

`POST /api/token-validity`

*Token Validity*

Checks if the provided token is valid. 

> Body parameter

```json
{
  "voting_terminal_id": "string",
  "payload": {
    "encrypted_message": "string",
    "encrypted_object": "string"
  }
}
```

<h3 id="token_validity_api_token_validity_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_token_validity_api_token_validity_post](#schemabody_token_validity_api_token_validity_post)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="token_validity_api_token_validity_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="token_validity_api_token_validity_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_Body_token_validity_api_token_validity_post">Body_token_validity_api_token_validity_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_token_validity_api_token_validity_post"></a>
<a id="schema_Body_token_validity_api_token_validity_post"></a>
<a id="tocSbody_token_validity_api_token_validity_post"></a>
<a id="tocsbody_token_validity_api_token_validity_post"></a>

```json
{
  "voting_terminal_id": "string",
  "payload": {
    "encrypted_message": "string",
    "encrypted_object": "string"
  }
}

```

Body_token_validity_api_token_validity_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|voting_terminal_id|string|true|none|none|
|payload|[VoteEncrypted](#schemavoteencrypted)|true|none|Attributes<br>----------<br>encrypted_message: str<br>    AES encrypted message.<br>encrypted_object: str<br>    RSA encrypted AES key and other data.|

<h2 id="tocS_Body_vote_api_vote_post">Body_vote_api_vote_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_vote_api_vote_post"></a>
<a id="schema_Body_vote_api_vote_post"></a>
<a id="tocSbody_vote_api_vote_post"></a>
<a id="tocsbody_vote_api_vote_post"></a>

```json
{
  "voting_terminal_id": "string",
  "payload": {
    "encrypted_message": "string",
    "encrypted_object": "string"
  }
}

```

Body_vote_api_vote_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|voting_terminal_id|string|true|none|none|
|payload|[VoteEncrypted](#schemavoteencrypted)|true|none|Attributes<br>----------<br>encrypted_message: str<br>    AES encrypted message.<br>encrypted_object: str<br>    RSA encrypted AES key and other data.|

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

<h2 id="tocS_VoteEncrypted">VoteEncrypted</h2>
<!-- backwards compatibility -->
<a id="schemavoteencrypted"></a>
<a id="schema_VoteEncrypted"></a>
<a id="tocSvoteencrypted"></a>
<a id="tocsvoteencrypted"></a>

```json
{
  "encrypted_message": "string",
  "encrypted_object": "string"
}

```

VoteEncrypted

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|encrypted_message|string|true|none|none|
|encrypted_object|string|true|none|none|

