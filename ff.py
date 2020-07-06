# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 21:44:05 2019
  
@author: Duke Young
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:57:19 2019

@author: Duke Young
"""
"The end"
"The end"
import re
import sys
import time
import mysql.connector
from arbfunction import arb_opp,delete_arb
import threading
from today_tomorrow import today_tomorrow1
from booker import books
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException   
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(r'C:\Users\Duke Young\Desktop\chromedriver_win32\chromedriver.exe')
wait =WebDriverWait(driver,60)
   


def over_and_unders(driver,over_and_under,n1,n2,arb_urls,arb_opp,id_append,o_id,dont_add,books):
    type_events =[]
    odds = []
    bookmakers =[]
    for o_u in over_and_under:
        if o_u.get_attribute('data-bname')== n1 or o_u.get_attribute('data-bname') ==n2:
            type_events.append(o_u.get_attribute('data-bname'))
            odds.append(o_u.get_attribute('data-best-dig'))
            bookmakers.append(o_u.get_attribute('data-best-bks'))
    teams_or_players =wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="betting-odds"]/div[1]/section/div/div/header/h1')))
    if teams_or_players:
        print(teams_or_players.text)
        print(odds)
        arb(teams_or_players.text,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,n1,n2)


def get_webpage(driver,sport):
    driver.get(sport)
    #close =wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="promo-modal"]/div[1]/div/span')))
    #if close:
        #driver.execute_script("arguments[0].click();",close)
    try:
        close = driver.find_element_by_xpath('//*[@id="promo-modal"]/div[1]/div/span')
        if close:
            driver.execute_script("arguments[0].click();",close)
    except:
            pass
    

   
    print ("\n----------------------------\n" + sport + "\n----------------------------\n")
    return sport
    
def get_all_odds(driver,wait):
    flag3 =False
    try:
        eleme_name1=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//p[@class="fixtures-bet-name beta-footnote"]')))                                                                                     
    
        if eleme_name1:
            name =  eleme_name1[0].text
            name2 = eleme_name1[1].text
            element = eleme_name1[0]
       
 #//*[@id="fixtures"]/div/table/tbody/tr[2]/td[5]/a//
#Clicking of all odds
 #'//*[@id="fixtures"]/div/table/tbody/tr[2]/td[6]/a'
  
    #element_name0 =wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//span[@class="beta-footnote betam-caption2 comp-odds-text"]' )))
    #element_name1 =  element_name0[0].get_attribute('href')
    #//*[@id="fixtures"]/div/table/tbody/tr[2]/td[5]/a/span[1]
    
    
        #element = wait.until(EC.element_to_be_clickable((By.XPATH,'//span[@class="beta-footnote betam-caption2 comp-odds-text"]')))
        
        if element:
            driver.execute_script("arguments[0].click();", element)
        element_name1 = driver.current_url
        
    except:
       flag3 = True
       name ="Not available"
       name2 = "Not avialable"
       element_name1 = "Not available at the moment"
    return name,name2,element_name1,flag3
    


#Checking to see if the match is live or not

def live_or_not(driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books):
    #times = wait.until(EC.visibility_of_element_located((By.XPATH,'//span[@class="date beta-caption4 betam-caption2"]')))
    date = wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class="date beta-caption4 betam-caption2"]')))
    #date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
    
    date1,date2 = today_tomorrow1()
    flag = False
    print(date.text)
    try:
        #live = wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class ="no-arrow in-play"]')))
        live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
        if live.text:
            change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
            driver.execute_script("arguments[0].click();", change_match_drop_down)
    
    except:
        print("It is not live")
        if date1 in date.text or date2 in date.text:
            try:
                names =[]             
                odds =[]
                bookmakers =[]
                best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                for best_odd in best_odds:
                    names.append(best_odd.get_attribute('data-bname'))  
                    odds.append(best_odd.get_attribute('data-best-dig'))
                    bookmakers.append(best_odd.get_attribute('data-best-bks'))
                print(odds)
                for n in names:
                    print("This is the fucking names of  the matches:" + n)
                arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books)
            except NoSuchElementException:
                print("It is not available")
        
            change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
            driver.execute_script("arguments[0].click();", change_match_drop_down)
            
            
        else:
            flag =True
            
    return flag,date1,date2
  
def check_name(driver,wait,name,name2):  
    
    try:
        
        check_first_element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[1]/div[2]/div/ul[1]/li[2]/a')))
        if check_first_element:
            markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
            #markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
        markets_text =[]
   
        for i in markets:
            if i.text:
                markets_text.append(i.text)
    #print(markets_text)
    #for m in markets:
     #   markets_text1.append(m.text)
    #print(markets_text1)    


    
        for m in markets:
            if name not in m.text or name2 not in m.text:
                continue
            if name in m.text or name2 in m.text:
                index=markets.index(m)
                break
    
        next_clickable_match = index + 1
        print("Size is " + str(len(markets_text)))
        print(markets_text)
   
    except:
        next_clickable_match = 1
        markets_text =["Not available"]
        markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
       # markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
        
    return next_clickable_match, markets_text,markets

#Scroll and click through the elements to find the best odds
def scroll_odds(next_clickable_match,driver,markets,markets_text,sport,get_webpage,arb_urls,arb_opp,id_apppend,o_id,dont_add,books ):
    while next_clickable_match < len(markets_text) :
        try:
            if markets[next_clickable_match].text:
                next_one=driver.find_element_by_link_text((markets[next_clickable_match]).text)
                driver.execute_script("arguments[0].click();",next_one)
                next_clickable_match = next_clickable_match + 1
                change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                if change_match_or_change_event.text == "Change Match": 
                    flag,date1,date2=live_or_not(driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                    if flag:
                        break
                elif change_match_or_change_event.text == "Change Event":
                    next_clickable_match =len(markets_text)
                #change_match_drop_down = driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                #driver.execute_script("arguments[0].click()",change_match_drop_down)
                markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                print(str(next_clickable_match))
                print(str(len(markets_text)))
    
    
    
        except NoSuchElementException:
            print("Page got redirected")
            next_clickable_match = next_clickable_match + 1
            try:
                go_back_to_page = driver.find_element_by_xpath('//*[@id="fixtures"]/div/table/tbody/tr[3]/td[5]/a/span[1]')
                if go_back_to_page:
                    driver.execute_script("arguments[0].click();",go_back_to_page)
            
                    change_match_drop_down = driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                    driver.execute_script("arguments[0].click()",change_match_drop_down)
                    markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
            except:
                try:
                    page_not_found = driver.find_element_by_xpath('//*[@id="mc"]/section/div/div/header/h1')
                    if page_not_found:
                        driver.get(sport)
                        go_back_to_page = driver.find_element_by_xpath('//*[@id="fixtures"]/div/table/tbody/tr[3]/td[5]/a/span[1]')
                        if go_back_to_page:
                            driver.execute_script("arguments[0].click();",go_back_to_page)
                            
                            change_match_drop_down = driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                            driver.execute_script("arguments[0].click()",change_match_drop_down)
                            markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                except:
                    print("CLicking on the link to refresh the page")
                    get_webpage(driver,sport)
                    get_all_odds(driver,wait)
                    live_or_not(driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                    print(len(markets_text))
                    markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                    
    print(len(markets_text))
    print("last digit is " + str(next_clickable_match))
    #return flag                
def arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,n1='',n2=''):
    def get_team(text,url):
         url ='https://www.oddschecker.com/football/english/premier-league/tottenham-v-wolves/winner'
         if 'football' in url:
             market = 'soccer'
         if 'Winner' in text:
    
             name = re.findall("(.*)(?:Betting .*)",text)
             market_t = 'Winner'
         elif 'Total Goals' in text:
             name = re.findall("(.*)(?:-.*)",text)
             market ='soccer'
             market_t ='Over and under'
       # print(name[0])
         print("Event: " + name[0] + "  market is :" + market)
         return name,market,market_t
    def get_Event():
        E = driver.find_element_by_xpath('//*[@id="betting-odds"]/div[1]/section/div/div/header/h1')
        return E.text
    
    if len(odds) == 2:
        odd1 = odds[0]
        odd2 = odds[1]
        book1 = books(bookmakers[0])
        book2 = books(bookmakers[1])
        
        if odd1 != 9999 and odd2 !=9999:
            arb1 = (1 /float(odd1))*100
            arb2 = (1 /float(odd2))*100
    
            total  =arb1 +arb2
            def get_odd():
                c = get_Event()
                print("The fucking event is " + c)
                
                E,M,market_t=get_team(c,url)
           
                date = driver.find_element_by_xpath('//*[@id="betting-odds"]/div[1]/section/div/div/header/div/div/div/span')
                
                if id_append:
                    i = id_append.pop(0)
                    dont_add.append(i)
                    if n1 or n2:
                        nam = names + "-" + n1 +"/ " + n2
                        li = {'Event':nam,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'n1':n1,'n2':n2,'lilen':2,'url':url}
                        #li = {'id':i,'names':nam,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'n1':n1,'n2':n2,'lilen':2}
                        arb_opp(li)
                        arb_urls.append(li)
                    else:
                        na = names[0] + " vs " + names[1]
                        li = {'Event':na,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':2,'url':url}
                        #li = {'id':i,'names':na,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'lilen':2}
                        arb_opp(li)
                        arb_urls.append(li)
                else:
                    try:
                        i = o_id[0]
                        if n1 or n2:
                            nam = names + "-" + n1 +"/ " + n2 
                            li = {'Event':nam,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'n1':n1,'n2':n2,'lilen':2,'url':url}
                            #li = {'id':i,'names':nam,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'n1':n1,'n2':n2,'lilen':2}
                        else:
                            na = names[0] + " vs " + names[1]
                            li = {'Event':na,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':2,'url':url}
                            #li ={'id':i,'names':na,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'lilen':2}
                        
                        o_id[0] = o_id[0] + 1
                        arb_opp(li)
                        arb_urls.append(li)
                    except:
                        truth = True
                          
                        while truth:
                            if o_id[0] in dont_add:
                                o_id[0] = o_id[0] + 1
                            else:
                                truth = False
                        i = o_id[0]
                        if n1 or n2:
                            nam = names + "-" + n1 +"/ " + n2 
                            li = {'Event':nam,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'n1':n1,'n2':n2,'lilen':2,'url':url}
                            #li = {'id':i,'names':nam,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'n1':n1,'n2':n2,'lilen':2}
                        else:
                            na = names[0] + " vs " + names[1]
                            li = {'Event':na,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':2,'url':url}
                            #li ={'id':i,'names':na,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'lilen':2}
                        #li = {'id':i,'names':names[0],'odd1':odd1,'odd2':odd2,'url':url,'profi':profit}
                        arb_opp(li)
                        arb_urls.append(li)
                        o_id[0] = o_id[0] + 1
                print(li)
            
               # arb_urls.append(driver.current_url) 
            
          
            if total < 120:
                overall_stake = 100
                stake1 = (int(overall_stake) * arb1)/total
                stake2 = (int(overall_stake) * arb2)/total
                profit = 120- total
                url =driver.current_url
                available = False
                
                if arb_urls:
                    if n1 and n2:
                        for a in arb_urls:
                            if url in a['url'] and n1 in a['n1'] and n2 in a['n2']:
                                available = True
                    else:
                        for a in arb_urls:
                            if url in a['url']:
                                available = True
                    if available:
                        print("Already in the database")
                    else:
                        get_odd()
                        
                                
                else:
                     get_odd()
                    
                
               
   
                
                
           
                #print(arb_urls)
               
        
                print("Players playing:")
                print(names)
                print("Arb opportunity " + str(profit) )
                print("Bet to be placed at " + book1)
                print(stake1)
                print("Bet to be played at " + book2)
                print(stake2)
                
               
            else:
                pass
        else:
            pass
    elif len(odds) == 3:
       
        if names[2] == "Draw":
            odd1 = odds[0]
            odd2 = odds[1]
            odd3 = odds[2]
            name = names[0] + " vs " + names[1]
        elif names[1] == "Draw":
            odd1 = odds[0]
            odd2 = odds[2]
            odd3 = odds[1]
            name = names[0] + " vs " + names[2]
        if odd1 != 9999 and odd2 != 9999 and odd3 != 9999:
            arb1 =(1/float(odd1))*100
            arb2 =(1/float(odd2))*100
            arb3 =(1/float(odd3))*100
            
            book1 = books(bookmakers[0])
            book2 = books(bookmakers[1])
            book3 = books(bookmakers[2])
            
            total =arb1 + arb2 + arb3
        
        
            if total < 1220:
                overall_stake  = 100
                stake1 = (int(overall_stake) * arb1)/total
                stake2 = (int(overall_stake) * arb2)/total
                stake3 = (int(overall_stake) * arb3)/total
                profit = 120- total
                url = driver.current_url
                
                
                c = get_Event()
                print("The fucking event is " + c)
                
                E,M,market_t=get_team(c,url)
                print(E)
                print(M)
                print(market_t)
                date = driver.find_element_by_xpath('//*[@id="betting-odds"]/div[1]/section/div/div/header/div/div/div/span')
                print(date.text)
                available = False
                if arb_urls:
                    for a in arb_urls:
                        
                        if url in a['url']:
                            print("It is already avalilable")
                            available = True
                    if available:
                        pass
                    else:
                        if id_append:
                            i = id_append.pop(0)
                            dont_add.append(i)
                            #I am currently workin here
                            li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                            #li = {'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                            arb_opp(li)
                            arb_urls.append(li)
                            print("Dont add" + str(dont_add))
                                
                            
                        else:
                    
                            truth =True
                            while truth:
                                if o_id[0] in dont_add:
                                    o_id[0] = o_id[0] + 1
                                else:
                                    truth = False
                            i = o_id[0]
                            li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                            #li = {'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                            arb_opp(li)
                            arb_urls.append(li)
                            print(dont_add)
                        
                            o_id[0] = o_id[0] + 1
                            
                            
                else:   
                    if id_append:
                        i = id_append.pop(0)
                        dont_add.append(i)
                        li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                        #li ={'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                        arb_opp(li)
                        arb_urls.append(li)
                        print("Dont add" + str(dont_add))
                            
                    else:
                    
                        truth =True
                        while truth:
                            if o_id[0] in dont_add:
                                o_id[0] = o_id[0] + 1
                            else:
                                truth = False
                        i = o_id[0]
                        li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                        #li = {'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                        arb_opp(li)
                        arb_urls.append(li)
                        print(dont_add)
                        
                        o_id[0] = o_id[0] + 1
                                
                    #except:
                     #   print("There was an error")
                        #truth = True
                        #while truth:
                         #   if o_id[0] in dont_add:
                          #      o_id[0] = o_id[0] + 1
                           # else:
                            #    truth = False
                       # i = o_id[0]
                        #li = {'id':i,'names':names[0],'odd1':odd1,'odd2':odd2,'odd3':odd3,'url':url,'profi':profit}
                        #arb_opp(li)
                        #arb_urls.append(li)
                            
             
            
                print("Players playing:")
                print(name)
                print("Arv opportunity " + str(profit))
                print("Bet to be placed at " +book1)
                print(stake1)
                print("Bet to be placed at " +book2)
                print(stake2)
                print("Bet to be placed at " +book3)
                print(stake3)
            else:
                pass
    
        else:
            pass

#print(nexto.text)
   
   
def check_over_under(driver,wait,name,name2,element_name1,switch,date1,date2,over_and_unders,arb_urls,arb_opp,id_append,o_id,dont_add,books):
    driver.get(element_name1)
    
    
    next_match = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[1]/div[1]')))
    driver.execute_script("arguments[0].click()",next_match)
    
    #//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a
    word = "Total Goals Over/Under"
    
    patience = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a')))
    if patience:
        lists=driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
        for l in lists:
            if word in l.text:
                i = lists.index(l)
                break
        nexto = driver.find_element_by_link_text(lists[i].text)
        print("Hello")
    
    #print(nexto.text)
    driver.execute_script("arguments[0].click()",nexto)
    switch(name,name2,over_and_unders,date1,date2,arb_urls,arb_opp,id_append,o_id,dont_add,books)
    print("Da baby")
    
       
        
  
def switch(name,name2,over_and_unders,date1,date2,arb_urls,arb_opp,id_append,o_id,dont_add,books):
    change_match_drop_down = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="select-item selected beta-callout"]')))
    #change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
    driver.execute_script("arguments[0].click();", change_match_drop_down)
    
    next_click_match,markets_text,markets=check_name(driver,wait,name,name2)


    ind = next_click_match -1
    while ind <(len(markets_text)):
        try:
            if markets[ind].text:
                next_one=driver.find_element_by_link_text((markets[ind]).text)
                driver.execute_script("arguments[0].click();",next_one)
                ind = ind +1
                change_match_or_change_event = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class = "select-item selected beta-callout"]')))
            #change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                if change_match_or_change_event.text == "Change Match": 
                    try:
                        live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
                        if live.text:
                            change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                            driver.execute_script("arguments[0].click();", change_match_drop_down)
                    except NoSuchElementException:
                        print("It is not live")
                    
                        date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                        if date1 in date.text or date2 in date.text:           
                        
                            over_and_under = driver.find_elements_by_xpath('//tr[@class="diff-row handicap-participant evTabRow bc"]')
                            over_and_unders(driver,over_and_under,"Over 0.5","Under 0.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                            print(date2)
                            over_and_unders(driver,over_and_under,"Over 1.5","Under 1.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                            over_and_unders(driver,over_and_under,"Over 2.5","Under 2.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                            over_and_unders(driver,over_and_under,"Over 3.5","Under 3.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                            change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                            driver.execute_script("arguments[0].click();", change_match_drop_down)
                        else:
                            continue
                elif change_match_or_change_event.text == "Change Event":
                    ind = len(markets_text)
            markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
        except StaleElementReferenceException:
            ind = ind + 1
            break
       # markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
 
sportsw = ['https://www.oddschecker.com/tennis/itf-tour','https://www.oddschecker.com/basketball/nba','https://www.oddschecker.com/american-football/nfl',
	'https://www.oddschecker.com/australian-rules/afl', 'https://www.oddschecker.com/badminton', 'https://www.oddschecker.com/boxing', 'https://www.oddschecker.com/ufc-mma',
	'https://www.oddschecker.com/gaelic-games/gaelic-football','https://www.oddschecker.com/handball/handball-coupon', 'https://www.oddschecker.com/hockey/all-matches',
	'https://www.oddschecker.com/rugby-league/match-coupon','https://www.oddschecker.com/rugby-league/handicaps-coupon','https://www.oddschecker.com/rugby-union/match-coupon',
	'https://www.oddschecker.com/rugby-union/handicaps-coupon', 'https://www.oddschecker.com/rugby-union/european-champions-cup', 'https://www.oddschecker.com/rugby-union/lions-tour',
	'https://www.oddschecker.com/cricket/ipl','https://www.oddschecker.com/ice-hockey/nhl','https://www.oddschecker.com/tennis/itf-futures',
	'https://www.oddschecker.com/tennis/challenger-tour','https://www.oddschecker.com/tennis/wta-rome','https://www.oddschecker.com/football/football-coupons/over-under-2.5',
	'https://www.oddschecker.com/football/football-coupons/over-under-1.5', 'https://www.oddschecker.com/football/football-coupons/over-under-0.5', 
	'https://www.oddschecker.com/football/football-coupons/both-teams-to-score'] 
arb_urls1=[{'id':2,'names':'Derby vs Charlton','odd1':1,'odd2':3,'odd3':5,'url':'https://www.oddschecker.com/football/english/championship/derby-v-charlton/winner','profi':5},
          {'id':3,'names':'Derby vs Charlton over and under','odd1':2,'odd2':8,'url':'https://www.oddschecker.com/football/english/championship/derby-v-charlton/total-goals-over-under','profi':6,'n1':'Over 3.5','n2':'Under 3.5'}]
#li = [{'id':i,'names':names[0],'odd1':odd1,'odd2':odd2,'url':url,'profi':profi}]
new_urls=[]
dont_add=[]
arb_urls = []
id_append=[4,5]
o_id = [1]
sportswr = ['https://www.oddschecker.com/football/english/league-1', 'https://www.oddschecker.com/football/english/league-2', 'https://www.oddschecker.com/football/english/fa-cup', 'https://www.oddschecker.com/football/france/ligue-2','https://www.oddschecker.com/tennis/challenger-tour','https://www.oddschecker.com/tennis/wta-auckland','https://www.oddschecker.com/tennis/wta-brisbane']
 
sports= ['https://www.oddschecker.com/football/spain/copa-del-rey',  'https://www.oddschecker.com/football/english/championship',
	'https://www.oddschecker.com/football/english/league-1', 'https://www.oddschecker.com/football/english/league-2', 'https://www.oddschecker.com/football/english/fa-cup',
	'https://www.oddschecker.com/football/elite-coupon', 'https://www.oddschecker.com/football/france/ligue-2', 'https://www.oddschecker.com/football/champions-league',
	'https://www.oddschecker.com/football/europa-league', 'https://www.oddschecker.com/football/womens-coupon','https://www.oddschecker.com/football/germany/bundesliga','https://www.oddschecker.com/football/italy/serie-a',
    'https://www.oddschecker.com/football/spain/la-liga-primera','https://www.oddschecker.com/football/scottish/premiership','https://www.oddschecker.com/football/netherlands/eredivisie','https://www.oddschecker.com/football/netherlands/eerste-divisie','https://www.oddschecker.com/football/italy/serie-b',
    'https://www.oddschecker.com/football/italy/super-cup','https://www.oddschecker.com/football/spain/la-liga-segunda','https://www.oddschecker.com/football/spain/la-liga-segunda-b','https://www.oddschecker.com/football/portugal/segunda-liga'
    'https://www.oddschecker.com/football/poland/ekstraklasa','https://www.oddschecker.com/football/norway/eliteserien','https://www.oddschecker.com/football/poland/cup','https://www.oddschecker.com/football/sweden/allsvenskan',
    'https://www.oddschecker.com/football/switzerland/super-league','https://www.oddschecker.com/football/wales/premier-league','https://www.oddschecker.com/football/world/australia/a-league',
    'https://www.oddschecker.com/football/world/japan/emperors-cup','https://www.oddschecker.com/football/world/tunisia/league-1','https://www.oddschecker.com/football/world/uae/premier-league',
    
    'https://www.oddschecker.com/football/france/ligue-1','https://www.oddschecker.com/football/portugal/league-cup','https://www.oddschecker.com/football/belgium/jupiler-pro-league','https://www.oddschecker.com/football/belgium/division-2','https://www.oddschecker.com/football/cyprus/1-division',
    'https://www.oddschecker.com/football/greece/superleague','https://www.oddschecker.com/football/finland/veikkausliiga','https://www.oddschecker.com/football/hungary/nb1','https://www.oddschecker.com/football/ireland/premier-division',
    'https://www.oddschecker.com/football/scottish/championship'
    ]   
def main_job():
    #driver = webdriver.Chrome(r'C:\Users\Duke Young\Desktop\chromedriver_win32\chromedriver.exe')
    #wait =WebDriverWait(driver,50)
    
    
    while True:
        
        for sport in new_urls:            
            get_webpage(driver,sport)
            print("STAGE 1 COMPLETE")
            name,name2,element_name1,flag3= get_all_odds(driver,wait)
            if flag3:
                continue
            print("STAGE 2 COMPLETE")
            flag,date1,date2=live_or_not(driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books)
            if flag:
                continue

            print("STAGE 3 COMPLETE")
            next_clickable_match,markets_text,markets  = check_name(driver,wait,name,name2)
            print("STAGE 4 COMPLETE")
            flag1=scroll_odds(next_clickable_match,driver,markets,markets_text,sport,get_webpage,arb_urls,arb_opp,id_append,o_id,dont_add,books)
            print("LAST STAGE COMPLETE")
            check_over_under(driver,wait,name,name2,element_name1,switch,date1,date2,over_and_unders,arb_urls,arb_opp,id_append,o_id,dont_add,books)
            
def get_all_odds1(driver,wait,sport):
    

    flag4 =False
    try:
       # //*[@id="fixtures"]/div/table/tbody/tr[3]/td[2]/p[1]
        #element_name1 = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixtures"]/div/table/tbody/tr[3]/td[2]/p[1]')))
        #element_name3 = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixtures"]/div/table/tbody/tr[3]/td[2]/p[2]')))
        eleme_name1=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//p[@class="fixtures-bet-name beta-footnote"]')))                                                                                     
    
        if eleme_name1:
            name1 =  eleme_name1[0].text
            name3 = eleme_name1[1].text
            element1 = eleme_name1[0]
           ##name3 = name3.split()
            #name3 = name3[0]
            ##name1 = name1[0]
           # print(name1 + " " + name3)
 #//*[@id="fixtures"]/div/table/tbody/tr[2]/td[5]/a//
#Clicking of all odds
 #'//*[@id="fixtures"]/div/table/tbody/tr[2]/td[6]/a'
  
    #element_name0 =wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//span[@class="beta-footnote betam-caption2 comp-odds-text"]' )))
    #element_name1 =  element_name0[0].get_attribute('href')
    #//*[@id="fixtures"]/div/table/tbody/tr[2]/td[5]/a/span[1]
    #//span[@class="beta-footnote betam-caption2 comp-odds-text"]
    #//*[@id="fixtures"]/div/table/tbody/tr[3]/td[7]/a/span[1]
    #//*[@id="fixtures"]/div/table/tbody/tr[3]/td[7]/a

    #element1 = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="fixtures"]/div/table/tbody/tr[3]/td[7]/a/span[1]')))
        print("ficj")                                                      #//*[@id="fixtures"]/div/table/tbody/tr[3]/td[6]/a/span[1] 
        if element1:
            driver.execute_script("arguments[0].click();", element1)
        element_name2 = driver.current_url
        if sport  in element_name2:
            date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
            
            
            dat1,dat2 = today_tomorrow1()
            print(date.text)
            
            print(dat1 + " " + dat2)
            if dat1 in date.text or dat2 in date.text:
                new_urls.append(sport)
            else:
                print("The time of match is not within available selected duration we need")
                
        
    except:
        print("Unexpected error ", sys.exc_info()[0])
        flag4 = True
        name1 ="Not available"
        name3 = "Not avialable"
        element_name2 = "Not available at the moment"
    print(new_urls)
    return name1,name3,element_name2,flag4
def update(odd1,odd2,itt,bookmakers,profit,odd3=''):
    mydb = mysql.connector.connect(
        host="localhost",
        user = "root",
        database = "testdb"
        )
    mycursor = mydb.cursor()
    if odd3:
        book1 = books(bookmakers[0])
        book2 = books(bookmakers[1])
        book3 = books(bookmakers[2])
        sqlformula = "UPDATE arb9 set Team1 = %s,Team2 =%s,Team3 = %s,Bookmaker1 = %s,Bookmaker2 =%s,Bookmaker3 = %s,Profit = %s where id = %s"
        inputData =(odd1,odd2,odd3,book1,book2,book3,profit,itt)
    else:
        book1 = books(bookmakers[0])
        book2 = books(bookmakers[1])
        
        sqlformula = "UPDATE arb9 set Team1 =%s,Team2 =%s,Bookmaker1 = %s,Bookmaker2 = %s, Profit=%s where id = %s"
        inputData=(odd1,odd2,book1,book2,profit,itt)
    mycursor.execute(sqlformula,inputData)
    mydb.commit()
    print("Updated successfully")
    mycursor.close()
    
    
def arbsopp(names,odds,bookmakers,itt,update,index,delete_arb):
    if len(odds) == 3:
        if names[2] == "Draw":
            odd1 = odds[0]
            odd2 = odds[1]
            odd3 = odds[2]
        elif names[1] == "Draw":
            odd1 = odds[0]
            odd2 = odds[2]
            odd3 = odds[1] 
    
        if odd1 != 9999 and odd2 !=9999 and odd3 != 9999:
            arb1 = (1 /float(odd1))*100
            arb2 = (1 /float(odd2))*100
            arb3 =(1/float(odd3))*100
    
            total  =arb1 +arb2 +arb3
            
            
            print(odd1 + " " + odd2 + " " +odd3)
            ing = arb_urls[index]['Id']
            if total < 120:
                profit = 120 - total
                
                
                update(odd1,odd2,itt,bookmakers,profit,odd3)
            else:
                delete_arb(ing)
                arb_urls.pop(index)
                print(arb_urls)
                id_append.append(ing)
                print(id_append)
    elif len(odds) == 2:
        odd1= odds[0]
        odd2 = odds[1]
        if odd1 != 9999 and odd2 != 9999:
            arb1 = (1/float(odd1))*100
            arb2 = (1/float(odd2))*100
            
            total = arb1 + arb2
            
            print(odd1 + " " + odd2)
            ing = arb_urls[index]['id']
            if total < 120:
                profit = 120-total
                update(odd1,odd2,itt,bookmakers,profit)
               
                print("The index updated is " + str(ing))
             
                
              
               
            else:
                delete_arb(ing)
                arb_urls.pop(index)
                print(arb_urls)
                id_append.append(ing)
                print(id_append)
    

def provide_urls():
    
    driver = webdriver.Chrome(r'C:\Users\Duke Young\Desktop\chromedriver_win32\chromedriver.exe')
    wait =WebDriverWait(driver,50)
   
    for sport in sports:
        sport = get_webpage(driver,sport)
        get_all_odds1(driver,wait,sport)
def over_and_unders1(driver,n1,n2,id_append,wait):
    type_events =[]
    odds = []
    bookmakers =[]
    over_and_under = driver.find_elements_by_xpath('//tr[@class="diff-row handicap-participant evTabRow bc"]')
    for o_u in over_and_under:
        if o_u.get_attribute('data-bname')== n1 or o_u.get_attribute('data-bname') ==n2:
            type_events.append(o_u.get_attribute('data-bname'))
            odds.append(o_u.get_attribute('data-best-dig'))
            bookmakers.append(o_u.get_attribute('data-best-bks'))
                        
    teams_or_players =wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="betting-odds"]/div[1]/section/div/div/header/h1')))
    if teams_or_players:
        print(teams_or_players.text)
        
        print(odds)
    print(bookmakers)
    return teams_or_players.text,odds,bookmakers
        #arb(type_events,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,last)
def ab():
    while True:
        if arb_urls:
            time.sleep(10)
            print("It is lit")
            print(arb_urls)
        
def update_urls():
      
    driver = webdriver.Chrome(r'C:\Users\Duke Young\Desktop\chromedriver_win32\chromedriver.exe')
    wait =WebDriverWait(driver,50)
    while True:
        for index,l in enumerate(arb_urls):
            get_webpage(driver,l['url'])
            c = driver.current_url
            if 'total-goals-over-under' in c:
                names,odds,bookmakers=over_and_unders1(driver,l['n1'],l['n2'],id_append,wait)
                itt = l['id']
                arbsopp(names,odds,bookmakers,itt,update,index,delete_arb)
            else:
                names =[]             
                odds =[]  
                bookmakers =[]
                itt = l['Id']
                best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                for best_odd in best_odds:
                    names.append(best_odd.get_attribute('data-bname'))  
                    odds.append(best_odd.get_attribute('data-best-dig'))
                    bookmakers.append(best_odd.get_attribute('data-best-bks'))
                print(odds)
                arbsopp(names,odds,bookmakers,itt,update,index,delete_arb)
    

if __name__ == "__main__":
    thread1 = threading.Thread(target=main_job)
    thread2 = threading.Thread(target=provide_urls)
    #thread3 = threading.Thread(target=update_urls)
    
    thread1.start()
    thread2.start()
    #thread3.start()
    
    thread1.join()
    thread2.join()
    #thread3.join()