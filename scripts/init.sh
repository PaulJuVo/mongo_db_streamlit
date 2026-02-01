#!/bin/bash
set -e

MODE="prod"
COMPOSE="docker-compose.prod.yml"

while getopts "d" opt; do
  case $opt in
    d)
      MODE="dev"
      COMPOSE="docker-compose.yml"
      ;;
    *)
      ;;
  esac
done



echo "--- $MODE initialisation started---"
docker compose -f $COMPOSE up -d mongodb
docker compose -f $COMPOSE run --rm migrate     
# docker compose up --build app 