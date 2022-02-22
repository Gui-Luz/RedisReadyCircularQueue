<img src="https://pbs.twimg.com/profile_images/1427657682626961410/aJp7nOdu_400x400.jpg" width="100" height="100">

# Redis Ready Circular Queue
### A pythonic implementation of circular queue connected to a redis client
Redis Ready Circular Queue is an object that can be used whenever you need to iterate over a circular queue. It uses Redis as the cache memory for your queue and pointer.  
##### Installation
```
git clone https://github.com/Gui-Luz/RedisReadyCircularQueue.git
```
##### How to use
After cloning the repo, you can import the **ReadisReadyCircularQueue** class to your project:
```
from rrcq import RedisReadyCircularQueue
```
You can instantiate the **RedisReadyCircularQueue** object passing a Redis **host** an a **port** as arguments:
```
host = 'localhost'
port = 6379
rrcq = RedisReadyCircularQueue(host, port)
```
If its the first time you are using **rrcq** with a database you should set a new queue:
```
queue = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado']
pointer = 'Apple'
rrcq.set_new_queue(queue, pointer)
```
Then you can simply call rotate_left, to get next element, or rotate_right, to get previous element in queue:
```
rrcq.rotate_left()
>>>'Orange'
rrcq.rotate_left()
>>>'Avocado'
rrcq.rotate_left()
>>>'Banana'
rrcq.rotate_left()
>>>'Avocado'
```
