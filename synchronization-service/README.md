# Synchronization Service

Deployed as one of the microservices on Gateway. Service is synchronizing local votes database with main server database.


## How to run it

_Note: If you want to build and run the whole Gateway, reffer to [gateway repo](https://github.com/tp17-2021/gateway) and use docker-compose._

Clone the repo and navigate inside it. Build the image:

```bash
docker build -t synchronization-service-image .
```

Run the container:

```bash
docker run -d --name synchronization-service -p 8224:80 synchronization-service-image
```

Navigate to ```localhost:8224/docs``` and you should see FastAPI docs for the service.

---

## Vote structure
```
 {
    "token": "token",
    "candidates": [
        {
            "candidate_id" : "some_id"
        },
        {
            "candidate_id" : "another_id"
        }    
    ],
    "party_id": "custom_id1",
    "office_id": "custom_id2",
    "election_id": "custom_id3",
}
```

## API description

### synchronization

```http
POST /api/synchronize
```
Request try to send local votes to server and updates local status. If server response is different than `200`, response has status `500` with error from server.

### statistics
```http
POST /api/statistics
```
Request provide statistics of votes in gateway database. Count of synchronized and unsynchronized votes.