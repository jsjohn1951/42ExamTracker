FROM postgres:16-alpine

USER postgres

RUN chmod 0700 /var/lib/postgresql/data

COPY ./scripts /scripts
