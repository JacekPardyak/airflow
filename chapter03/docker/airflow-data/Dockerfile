ARG AIRFLOW_BASE_IMAGE="apache/airflow:3.5.1-python3.8"
FROM ${AIRFLOW_BASE_IMAGE}

USER root
RUN mkdir -p /data && chown airflow /data

USER airflow
