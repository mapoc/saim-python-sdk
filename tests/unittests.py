import json
import unittest
import urllib.error
import urllib.request
import pprint

base_url = 'https://apisb.shop.com/saim/v1'
api_key = 'your-api-key-here'

# if you run TestHouseholds.test_post_households(), this will be overwritten in memory as intended
household_id = '1001'


class TestHouseholds(unittest.TestCase):
    #
    # expected successes
    #

    # when the tests are run en masse they are done alphabetically within the class, so this
    # post is set to run first since it needs to set the household id before everything else runs
    def test_1_post_households(self):
        req_body = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': 'Cardboard Box #3',
            'email': 'homeless@nowhere.com',
            'primary_phone': '(123) 456-7890'
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        resp = json.loads(resp.read().decode())

        print("Printing response information")
        pprint.pprint(resp)

        self.assertEqual(resp.getcode(), 201)

        # this allows a global override of the household id so that all the other methods
        # can use this variable
        global household_id
        household_id = resp['id']

    def test_get_households(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id,
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_put_households(self):
        req_body = {
            'last_name': 'Smith',
            'address': 'House, City, ST 12345',
            'first_name': 'John',
            'primary_phone': '123-456-0000',
            'email': 'noyb@z.com'
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id,
                                     data=req_json,
                                     headers=req_headers,
                                     method='PUT')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_put_households_subset(self):
        req_body = {
            'primary_phone': '111-222-3344',
            'email': 'testing@test.com'
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id,
                                     data=req_json,
                                     headers=req_headers,
                                     method='PUT')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    #
    # expected failures
    #
    def test_post_households_missing_address_bad_email(self):
        req_body = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'homeless@nowhere',
            'primary_phone': '(123) 456-7890'
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 400)

    def test_get_households_invalid_household_id(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/bad_id',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 401)

    def test_put_households_invalid_email(self):
        req_body = {
            'primary_phone': '123-456-0000',
            'email': 'noyb@z'
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}

        req = urllib.request.Request(base_url + '/households/' + household_id,
                                     data=req_json,
                                     headers=req_headers,
                                     method='PUT')
        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 400)


class TestHouseholdsLists(unittest.TestCase):
    #
    # expected successes
    #
    def test_get_households_lists(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    #
    # expected failures
    #
    def test_get_households_lists_invalid_household_id(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/bad_id/lists',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 401)


class TestHouseholdsStockLists(unittest.TestCase):
    #
    # expected successes
    #
    def test_post_households_stock_list(self):
        req_body = [
            {'id': '1310035849',
             'title': 'a title',
             'on_hand': 3,
             'on_order': 0,
             'min': 2,
             'max': 5},
            {'id': '1470432411',
             'title': 'any old title',
             'on_hand': 8,
             'on_order': 0,
             'min': 4,
             'max': 10}
        ]
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_get_households_stock_list(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_get_households_stock_list_2(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    #
    # expected failures
    #
    def test_post_households_stock_list_invalid_list_id(self):
        req_body = [
            {'id': '1310035849',
             'title': 'a title',
             'on_hand': 3,
             'on_order': 0,
             'min': 2,
             'max': 5},
            {'id': '1470432411',
             'title': 'any old title',
             'on_hand': 8,
             'on_order': 0,
             'min': 4,
             'max': 10}
        ]
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/bad_list/stock',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 404)

    def test_post_households_stock_list_empty_min_on_hand(self):
        req_body = [
            {'id': '1310035849',
             'title': 'a title',
             'on_hand': 3,
             'on_order': 0,
             'max': 5},
            {'id': '1470432411',
             'title': 'any old title',
             'on_order': 0,
             'min': 4,
             'max': 10}
        ]
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 400)

    def test_get_households_stock_list_invalid_household_id(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/bad_id/lists/main',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 401)


class TestHouseholdsStock(unittest.TestCase):
    #
    # expected successes
    #
    def test_get_households_stock(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock/1310035849',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_put_households_stock(self):
        req_body = {
            'title': 'some title',
            'min': 2,
            'max': 5
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock/1310035849',
                                     data=req_json,
                                     headers=req_headers,
                                     method='PUT')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_put_households_stock_subset(self):
        req_body = {
            'title': 'a better title',
            'max': 15
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock/1310035849',
                                     data=req_json,
                                     headers=req_headers,
                                     method='PUT')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_delete_households_stock(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock/1470432411',
                                     headers=req_headers,
                                     method='DELETE')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    #
    # expected failures
    #
    def test_get_households_stock_invalid_stock_id(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/households/' + household_id + '/lists/main/stock/bad_id',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 404)


class TestHouseholdsTransactions(unittest.TestCase):
    #
    # expected successes
    #
    def test_post_households_transactions(self):
        req_body = {
            'type': 'add',
            'quantity': 10
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url+'/households/'+household_id+'/lists/main/stock/1310035849/transactions',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_get_households_transactions(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url+'/households/'+household_id+'/lists/main/stock/1310035849/transactions',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    #
    # expected failures
    #
    def test_post_households_transactions_invalid_type(self):
        req_body = {
            'type': 'invalid',
            'quantity': 10
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url+'/households/'+household_id+'/lists/main/stock/1310035849/transactions',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 422)

    def test_post_households_transactions_missing_type(self):
        req_body = {
            'quantity': 10
        }
        req_json = json.dumps(req_body).encode()
        req_headers = {'Content-Type': 'application/json',
                       'api_key': api_key}
        req = urllib.request.Request(base_url+'/households/'+household_id+'/lists/main/stock/1310035849/transactions',
                                     data=req_json,
                                     headers=req_headers,
                                     method='POST')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 400)


class TestProducts(unittest.TestCase):
    #
    # expected successes
    #
    def test_get_products_list(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/products',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    def test_get_products_item(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + '/products/1207714220',
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 200)

    #
    # expected failures
    #
    def test_get_products_item_long_product_id(self):
        req_headers = {'api_key': api_key}
        req = urllib.request.Request(base_url + ('/products/11111111111111111111111111111111111111111111111111111111111'
                                                 '111111111111111111111111111111111111111111111111111111111111111111111'
                                                 '111111111111111111111111111111111111111111111111111111111111111111111'
                                                 '111111111111111111111111111111111111111111111111111111111111111111111'
                                                 '111111111111111111111111111'),
                                     headers=req_headers,
                                     method='GET')

        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            resp = e

        self.assertEqual(resp.getcode(), 400)

if __name__ == '__main__':
    # there's a bug because failures happen when they shouldn't when doing the run_all but not if the tests
    # are all run individually

    run_all = False

    if run_all:
        # to run all tests, which will be in alphabetical order in the classes not in the order they are listed
        unittest.main(verbosity=2)
    else:
        # if using Eclipse, this should work fine as is;
        # if using PyCharm (presumably also IDEA), you have to go to some extra lengths to make sure it doesn't just
        # run all of the unittests (see https://stackoverflow.com/questions/20835466/pycharm-wont-allow-to-run-a-file-
        # shows-run-unittest-option-only)
        # in short, at least the first time don't just right-click and do run because it will do a unittests run.
        # instead:
        # 1. click the Run menu
        # 2. choose Run...
        # 3. choose run unittests
        # going forward you can right-click and just choose Run unittests

        # to run specific tests, all of them are listed
        test_suite = unittest.TestSuite()

        test_suite.addTest(TestHouseholds('test_1_post_households'))
        test_suite.addTest(TestHouseholds('test_get_households'))
        test_suite.addTest(TestHouseholds('test_put_households'))
        test_suite.addTest(TestHouseholds('test_post_households_missing_address_bad_email'))
        test_suite.addTest(TestHouseholds('test_get_households_invalid_household_id'))
        test_suite.addTest(TestHouseholds('test_put_households_invalid_email'))

        test_suite.addTest(TestHouseholdsLists('test_get_households_lists'))
        test_suite.addTest(TestHouseholdsLists('test_get_households_lists_invalid_household_id'))

        test_suite.addTest(TestHouseholdsStockLists('test_post_households_stock_list'))
        test_suite.addTest(TestHouseholdsStockLists('test_get_households_stock_list'))
        test_suite.addTest(TestHouseholdsStockLists('test_get_households_stock_list_2'))
        test_suite.addTest(TestHouseholdsStockLists('test_post_households_stock_list_invalid_list_id'))
        test_suite.addTest(TestHouseholdsStockLists('test_post_households_stock_list_empty_min_on_hand'))
        test_suite.addTest(TestHouseholdsStockLists('test_get_households_stock_list_invalid_household_id'))

        test_suite.addTest(TestHouseholdsStock('test_get_households_stock'))
        test_suite.addTest(TestHouseholdsStock('test_put_households_stock'))
        test_suite.addTest(TestHouseholdsStock('test_put_households_stock_subset'))
        test_suite.addTest(TestHouseholdsStock('test_delete_households_stock'))
        test_suite.addTest(TestHouseholdsStock('test_get_households_stock_invalid_stock_id'))

        test_suite.addTest(TestHouseholdsTransactions('test_post_households_transactions'))
        test_suite.addTest(TestHouseholdsTransactions('test_get_households_transactions'))
        test_suite.addTest(TestHouseholdsTransactions('test_post_households_transactions_invalid_type'))
        test_suite.addTest(TestHouseholdsTransactions('test_post_households_transactions_missing_type'))

        test_suite.addTest(TestProducts('test_get_products_list'))
        test_suite.addTest(TestProducts('test_get_products_item'))
        test_suite.addTest(TestProducts('test_get_products_item_long_product_id'))

        unittest.TextTestRunner(verbosity=2).run(test_suite)
