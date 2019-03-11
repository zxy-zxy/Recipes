## Django-REST-Framework based recipes project.

### To run project with Docker container:
```bash
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up
```

To make migrations:

```bash
docker-compose -f docker-compose-dev.yml run --rm recipes sh -c "python manage.py makemigrations"
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


### If you want to run without docker-container, than simply:
```bash
python manage.py makemigrations --settings=app.settings.local_development
python manage.py migrate --settings=app.settings.local_development
python manage.py runserver --settings=app.settings.local_development
```