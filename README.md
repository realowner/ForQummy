# GET STARTED

После клонирования запустьть докер контейнер при помощи команд:

```
docker build -t qummyimage .
docker run -d --name fastapicontainer -p 80:80 qummyimag
```

Перейти по адресу http://127.0.0.1:80

Для остановки:

```
docker stop fastapicontainer
```