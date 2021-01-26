# [Stock Bot](https://devpost.com/software/stockbot-ckd9j3)

## Award
- Captial One Best Financial Hack

## Contributors
Name | Email|
-----|------
Brian Latimer | brianmlatimer@gmail.com|
Emma Clary | eclary2000@gmail.com |
Matthew Wen | mattwen2018@gmail.com|

## Inspiration
The inspiration was from the Joe Rogan Podcast with Kevin Hart, in which Kevin Hart explained how people have a social responsibility to learn how to become financially independent. As a result, he teamed up with several banks to encourage people from his community to learn how to become financially independent. 

We thought to expand on this idea and instead of just reading a user's bank statement, we utilized the Capital One API (api.nessieisreal.com) to track the user's spending to determine which stock options to recommend buying (working on selling in the future) based off spending habits.
* (General Idea but not fully implemented) If a user is low on cash (it currently checks every 10 minutes if you are low on cash), but is invested in Netflix. Because of Netflix change in prices, it will recommend selling Netflix when it is around $570 and then remind you to buy Netflix in future when it reach about $490. The program checks your balance every few minutes. 

## What it does
As college students who have just started learning about the stock market, we think the best way to learn about it is from other people. As a result, we created a Discord bot where people can publicly view stocks information, make trades through discord, discuss their change in equity throughout their day of trading, and notice trends where you see your peers selling and buying stocks. 

## How we built it
We used python to build our bot, and we have plans to use Google Cloud to run the bot on a Google Cloud Function. We also use Google Cloud Database (Firebase) Firestore to store account data; each collection id is the user's discord username, and each collection has access to the user's accounts and customer ids from the Capital One API. To get active trading with stocks working, we used Robinhood, so this bot actually connects to the user's Robinhood account, so we they can buy and sell stocks or cryptocurrency, withdrawing and depositing money into the Robinhood account. 

## Challenges we ran into
Our biggest problem is that Robinhood utilizes real money, and the Capital Ones API utilizes mock data, so we couldn't test our trading functionality in Robinhood with the Capital Ones API. However, every time we made a real purchase through Robinhood, the movement of money is still recorded through via Capital One API. 

## Accomplishments that we're proud of
Our greatest accomplishment was getting the recommendation and trading features to work. We want everybody to see what trades you are making so you can discuss about the stocks or cryptocurrency you just purchased. 

## What we learned
We learned a lot about python with this project. From discord bots, to connecting our APIs, this project was something some of us have never really worked with before.

## What's next for StockBot
One of the things we have a lot of room to improve would be our algorithm to recommend stocks, as there are many ways in which we can optimize the way StockBot decides. Another thing would be to get a broader range of stock history, to have more data to be able to make more accurate decisions.  

In addition, we were also working on keeping track on the amount of money in Capital One Bank account, so the balance goes too low, it will recommend to withdraw money from Robinhood (and with stocks to sell to obtain money for rent, food etc). As a result, you can feel more confident investing with small amount of money. 
