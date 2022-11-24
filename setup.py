import sqlite3

con = sqlite3.connect("spy.db")
cur = con.cursor()

cur.execute("""
create table if not exists config (
   name text not null unique
   , value text not null
)
""")

cur.execute("""
create table if not exists users (
  id integer primary key
  , github_id text not null unique
  , login text not null unique
  , name text
  , location text
  , website_url text
  , status_message text
  , status_emoji text
  , removed bool default false
);
""")

cur.execute("""
create table if not exists set_changes (
  id integer primary key
  , user_id text not null
  , change text not null
  , time datetime not null default current_timestamp
);
""")

cur.execute("""
create table if not exists user_changes (
  id integer primary key
  , user_id text not null
  , diff text not null
  , time datetime not null default current_timestamp
);
""")

cur.execute("""
insert into users
(github_id, name, login, location, website_url, status_message, status_emoji)
values
(?, ?, ?, ?, ?, ?, ?)
on conflict (login) do nothing
""", ["taco", "Fake User", "fake", None, None, None, None])
con.commit()
