#!/usr/bin/env bash
set -e

TOPIC_NAME="notifications"

echo "Waiting for Kafka to be ready..."

while ! kafka-topics.sh --bootstrap-server kafka-0:9092 --list; do
  sleep 1
done

echo "Kafka is ready"

declare -a topics=("email_notification" "websocket_notification")

for topic in "${topics[@]}"
do
  if kafka-topics.sh --bootstrap-server kafka-0:9092 --list | grep -q "^${topic}$"; then
    echo "Topic '${topic}' already exists. Skipping creation."
  else
    echo "Creating topic '${topic}'..."
    kafka-topics.sh --create --bootstrap-server kafka-0:9092 \
            --replication-factor 3 --partitions 3 --topic "${topic}" \
            --config min.insync.replicas=2 \
            --config retention.ms=86400000 \
            --config cleanup.policy=delete
    echo "Topic '${topic}' created successfully."
  fi
done


