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
	docker exec my_wallet python3 manage.py dumpdata wallet_app.Account > wallet_app/fixtures/account.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.Share > wallet_app/fixtures/share.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.Saving > wallet_app/fixtures/transaction.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.FixedInvestment > wallet_app/fixtures/transaction.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.VariableInvestment > wallet_app/fixtures/transaction.json
	docker exec my_wallet python3 manage.py dumpdata wallet_app.MonthlyExpense > wallet_app/fixtures/transaction.json
loaddata:
	docker exec -it my_wallet python3 manage.py loaddata */fixtures/*.json
database:
	docker exec -it db_wallet postgres -u -p -e"drop database wallet_db; create database wallet_db;"
pandas:
	docker exec my_wallet python3 manage.py excel_pandas
shares:
	docker exec my_wallet python3 manage.py share_values
