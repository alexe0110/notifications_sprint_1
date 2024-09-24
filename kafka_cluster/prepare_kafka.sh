#!/usr/bin/env bash
set -e

TOPIC_NAME="notifications"

echo "Waiting for Kafka to be ready..."

while ! kafka-topics.sh --bootstrap-server kafka-0:9092 --list; do
  sleep 1
done

echo "Kafka is ready"

if kafka-topics.sh --bootstrap-server kafka-0:9092 --list | grep -q "^${TOPIC_NAME}$"; then
  echo "Topic '${TOPIC_NAME}' already exists. Skipping creation."
else
  echo "Creating topic '${TOPIC_NAME}'..."
  kafka-topics.sh --create --bootstrap-server kafka-0:9092 \
          --replication-factor 3 --partitions 3 --topic "${TOPIC_NAME}" \
          --config min.insync.replicas=2 \
          --config retention.ms=86400000 \
          --config cleanup.policy=delete
  echo "Topic '${TOPIC_NAME}' created successfully."
fi
