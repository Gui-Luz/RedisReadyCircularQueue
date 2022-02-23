from redis import Redis
from rrcq.circular_queue.circular_queue import CircularQueue
import ast


class RedisReadyCircularQueue:
    def __init__(self, host, port, db=0):
        self.redis_connection_host = host
        self.redis_connection_port = port
        self.redis_connection_db = db
        self.redis_queue_key = 'RRCQ:circularqueue'
        self.redis_pointer_key = 'RRCQ:pointer'

    def set_new_queue(self, new_queue, new_pointer):
        self._set_queue(new_queue)
        self._set_pointer(new_pointer)

    def unset_queue(self):
        self._unset_queue()
        self._unset_pointer()

    def rotate_right(self):
        queue, pointer = self._get_redis_queue_and_pointer_values()
        circular_queue = CircularQueue(queue, pointer)
        next_element = circular_queue.get_next_element()
        self._set_pointer(next_element)
        return next_element

    def rotate_left(self):
        queue, pointer = self._get_redis_queue_and_pointer_values()
        circular_queue = CircularQueue(queue, pointer)
        previous_element = circular_queue.get_previous_element()
        self._set_pointer(previous_element)
        return previous_element

    def get_batch(self, batch_size, rotation='right'):
        retrieved_elements = []
        for i in range(0, batch_size):
            if rotation == 'right':
                element = self.rotate_right()
                retrieved_elements.append(element)
            elif rotation == 'left':
                element = self.rotate_left()
                retrieved_elements.append(element)
            else:
                raise AttributeError('An invalid rotation was provided. Please use left or right rotation.')
        return retrieved_elements

    def _get_redis_queue_and_pointer_values(self):
        queue = self._get_redis_queue_value()
        pointer = self._get_redis_pointer_value()
        return queue, pointer

    def _get_redis_queue_value(self):
        redis_client = self._connect_to_redis()
        queue_bytes = redis_client.get(self.redis_queue_key)
        if queue_bytes:
            queue_string = self._convert_bytes_to_string(queue_bytes)
            queue_list = self._convert_string_to_list(queue_string)
            return queue_list
        else:
            raise ConnectionError("You didn't set a queue in Redis yet. Please use set_new_queue_method before "
                                  "rotating the queue.")

    def _get_redis_pointer_value(self):
        redis_client = self._connect_to_redis()
        pointer_bytes = redis_client.get(self.redis_pointer_key)
        if pointer_bytes:
            pointer_string = self._convert_bytes_to_string(pointer_bytes)
            return pointer_string
        raise ConnectionError("You didn't set a pointer in Redis yet. Please use set_new_queue_method before rotating "
                              "the queue.")

    def _set_queue(self, queue):
        converted_queue = self._convert_list_to_string(queue)
        redis_client = self._connect_to_redis()
        redis_client.set(self.redis_queue_key, converted_queue)

    def _unset_queue(self):
        redis_client = self._connect_to_redis()
        redis_client.delete(self.redis_queue_key)

    def _set_pointer(self, pointer):
        redis_client = self._connect_to_redis()
        redis_client.set(self.redis_pointer_key, pointer)

    def _unset_pointer(self):
        redis_client = self._connect_to_redis()
        redis_client.delete(self.redis_pointer_key)

    def _connect_to_redis(self):
        redis_client = Redis(host=self.redis_connection_host, port=self.redis_connection_port,
                             db=self.redis_connection_db)
        return redis_client

    @staticmethod
    def _convert_list_to_string(mylist):
        string_list = str(mylist)
        return string_list

    @staticmethod
    def _convert_bytes_to_string(mybytes):
        mystring = mybytes.decode()
        return mystring

    @staticmethod
    def _convert_string_to_list(mystring):
        mylist = ast.literal_eval(mystring)
        return mylist




