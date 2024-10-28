# ODBC buddy

utility i set up once i configured odbc on one system because it's hard to do on each new computer


docker-compose up --build -d



it should work on the computer you run it on but then you can just hit this url - just keep it secret. this is for a temporary project and i only use it when i need it.

configure via nginx so you can only access from development computer

runs via sudo systemctl restart gunicorn-flask

then you can see logs with `sudo journalctl -u gunicorn-flask | tail -n 200`
