from selenium import webdriver
import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
driver=webdriver.Chrome()
driver.get("https://in.tradingview.com")
driver.maximize_window()
import matplotlib.pyplot as plt
import csv
symbol=input("enter the symbol of the share:")
#LOGIN
userid='your tradingView email_id'
mypassword='tradingView account password'

driver.find_element(By.XPATH,'/html/body/div[3]/div[3]/div[2]/div[3]/button[1]').click()
#clicking sign in button
driver.find_element(By.XPATH,'//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/button[1]').click()
#clicking the email option
driver.find_element(By.XPATH,'/html/body/div[9]/div/div/div[1]/div/div[2]/div[2]/div/div/button').click()

email=driver.find_element(By.XPATH,'//*[@id="id_username"]')
email.send_keys(userid)

password=driver.find_element(By.XPATH,'//*[@id="id_password"]')
password.send_keys(mypassword)

sleep(60)
print('login done')

sleep(10)
#SEARCHING THE REQUIRED STOCK
#clicking the search button
driver.find_element(By.XPATH,'/html/body/div[4]/div[3]/div[2]/div[2]/div/div/button[1]').click()

#entering the search
search=driver.find_element(By.XPATH,'//*[@id="overlap-manager-root"]/div/div/div[2]/div/div/div[1]/div/div[1]/span/form/input')
search.send_keys(symbol)

#clicking the search icon
driver.find_element(By.XPATH,'//*[@id="overlap-manager-root"]/div/div/div[2]/div/div/div[1]/div/div[1]/span/form/button[1]').click()

sleep(10)


empty=True #it tells whether the file is empty or not 

x=100000
#FETCHING THE DATA AND STORING IN txt FILE
# to create a file to store the data if the data does not already exist else to clear the file of previous data
with open("C:/Users/bbeha/Desktop/RTTS/{}.txt".format(symbol),'w') as file:
    empty=True

while x>0:
    length=0
    with open("C:/Users/bbeha/Desktop/RTTS/{}.txt".format(symbol),'r') as file:
        t=file.readlines()
        length=len(t)
        if(length>960):
            with open("C:/Users/bbeha/Desktop/RTTS/{}.txt".format(symbol),'w') as file:
                empty=True
            
    print(datetime.now().strftime('%H:%M:%S'))
    for i in range(0,5):

        with open("C:/Users/bbeha/Desktop/RTTS/{}.txt".format(symbol),'a') as file:
                data=driver.find_element(By.XPATH,'/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]').text
                print(i,data)
                sleep(0.8)
                x-=1
                if(empty==False):
                    file.write('\n')
                else:
                    empty=False

                file.write(data)
    print(datetime.now().strftime('%H:%M:%S'))
    sleep(1)

    
    