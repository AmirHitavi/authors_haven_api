#!/bin/bash

set -o errexit

set -o nounset

set -o pipefail

if [ -z "${POSTGRES_USER}" ]; then
  default_user='postgres'
  export POSTGRES_USER="${default_user}"
fi

export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

python << END
import sys
import time
import psycopg2

TIME_LIMIT = 30

start = time.time()

while True:
    try:
        psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
        break
    except psycopg2.OperationalError as e:
        sys.stderr.write("Waiting for PostgreSQL to become available.\n")
        if time.time() - start > TIME_LIMIT:
            sys.stderr.write(f"This is taking too long than expected. The following errors: {e}")
    time.sleep(1)
END

>&2 echo "PostgreSQL is available."

exec "$@"