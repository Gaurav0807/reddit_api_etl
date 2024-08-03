FROM apache/airflow:2.7.1-python3.11

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-11-jdk && \
    apt-get clean

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install apache-airflow-providers-apache-spark
RUN pip install airflow-provider-great-expectations 
RUN pip install apache-airflow
RUN pip install praw
RUN pip install s3fs
RUN pip install configparser datetime pandas pathlib numpy

