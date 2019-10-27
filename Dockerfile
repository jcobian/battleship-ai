FROM python:3.6

RUN pip install -U pip > /dev/null

COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ./docker-entrypoint.sh
