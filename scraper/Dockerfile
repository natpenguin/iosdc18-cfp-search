FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY constraints.txt ./

RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

COPY . .

ENV CFP_MONGO_HOST=mongo

CMD [ "python", "cfp_scraping.py" ]
