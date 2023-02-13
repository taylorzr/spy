import os
import sqlite3

import db
import github

org = os.getenv("ORG")
github_token = os.getenv("GITHUB_TOKEN")

con = sqlite3.connect("spy.db")
cur = con.cursor()


def diff(ghu):
    dbu = db.user(con, cur, ghu["github_id"])

    diff = {}

    if dbu["removed"] == 1:
        diff["removed"] = ["true", "false"]

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

    # NOTE: We get users from database including removed
    # because sometimes people are re-added, so we already have them in the db
    # and just need to mark them re-added
    #
    # But this means we need to check if someone has already been removed
    # when we're marking them removed
    dbu = db.users(con, cur, include_removed=True)
    dbru = db.users_removed(con, cur)
    ghu = github.users(github_token, org)

    added = ghu.keys() - dbu.keys()
    removed = dbu.keys() - ghu.keys()
    readded = ghu.keys() & dbru.keys()

    for id in added:
        if initialized:
            print(f"creating user: {ghu[id]}")
        db.create_user(con, cur, ghu[id], initialized)

    for id in removed:
        if dbu[id]["removed"] == 0:
            if initialized:
                print(f"removing user: {dbu[id]}")
            db.remove_user(con, cur, id, initialized)

    for id in readded:
        db.readd_user(con, cur, id)

    for id in ghu:
        user = ghu[id]
        d = diff(user)

        if d:
            print(f"updating user {user['login']}: {d}...")
            db.update_user(con, cur, user, d, initialized)

    if not initialized:
        db.set_config(con, cur, "initialized", "true")
