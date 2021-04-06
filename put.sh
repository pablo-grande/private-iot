#!/bin/sh

device_id=${1:-1}
heartbeat=${2:-500}
port=${3:-8000}

curl -X PUT http://localhost:$port \
  -H "Content-Type: application/json" \
  --data '{"device_id": '$device_id', "data": {"heartbeat": '$heartbeat'}}'
