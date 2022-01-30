# Voting process manager

Deployed as one of the microservices on Gateway. Service notifies voting terminals when voting status changed. 


## How to run it

_Note: If you want to build and run the whole Gateway, reffer to [gateway repo](https://github.com/tp17-2021/gateway) and use docker-compose._

Clone the repo and navigate inside it. Build the image:

```bash
docker build -t voting-process-manager-image .
```

Run the container:

```bash
docker run -d --name voting-process-manager -p 8225:80 voting-process-manager-image
```

Navigate to ```localhost:8225/docs``` and you should see FastAPI docs for the service.

---