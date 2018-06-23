# Arsenal_Goal_Bot
A Goal bot to serve the /r/Gunners subreddit.  With simple commands members of the subreddit can rewatch their favorite goals

## How to run this package

1. Clone the repo
2. Create `config.py`, `assistComments.txt`, and `goalComments.txt` files
3. Ask @nicbaughman for information about those 3 files
4. Install posgres (recommend using [brew](https://brew.sh/)) Once Brew is installed run `brew install postgres`
5. Start postgres server `pg_ctl -D /usr/local/var/postgres start`
6. Log into that server using automatic user postgres `psql postgres`
7. Create new database in postgres `CREATE DATABASE arsenal_bot`
8. Create table in database (ask for proper table name)
    ```
    CREATE TABLE mens_goals (
        date CHAR(10),
        opposition CHAR(50),
        result CHAR(10),
        competition CHAR(50),
        season CHAR(10),
        scorer CHAR(50),
        assist CHAR(50),
        url CHAR(70),
        pen BOOLEAN
    );
    ```
9. Inspect the table was created correctly `\d+ TABLENAME`
10. Import CSV of all goal data `\copy mens_goals FROM '~/Downloads/Arsenal_goals.csv' DELIMITER ',' CSV HEADER;`
11. Import python packages `pip3 install praw psycopg2 unidecode`
12. Run script `python3 arsenalGoalBot.py`

## Other important things

- Starting Postgres `pg_ctl -D /usr/local/var/postgres start`
- Stopping Postgres `pg_ctl -D /usr/local/var/postgres stop`