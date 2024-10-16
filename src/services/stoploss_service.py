from services.dhan_services import fetch_positions_and_holdings, cancel_pending_orders,get_market_feed,place_stoploss_orders
from utils.helpers import adjust_to_tickr_size, calculate_average_buy_price, get_security_id,get_total_stock_qty, get_sl_details
from services.firebase_services import fetch_stock_details_from_db, update_stock_in_db, delete_stock_from_db

def process_stoploss_placement(dhan, db):
    grouped_data = fetch_positions_and_holdings(dhan)
    #existing_orders = fetch_existing_orders()
    #TODO : Instead of cancelling,look into modifying order elegantly
    cancel_pending_orders(dhan)
    ltp_map = get_market_feed(grouped_data)

    for stock_symbol, stock_data in grouped_data.items():
        average_buy_price = calculate_average_buy_price({stock_symbol: stock_data})
        security_id = get_security_id(stock_data)
        current_price = ltp_map[security_id]
        current_gain_percent = round(((current_price - average_buy_price) / average_buy_price) * 100, 2)
        total_qty_dhan = get_total_stock_qty(stock_data)
        stock_details = fetch_stock_details_from_db(db, stock_symbol)

        if (stock_details and  stock_details['Average_Buy_Price'] == average_buy_price and
              total_qty_dhan <= sum(detail['quantity'] for detail in stock_details['Stoploss_Details'])):
            # Cancel existing pending orders
            #cancel_existing_orders(existing_orders, stock_symbol)

            treat_as_existing_stock(db, dhan, average_buy_price, current_gain_percent, current_price, stock_details, stock_symbol, total_qty_dhan)

        else:
            max_gain_percent = current_gain_percent if current_gain_percent > 0 else 0
            # Cancel existing pending orders
            #cancel_existing_orders(existing_orders, stock_symbol)
            treat_as_new_stock(db, dhan, average_buy_price, current_price, max_gain_percent, security_id, stock_symbol, total_qty_dhan)


def treat_as_new_stock(db, dhan, average_buy_price, current_price, max_gain_percent, security_id, stock_symbol, total_qty_dhan):
    delete_stock_from_db(db, stock_symbol)
    max_gain_price = round(average_buy_price * (1 + max_gain_percent / 100), 2)
    stoploss_details = []

    if max_gain_percent <= 5:
        if total_qty_dhan * average_buy_price >= 150000:
            sl_40 = adjust_to_tickr_size(min(max_gain_price * 0.96, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_40, 0.4 * total_qty_dhan))

            sl_60 = adjust_to_tickr_size(min(max_gain_price * 0.94, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_60, total_qty_dhan - stoploss_details[0]['quantity']))

        else:
            sl = adjust_to_tickr_size(min(max_gain_price * 0.94, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl, total_qty_dhan))

    elif 18 >= max_gain_percent > 5:
        if total_qty_dhan * average_buy_price >= 220000:
            sl_40 = adjust_to_tickr_size(min(max_gain_price * 0.96, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_40, 0.4 * total_qty_dhan))

            sl_60 = adjust_to_tickr_size(min(max_gain_price * 0.94, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_60, total_qty_dhan - stoploss_details[0]['quantity']))
        else:
            sl = adjust_to_tickr_size(min(max_gain_price * 0.94, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl, total_qty_dhan))

    else:
        if total_qty_dhan * average_buy_price >= 220000:
            sl_25 = adjust_to_tickr_size(min(max_gain_price * 0.97, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_25, 0.25 * total_qty_dhan))

            sl_35 = adjust_to_tickr_size(min(max_gain_price * 0.95, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_35, 0.35 * total_qty_dhan))

            sl_remaining = adjust_to_tickr_size(min(max_gain_price * 0.93, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_remaining,
                                                   total_qty_dhan - stoploss_details[0]['quantity'] -
                                                   stoploss_details[1]['quantity']))

        elif total_qty_dhan * average_buy_price >= 170000:
            sl_35 = adjust_to_tickr_size(min(max_gain_price * 0.95, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_35, 0.35 * total_qty_dhan))

            sl_remaining = adjust_to_tickr_size(min(max_gain_price * 0.93, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_remaining,
                                                   total_qty_dhan - stoploss_details[0]['quantity']))

        else:
            sl = adjust_to_tickr_size(min(max_gain_price * 0.93, current_price))
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl, total_qty_dhan))

    place_stoploss_orders(dhan, stoploss_details)
    update_stock_in_db(db, stock_symbol,
                       {'Average_Buy_Price': average_buy_price, 'Max_Gain_Percent': max_gain_percent,
                        'Stoploss_Details': stoploss_details})


def treat_as_existing_stock(db, dhan, average_buy_price, current_gain_percent, current_price, stock_details, stock_symbol, total_qty_dhan):
    max_gain_percent = stock_details['Max_Gain_Percent']
    stoploss_details = stock_details['Stoploss_Details']
    # Sort stop-loss details by the lowest stop-loss price
    stoploss_details.sort(key=lambda x: x['stoploss_price'])
    # Adjust stop-loss prices based on current gain percentage
    for details in stoploss_details:
        #If quantity of available stocks in dhan is zero,break out of loop
        if total_qty_dhan == 0:
            break
        #If quantity mentioned in db for a sl is more than total quantity,it indicates some stocks have been sold.In such case update the stock
        #in db to same as present in dhan
        if details['quantity'] > total_qty_dhan:
            details['quantity'] = total_qty_dhan

        total_qty_dhan -= details['quantity']

        if current_gain_percent > max_gain_percent:
            max_gain_percent = current_gain_percent
            details['stoploss_price'] = round(round(details['stoploss_price'] * (
                    1 + (current_gain_percent - max_gain_percent) / 100) / 0.05) * 0.05, 2)

        else:
            details['stoploss_price'] = round(round(min(details['stoploss_price'], current_price) / 0.05) * 0.05, 2)

    place_stoploss_orders(dhan, stoploss_details)
    update_stock_in_db(db, stock_symbol,
                       {'Average_Buy_Price': average_buy_price, 'Max_Gain_Percent': max_gain_percent,
                        'Stoploss_Details': stoploss_details})

    return max_gain_percent

