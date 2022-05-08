# Voting process manager

Deployed as one of the microservices on Gateway. Service notifies voting terminals when voting status changed. 


## How to run it

Clone the repo and navigate inside it. Build the image:

```bash
docker build -t voting-process-manager-image .
```

Run the container:

```bash
docker run -d --name voting-process-manager -p 8225:80 voting-process-manager-image
```

Navigate to ```localhost:8225/docs``` and you should see FastAPI docs for the service.

## API descriptions

### Start elections
Starts elections and notify all voting terminals.

```http
POST /start
```


### Stop elections
Stops elections and notify all voting terminals.

```http
POST /end
```

### Elections configuration
Returns necessary config fields for gateway from config.
```http
GET /election-config
```

### Terminals status
Returns necessary staus information of connected voting terminals.

```http
GET /terminals-status
```

### Gateway elections events
Get all elections events of start and end of elections.

```http
GET /gateway-elections-events
```

### Generate commission paper
Generate commission paper in pdf format encoded in base64 and store it into database.

```http
POST /commission-paper/generate
```

```json
{
  "polling_place_id": 0,
  "participated_members": [
    {
      "name": "Jožko Mrkvička",
      "agree": true
    },
    {
      "name": "Ferko Mrkvička",
      "agree": false
    },
    {
      "name": "Jan Mrkvička",
      "agree": true
    }
  ],
  "president": {
    "name": "Jožko Hlavný",
    "agree": true
  }
}
```

### Get commission paper
Get commission paper from database encoded in base64

```http
GET /commission-paper
```

### Send commission paper
Send commission paper to server.

```http
POST /commission-paper/send
```
