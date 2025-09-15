# Kubernetes

---

## Local K8S Development

### Create Deployment
```shell
kubectl apply --validate=true --dry-run=true -f iws-deployment.yaml

Then

kubectl create -f iws-deployment.yaml
```

### Setup Local Registry

- Set the local registry first using this command
```
docker run -d -p 5000:5000 --restart=always --name registry registry:latest

OR

docker run -d -p 5016:5000 --restart=always --name local-registry registry:latest

OR
docker run -d -p 5000:5000 --name registry registry:latest
```


- Remove Registry
```shell
docker container stop registry && docker container rm -v registry
```

- To display available images we can simply run:
```shell
curl -X GET http://localhost:5000/v2/_catalog

OR

curl -X GET http://localhost:5016/v2/_catalog

OR

curl http://localhost:5016/v2/_catalog
```
Response:
```json
{"repositories":["posts-iws"]}
```


- 

### Docker Commands

- Build Docker Image & Tag

Given a ```Dockerfile```, the image could be built and tagged this easy way:

```shell
docker build -t localhost:5000/posts-iws:latest -f Dockerfile .

OR

docker build -t localhost:5000/posts-iws:latest .

OR

docker build . -t localhost:5000/posts-iws
```

- Image Tag

Tag the image to point to your local registry:
```shell
docker tag posts-iws:latest localhost:5000/posts-iws:latest
OR
docker tag posts-iws:latest localhost:5016/posts-iws:latest
```
- 

- Push the image on the local repo:
```shell
docker push localhost:5000/posts-iws
OR
docker push localhost:5016/posts-iws:latest
OR
sudo -E docker push localhost:5016/posts-iws:latest
```


- Verify your Local Registry setup

Log in to the Local Registry container and verify whether the image is present in it.
```shell
docker exec -it local-registry sh
ls -la var/lib/registry/docker/registry/v2/repositories/
```

- Runs the docker container as background service
```shell
docker run --name posts-iws -p 8080:8080 -d posts-iws:latest
OR
docker run --name posts-iws --rm -p 8080:8080 -d posts-iws:latest
```

- Shows the docker container's log
```shell
docker logs -f posts-iws
```

- Executes the 'bash' shell in the container
```shell
docker exec -it posts-iws bash
```

```shell
docker stop posts-iws && docker container rm posts-iws
```

### Deployment

The pod can be deployed using:
```shell
kubectl create -f iac/k8s/iws-pod.yaml
```

# Kubectl

Kubernetes Commands

## Deployment

- Create
```shell
kubectl create deployment posts-iws-deployment --image=localhost:5016/posts-iws

OR

kubectl apply -f iac/eks/nginx-deployment.yaml
```


- Delete
```shell
kubectl delete deployment posts-iws-deployment
OR
kubectl delete -f iac/eks/nginx-deployment.yaml
```

- Replace
```shell
kubectl edit deployment posts-iws-deployment
```


Note: -
In local ```minikube``` the external IP is not allocated by default.
To allocate an external IP run the following command:
````shell
minikube service mongo-express-service
````

- Check the logs of the ```mongo-express``` pod:
```shell
kubectl logs mongo-express-5d74874b84-79vr9
```

And notice the **basicAuth** credentials to login:

```text
Mongo Express server listening at http://0.0.0.0:8081
Server is open to allow connections from anyone (0.0.0.0)
basicAuth credentials are "admin:pass", it is recommended you change this in your config.js!
```




# Reference

- [Build a Scalable Flask Web Project From Scratch](https://kubeyaml.com/)
- [connection-refused-on-pushing-a-docker-image](https://stackoverflow.com/questions/52698748/connection-refused-on-pushing-a-docker-image)


### Docker

- [Docker Awesome Compose](https://github.com/docker/awesome-compose)


# Author
- Rohtash Lakra
