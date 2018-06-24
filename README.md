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
9. Inspect the table was created correctly `\d+ TABLENAME;`
10. Import CSV of all goal data `\copy mens_goals FROM '~/Downloads/Arsenal_goals.csv' DELIMITER ',' CSV HEADER;`
11. Import python packages `pip3 install praw psycopg2 unidecode`
12. Run script `python3 arsenalGoalBot.py`

## Other important things

- Starting Postgres `pg_ctl -D /usr/local/var/postgres start`
- Stopping Postgres `pg_ctl -D /usr/local/var/postgres stop`

## Big Learnings I had

Moving the bot to Heroku was NOT as straight forward as I imagined.  I should probably document this for anyone looking to deploy their bot to Heorku.  One of the main drivers for me to use Heroku is their free tier.  Sure the bot may be down for a few hours a day but that seems like a small price to pay IMO.  Also I have never done any dev ops or Continuous Integration before so this seemed like a good opportunity to learn.

1. Make an account on Heroku and then in your repo run `heroku login`
2. I needed a requirements.txt file so I ran `pip freeze > requirements.txt `
3. Had to create a Procfile to run my script so added `worker: python arsenalGoalBot.py` to run the script
4. Once I had the requirements and Procfile files I created a server in Heroku by navigating to the project folder and running `heroku create`
5. From there I setup some config variables in the server settings.
6. Then added some [Production and Local config variables](https://github.com/nicbaughman/Arsenal_Goal_Bot/commit/28b8df0fd8843de4cacfbf6eb480c1b6da8b391c) in my script
7. Pushed the code to the heroku server `git push heroku master`
8. Observe the logs with `heroku logs` to make ssure everything worked okay
9. Then I had to setup the postgress DB. Which included updating the postgres config to check if we are in Production or Local
10. Then looked at the configs for the Postgres DB in Heroku and added them as config variables