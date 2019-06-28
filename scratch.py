import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re
import ast
import time 
from datetime import datetime


# function to run everything
def run_scrape():
    make_game_df()n poor areas
    return None

# function to get game info
def get_game_info(url):
    '''
    creates a pandas dataframe of game info using beautiful soup to scrape
     from baseball-reference.com

    Parameters
    ----------
    url: the URL of the game page to scrape
    
    Returns
    -------
    game_info_df: the dtaframe of game info
    '''

    # set page source
    game_page = requests.get(url) # used url passed through as a parameter
    soup = BeautifulSoup(game_page.text, 'html.parser')

    # get game info including attendance data
    game_info = []
    game_info_raw = soup.find('div', attrs = {'class': 'scorebox_meta'}) # gets game info data by class
    for data in game_info_raw.find_all('div'):  # for loop to go through game info
        game_info.append(data.get_text()) # add game info to list

    # remove last three lines of list, unneeded info
    game_info.pop() 
    game_info.pop()
    game_info.pop()

    # standardize format of elements in list by fixing date element
    game_info[0]='date: '+game_info[0]   

    # add game id 
    sep1, sep2 = '.', '/'
    game_id = url.split(sep1)[2]
    game_id = str('game_id: ' + game_id.split(sep2)[3])
    game_info = [game_id] + game_info  # add game id to beginning of game info list

    # get runs scored
    game_runs = []
    for data in soup.find_all('div', attrs = {'class': 'score'}):  # for loop to go through game runs
        game_runs.append(data.get_text())    # add game runs to list


    # combine game_info and _game_runs and make all the data formatted the same
    game_info = game_info + game_runs   # combine game_runs and game_info
    game_info[-1]='home_team_runs: '+game_info[-1] # add formatting to new entries to get the whole list the same
    game_info[-2]='away_team_runs: '+game_info[-2]
    game_info = [x.replace(' ', '_') for x in game_info]  # replaces spaces with underscores
    game_info = [x.replace(':_', '":"') for x in game_info] 
    game_info = [x.lower() for x in game_info]  # lowercase
    game_info = ['"' + x + '"' for x in game_info]
    game_info = ','.join(game_info)
    game_info = '{' + game_info + '}'
    game_info = [game_info] 


    # convert game_info to a list of dictionaries
    game_info_dicts = []
    for i in game_info:
        game_info_dicts.append(ast.literal_eval(i))
    
    game_info_df = pd.DataFrame(game_info_dicts)
    return game_info_df


# function to run scrape,  merge dataframes, return final dataframe
def make_game_df():
    '''
    Begin the scrape process for 2018 MLB game data, 
    save as csv, and return as a dataframe.
    
    Paramters:  None

    '''

    # open the games file
    with open('/home/jake/data_science/capstones/scoring-attendance/scrape/games20.txt', 'r') as games:
        raw_text=games.read()
        while '\n,' in raw_text:  # clean up formatting
            raw_text=raw_text.replace('\n,', ',')

    game_list = raw_text.split(',')  # create game list

    all_game_info_df = pd.DataFrame()  # create empty dataframe


    # open log file
    scrape_log = open('scrape_log.txt','a')


    # loop through urls, check for valid site, if valid append df, log results
    # timers:  2 sec on success, 4 sec on fail
    for url in game_list:
        try:
            game_page = requests.get(url)
            if game_page.status_code == 200:
                all_game_info_df = all_game_info_df.append(get_game_info(url), ignore_index=True)
                result = str(datetime.now()) + ':::' + str(game_page.status_code) + ':::' + str(url)
                scrape_log.write("\nsuccess %s" % (result))
                print("success %s" % (result))
                time.sleep(2) # VERY IMPORTANT - timer delay for get requests - DO NOT DELETE
            else:
                result = str(datetime.now()) + ':::' + str(game_page.status_code) + ':::' + str(url) 
                scrape_log.write("\nFAILURE %s" % (result))
                print("FAILURE %s" % (result))
                time.sleep(3) # VERY IMPORTANT - timer delay for get requests - DO NOT DELETE
        except Exception as e:
            result = str(datetime.now()) + ':::' + str(e) + ':::' + str(url)
            scrape_log.write('\nEXCEPTION: %s' % (result))
            print('EXCEPTION: ' + str(e) + result)

    # close log file
    scrape_log.close()


    # final cleanup on dataframe, these issues were discovered during EDA
    all_game_info_df['attendance'] = all_game_info_df['attendance'].replace({',': ''}, regex=True)
    all_game_info_df['attendance'] = pd.to_numeric(all_game_info_df['attendance'])
    all_game_info_df['date'] = all_game_info_df['game_id'].map(lambda x: str(x)[:-1])
    all_game_info_df['date'] = all_game_info_df['date'].map(lambda x: str(x)[3:])
    all_game_info_df['date'] = pd.to_datetime(all_game_info_df['date'])
    all_game_info_df['team_id'] = all_game_info_df['game_id'].map(lambda x: str(x)[:-9])    # add team_id
    
    # add capacity column
    capacity_df = pd.read_csv('/home/jake/data_science/capstones/scoring-attendance/scrape/capacity.csv')
    all_game_info_df = pd.merge(all_game_info_df, capacity_df, on='team_id', how='outer') 
    all_game_info_df = all_game_info_df.reset_index()

    
    # save csv file from dataframe
    all_game_info_df.to_csv('final_game_info.csv')


    # return the dataframe
    return all_game_info_df


# for debugging

'''
if __name__ == '__main__':
    make_game_df()

    '''