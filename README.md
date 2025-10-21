### Required:

create super user:
```
(.djenv) [vagrant@docker django-fullstack]$ docker exec -it docker-web-1 /bin/bash
root@2b810f3f351e:/app# python manage.py createsuperuser
```


as super user, go to /admin, social applications, add google login

under config/const/const.py, provide google login and password

```
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
```

Due to `api/` using token with body username and password, requires https for security.
Recommend setup nginx, and proxy https and enable in settings

```aiignore
# Forces Django to redirect all HTTP requests to HTTPS — useful if Django is directly exposed to clients (not always needed behind Nginx)
SECURE_SSL_REDIRECT = True
# Ensures session cookies are only sent over HTTPS — protects user sessions from being intercepted
SESSION_COOKIE_SECURE = True
# Ensures CSRF tokens are only sent over HTTPS — prevents token leakage
CSRF_COOKIE_SECURE = True
# Tells Django to trust Nginx’s header and treat the request as HTTPS, even though it arrives as HTTP internally
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
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
