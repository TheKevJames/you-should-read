all:
	@cat Makefile


db:
	sqlite3 database/database.db

reset:
	sqlite3 database/database.db < database/schema.sql

run:
	python server.py

sass:
	sass --watch you_should_read/static/sass:you_should_read/static/css
