import json
import sys


def config(con, cur, name):
    res = cur.execute("""
        select value from config
        where name = ?
    """, [name])
    result = res.fetchone() or ("false",)

    return result[0] == "true"


def set_config(con, cur, name, value):
    try:
        cur.execute("""
            insert or replace into config
            (name, value)
            values
            (?, ?)
        """, [name, value])
        con.commit()
    except Exception as e:
        print("Error setting config...")
        sys.exit(e)


def user(con, cur, id):
    res = cur.execute("""
        select * from users
        where github_id = ?
    """, [id])

    result = res.fetchone()
    columns = [desc[0] for desc in cur.description]
    data = dict(zip(columns, result))

    return data


def create_user(con, cur, user, initialized):
    try:
        cur.execute("""
            insert into users
            (github_id, name, login, location, website_url, status_message, status_emoji)
            values
            (?, ?, ?, ?, ?, ?, ?)
        """, [user["github_id"], user["name"], user["login"], user["location"], user["website_url"], user["status_message"], user["status_emoji"]])

        if initialized:
            cur.execute("""
                insert into set_changes
                (user_id, change, time)
                values
                (?, 'added', datetime('now'))
            """, [user["github_id"]])

        con.commit()
    except Exception as e:
        print("Error creating user...")
        sys.exit(e)


def remove_user(con, cur, user_id, initialized):
    try:
        cur.execute("""
            update users
            set removed = true
            where github_id = ?
        """, [user_id])

        if initialized:
            cur.execute("""
                insert into set_changes
                (user_id, change, time)
                values
                (?, 'removed', datetime('now'))
            """, [user_id])

        con.commit()
    except Exception as e:
        print("Error creating user...")
        sys.exit(e)


def update_user(con, cur, user, diff):
    data = json.dumps(diff)

    cur.execute("""
        insert into user_changes
        (user_id, diff)
        values
        (?, ?)
    """, [user["github_id"], data])

    cur.execute("""
        update users
        set name = ?
        , location = ?
        , website_url = ?
        , status_message = ?
        , status_emoji = ?
        where github_id = ?
    """, [user["name"], user["location"], user["websiteUrl"], user["status_message"], user["status_emoji"], user["github_id"]])

    con.commit()


def users(con, cur):
    res = cur.execute("""
        select * from users
        where removed = false
    """)

    result = res.fetchall()
    columns = [desc[0] for desc in cur.description]
    db_users = {}
    for row in result:
        data = dict(zip(columns, row))
        db_users[data["github_id"]] = data

    return db_users
