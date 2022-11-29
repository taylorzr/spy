import os
import sqlite3

import db
import github

org = os.getenv("ORG")
github_token = os.getenv('GITHUB_TOKEN')

con = sqlite3.connect("spy.db")
cur = con.cursor()


def diff(ghu):
    dbu = db.user(con, cur, ghu["github_id"])

    diff = {}
    for key, value in ghu.items():
        if key in ["id", "github_id"]:
            continue

        if key not in dbu:
            # print(f"warning: db not tracking {key}")
            continue

        db_value = dbu[key]

        if db_value != value:
            diff[key] = (db_value, value)

    return diff


if __name__ == "__main__":
    initialized = db.config(con, cur, "initialized")

    if not initialized:
        print("looks like the first run, initializing database...")

    dbu = db.users(con, cur)
    ghu = github.users(github_token, org)

    added = ghu.keys() - dbu.keys()
    removed = dbu.keys() - ghu.keys()

    for id in added:
        if initialized:
            print(f"creating user: {ghu[id]}")
        db.create_user(con, cur, ghu[id], initialized)

    for id in removed:
        if initialized:
            print(f"removing user: {dbu[id]}")
        db.remove_user(con, cur, id, initialized)

    for id in ghu:
        d = diff(ghu[id])

        if d:
            print(f"updating user {ghu['login']: {d}}...")
            db.update_user(con, cur, ghu[id], d, initialized)

    if not initialized:
        db.set_config(con, cur, "initialized", "true")
