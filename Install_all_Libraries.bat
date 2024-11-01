#!/bin/bash

# Install Airflow with constraints, using --user
pip install --user "apache-airflow==2.5.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt"

# Install the rest of the packages with --user
pip install --user -r requirements.txt
