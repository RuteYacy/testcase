build:
	docker-compose build
run:
	docker-compose up
down:
	docker-compose down
purge:
	docker-compose -f docker-compose.yml down -v --rmi local
	docker volume rm -f $$(docker volume ls -q)
lint:
	docker-compose run app flake8