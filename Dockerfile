FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -c constraint.txt

COPY . .

CMD [ "gunicorn", "api:app", "-b", "0.0.0.0:8000" ]
