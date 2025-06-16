FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ldap3 mysql-connector-python pytest
CMD ["python", "sync_ad_group.py"]
