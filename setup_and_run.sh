#!/usr/bin/env bash
echo "Setting up project dependencies python,docker ..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip python3-pip python3-* vim docker git curl -y
pip3 install -r requirements.txt
echo "Starting Docker with RabbitMQ as Message Broker ..."
sudo docker run -p 5462:5462 rabbitmq
echo "Running Background Job..."
celery -A bg_celery_worker beat --loglevel=INFO
