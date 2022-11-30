.PHONY: setup run db changes users locations websites statuses
default: setup run

setup:
	python setup.py

run:
	python main.py

db:
	sqlite3 spy.db

schema:
	sqlite3 spy.db .schema

changes:
	sqlite3 spy.db --header --table "select users.name, users.login, set_changes.change, set_changes.time from set_changes join users on users.github_id = set_changes.user_id order by time desc limit 10"
	sqlite3 spy.db --header --table "select users.name, users.login, user_changes.diff, user_changes.time from user_changes join users on users.github_id = user_changes.user_id order by time desc limit 10"

users:
	sqlite3 spy.db --header --table "select * from users"

locations:
	sqlite3 spy.db --header --table "select name, login, location from users where location not null"
	sqlite3 spy.db --header --table "select location, count(*) from users group by location having count(*) > 1 order by count(*) desc"

websites:
	sqlite3 spy.db --header --table "select name, login, website_url from users where website_url not null"

statuses:
	sqlite3 spy.db --header --table "select name, login, status_message from users where status_message not null"
