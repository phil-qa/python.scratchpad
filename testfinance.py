import unittest
from finance import *

class MyTestCase(unittest.TestCase):
    def test_revenue_item(self):
        ri = ValueItem('mine', 10, ValueType.RETAIL)
        self.assertEqual(10, ri.total_value(1))

    def test_revenue_item_subscription(self):
        ri = ValueItem('mine', 10, ValueType.SUBSCRIPTION, frequency=[1, 1])
        self.assertEqual(10, ri.total_value(1))

    def test_revenue_item_subscription_term(self):
        ri = ValueItem('mine', 10, ValueType.SUBSCRIPTION, frequency=[1, 12])
        self.assertEqual( 20, ri.total_value(24))
    def test_cost_item(self):
        ci = CostItem('mine', 10, ValueType.RETAIL)
        self.assertEqual(-10, ci.total_value(1))

    def test_cost_item_subscription(self):
        ci = CostItem('mine', 10, ValueType.SUBSCRIPTION, [1,1])
        self.assertEqual(-50, ci.total_value(5))

    def test_cost_item_term(self):
        ci = CostItem('mine', 10, ValueType.SUBSCRIPTION, [1, 12])
        self.assertEqual(-20, ci.total_value(24))



    '''
    Given a series of value items stored in a RevenueStream 
    When the total is requested 
    Then the result is the values - the costs'''

    def test_value_stream_initialises(self):
        '''The stream initialises on a retail model unless told otherwise'''
        rs = RevenueStream()
        for vi in self.get_10_value_items():
            rs.add_or_update_model_item(vi)
        self.assertEqual(100, rs.positive_value)
        self.assertEqual(100, rs.stream_value())

    def test_value_stream_streams(self):
        '''A revenue stream initialises to hold all value streams
        it wil then run for the term it is initialises with default 1
        and update the total value'''
        rs = RevenueStream(2)
        rs.add_or_update_model_item(ValueItem('cust_1',1,ValueType.SUBSCRIPTION,[3,1]))
        #if a subscription hits vaue 3 times in 1 term then the value for the subscription
        #after 2 terms for a base value of 1 then its value in a stream is 6
        self.assertEqual(6, rs.stream_value())



    def test_stream_adjustments(self):
        rs = RevenueStream()
        for vi in self.get_10_value_items():
            rs.add_or_update_model_item(vi)

        rs.revenue_items[0].value_type=ValueType.SUBSCRIPTION
        rs.revenue_items[0].frequency=[1,1]




    def get_10_value_items(self, value_type=ValueType.RETAIL, frequency=[0,0]):
        value_items = []
        for i in range (1,11):
            name = 'user'+str(i)
            value_items.append(ValueItem(name, 10, value_type, frequency))
        return value_items

if __name__ == '__main__':
    unittest.main()
