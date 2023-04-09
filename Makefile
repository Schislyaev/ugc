#Makefile

up:
	cp ucg_service/env/.env.prod ucg_service/.env.example
	docker-compose --file ./elk_service/docker-compose.yml up -d --build
	docker-compose up -d --build

test:
	cp ucg_service/env/.env.test ucg_service/.env.example
	docker-compose -f docker-compose.test.yaml up -d --build
