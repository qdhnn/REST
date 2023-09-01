import json
import http.client
import pprint

# API Settigs .+++++++3
AUTH_TOKEN = '5cc8a056f50f238c1f81300ce81a4fd31bf95d27'  # Your authorization token
HOST = 'my.prom.ua'  # e.g.: my.prom.ua, my.tiu.ru, my.satu.kz, my.deal.by, my.prom.md
print('''
1 = orders list
2 = product list
3 = group list
4 = client list
5 = order/ID
6 = POST order status

''')

a = int(input('''input a
'''))


class HTTPError(Exception):
    pass


class EvoClientExample(object):

    def __init__(self, token):
        self.token = token

    def make_request(self, method, url, body=None):
        connection = http.client.HTTPSConnection(HOST)

        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-type': 'application/json'}
        if body:
            body = json.dumps(body)

        connection.request(method, url, body=body, headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            raise HTTPError('{}: {}'.format(response.status, response.reason))

        response_data = response.read()
        return json.loads(response_data.decode())

    def get_order_list(self):
        url = '/api/v1/orders/list'
        method = 'GET'

        return self.make_request(method, url)

    def get_product_list(self):
        url = '/api/v1/products/list'
        method = 'GET'

        return self.make_request(method, url)

    def get_client_list(self):
        url = '/api/v1/clients/list'
        method = 'GET'

        return self.make_request(method, url)

    def get_order(self, order_id):
        url = '/api/v1/orders/{id}'
        method = 'GET'

        return self.make_request(method, url.format(id=order_id))

    def get_group(self):
        url = '/api/v1/groups/list'
        method = 'GET'

        return self.make_request(method, url)

    def set_order_status(self, status, ids, cancellation_reason=None, cancellation_text=None):
        url = '/api/v1/orders/set_status'
        method = 'POST'

        body = {
            'status': status,
            'ids': ids
        }
        if cancellation_reason:
            body['cancellation_reason'] = cancellation_reason

        if cancellation_text:
            body['cancellation_text'] = cancellation_text

        return self.make_request(method, url, body)


def main():
    # Initialize Client
    if not AUTH_TOKEN:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN!')

    api_example = EvoClientExample(AUTH_TOKEN)

    if a == 1:
        #
        #
        pprint.pprint(api_example.get_order_list())

    elif a == 2:
        product_list = api_example.get_product_list()
        if not product_list['products']:
            raise Exception('Sorry, there\'s no any product!')

        pprint.pprint(product_list)

    elif a == 3:
        group_list = api_example.get_group()
        pprint.pprint(api_example.get_group())

    elif a == 4:
        # client_list = api_example.get_client_list()
        pprint.pprint(api_example.get_client_list())

    if a == 5:
        # Order example data. Requred to be setup to get example work
        print('Ввести номер заказа или использовать 217414788 [y/n]?')
        q = str(input('''q
        '''))
        if q == str('y'):
            id = int(input('''input id
            '''))
        else:
            id = int(217414788)
        order = api_example.get_order(id)
        pprint.pprint(order)

    if a == 6:
        # Order example data. Requred to be setup to get example work
        print('Ввести номер заказа или использовать 217397388 [y/n]?')
        q = str(input('''q
        '''))
        if q == str('y'):
            id = int(input('''input id
            '''))
        else:
            id = int(217397388)
            # id = int(217414788)
            # id = int(217397388)
        # order_id = order_list['orders'][0]['id']
        # id = int(input('''input id
        # '''))
        # ---
        # order_id = order_list['orders'][0]['id']
        status = 'received'
        ids = [id]
        order = api_example.set_order_status(status=status, ids=ids)

    # Setting order status
        # pprint.pprint(api_example.set_order_status(status=status, ids=order_ids))

    # # Getting order by id--
        # pprint.pprint(api_example.get_order(order_id))
        # pprint.pprint(api_example.get_order())
        pprint.pprint(order)
    # else:
    #    print('wrong')


if __name__ == '__main__':
    main()

# end
