import praw
import prawcore 
#import config
import postgresConfig
import psycopg2
import time
import unidecode
import os


def authenticate():
    is_prod = os.environ.get('IS_HEROKU', None)
    # grab all user configs from the config file
    # Note: File is not shared to reduce multiple instances of the bot running
    print("is prod?? ", is_prod)
    if is_prod:
        r = praw.Reddit(username = os.environ['username'],
                password = os.environ['password'],
                client_id = cos.environ['client_id'],
                client_secret = os.environ['client_secret'],
                user_agent = "Arsenal Goal Bot v0.1",
                )
                
        return r
    else:
        r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Arsenal Goal Bot v0.1",
                )
                
        return r

FOOTER = '''___\n\n
^^[Wiki](https://www.reddit.com/r/arsenal_goal_bot/wiki/index)
^^| ^^[Feedback](/r/arsenal_goal_bot)
^^| ^^[Creator](/u/BSUWolf)'''

def parse_body(body):
    # Find comments that start with the keyword and start indexing the characters
    start_index = body.find('!arsenalgoal ')
    # Remove first 13 characters to pull request
    body = body[start_index + 13:]
    # End indexing at a new line
    end_index = body.find('\n')

    print('user query: {}'.format(body))
    # Split the query into different sections at each comma
    query = body.split(',')

    return query

def parse_body_assist(body):
    # Find comments that start with the keyword and start indexing the characters
    start_index = body.find('!arsenalassist ')
    # Remove first 13 characters to pull request
    body = body[start_index + 15:]
    # End indexing at a new line
    end_index = body.find('\n')

    print('user query: {}'.format(body))
    # Split the query into different sections at each comma
    query = body.split(',')

    return query


def get_sql_items(query):
    # Create an empty array for params to be added to
    params = []
    # Designate variable for first portion of the query
    player_name = query[0].strip()

    # Remove special characters
    player_name_string = unidecode.unidecode(player_name)
    # Add player_name to params array
    params.append(player_name_string)
    
    # If query is longer than one section..
    if 0 <= 1 < len(query):
        # Create a variable for the second portion of the query
        second_query = query[1].strip()
        # Search to see if the second portion is a competion specific query
        if second_query == "league cup" or second_query == "community shield" or second_query == "premier league" or second_query == "fa cup" or second_query == "europa league" or second_query == "champions league":
            
            # Add second portion to the params
            params.append(second_query)

            if 0 <= 2 < len(query):

                third_query = query[2].strip()
                params.append(third_query)
                sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND competition = %s AND season = %s; '''
                return sqlquery, params
            
            # Build a query specific to search for player and competion
            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND competition = %s; '''
            print("Search via leagues")
            return sqlquery, params
        
        elif second_query is None:
            # TODO handle this better....
            print('No second query item')
            return("no item")

        elif second_query == "2017-2018" or second_query == "2016-2017":
            params.append(second_query)
            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND season = %s; '''
            return sqlquery, params

        # If the second section does not state a competition
        else:
            # add second section to params
            params.append(second_query)
            if 0 <= 2 < len(query):

                third_query = query[2].strip()
                params.append(third_query)
                sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND opposition = %s AND season = %s; '''
                return sqlquery, params

            # Query specifically for player and opposition
            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE scorer = %s AND opposition = %s; '''
            print("Not league query")
            return sqlquery, params


def get_assist_items(query):
    # Create an empty array for params to be added to
    params = []
    # Designate variable for first portion of the query
    player_name = query[0].strip()
    # Add player_name to params array
    params.append(player_name)
    
    # If query is longer than one section..
    if 0 <= 1 < len(query):
        # Create a variable for the second portion of the query
        second_query = query[1].strip()
        # Search to see if the second portion is a competion specific query
        if second_query == "league cup" or second_query == "community shield" or second_query == "premier league" or second_query == "fa cup" or second_query == "europa league" or second_query == "champions league":
            
            # Add second portion to the params
            params.append(second_query)

            if 0 <= 2 < len(query):

                third_query = query[2].strip()
                params.append(third_query)
                sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE assist = %s AND competition = %s AND season = %s; '''
                return sqlquery, params
            
            # Build a query specific to search for player and competion
            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE assist = %s AND competition = %s; '''
            print("Search via leagues")
            return sqlquery, params

        elif second_query == "2017-2018" or second_query == "2016-2017" or second_query == "2015-2016" or second_query == "2014-2015" or second_query == "2013-2014" or second_query == "2012-2013" or second_query == "2011-2012" or second_query == "2010-2011" or second_query == "2009-2010" or second_query == "2008-2009" or second_query == "2007-2008" or second_query == "2006-2007" or second_query == "2005-2006" or second_query == "2004-2005" or second_query == "2003-2004" or second_query == "2002-2003" or second_query == "2001-2002" or second_query == "2000-2001":
            params.append(second_query)
            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE assist = %s AND season = %s; '''
            return sqlquery, params

        # If the second section does not state a competition
        else:
            # add second section to params
            params.append(second_query)
            if 0 <= 2 < len(query):

                third_query = query[2].strip()
                params.append(third_query)
                sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE assist = %s AND opposition = %s AND season = %s; '''
                return sqlquery, params

            # Query specifically for player and opposition
            sqlquery = '''SELECT opposition, competition, season, url FROM mens_goals WHERE assist = %s AND opposition = %s; '''
            print("Not league query")
            return sqlquery, params


def get_urls(sqlquery, params):
    # Variables to connect to DB
    conn_string = "host='localhost' dbname='arsenal_bot' user='nic'"
    # Connect to DB
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    # Execute query to db for data
    cursor.execute(sqlquery, params)
    reply = ''

    if cursor:
        # For each record that comes back, loop through and build the reply
        for record in cursor:
            reply += '[{}: {} ({})](https://gfycat.com/{})'.format(record[0], record[1], record[2], record[3])
            reply += '\n\n'

        reply += FOOTER
        return reply
    

def run(r):
    # Get all comments from designated subreddits
    for comment in r.subreddit('arsenal_goal_bot+Gunners').stream.comments():
        body = comment.body
        # listen for any comments that contain the keyword
        if "!arsenalgoal" in body:
            with open('goalComments.txt', 'r') as outfile:
                seen_comments = outfile.read().splitlines()
            print(comment.id)
            # See if the comment in the subreddit has not already been answered.
            if comment.id not in seen_comments:

                body = comment.body.lower()
                query = parse_body(body)
                sql = get_sql_items(query)
                # If a query the individual tried to use is not in the correct format
                # mark it as helped and let the individual know where to get help.
                if sql is None:
                    reply = 'It looks liken your request is in a format I do not understand.  Feel free to [post a question in the help thread.](https://www.reddit.com/r/arsenal_goal_bot/comments/83i7ox/arsenal_goal_bot_questions/)'
                    comment.reply(reply)
                    with open('goalComments.txt', 'a+') as outfile:
                        outfile.write(comment.id + '\n')

                    print("not valid query..")
                    time.sleep(10)
                # If the comment uses the correct format find the results
                else:
                    print("this is sql: ", sql)
                    sqlThing = sql[0]
                    sqlParams = sql[1]
                    reply = get_urls(sqlThing, sqlParams)
                    
                    # Create and send the reply
                    if reply:
                        comment.reply(reply)
                        with open('goalComments.txt', 'a+') as outfile:
                            outfile.write(comment.id + '\n') 

                        print("Sleep for 10...")
                        time.sleep(10)
                    # If the reply comes back with no results. Let individual know
                    else:
                        reply = 'It seems that there is no information in the database for this request.  Feel free to [post a question in the help thread.](https://www.reddit.com/r/arsenal_goal_bot/comments/83i7ox/arsenal_goal_bot_questions/)'
                        comment.reply(reply)
                        with open('goalComments.txt', 'a+') as outfile:
                            outfile.write(comment.id + '\n') 

                        print("Sleep for 10...")
                        time.sleep(10)
            else:
                # print out when comment was already addressed
                print('comment already made')
                print("Sleep for 10...")
                time.sleep(10)

        # Pull in Gifs of Assists
        if "!arsenalassist" in body:
            print("arsenal assist command")
            # store list of existing comments associated with assists
            with open('assistComments.txt', 'r') as outfile:
                seen_comments = outfile.read().splitlines()
            print(comment.id)
            # See if the comment in the subreddit has not already been answered.
            if comment.id not in seen_comments:

                body = comment.body.lower()
                query = parse_body_assist(body)
                sql = get_assist_items(query)
                # If a query the individual tried to use is not in the correct format
                # mark it as helped and let the individual know where to get help.
                if sql is None:
                    reply = 'It looks liken your request is in a format I do not understand.  Feel free to [post a question in the help thread.](https://www.reddit.com/r/arsenal_goal_bot/comments/83i7ox/arsenal_goal_bot_questions/)'
                    comment.reply(reply)
                    with open('assistComments.txt', 'a+') as outfile:
                        outfile.write(comment.id + '\n')

                    print("not valid query..")
                    time.sleep(10)
                # If the comment uses the correct format find the results
                else:
                    print("this is sql: ", sql)
                    sqlThing = sql[0]
                    sqlParams = sql[1]
                    reply = get_urls(sqlThing, sqlParams)
                    
                    # Create and send the reply
                    if reply:
                        comment.reply(reply)
                        with open('assistComments.txt', 'a+') as outfile:
                            outfile.write(comment.id + '\n') 

                        print("Sleep for 10...")
                        time.sleep(10)
                    # If the reply comes back with no results. Let individual know
                    else:
                        reply = 'It seems that there is no information in the database for this request.  Feel free to [post a question in the help thread.](https://www.reddit.com/r/arsenal_goal_bot/comments/83i7ox/arsenal_goal_bot_questions/)'
                        comment.reply(reply)
                        with open('assistComments.txt', 'a+') as outfile:
                            outfile.write(comment.id + '\n') 

                        print("Sleep for 10...")
                        time.sleep(10)
            else:
                # print out when comment was already addressed
                print('comment already made')
                print("Sleep for 10...")
                time.sleep(10)


def main():
    # Authenticate the user
    r = authenticate()
    while True:
        # When authenticated...run the bot
        try:
            run(r)
        # For session time outs
        except prawcore.exceptions.ServerError as http_error:
            print(http_error)
            print('waiting 1 minute')
            time.sleep(60)
        except prawcore.exceptions.ResponseException as response_error:
            print(response_error)
            print('waiting 1 minute')
            time.sleep(60)
        except prawcore.exceptions.RequestException as request_error:
            print(request_error)
            print('waiting 1 minute')
            time.sleep(60)
        except Exception as e:
            print('error: {}'.format(e))
            print('waiting 1 minute')
            time.sleep(60)


if __name__ == '__main__':
    main()