import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

#os.environ['BBHead_APIKey'] = 'api_key'

apikey = os.environ.get('BBHEAD_APIKEY')

#Retrieve Player ID#
def retrieve_pid(f="stephen", l="curry"):
    '''
    Internal function used to retrieve player id from player name inputs. Player id is necessary to make certain API calls.
    '''
    url = "https://basketball-head.p.rapidapi.com/players/search"

    payload = {
    	"pageSize": 50,
    	"firstname": f,
    	"lastname": l
    }
    headers = {
    	"content-type": "application/json",
    	"X-RapidAPI-Key": apikey,
    	"X-RapidAPI-Host": "basketball-head.p.rapidapi.com"
    }

    try: 
        r = requests.post(url, json=payload, headers=headers)

        json_r = r.json()

        body_json_r = json_r['body']

        df_pid = pd.DataFrame(body_json_r)
        play_id = df_pid.loc[0]['playerId']

        return play_id

    except:
        raise Exception("There was an error retrieving data from the API. Please double check spelling of player name and your API Key.")

#Return Basic Player Info#
def info(firstname="stephen", lastname="curry"):
    '''
    This function retrieves information from Basketball Head's search player endpoint. 
    Returns personal information, teams played for, draft information, awards, etc.

    Basketball Head API: https://rapidapi.com/kaylanhusband/api/basketball-head

    Parameters:
        1) firstname (default: "stephen")
        2) lastname (default: "curry")
        Both parameters must be lower case strings

    Output:
        List of player information

    Usage example:
        player_info(firstname="lebron", lastname="james")

            Output would be a list that includes various information on Lebron James,
            including date and place of birth, teams played for, draft position, awards, etc.
    '''
    url = "https://basketball-head.p.rapidapi.com/players/search"

    payload = {
    	"pageSize": 50,
    	"firstname": firstname,
    	"lastname": lastname
    }
    headers = {
    	"content-type": "application/json",
    	"X-RapidAPI-Key": apikey,
    	"X-RapidAPI-Host": "basketball-head.p.rapidapi.com"
    }

    r = requests.post(url, json=payload, headers=headers)
    
    print(r.json())
    return f"Here is some basic information about {firstname} {lastname}. If no information displays, please double check player name spelling."

#Return Salary Line Graph#
def salary(firstname="stephen", lastname="curry"):
    '''
    This function retrieves information from Basketball Head's salary endpoint. 
    Returns a simple line graph plotting salaries across seasons.

    Basketball Head API: https://rapidapi.com/kaylanhusband/api/basketball-head

    Parameters:
        1) firstname (default: "stephen")
        2) lastname (default: "curry")
        Both parameters must be lower case strings

    Output:
        Line graph of salaries across seasons.

    Usage example:
        salary(firstname="joel", lastname="embiid")

            Output would be a line graph showing Joel Embiid's salary across seasons played.
    '''
    pid=retrieve_pid(f=firstname, l=lastname)

    url = "https://basketball-head.p.rapidapi.com/players/{}/stats/Salary".format(pid)
    
    payload = {
    	"pageSize": 50,
    	"firstname": firstname,
    	"lastname": lastname
    }

    headers = {
        "content-type": "application/json",
    	"X-RapidAPI-Key": apikey,
    	"X-RapidAPI-Host": "basketball-head.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers)

    json_r = r.json()

    body_json_r = json_r['body']

    df = pd.DataFrame(body_json_r)

    df["salary"] = df["salary"].replace('[\$,]', '', regex=True).astype(float)
    df.plot.line(x = 'season', y = 'salary', title = firstname + ' ' + lastname)
    cvals = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in cvals])
        
    return plt.show()
        
#Return Specified Statistics Line Graph#
def stats(firstname="stephen", lastname="curry", stat="points", per="Game"):
    '''
    Pulls player statistics by age from Basketball Head API. Statistics can be per game, 36 minutes, or 100 possessions.
    Returns a simple line graph displaying the statistic across seasons.

    Basketball Head API: https://rapidapi.com/kaylanhusband/api/basketball-head

    Parameters:
        1) firstname (default: "stephen")
        2) lastname (default: "curry")
        First and second parameters must be lower case strings.

        3) stat (default: "points")
        Third parameter options: "points", "totalRebounds", "blocks", "steals", and others. 
        See Basketball Head API for full set of available statistics.
        Third parameter must be a string.
        
        4) per (default: "Game")
        Fourth parameter options: "Game", "36", or "100"
        Fourth parameter options indicate per game, per 36 minutes, or per 100 possessions.
        Fourth parameter must be a string.
        Fourth parameter input is used to tell function from which endpoint to pull.
        
    Output:
        Line graph of specified statistic across seasons.

    Usage examples:
        player_stats(firstname="joel", lastname="embiid")

            Output would be a line graph showing Joel Embiid's points per game across seasons.

        player_stats(firstname="joel", lastname="embiid", stat="totalRebounds", per="36")

            Output would be a line graph showing Joel Embiid's rebounds per 36 possessions across seasons.
    '''
    pid=retrieve_pid(f=firstname, l=lastname)

    url = "https://basketball-head.p.rapidapi.com/players/{}/stats/Per{}".format(pid, per)

    payload = {
    	"pageSize": 50,
    	"firstname": firstname,
    	"lastname": lastname
    }
    
    headers = {
        "content-type": "application/json",
    	"X-RapidAPI-Key": apikey,
    	"X-RapidAPI-Host": "basketball-head.p.rapidapi.com"
    }
        
    r = requests.get(url, headers=headers)
    
    json_r = r.json()

    body_json_r = json_r['body']

    df = pd.DataFrame(body_json_r)
        
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass
          
    try:
        if per=="Game":
            df.plot.line(x = 'season', y = '{}PerGame'.format(stat), title = firstname + ' ' + lastname)
            return plt.show()

        if per=="36":
            df.plot.line(x = 'season', y = '{}Per36Minutes'.format(stat), title = firstname + ' ' + lastname)
            return plt.show()
            
        if per=="100":
            df.plot.line(x = 'season', y = '{}Per100Possessions'.format(stat), title = firstname + ' ' + lastname)
            return plt.show()
    except:
        raise Exception("Error. Double check inputs. Is the statistic available on Basketball Head? Is it spelled properly?")

    else:
        return "Error. Is the per parameter a string?"
            