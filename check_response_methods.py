from data import ResponseSample


def check_user_data_response(response, sample):
    if response['success']:
        if response.keys() == sample.keys():
            if response['user'].keys() == sample['user'].keys():
                return "OK"


def check_user_orders_response(response):
    sample = ResponseSample.USER_ORDERS_LIST
    order_sample = ResponseSample.ORDER
    if response['success']:
        if response.keys() == sample.keys():
            orders = response['orders']
            checked_orders = 0
            for order in orders:
                if order.keys() == order_sample.keys():
                    checked_orders += 1
            if checked_orders == len(orders):
                return "OK"


def check_order_creation_response(response):
    sample = ResponseSample.ORDER_CREATION
    if response['success']:
        if response.keys() == sample.keys():
            if response['order'].keys() == sample['order'].keys():
                return "OK"


def check_error_response(response, sample):
    if not response['success']:
        if response['message'] == sample:
            return "OK"
