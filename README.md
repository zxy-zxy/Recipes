Django-REST-Framework based recipes project.

To run project with Docker container:
```bash
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up
```

Start container, then open another terminal and create user with admin access.
To run command with a running container:

Check container name:
```bash
docker container ls
```

Create superuser:
```bash
docker exec -i -t <container_name> python manage.py createsuperuser
```
