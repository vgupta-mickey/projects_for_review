#ifndef __QUEUE_PROTECTED__
#define __QUEUE_PROTECTED__
#include <iostream>
#include <string>
#include <mutex>
#include <boost/shared_ptr.hpp>
#define QUEUE_MAX_CAPACITY 500

using namespace std;

typedef boost::shared_ptr<string> msg_shared_ptr;

class  queue_msg
{
    public:
    std::string channel;
    msg_shared_ptr msg;

    queue_msg ():
    msg (nullptr)
    {
	}
    queue_msg (std::string& _channel, msg_shared_ptr& _msg):
    channel(_channel),
    msg (_msg)
    {
    }
    queue_msg& operator=(const queue_msg& x) {
     channel = x.channel;
     msg = x.msg;
     return *this;
    }
};

class queue_protected
{
public:
    queue_protected():
        head(0),
        tail(0),
        capacity(QUEUE_MAX_CAPACITY),
        current_size(0)

    {
      for (int i=0; i <QUEUE_MAX_CAPACITY; i++)
      {
        queue[i].msg = nullptr;
      }
    }

    int enque_msg_protected(queue_msg& msg);
    int deque_msg (queue_msg& msg);
	uint64_t current_queue_size (void);
private:
    int enque_msg (queue_msg& msg);
    int is_queue_full(void);
    int is_queue_empty(void);

    uint64_t head;
    uint64_t tail;
    queue_msg  queue[QUEUE_MAX_CAPACITY];
    uint64_t  capacity;
    uint64_t  current_size;
    std::mutex writeLock;
};
#endif
