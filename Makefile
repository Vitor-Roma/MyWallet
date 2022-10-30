all:
	docker-compose up --build
up:
	docker-compose down
	docker-compose up -d
run:
	docker-compose down
	docker-compose up
build:
	docker exec my_wallet python3 manage.py migrate
migrations:
	docker exec my_wallet python3 manage.py makemigrations
down:
	docker-compose down
attach:
	docker attach my_wallet
enter:
	docker exec -it my_wallet /bin/bash
admin:
	docker exec -it my_wallet python3 manage.py createsuperuser --username admin
dumpdata:
	docker exec my_wallet python3 manage.py dumpdata wallet_app.AccountType > wallet_app/fixtures/account_type.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.Account > wallet_app/fixtures/account.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.TransactionCategory > wallet_app/fixtures/transaction_category.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.Transaction > wallet_app/fixtures/transaction.json
loaddata:
	docker exec -it my_wallet python3 manage.py loaddata */fixtures/*.json