.PHONY:
run:
	@docker-compose -f docker/docker-compose.yml up --build


.PHONY:
test:
	@docker-compose -f docker/docker-compose.yml run --rm web python3 manage.py test

.PHONY:
create_admin:
	@docker-compose -f docker/docker-compose.yml run --rm web python3 manage.py createsuperuser