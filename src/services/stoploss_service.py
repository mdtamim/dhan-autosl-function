from services.dhan_services import fetch_positions_and_holdings, cancel_pending_orders,get_market_feed,place_stoploss_orders
from utils.helpers import calculate_average_buy_price, get_security_id,get_total_stock_qty, get_sl_details
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

            max_gain_percent = stock_details['Max_Gain_Percent']
            stoploss_details = stock_details['Stoploss_Details']

            # Sort stop-loss details by the lowest stop-loss price
            stoploss_details.sort(key=lambda x: x['stoploss_price'])

            # Adjust stop-loss prices based on current gain percentage
            for detail in stoploss_details:
                if current_gain_percent > max_gain_percent:
                    max_gain_percent = current_gain_percent
                    detail['stoploss_price'] = round(
                        round(detail['stoploss_price'] * (
                                    1 + (current_gain_percent - max_gain_percent) / 100) / 0.05) * 0.05, 2)

            place_stoploss_orders(dhan, stoploss_details)
            update_stock_in_db(db, stock_symbol,
                               {'Average_Buy_Price': average_buy_price, 'Max_Gain_Percent': max_gain_percent,
                                'Stoploss_Details': stoploss_details})
            return

        elif current_gain_percent > 0:
            max_gain_percent = current_gain_percent

        else:
            max_gain_percent = 0

        # Cancel existing pending orders
        #cancel_existing_orders(existing_orders, stock_symbol)

        delete_stock_from_db(db, stock_symbol)

        max_gain_price = round(average_buy_price * (1 + max_gain_percent / 100), 2)
        stoploss_details = []

        if max_gain_percent <= 5:
            sl_40 = round(round(min(max_gain_price * 0.96, current_price)/ 0.05) * 0.05, 2)
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_40, 0.4*total_qty_dhan))

            sl_60 = round(round(min(max_gain_price * 0.94, current_price) / 0.05) * 0.05, 2)
            stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_60, total_qty_dhan - stoploss_details[0]['quantity']))

        if 18 >= max_gain_percent > 5:
            if total_qty_dhan*average_buy_price >= 220000:
                sl_40 = round(round(min(max_gain_price * 0.96, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_40, 0.4 * total_qty_dhan))

                sl_60 = round(round(min(max_gain_price * 0.94, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_60, total_qty_dhan - stoploss_details[0]['quantity']))
            else:
                sl = round(round(min(max_gain_price * 0.94, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl, total_qty_dhan))

        if max_gain_percent > 18:
            if total_qty_dhan * average_buy_price >= 220000:
                sl_25 = round(round(min(max_gain_price * 0.97, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_25, 0.25*total_qty_dhan))

                sl_35 = round(round(min(max_gain_price * 0.95, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_35, 0.35*total_qty_dhan))

                sl_remaining = round(round(min(max_gain_price * 0.93, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_remaining, total_qty_dhan - stoploss_details[0]['quantity'] - stoploss_details[1]['quantity']))

            elif total_qty_dhan*average_buy_price >= 170000:
                sl_35 = round(round(min(max_gain_price * 0.95, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_35, 0.35 * total_qty_dhan))

                sl_remaining = round(round(min(max_gain_price * 0.93, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl_remaining, total_qty_dhan - stoploss_details[0]['quantity']))

            else:
                sl = round(round(min(max_gain_price * 0.93, current_price) / 0.05) * 0.05, 2)
                stoploss_details.append(get_sl_details(stock_symbol, security_id, sl, total_qty_dhan))


        place_stoploss_orders(dhan, stoploss_details)

        update_stock_in_db(db, stock_symbol,
                           {'Average_Buy_Price': average_buy_price, 'Max_Gain_Percent': max_gain_percent,
                            'Stoploss_Details': stoploss_details})
