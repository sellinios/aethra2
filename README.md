microk8s kubectl port-forward svc/postgres 5432:5432 -n backend
python manage.py runserver 8080
