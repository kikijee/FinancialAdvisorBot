from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import mplfinance as mpf
import StockPredictionModel as spm
import json

import pickle
import sys
import datetime as dt
import sys
import time

yf.pdr_override()

# initialized portfolio
# portfolio = {'AAPL': 20, 'TSLA': 5, 'GS': 10}

# write portfolio to file
# with open('portfolio.pkl', 'wb') as f:
#   pickle.dump(portfolio, f)

# load portfolio

class ChatBot():
  def __init__(self,guiObj):
    with open('portfolio.pkl', 'rb') as f:
      self.portfolio = pickle.load(f)

    self.guiObj = guiObj
    
    self.response = None

    self.mappings = {
      'greetings': self.greetings,
      'plot_chart': self.plot_chart,
      'add_portfolio': self.add_portfolio,
      'remove_portfolio': self.remove_portfolio,
      'show_portfolio': self.show_portfolio,
      'stock_price': self.stock_price,
      'stock_prediction': self.stock_prediction,
      'portfolio_gains': self.portfolio_gains,
      'portfolio_worth': self.portfolio_worth,
      'introduction':self.introduction,
      'functionality':self.functionality,
      'bye': self.bye
    }

    if 'intents.json'.endswith(".json"):
      self.intents = json.loads(open('intents.json').read())

    self.assistant = GenericAssistant('intents.json', self.mappings, "financial_assistant_model")

    self.assistant.load_model()

  def save_portfolio(self):
    with open('portfolio.pkl', 'wb') as f:
      pickle.dump(self.portfolio, f)

  def greetings(self):
    self.response = self.intents['intents'][self.find_tag('greetings')]['responses'][0]

  def introduction(self):
    self.response = self.intents['intents'][self.find_tag('introduction')]['responses'][0]

  def functionality(self):
    self.response = self.intents['intents'][self.find_tag('functionality')]['responses'][0]
  
  def find_tag(self,tag):
    i = 0
    for intent in self.intents['intents']:
      if (intent['tag'] == tag):
        return i
      i+=1
      
  

  def add_portfolio(self):
    ticker = self.guiObj.respond("which stock do you want to buy? ")
    amount = self.guiObj.respond("How many shares do you want to buy? ")
    
    data = web.DataReader(ticker) 
    if(len(data) <= 0):
      self.guiObj.reset_button()
      self.response = f"hmm... the ticker {ticker} seems to be invalid."
      return
    
    if ticker in self.portfolio.keys():
      self.portfolio[ticker] += int(amount)
    else:
      self.portfolio[ticker] = int(amount)
    
    self.response = f"Success! You bought {amount} shares of {ticker}"
    self.guiObj.reset_button()

    self.save_portfolio()

  def remove_portfolio(self):
    ticker = self.guiObj.respond("Which stock to you want to sell?")
    amount = self.guiObj.respond("How many shares do you want to sell: ")

    if ticker in self.portfolio.keys():
      if int(amount) <= self.portfolio[ticker]:
        self.portfolio[ticker] -= int(amount)
        if self.portfolio[ticker] <= 0:
          del self.portfolio[ticker]
        self.save_portfolio()
        self.response = f"Success! You sold {amount} shares of {ticker}"
      else:
        self.response = "You don't have enough shares!"
    else:
      self.response = f"You don't own any shares of {ticker}"
    self.guiObj.reset_button()

  def show_portfolio(self):
    response = "Your portfolio:\n\n"
    for ticker in self.portfolio.keys():
      response += f"You own {self.portfolio[ticker]} shares of {ticker}\n"
    self.response = response

  def portfolio_worth(self):
    sum = 0
    for ticker in self.portfolio.keys():
      data = web.DataReader(ticker)
      price = data['Close'].iloc[-1]
      sum += price
      self.response = f"Your portfolio is worth {sum} USD"

  def portfolio_gains(self):
    starting_date = self.guiObj.respond("Please enter a date for comparison (YYYY-MM-DD)...")
    sum_now = 0
    sum_then = 0

    try:
      for ticker in self.portfolio.keys():
        data = web.DataReader(ticker)
        price_now = data['Close'].iloc[-1]
        price_then = data.loc[data.index == starting_date]['Close'].values[0]
        sum_now += price_now
        sum_then += price_then
      
      self.response = f"Relative Gains: {((sum_now-sum_then)/sum_then) * 100}%"+f"\nAbsolute Gains: {sum_now-sum_then} USD"

      
    except IndexError:
      self.response = "There was no trading on this day."

    self.guiObj.reset_button()

  def stock_price(self):
    ticker = self.guiObj.respond("Enter ticker for price: ")
    data = web.DataReader(ticker)
    if(len(data) <= 0):
      self.response = f"hmm... the ticker {ticker} seems to be invalid."
    else:
      data_t = '%.2f' % data['Close'].iloc[-1]
      self.response = f"Latest {ticker} price: ${data_t}"
    self.guiObj.reset_button()

  def stock_prediction(self):
    ticker = self.guiObj.respond("Enter ticker for price prediction: ")
    data = spm.portfolio_predict(ticker)
    if(len(data) <= 0):
      self.response = f"hmm... the ticker {ticker} seems to be invalid."
    else:
      data_t = '%.2f' % data
      self.response = f"Price prediction of {ticker} for tomorrow: ${data_t}"
    self.guiObj.reset_button()

  def plot_chart(self):
    ticker = self.guiObj.respond("Choose a ticker symbol: ")
    starting_string = self.guiObj.respond("Choose a starting date (YYYY-MM-DD): ")

    plt.style.use('dark_background')
    try:
      start = dt.datetime.strptime(starting_string, "%Y-%m-%d")
    except ValueError:
      self.response = "Invalid date format!"
      self.guiObj.reset_button()
      return

    end = dt.datetime.now()

    data = web.DataReader(ticker, start, end)
  
    if(len(data) <= 0):
      self.response = f"hmm... the ticker {ticker} seems to be invalid."
      self.guiObj.reset_button()
      return
    else:
      colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
      mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
      mpf.plot(data, type='candle', style=mpf_style, volume=True)

    self.guiObj.reset_button()
    self.response = None

  def bye(self):
    print("Goodbye!")
    sys.exit(0)

  def ask(self,message):
    self.assistant.request(message)
    return self.response
      


#ONLY FOR TRAINING
# def greetings(): pass
# def plot_chart(): pass
# def introduction(): pass
# def functionality(): pass
# def add_portfolio(): pass
# def remove_portfolio(): pass
# def show_portfolio(): pass
# def stock_price(): pass
# def stock_prediction(): pass
# def portfolio_gains(): pass
# def bye(): pass
# mappings = {
#   'greetings': greetings,
#   'plot_chart': plot_chart,
#   'add_portfolio': add_portfolio,
#   'remove_portfolio': remove_portfolio,
#   'show_portfolio': show_portfolio,
#   'stock_price': stock_price,
#   'stock_prediction': stock_prediction,
#   'portfolio_gains':  portfolio_gains,
#   'introduction': introduction,
#   'functionality': functionality,
#   'bye': bye
# }

# assistant = GenericAssistant('intents.json', mappings, "financial_assistant_model")

# assistant.train_model()
# assistant.save_model()