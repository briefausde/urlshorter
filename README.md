# Links shorter
Web service to shorten links with statistics of clicks in the last 30 days.

## How to start
If you use project locally, rename settings_local.py to settings.py

Further install requirements and make migrations

```python
pip install -r requirements.txt
```

```python
python manage.py makemigrations
python manage.py migrate
```

Ready! You can run the server

```python
python manage.py runserver
```
