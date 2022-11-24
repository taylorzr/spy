.PHONY: setup run db changes
default: setup run

setup:
	python setup.py

run:
	python main.py

db:
	sqlite3 spy.db

changes:
	sqlite3 spy.db --header --table "select users.name, users.login, set_changes.change, set_changes.time from set_changes join users on users.github_id = set_changes.user_id order by time desc limit 10"
	sqlite3 spy.db --header --table "select users.name, users.login, user_changes.diff, user_changes.time from user_changes join users on users.github_id = user_changes.user_id order by time desc limit 10"
