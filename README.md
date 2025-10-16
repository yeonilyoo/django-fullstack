### Required:

as super user, go to /admin, social applications, add google login

under config/const/const.py, provide google login and password

```
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
```

### Note:

to generate translation

```
django-admin makemessages -l en
django-admin makemessages -l ko
```

then

```
django-admin compilemessages
```
