<img src="https://pbs.twimg.com/profile_images/1427657682626961410/aJp7nOdu_400x400.jpg" width="100" height="100">

# Redis Ready Circular Queue
### A pythonic implementation of circular queue connected to a redis client
Redis Ready Circular Queue is an object that can be used whenever you need to iterate over a circular queue. It uses Redis as the cache memory for your queue and pointer.  
##### Installation
```shell
git clone https://github.com/Gui-Luz/RedisReadyCircularQueue.git
```
##### How to use
After cloning the repo, you can import the **ReadisReadyCircularQueue** class to your project:
```python
from rrcq.rrcq import RedisReadyCircularQueue
```
You can instantiate the **RedisReadyCircularQueue** object passing a Redis **host** an a **port** as arguments:
```python
host = 'localhost'
port = 6379
rrcq = RedisReadyCircularQueue(host, port)
```
If its the first time you are using **rrcq** with a database you should set a new queue:
```python
queue = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado']
pointer = 'Apple'
rrcq.set_new_queue(queue, pointer)
```
Then you can simply call rotate_right, to get next element, or rotate_left, to get previous element in queue:

```python
rrcq.rotate_right()
>> > 'Orange'
rrcq.rotate_right()
>> > 'Avocado'
rrcq.rotate_right()
>> > 'Banana'
rrcq.rotate_left()
>> > 'Avocado'
```
If you need to get a batch of elements, let's say to deliver it to a multi-thread routine, you can call the get_batch method:
```python
queue = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado']
pointer = 'Banana'
batch_size = 2
rrcq.set_new_queue(queue, pointer)
mybatch = rrcq.get_batch(batch_size)
>>> ['Star Fruit', 'Apple']
```
If you need to get a batch rotating the queue to the left, you simply pass 'left' as a rotation value:
```python
queue = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado']
pointer = 'Banana'
batch_size = 2
rrcq.set_new_queue(queue, pointer)
mybatch = rrcqw.get_batch(batch_size, rotation='left')
>>> ['Avocado', 'Orange']
```