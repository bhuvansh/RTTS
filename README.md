# RTTS
"RTTS (Real-Time Trading System) is an Open Source that harnesses the power of web automation, Data visualisation and advanced data analytics, providing traders with real-time access to market data from TradingView. With dynamic graphs,custom time intervals and intuitive visualization, RTTS empowers traders to make well-informed decisions, identify trends, and seize lucrative opportunities in the fast-paced world of trading.

*Requiremets:*
->Trading View Account 
->python ide
->Chrome webdriver

*Python libreries used:*
->numpy
->pandas
->matplotlib
->selenium
->time

*Working:-*
using selenium the RTTS_dataFetcher script logins into trading view platform (*NOTE* :- if there is a captcha box after the email and password have been entered then you need to solve the captcha manually and click the sign in button, it is just one time requiremet and after that no intervension is needed. A time frame of 60 seconds have been provided to solve the captcha so after filling the captcha you may have to wait for few seconds to see the script print "login done")

once the login is complete the script will start to fetch the data of the required share and add it to a text file named as 
