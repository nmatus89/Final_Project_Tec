#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask_pymongo import pymongo
from scipy.stats import poisson
import math
import matplotlib.pyplot as plt

import requests


def init_browser_alf():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

VR_dict_WLT_premier={}
VR_dict_OU_premier={}

def scrape_premier_alf():
    url='https://www.futbolya.com/inglaterra/premier-league/2016-2017/temporada-regular/resultados-y-calendario'

    home_teams=[]
    away_teams=[]
    home_goals=[]
    away_goals=[]
    results=[]
    seasons=[]

    browser=init_browser_alf()
    browser.visit(url)
    response=requests.get(url)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2016-2017")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass
                except IndexError:
                    pass
        except AttributeError:
            pass
    url1='https://www.futbolya.com/inglaterra/premier-league/2017-2018/temporada-regular/resultados-y-calendario'
    browser.visit(url1)
    response=requests.get(url1)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2017-2018")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass

                except IndexError:
                    pass
        except AttributeError:
            pass
    url2='https://www.futbolya.com/inglaterra/premier-league/2018-2019/temporada-regular/resultados-y-calendario'
    browser.visit(url2)
    response=requests.get(url2)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2018-2019")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                if scores=="POST":
                    home_goals.append(0)
                    away_goals.append(0)
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass

                except IndexError:
                    pass
        except AttributeError:
            pass
    url3='https://www.futbolya.com/inglaterra/premier-league/Premier-League-2019-2020/Temporada-Regular/resultados-y-calendario'
    browser.visit(url3)
    response=requests.get(url3)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)            
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2019-2020")           
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                if "-" not in scores:
                    pass
                else:
                    home_goal=int(scores.split("-")[0].replace(" ",""))
                    home_goals.append(home_goal)
                    away_goal=int(scores.split("-")[1].replace(" ",""))
                    away_goals.append(away_goal)
        except AttributeError:
            pass
    browser.quit()

    played=int(len(home_goals))
    to_be_played=int(len(home_teams))

    away_to_be_played=away_teams[played:to_be_played]
    home_to_be_played=home_teams[played:to_be_played]
    games_to_be_played=list(zip(home_to_be_played,away_to_be_played))
    games_to_be_played_df=pd.DataFrame(games_to_be_played,columns=["home_team","away_team"])

    home_teams=home_teams[0:played]
    away_teams=away_teams[0:played]
    premier=list(zip(home_teams,away_teams,home_goals,away_goals, seasons))
    premier_df=pd.DataFrame(premier,columns=["home_team","away_team","home_goals","away_goals","season"])
    
    league_away_goals=premier_df.away_goals.mean()
    league_home_goals=premier_df.home_goals.mean()

    team_means_home=premier_df.groupby("home_team").mean().reset_index()
    team_means_away=premier_df.groupby("away_team").mean().reset_index()

    team_means_home["away_defense_force"]=team_means_away.home_goals/league_home_goals
    team_means_home["away_attack_force"]=team_means_away.away_goals/league_away_goals
    team_means_home["home_attack_force"]=team_means_home.home_goals/league_home_goals
    team_means_home["home_defense_force"]=team_means_home.away_goals/league_away_goals
    team_means_home["home_team_goals_league_average"]=league_home_goals
    team_means_home["away_team_goals_league_average"]=league_away_goals

    counting=premier_df.groupby(["home_team"])["away_team"].count()
    team_means_home=pd.merge(team_means_home, counting, on='home_team')
    team_means_home.rename(columns={"away_team":"N"})

    VR_input_apuestas=team_means_home
    
    VR_home_info=VR_input_apuestas.loc[:,["home_team","home_goals","home_defense_force","home_attack_force",
                                      "home_team_goals_league_average"]]

    VR_away_info=VR_input_apuestas.loc[:,["home_team","away_goals","away_defense_force","away_attack_force",
                                      "away_team_goals_league_average"]]
    VR_away_info=VR_away_info.rename(columns={"home_team":"away_team"})

    VR_input_tobe=games_to_be_played_df
    
    VR_GamesPlayed = VR_input_apuestas.loc[:,["home_team","away_team"]]
    
    VR_jornadas=9
    
    VR_complete=VR_input_tobe.head(VR_jornadas)
    
    VR_complete=VR_complete.merge(VR_home_info,on="home_team",how="left")
    
    VR_complete=VR_complete.merge(VR_away_info,on="away_team",how="left")
    
    VR_complete["home_team_goals"]=VR_complete["home_team_goals_league_average"]*VR_complete["home_attack_force"]*VR_complete["away_defense_force"]
    VR_complete["away_team_goals"]=VR_complete["home_team_goals_league_average"]*VR_complete["home_defense_force"]*VR_complete["away_attack_force"]
    
    VR_jornada=VR_complete.loc[:,["home_team","away_team",
                              "home_team_games_played","away_team_games_played",
                              "home_team_goals","away_team_goals"]]
    VR_jornada["home_wins"]=""
    VR_jornada["tie"]=""
    VR_jornada["away_wins"]=""
    VR_jornada["Over 2_5"]=""
    VR_jornada["Under 2_5"]=""
    VR_jornada["home_wins/tie"]=""
    VR_jornada["away_wins/tie"]=""

    VR_max_goals=30

    for row in range(len(VR_jornada["home_team"])):
        VR_home_wins=0
        VR_tie=0
        VR_away_wins=0
        VR_over=0
        VR_under=0

        for x in range(VR_max_goals):
            VR_home_goals=x
            VR_htgoals=VR_jornada["home_team_goals"][row]
            VR_poisson_home=math.exp(-VR_htgoals) * VR_htgoals**(x) / math.factorial(x)

            for y in range(VR_max_goals):
                VR_away_goals=y
                VR_atgoals=VR_jornada["away_team_goals"][row]
                VR_poisson_away=math.exp(-VR_atgoals) * VR_atgoals**(y) / math.factorial(y)
                VR_wins_tie_loss=VR_poisson_away*VR_poisson_home
                if x+y>=3:
                    VR_over=VR_over+VR_wins_tie_loss
                else:
                    VR_under=VR_under+VR_wins_tie_loss
                if x > y:
                    VR_home_wins=VR_home_wins+VR_wins_tie_loss
                elif x ==y:
                    VR_tie=VR_tie+VR_wins_tie_loss
                else:
                    VR_away_wins=VR_away_wins+VR_wins_tie_loss

        VR_jornada["home_wins"][row]=VR_home_wins*100
        VR_jornada["away_wins"][row]=VR_away_wins*100
        VR_jornada["tie"][row]=VR_tie*100
        VR_jornada["Over 2_5"][row]=VR_over*100
        VR_jornada["Under 2_5"][row]=VR_under*100

    VR_jornada["home_wins/tie"]=VR_jornada["home_wins"]+VR_jornada["tie"]
    VR_jornada["away_wins/tie"]=VR_jornada["away_wins"]+VR_jornada["tie"]
    
    VR_bet=pd.DataFrame(columns=["home_team","away_team","odds"])
    
    VR_odds_WLT=VR_jornada.loc[:,["home_team","away_team","home_wins"]]
    VR_odds_WLT["team"]=VR_odds_WLT["home_team"]
    VR_odds_WLT=VR_odds_WLT.rename(columns={"home_wins":"odds"})

    VR_odds_tie=VR_jornada.loc[:,["home_team","away_team","tie"]]
    VR_odds_tie=VR_odds_tie.rename(columns={"tie":"odds"})
    VR_odds_tie["team"]="Draw"
    VR_odds_WLT=VR_odds_WLT.append(VR_odds_tie)

    VR_odds_away=VR_jornada.loc[:,["home_team","away_team","away_wins"]]
    VR_odds_away=VR_odds_away.rename(columns={"away_wins":"odds"})
    VR_odds_away["team"]=VR_odds_away["away_team"]
    VR_odds_WLT=VR_odds_WLT.append(VR_odds_away)
    VR_odds_WLT=VR_odds_WLT.sort_values("odds",ascending=False)

    VR_bet_WLT=VR_odds_WLT.head(3)

    VR_bet_WLT["Game"]=VR_bet_WLT["home_team"]+" - "+VR_bet_WLT["away_team"]
    VR_bet_WLT=VR_bet_WLT.loc[:,["Game","odds","team"]]
    
    VR_odds_OU=VR_jornada.loc[:,["home_team","away_team","Over 2_5"]]

    VR_odds_OU=VR_odds_OU.rename(columns={"Over 2_5":"odds 2_5"})
    VR_odds_OU["Over / Under"]="Over"

    VR_odds_under=VR_jornada.loc[:,["home_team","away_team","Under 2_5"]]
    VR_odds_under=VR_odds_under.rename(columns={"Under 2_5":"odds 2_5"})
    VR_odds_under["Over / Under"]="Under"
    VR_odds_OU=VR_odds_OU.append(VR_odds_under)
    VR_odds_OU=VR_odds_OU.sort_values("odds 2_5",ascending=False)

    VR_bet_OU=VR_odds_OU.head(3)

    VR_bet_OU["Game"]=VR_bet_OU["home_team"]+" - "+VR_bet_OU["away_team"]
    VR_bet_OU=VR_bet_OU.loc[:,["Game","odds 2_5","Over / Under"]]
    
    VR_dict_WLT_england=VR_bet_WLT.to_dict(orient="records")
    VR_dict_OU_england=VR_bet_OU.to_dict(orient="records")
    
    #print(VR_dict_WLT)
    
    return VR_dict_WLT_england, VR_dict_OU_england


VR_dict_WLT_bundesliga={}
VR_dict_OU_bundesliga={}

def scrape_bundesliga_alf():
    url='https://www.futbolya.com/alemania/bundesliga/2016-2017/temporada-regular/resultados-y-calendario'

    home_teams=[]
    away_teams=[]
    home_goals=[]
    away_goals=[]
    results=[]
    seasons=[]

    browser=init_browser_alf()
    browser.visit(url)
    response=requests.get(url)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2016-2017")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass
                except IndexError:
                    pass
        except AttributeError:
            pass
    url1='https://www.futbolya.com/alemania/bundesliga/2017-2018/temporada-regular/resultados-y-calendario'
    browser.visit(url1)
    response=requests.get(url1)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2017-2018")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass

                except IndexError:
                    pass
        except AttributeError:
            pass
    url2='https://www.futbolya.com/alemania/bundesliga/2018-2019/temporada-regular/resultados-y-calendario'
    browser.visit(url2)
    response=requests.get(url2)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2018-2019")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                if scores=="POST":
                    home_goals.append(0)
                    away_goals.append(0)
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass

                except IndexError:
                    pass
        except AttributeError:
            pass
    url3='https://www.futbolya.com/alemania/bundesliga/Liga-de-Alemania/Temporada-Regular/resultados-y-calendario'
    browser.visit(url3)
    response=requests.get(url3)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)            
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2019-2020")           
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                if "-" not in scores:
                    pass
                else:
                    home_goal=int(scores.split("-")[0].replace(" ",""))
                    home_goals.append(home_goal)
                    away_goal=int(scores.split("-")[1].replace(" ",""))
                    away_goals.append(away_goal)
        except AttributeError:
            pass
    browser.quit()

    played=int(len(home_goals))
    to_be_played=int(len(home_teams))
    
    away_to_be_played=away_teams[played+1:to_be_played]
    home_to_be_played=home_teams[played+1:to_be_played]
    
    games_to_be_played=list(zip(home_to_be_played,away_to_be_played))
    games_to_be_played_df=pd.DataFrame(games_to_be_played,columns=["home_team","away_team"])
    
    home_teams=home_teams[0:played]
    away_teams=away_teams[0:played]
    
    bundesliga=list(zip(home_teams,away_teams,home_goals,away_goals, seasons))
    bundesliga_df=pd.DataFrame(bundesliga,columns=["home_team","away_team","home_goals","away_goals","season"])
    
    league_away_goals=bundesliga_df.away_goals.mean()
    league_home_goals=bundesliga_df.home_goals.mean()

    team_means_home=bundesliga_df.groupby("home_team").mean().reset_index()
    team_means_away=bundesliga_df.groupby("away_team").mean().reset_index()

    team_means_home["away_defense_force"]=team_means_away.home_goals/league_home_goals
    team_means_home["away_attack_force"]=team_means_away.away_goals/league_away_goals
    team_means_home["home_attack_force"]=team_means_home.home_goals/league_home_goals
    team_means_home["home_defense_force"]=team_means_home.away_goals/league_away_goals
    team_means_home["home_team_goals_league_average"]=league_home_goals
    team_means_home["away_team_goals_league_average"]=league_away_goals

    counting=bundesliga_df.groupby(["home_team"])["away_team"].count()
    team_means_home=pd.merge(team_means_home, counting, on='home_team')
    team_means_home.rename(columns={"away_team":"N"})

    VR_input_apuestas=team_means_home
    
    VR_home_info=VR_input_apuestas.loc[:,["home_team","home_goals","home_defense_force","home_attack_force",
                                      "home_team_goals_league_average"]]

    VR_away_info=VR_input_apuestas.loc[:,["home_team","away_goals","away_defense_force","away_attack_force",
                                      "away_team_goals_league_average"]]
    VR_away_info=VR_away_info.rename(columns={"home_team":"away_team"})

    VR_input_tobe=games_to_be_played_df
    
    VR_GamesPlayed = VR_input_apuestas.loc[:,["home_team","away_team"]]
    
    VR_jornadas=9
    
    VR_complete=VR_input_tobe.head(VR_jornadas)
    
    VR_complete=VR_complete.merge(VR_home_info,on="home_team",how="left")
    
    VR_complete=VR_complete.merge(VR_away_info,on="away_team",how="left")
    
    VR_complete["home_team_goals"]=VR_complete["home_team_goals_league_average"]*VR_complete["home_attack_force"]*VR_complete["away_defense_force"]
    VR_complete["away_team_goals"]=VR_complete["home_team_goals_league_average"]*VR_complete["home_defense_force"]*VR_complete["away_attack_force"]
    
    VR_jornada=VR_complete.loc[:,["home_team","away_team",
                              "home_team_games_played","away_team_games_played",
                              "home_team_goals","away_team_goals"]]
    VR_jornada["home_wins"]=""
    VR_jornada["tie"]=""
    VR_jornada["away_wins"]=""
    VR_jornada["Over 2_5"]=""
    VR_jornada["Under 2_5"]=""
    VR_jornada["home_wins/tie"]=""
    VR_jornada["away_wins/tie"]=""

    VR_max_goals=30

    for row in range(len(VR_jornada["home_team"])):
        VR_home_wins=0
        VR_tie=0
        VR_away_wins=0
        VR_over=0
        VR_under=0

        for x in range(VR_max_goals):
            VR_home_goals=x
            VR_htgoals=VR_jornada["home_team_goals"][row]
            VR_poisson_home=math.exp(-VR_htgoals) * VR_htgoals**(x) / math.factorial(x)

            for y in range(VR_max_goals):
                VR_away_goals=y
                VR_atgoals=VR_jornada["away_team_goals"][row]
                VR_poisson_away=math.exp(-VR_atgoals) * VR_atgoals**(y) / math.factorial(y)
                VR_wins_tie_loss=VR_poisson_away*VR_poisson_home
                if x+y>=3:
                    VR_over=VR_over+VR_wins_tie_loss
                else:
                    VR_under=VR_under+VR_wins_tie_loss
                if x > y:
                    VR_home_wins=VR_home_wins+VR_wins_tie_loss
                elif x ==y:
                    VR_tie=VR_tie+VR_wins_tie_loss
                else:
                    VR_away_wins=VR_away_wins+VR_wins_tie_loss

        VR_jornada["home_wins"][row]=VR_home_wins*100
        VR_jornada["away_wins"][row]=VR_away_wins*100
        VR_jornada["tie"][row]=VR_tie*100
        VR_jornada["Over 2_5"][row]=VR_over*100
        VR_jornada["Under 2_5"][row]=VR_under*100

    VR_jornada["home_wins/tie"]=VR_jornada["home_wins"]+VR_jornada["tie"]
    VR_jornada["away_wins/tie"]=VR_jornada["away_wins"]+VR_jornada["tie"]
    
    VR_bet=pd.DataFrame(columns=["home_team","away_team","odds"])
    
    VR_odds_WLT=VR_jornada.loc[:,["home_team","away_team","home_wins"]]
    VR_odds_WLT["team"]=VR_odds_WLT["home_team"]
    VR_odds_WLT=VR_odds_WLT.rename(columns={"home_wins":"odds"})

    VR_odds_tie=VR_jornada.loc[:,["home_team","away_team","tie"]]
    VR_odds_tie=VR_odds_tie.rename(columns={"tie":"odds"})
    VR_odds_tie["team"]="Draw"
    VR_odds_WLT=VR_odds_WLT.append(VR_odds_tie)

    VR_odds_away=VR_jornada.loc[:,["home_team","away_team","away_wins"]]
    VR_odds_away=VR_odds_away.rename(columns={"away_wins":"odds"})
    VR_odds_away["team"]=VR_odds_away["away_team"]
    VR_odds_WLT=VR_odds_WLT.append(VR_odds_away)
    VR_odds_WLT=VR_odds_WLT.sort_values("odds",ascending=False)

    VR_bet_WLT=VR_odds_WLT.head(3)

    VR_bet_WLT["Game"]=VR_bet_WLT["home_team"]+" - "+VR_bet_WLT["away_team"]
    VR_bet_WLT=VR_bet_WLT.loc[:,["Game","odds","team"]]
    
    VR_odds_OU=VR_jornada.loc[:,["home_team","away_team","Over 2_5"]]

    VR_odds_OU=VR_odds_OU.rename(columns={"Over 2_5":"odds 2_5"})
    VR_odds_OU["Over / Under"]="Over"

    VR_odds_under=VR_jornada.loc[:,["home_team","away_team","Under 2_5"]]
    VR_odds_under=VR_odds_under.rename(columns={"Under 2_5":"odds 2_5"})
    VR_odds_under["Over / Under"]="Under"
    VR_odds_OU=VR_odds_OU.append(VR_odds_under)
    VR_odds_OU=VR_odds_OU.sort_values("odds 2_5",ascending=False)

    VR_bet_OU=VR_odds_OU.head(3)

    VR_bet_OU["Game"]=VR_bet_OU["home_team"]+" - "+VR_bet_OU["away_team"]
    VR_bet_OU=VR_bet_OU.loc[:,["Game","odds 2_5","Over / Under"]]
    
    VR_dict_WLT_germany=VR_bet_WLT.to_dict(orient="records")
    VR_dict_OU_germany=VR_bet_OU.to_dict(orient="records")
    
    #print(VR_dict_WLT)
    
    return VR_dict_WLT_germany, VR_dict_OU_germany

VR_dict_WLT_laliga={}
VR_dict_OU_laliga={}

def scrape_laliga_alf():
    url='https://www.futbolya.com/espana/liga/2016-2017/temporada-regular/resultados-y-calendario'

    home_teams=[]
    away_teams=[]
    home_goals=[]
    away_goals=[]
    results=[]
    seasons=[]

    browser=init_browser_alf()
    browser.visit(url)
    response=requests.get(url)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2016-2017")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass
                except IndexError:
                    pass
        except AttributeError:
            pass
    url1='https://www.futbolya.com/espana/liga/2017-2018/temporada-regular/resultados-y-calendario'
    browser.visit(url1)
    response=requests.get(url1)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2017-2018")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass

                except IndexError:
                    pass
        except AttributeError:
            pass
    url2='https://www.futbolya.com/espana/liga/2015-2016/temporada-regular/resultados-y-calendario'
    browser.visit(url2)
    response=requests.get(url2)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2015-2016")
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                if scores=="POST":
                    home_goals.append(0)
                    away_goals.append(0)
                try:
                    try:
                        home_goal=int(scores.split("-")[0].replace(" ",""))
                        home_goals.append(home_goal)
                    except ValueError:
                        pass
                    try:
                        away_goal=int(scores.split("-")[1].replace(" ",""))
                        away_goals.append(away_goal)
                    except ValueError:
                        pass

                except IndexError:
                    pass
        except AttributeError:
            pass
    url3='https://www.futbolya.com/espana/liga/espana-laliga-santander-2019-2020/Temporada-Regular/resultados-y-calendario'
    browser.visit(url3)
    response=requests.get(url3)
    soup=bs(response.text,'html.parser')
    results=soup.find_all('ul', class_='ls2 ls-prt Tournaments')
    for r in results:
        try:
            pre_team=r.find_all('li')
            for p in pre_team:
                home_team=(p.find("em",class_="e").text)
                home_teams.append(home_team)            
                away_team=(p.find_all("em",class_="e")[1].text)
                away_teams.append(away_team)                        
                seasons.append("2019-2020")           
            score=r.find_all('em',class_='LiveHora')
            for s in score:
                scores=s.text
                if "-" not in scores:
                    pass
                else:
                    home_goal=int(scores.split("-")[0].replace(" ",""))
                    home_goals.append(home_goal)
                    away_goal=int(scores.split("-")[1].replace(" ",""))
                    away_goals.append(away_goal)
        except AttributeError:
            pass
    browser.quit()

    played=int(len(home_goals))
    to_be_played=int(len(home_teams))

    away_to_be_played=away_teams[played+1:to_be_played]
    home_to_be_played=home_teams[played+1:to_be_played]
    
    games_to_be_played=list(zip(home_to_be_played,away_to_be_played))
    games_to_be_played_df=pd.DataFrame(games_to_be_played,columns=["home_team","away_team"])

    
    home_teams=home_teams[0:played]
    away_teams=away_teams[0:played]
    laliga=list(zip(home_teams,away_teams,home_goals,away_goals, seasons))
    laliga_df=pd.DataFrame(laliga,columns=["home_team","away_team","home_goals","away_goals","season"])
    
    league_away_goals=laliga_df.away_goals.mean()
    league_home_goals=laliga_df.home_goals.mean()

    team_means_home=laliga_df.groupby("home_team").mean().reset_index()
    team_means_away=laliga_df.groupby("away_team").mean().reset_index()

    team_means_home["away_defense_force"]=team_means_away.home_goals/league_home_goals
    team_means_home["away_attack_force"]=team_means_away.away_goals/league_away_goals
    team_means_home["home_attack_force"]=team_means_home.home_goals/league_home_goals
    team_means_home["home_defense_force"]=team_means_home.away_goals/league_away_goals
    team_means_home["home_team_goals_league_average"]=league_home_goals
    team_means_home["away_team_goals_league_average"]=league_away_goals

    counting=laliga_df.groupby(["home_team"])["away_team"].count()
    team_means_home=pd.merge(team_means_home, counting, on='home_team')
    team_means_home.rename(columns={"away_team":"N"})

    VR_input_apuestas=team_means_home
    
    VR_home_info=VR_input_apuestas.loc[:,["home_team","home_goals","home_defense_force","home_attack_force",
                                      "home_team_goals_league_average"]]

    VR_away_info=VR_input_apuestas.loc[:,["home_team","away_goals","away_defense_force","away_attack_force",
                                      "away_team_goals_league_average"]]
    VR_away_info=VR_away_info.rename(columns={"home_team":"away_team"})

    VR_input_tobe=games_to_be_played_df
    
    VR_GamesPlayed = VR_input_apuestas.loc[:,["home_team","away_team"]]
    
    VR_jornadas=9
    
    VR_complete=VR_input_tobe.head(VR_jornadas)
    
    VR_complete=VR_complete.merge(VR_home_info,on="home_team",how="left")
    
    VR_complete=VR_complete.merge(VR_away_info,on="away_team",how="left")
    
    VR_complete["home_team_goals"]=VR_complete["home_team_goals_league_average"]*VR_complete["home_attack_force"]*VR_complete["away_defense_force"]
    VR_complete["away_team_goals"]=VR_complete["home_team_goals_league_average"]*VR_complete["home_defense_force"]*VR_complete["away_attack_force"]
    
    VR_jornada=VR_complete.loc[:,["home_team","away_team",
                              "home_team_games_played","away_team_games_played",
                              "home_team_goals","away_team_goals"]]
    VR_jornada["home_wins"]=""
    VR_jornada["tie"]=""
    VR_jornada["away_wins"]=""
    VR_jornada["Over 2_5"]=""
    VR_jornada["Under 2_5"]=""
    VR_jornada["home_wins/tie"]=""
    VR_jornada["away_wins/tie"]=""

    VR_max_goals=30

    for row in range(len(VR_jornada["home_team"])):
        VR_home_wins=0
        VR_tie=0
        VR_away_wins=0
        VR_over=0
        VR_under=0

        for x in range(VR_max_goals):
            VR_home_goals=x
            VR_htgoals=VR_jornada["home_team_goals"][row]
            VR_poisson_home=math.exp(-VR_htgoals) * VR_htgoals**(x) / math.factorial(x)

            for y in range(VR_max_goals):
                VR_away_goals=y
                VR_atgoals=VR_jornada["away_team_goals"][row]
                VR_poisson_away=math.exp(-VR_atgoals) * VR_atgoals**(y) / math.factorial(y)
                VR_wins_tie_loss=VR_poisson_away*VR_poisson_home
                if x+y>=3:
                    VR_over=VR_over+VR_wins_tie_loss
                else:
                    VR_under=VR_under+VR_wins_tie_loss
                if x > y:
                    VR_home_wins=VR_home_wins+VR_wins_tie_loss
                elif x ==y:
                    VR_tie=VR_tie+VR_wins_tie_loss
                else:
                    VR_away_wins=VR_away_wins+VR_wins_tie_loss

        VR_jornada["home_wins"][row]=VR_home_wins*100
        VR_jornada["away_wins"][row]=VR_away_wins*100
        VR_jornada["tie"][row]=VR_tie*100
        VR_jornada["Over 2_5"][row]=VR_over*100
        VR_jornada["Under 2_5"][row]=VR_under*100

    VR_jornada["home_wins/tie"]=VR_jornada["home_wins"]+VR_jornada["tie"]
    VR_jornada["away_wins/tie"]=VR_jornada["away_wins"]+VR_jornada["tie"]
    
    VR_bet=pd.DataFrame(columns=["home_team","away_team","odds"])
    
    VR_odds_WLT=VR_jornada.loc[:,["home_team","away_team","home_wins"]]
    VR_odds_WLT["team"]=VR_odds_WLT["home_team"]
    VR_odds_WLT=VR_odds_WLT.rename(columns={"home_wins":"odds"})

    VR_odds_tie=VR_jornada.loc[:,["home_team","away_team","tie"]]
    VR_odds_tie=VR_odds_tie.rename(columns={"tie":"odds"})
    VR_odds_tie["team"]="Draw"
    VR_odds_WLT=VR_odds_WLT.append(VR_odds_tie)

    VR_odds_away=VR_jornada.loc[:,["home_team","away_team","away_wins"]]
    VR_odds_away=VR_odds_away.rename(columns={"away_wins":"odds"})
    VR_odds_away["team"]=VR_odds_away["away_team"]
    VR_odds_WLT=VR_odds_WLT.append(VR_odds_away)
    VR_odds_WLT=VR_odds_WLT.sort_values("odds",ascending=False)

    VR_bet_WLT=VR_odds_WLT.head(3)

    VR_bet_WLT["Game"]=VR_bet_WLT["home_team"]+" - "+VR_bet_WLT["away_team"]
    VR_bet_WLT=VR_bet_WLT.loc[:,["Game","odds","team"]]
    
    VR_odds_OU=VR_jornada.loc[:,["home_team","away_team","Over 2_5"]]

    VR_odds_OU=VR_odds_OU.rename(columns={"Over 2_5":"odds 2_5"})
    VR_odds_OU["Over / Under"]="Over"

    VR_odds_under=VR_jornada.loc[:,["home_team","away_team","Under 2_5"]]
    VR_odds_under=VR_odds_under.rename(columns={"Under 2_5":"odds 2_5"})
    VR_odds_under["Over / Under"]="Under"
    VR_odds_OU=VR_odds_OU.append(VR_odds_under)
    VR_odds_OU=VR_odds_OU.sort_values("odds 2_5",ascending=False)

    VR_bet_OU=VR_odds_OU.head(3)

    VR_bet_OU["Game"]=VR_bet_OU["home_team"]+" - "+VR_bet_OU["away_team"]
    VR_bet_OU=VR_bet_OU.loc[:,["Game","odds 2_5","Over / Under"]]
    
    VR_dict_WLT_spain=VR_bet_WLT.to_dict(orient="records")
    VR_dict_OU_spain=VR_bet_OU.to_dict(orient="records")
    
    #print(VR_dict_WLT)
    
    return VR_dict_WLT_spain, VR_dict_OU_spain

def laliga_top_picks():
    VR_dict_WLT_laliga, VR_dict_OU_laliga= scrape_laliga_alf()
    
    return VR_dict_WLT_laliga, VR_dict_OU_laliga

def bundesliga_top_picks():
    VR_dict_WLT_bundesliga, VR_dict_OU_bundesliga= scrape_bundesliga_alf()

    return VR_dict_WLT_bundesliga, VR_dict_OU_bundesliga

def premier_top_picks():
    VR_dict_WLT_premier, VR_dict_OU_premier= scrape_premier_alf()
    
    return VR_dict_WLT_premier, VR_dict_OU_premier