FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY constraints.txt ./

RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

COPY . .

CMD [ "gunicorn", "api:app", "-b", "0.0.0.0:8000" ]
