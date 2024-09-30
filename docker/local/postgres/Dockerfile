FROM postgres:15-bullseye

COPY ./docker/local/postgres/db_scripts /usr/local/bin/db_scripts

RUN chmod +x /usr/local/bin/db_scripts/*

RUN mv /usr/local/bin/db_scripts/* /usr/local/bin \
    && rmdir /usr/local/bin/db_scripts