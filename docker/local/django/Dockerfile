ARG PYTHON_VERSION=3.11.2-bullseye

FROM python:${PYTHON_VERSION} as python


FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt


FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY ./docker/local/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY ./docker/local/django/celery/worker/start.sh /start_worker.sh
RUN sed -i 's/\r$//g' /start_worker.sh
RUN chmod +x /start_worker.sh

COPY ./docker/local/django/celery/flower/start.sh /start_flower.sh
RUN sed -i 's/\r$//g' /start_flower.sh
RUN chmod +x /start_flower.sh

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint.sh"]