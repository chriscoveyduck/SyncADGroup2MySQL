#!/bin/bash
# Script to prompt for secret values and output base64-encoded YAML for Kubernetes

read -p "AD_SERVER: " AD_SERVER
read -p "AD_USER: " AD_USER
read -s -p "AD_PASSWORD: " AD_PASSWORD; echo
read -p "MYSQL_HOST: " MYSQL_HOST
read -p "MYSQL_USER: " MYSQL_USER
read -s -p "MYSQL_PASSWORD: " MYSQL_PASSWORD; echo
read -p "MYSQL_DB: " MYSQL_DB
read -p "AD_GROUP [SmtpEnabledUsers]: " AD_GROUP
AD_GROUP=${AD_GROUP:-SmtpEnabledUsers}
read -p "AD_DOMAIN_FQDN (e.g. your.domain.com): " AD_DOMAIN_FQDN
read -p "SYNC_INTERVAL_MINUTES [60]: " SYNC_INTERVAL_MINUTES
SYNC_INTERVAL_MINUTES=${SYNC_INTERVAL_MINUTES:-60}

echo "apiVersion: v1
kind: Secret
metadata:
  name: syncadgroup-secrets
type: Opaque
data:
  AD_SERVER: $(echo -n "$AD_SERVER" | base64)
  AD_USER: $(echo -n "$AD_USER" | base64)
  AD_PASSWORD: $(echo -n "$AD_PASSWORD" | base64)
  MYSQL_HOST: $(echo -n "$MYSQL_HOST" | base64)
  MYSQL_USER: $(echo -n "$MYSQL_USER" | base64)
  MYSQL_PASSWORD: $(echo -n "$MYSQL_PASSWORD" | base64)
  MYSQL_DB: $(echo -n "$MYSQL_DB" | base64)
  AD_GROUP: $(echo -n "$AD_GROUP" | base64)
  AD_DOMAIN_FQDN: $(echo -n "$AD_DOMAIN_FQDN" | base64)
  SYNC_INTERVAL_MINUTES: $(echo -n "$SYNC_INTERVAL_MINUTES" | base64)" > secrets.yaml

echo "secrets.yaml generated. Review and apply with: kubectl apply -f secrets.yaml"
