import time
import requests

from config.dhan_init import headers,url
from utils.helpers import adjust_to_tickr_size

def fetch_positions_and_holdings(dhan):
    """Fetch all positions and holdings from Dhan and group by stock."""
    positions = dhan.get_positions().get('data', [])
    holdings = dhan.get_holdings().get('data', [])

    print("Type of positions:", type(positions))
	print("Type of holdings:", type(holdings))

    grouped_data = {}

    for item in positions + holdings:
        trading_symbol = item['tradingSymbol']
        if trading_symbol not in grouped_data:
            grouped_data[trading_symbol] = {'positions': [], 'holdings': []}
        if item in positions and item['positionType'] != 'SHORT':
            grouped_data[trading_symbol]['positions'].append(item)
        else:
            grouped_data[trading_symbol]['holdings'].append(item)
    print('grouped_data',grouped_data)
    return grouped_data


def cancel_pending_orders(dhan):
    all_orders = dhan.get_order_list().get('data', [])
    for order in all_orders:
        if order['orderStatus'] in ['REJECTED','CANCELLED','EXPIRED','TRADED']:
            continue
        dhan.cancel_order(order['orderId'])
    time.sleep(5)


def get_market_feed(grouped_data):
    # Extracting unique securityId into a set
    security_ids = set()

    # Adding securityIds from holdings
    for stock in grouped_data.values():
        for holding in stock['holdings']:
            security_ids.add(holding['securityId'])

    # Adding securityIds from positions
    for stock in grouped_data.values():
        for position in stock['positions']:
            security_ids.add(position['securityId'])

    # Converting the set back to a list
    unique_security_ids = list(map(int, security_ids))

    data = { "NSE_EQ": unique_security_ids }
    response = requests.post(url, headers=headers, json=data)
    #print('Market Feed ',response.json())
    if response.status_code == 200:
        ltp_map = {}
        response_data = response.json()
        for market_type, securities in response_data.get("data", {}).items():
            print('Market Type ',market_type)
            print('Securities ', securities)
            for security_id, details in securities.items():
                last_price = details.get("last_price")
                ltp_map[security_id] = last_price
        return ltp_map
    else:
        return {"error": response.status_code, "message": response.text}


# Function to handle placing or modifying stop-loss orders based on conditions
def place_stoploss_orders(dhan, stoploss_details):
    for detail in stoploss_details:
        stoploss_price = detail['stoploss_price']
        quantity = detail['quantity']
        trigger_price = adjust_to_tickr_size(stoploss_price * 1.0025) # Trigger price is 0.25% more than Stoploss
        # Place order using Dhan API
        dhan.place_order(
            transaction_type=dhan.SELL,
            exchange_segment=dhan.NSE,
            product_type=dhan.CNC,
            order_type=dhan.SL,
            validity='DAY',
            security_id=detail['security_id'],
            quantity=quantity,
            price=stoploss_price,
            trigger_price=trigger_price
        )
