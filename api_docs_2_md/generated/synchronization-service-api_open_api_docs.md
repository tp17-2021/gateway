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

* <a href="/gateway/synchronization-service-api">/gateway/synchronization-service-api</a>

<h1 id="fastapi-default">Default</h1>

## root__get

<a id="opIdroot__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/synchronization-service-api/', headers = headers)

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

## synchronize_synchronize_post

<a id="opIdsynchronize_synchronize_post"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.post('/gateway/synchronization-service-api/synchronize', headers = headers)

print(r.json())

```

`POST /synchronize`

*Synchronize*

Try to send local votes to server and updates local status.
If server response is different than 200, response has status 500 with error from server.

> Example responses

> 200 Response

```json
null
```

<h3 id="synchronize_synchronize_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="synchronize_synchronize_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## statistics_statistics_post

<a id="opIdstatistics_statistics_post"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.post('/gateway/synchronization-service-api/statistics', headers = headers)

print(r.json())

```

`POST /statistics`

*Statistics*

Provide statistics of votes in gateway database. Count of synchronized and unsynchronized votes.

> Example responses

> 200 Response

```json
null
```

<h3 id="statistics_statistics_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="statistics_statistics_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## seed_seed_post

<a id="opIdseed_seed_post"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.post('/gateway/synchronization-service-api/seed', headers = headers)

print(r.json())

```

`POST /seed`

*Seed*

Insert 10 unsynced dummy votes into gataway local gatabase. 

> Example responses

> 200 Response

```json
null
```

<h3 id="seed_seed_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="seed_seed_post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## test_encrypt_test_encrypt_get

<a id="opIdtest_encrypt_test_encrypt_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/gateway/synchronization-service-api/test-encrypt', headers = headers)

print(r.json())

```

`GET /test-encrypt`

*Test Encrypt*

Get a batch of encrypted votes. 

> Example responses

> 200 Response

```json
null
```

<h3 id="test_encrypt_test_encrypt_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="test_encrypt_test_encrypt_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

