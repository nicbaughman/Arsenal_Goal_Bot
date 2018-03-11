import praw
import config
import postgresConfig
import psycopg2
import time

def authenticate():
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Arsenal Goal Bot v0.1",
            )

    return r

def parse_body(body):
    start_index = body.find('!arsenalgoal ')
    body = body[start_index + 13:]
    end_index = body.find('\n')

    print('user query: {}'.format(body))

    query = body.split(',')

    return query

def get_sql_items(query):

    params = []
    player_name = query[0].strip()
    params.append(player_name)
    

    if 0 <= 1 < len(query):
        second_query = query[1].strip()
        if second_query == "league cup" or second_query == "community shield" or second_query == "premier league" or second_query == "fa cup" or second_query == "europa league" or second_query == "champions league":
            params.append(second_query)

            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND competition = %s; '''
            print("Search via leagues")
            return sqlquery, params

        else:
            params.append(second_query)

            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND opposition = %s; '''
            print("Not league query")
            return sqlquery, params
            



def get_urls(sqlquery, params):
    conn_string = "host='localhost' dbname='arsenal_bot' user='nicbaughman'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('doing things...')
    print(sqlquery)
    print(params)
    cursor.execute(sqlquery, params)
    reply = ''

    if cursor:
        for record in cursor:
            reply += '[{}: {} ({})](https://gfycat.com/{})'.format(record[0], record[1], record[2], record[3])
            reply += '\n\n'

        return reply
    else:
        return rows
    



    
    


def run(r):
    print("Obtaining comments...")
    for comment in r.subreddit('arsenal_goal_bot+Gunners').comments(limit=25):
        body = comment.body
        print('lower body: ', body)
        if "!arsenalgoal" in body:

            with open('commented.txt', 'r') as outfile:
                seen_comments = outfile.read().splitlines()

            if comment.id not in seen_comments:

                body = comment.body.lower()
                query = parse_body(body)
                sql = get_sql_items(query)
                print("this is sql: ", sql)
                sqlThing = sql[0]
                sqlParams = sql[1]
                reply = get_urls(sqlThing, sqlParams)
                print("what are this: ", reply)
                if reply:
                    comment.reply(reply)
                    with open('commented.txt', 'a+') as outfile:
                        outfile.write(comment.id + '\n') 

                    print("Sleep for 10...")
                    time.sleep(10)
                else:
                    with open('commented.txt', 'a+') as outfile:
                        outfile.write(comment.id + '\n') 

                    print("Sleep for 10...")
                    time.sleep(10)
            else:
                print('comment already made')
                print("Sleep for 10...")
                time.sleep(10)






    






r = authenticate()
while True:
        run(r)