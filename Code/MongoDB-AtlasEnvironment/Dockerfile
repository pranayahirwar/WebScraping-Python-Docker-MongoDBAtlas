FROM python:3.9.17-slim-bullseye

WORKDIR /web-scraping-code-here

COPY send-scrapedata-atlas.py .

RUN pip install selenium pymongo

CMD ["python", "send-scrapedata-atlas.py"]