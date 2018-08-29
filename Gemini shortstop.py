# api from https://github.com/mattselph/gemini-python-unoffc
from gemini.client import Client
from datetime import datetime
from time import strftime, gmtime, sleep
#go to gemini.com and get api key and secret. insert below, between the apostrophe
#e.g. api_key = '123456' api_secret='7890123'.
api_key = ''
api_secret = ''
#for real trading account, change sandbox = True to sandbox = False
gemi = Client(api_key, api_secret, sandbox=True)
all_is_well = True

def check_price(currency , shortstop_price , sell_price , sell_amount):
    '''
    a function that works as a shortstop.
    currency input options: 'btcusd', 'ethusd', 'ethbtc'
    'btcusd' = bitcoin/usd. 'ethusd' = ethereum/usd. 'ethbtc' = ethereum/btc
    shortstop_price: the price at which function will begin to place sell order once current
    price goes beyond this price
    sell_price: order will be placed to sell currency at this price.
    sell amount: amount of cryptocurrency that will be sold when conditions are met.
    E.G.
    checkprice(currency='btcusd', shortstop_price=19000, sell_price = 19100, sell_amount= 0.5)
    When trade price of btc reaches 19000 usd or below, an order will be placed to sell 0.5btc.
    '''
    #latest trade price of currency
    trade_price = float(gemi.get_ticker(currency)['ask'])
    #current time
    time_now = str(datetime.now())
    #client order id: set to be date and time when order is placed
    order_id = strftime('%m-%d_%H:%M',gmtime())
    if shortstop_price:
        if trade_price <= shortstop_price:
            gemi.new_order(symbol=currency, amount=sell_amount, price=sell_price,
                            side='sell', type = 'exchange limit', client_order_id = order_id)
            print('stop limit for '+currency+' triggered at '+time_now+'.'+ str(sell_amount)+currency+' sold.')
            all_is_well = False
        else:
            print(str(currency)+':'+str(trade_price)+' at '+ time_now)
        #enter the period (in seconds) how often you'd like the bot to check the prices.
        #e.g. sleep(30) would mean checking every 30 secs
        

#change the numbers in check_price below to set the stop loss you want.
def trade():
    while all_is_well:
        check_price('ethusd', shortstop_price=4000, sell_price=4100,sell_amount=0.3)
        sleep(30)
#press f5 to begin the stop loss program
trade()


            
            

