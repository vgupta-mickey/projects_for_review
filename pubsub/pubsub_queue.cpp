#include "pubsub_queue.hpp"

int queue_protected::is_queue_full()
{
    if (((head +1) % capacity) == tail)
      return true;
    return false;
}


int queue_protected::is_queue_empty()
{
    if (head == tail)
      return true;
    return false; 
}

uint64_t queue_protected::current_queue_size ()
{
    return current_size;
}

int queue_protected::enque_msg_protected(queue_msg& msg)
{
    int ret;
    writeLock.lock();
    ret = enque_msg(msg);
    writeLock.unlock();
    return ret;
}

int queue_protected::enque_msg (queue_msg& msg)
{
    uint64_t _curSize_snap_shot;
    if (is_queue_full() == true)
    {
      cout << "queue full" <<endl;
      return false;
    }
    queue[head] = msg;
    _curSize_snap_shot = __sync_add_and_fetch(&current_size, 1);
    head = (head +1) % capacity;
    return true;
}


int queue_protected::deque_msg (queue_msg& msg)
{
    uint64_t _curSize_snap_shot;
    if (is_queue_empty() == true)
    {
      //printf("queue empty\n");
      return false;
    }
    msg = queue[tail];
    queue[tail].msg = nullptr;

    _curSize_snap_shot = __sync_fetch_and_sub(&current_size, 1);
    assert(_curSize_snap_shot);
    
    tail = (tail +1) % capacity;
    return true;
}
