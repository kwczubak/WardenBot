FROM postgres

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres

COPY initdb.sql /docker-entrypoint-initdb.d/
