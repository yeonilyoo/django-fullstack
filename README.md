Required:

as super user, go to /admin, social applications, add google login

under common/const/const.py, provide google login and password

Note:

to generate translation

```
django-admin makemessages -l en
django-admin makemessages -l ko
```

then

```
django-admin compilemessages
```
