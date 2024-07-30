DOCKER_COMPOSE_FILE := docker-compose.yml
DOCKER_SERVER_SERVICE := server
DOCKER_DATABASE_SERVICE := db

.PHONY: build up ps bash_db

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

up:
	# コンテナ名のコンフリクトを避けるために既存のコンテナを削除
	docker compose -f $(DOCKER_COMPOSE_FILE) rm -f
	docker compose -f $(DOCKER_COMPOSE_FILE) up

ps:
	docker compose -f $(DOCKER_COMPOSE_FILE) ps

bash_server:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec $(DOCKER_SERVER_SERVICE) bash

bash_db:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec $(DOCKER_DATABASE_SERVICE) bash