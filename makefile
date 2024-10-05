run-infra:
	docker-compose -f docker-compose-infra.yml up -d

run-app:
	docker-compose -f docker-compose-app.yml up app

down:
	docker-compose -f docker-compose-infra.yml -f docker-compose-app.yml down

purge:
	docker-compose -f docker-compose-infra.yml down -v --rmi local
	docker-compose -f docker-compose-app.yml down -v --rmi local
	docker volume rm -f $$(docker volume ls -q)

lint:
	docker-compose run app flake8