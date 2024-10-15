import math

# Helper function to fetch average buy price from positions and holdings
def calculate_average_buy_price(grouped_data):
    total_cost = 0
    total_quantity = 0
    for stock in grouped_data.values():
        for position in stock['positions']:
            if position['positionType'] != 'SHORT':
                total_cost += position['costPrice'] * abs(position['netQty'])
                total_quantity += abs(position['netQty'])
        for holding in stock['holdings']:
            if 'positionType' not in holding: #positionType in holdings happens when some holdings were sold,positionType becomes 'SHORT'
                total_cost += holding['avgCostPrice'] * holding['totalQty']
                total_quantity += holding['totalQty']

    if total_quantity == 0:
        return 0
    return round(total_cost / total_quantity, 2)

def get_security_id(stock_data):
    if stock_data['positions']:
        return stock_data['positions'][0]['securityId']
    else:
        return stock_data['holdings'][0]['securityId']

def get_total_stock_qty(stock_data):
    total_quantity = 0

    for position in stock_data['positions']:
        if position['positionType'] == 'LONG':
            total_quantity += position['netQty']

    for holding in stock_data['holdings']:
        if 'availableQty' in holding:
            total_quantity += holding['availableQty']

    return total_quantity


def get_sl_details(stock_symbol,security_id, sl_price, stock_qty):
    return {'stock_symbol': stock_symbol, 'stoploss_price': sl_price, 'quantity': math.ceil(stock_qty), 'security_id': security_id}