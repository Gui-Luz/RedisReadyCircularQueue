from rrcq.rrcq import RedisReadyCircularQueue
from unittest import TestCase


class TestRRRCQ(TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.port = 6379
        self.queue = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado', 'Watermelon']
        self.pointer = 'Watermelon'

    def test_should_return_error_when_trying_to_rotate_queue_before_setting_it(self):
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.unset_queue()
        self.assertRaises(ConnectionError, rrcq.rotate_right)

    def test_should_return_true_when_instantiating_rrcq_object(self):
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        self.assertEqual(str(type(rrcq)), "<class 'rrcq.rrcq.RedisReadyCircularQueue'>")

    def test_should_return_equal_when_creating_new_queue_and_getting_the_queue_from_redis(self):
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        queue = rrcq._get_redis_queue_value()
        self.assertEqual(queue, self.queue)

    def test_should_return_equal_when_creating_new_queue_and_getting_the_pointer_from_redis(self):
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        pointer = rrcq._get_redis_pointer_value()
        self.assertEqual(pointer, self.pointer)

    def test_should_return_next_element_in_queue(self):
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        next = rrcq.rotate_right()
        self.assertEqual(next, 'Banana')

    def test_should_return_previous_element_in_queue(self):
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        next = rrcq.rotate_left()
        self.assertEqual(next, 'Avocado')

    def test_should_return_previous_element_in_queue_when_pointer_is_at_0_position(self):
        self.pointer = 'Banana'
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        next = rrcq.rotate_left()
        self.assertEqual(next, 'Watermelon')

    def test_should_return_next_two_elements_when_calling_get_batch_method(self):
        self.pointer = 'Banana'
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        mybatch = rrcq.get_batch(2)
        self.assertEqual(['Star Fruit', 'Apple'], mybatch)

    def test_should_return_previous_two_elements_when_calling_get_batch_method_with_rotation_left(self):
        self.pointer = 'Banana'
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        mybatch = rrcq.get_batch(2, rotation='left')
        self.assertEqual(['Watermelon', 'Avocado'], mybatch)

    def test_should_return_attribute_error_when_calling_get_batch_method_with_invalid_rotation(self):
        self.pointer = 'Banana'
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        self.assertRaises(AttributeError, rrcq.get_batch, 2, rotation='center')

    def test_should_return_next_when_get_next_element_function_after_a_get_batch_function(self):
        self.pointer = 'Banana'
        rrcq = RedisReadyCircularQueue(host=self.host, port=self.port)
        rrcq.set_new_queue(self.queue, self.pointer)
        rrcq.get_batch(2, rotation='left')
        previous = rrcq.rotate_left()
        self.assertEqual('Orange', previous)
