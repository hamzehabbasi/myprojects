# FROM python:latest
#
# WORKDIR /code
#
# COPY requirements.txt/code/
# RUN pip install -u pip
# RUN pip install -r requirements.txt
#
# COPY ./code/
#
# CMD: ['gunicorn','webapp.wsgi',':8000']


# FROM python:3.8

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		sqlite3-client \
# 	&& rm -rf /var/lib/apt/lists/*
# #
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install -r requirements.txt
# COPY . .
#
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.8-slim

ADD . .
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD /usr/local/bin/gunicorn --bind 0.0.0.0:80 --workers 2 monirfund_back_proj.wsgi:application --timeout 100