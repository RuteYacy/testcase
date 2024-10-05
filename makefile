build:
	docker-compose build
run:
	docker-compose up
down:
	docker-compose down
purge:
	docker-compose down --volumes --rmi all