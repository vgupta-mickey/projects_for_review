#ifndef __PUBSUB_SOCK_CONN_HPP__
#define __PUBSUB_SOCK_CONN_HPP__
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <thread>
#include <memory>
#include <boost/asio.hpp>
#include <boost/array.hpp>
#include <boost/noncopyable.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/bind.hpp>
#include <mutex>
#include <functional>
#include "pubsub_queue.hpp"

using namespace std;
using boost::asio::ip::tcp;
typedef boost::shared_ptr<string> msg_shared_ptr;

class pubSubServerThread_t;

//This class manages connection specific data
//it maintains incoming buffer to receive the data
//outgoing buffer to send the msg
//it maintains a writeLock -- as 2 subsequent async_write w/o getting callback
//is a problem
//it maintains the list of all the channels currently subscribed by this client,
//so if client connection dies, we can remove this connection from the global
//list of channel subscriptions
//each connection is given a connection ID to search the connection in the
//global list

class sock_conn : public boost::enable_shared_from_this<sock_conn>
{
public:
 sock_conn(pubSubServerThread_t *_pThread, uint64_t _conId);
 ~sock_conn();
 uint64_t getConId(void);
 void start(void);
 void sendMsg (const string & _channel, msg_shared_ptr _msg);
 tcp::socket& socket(void);
 void enque_msg (const string& _channel, msg_shared_ptr);
 void new_msg (void);

private:
  void handle_read(const boost::system::error_code& e);
  void handle_write(const boost::system::error_code& e);
  void deleteAllChannels(void);
  tcp::socket socket_;
  pubSubServerThread_t *pThread;
  boost::asio::streambuf buf;
  uint64_t conId;
  vector<char> outbuf;
  std::mutex writeLock;
  unordered_set<std::string>  subscribedChannels;
  queue_protected queue;
};

//when nobody owns the connection obj - this customized deleter will be invoked  
// this is not doing any thing extra at this point of time

struct delete_sock_conn {
  void operator()(sock_conn* _con) const {
    if (_con != NULL)
    {
      cout << "conId: " << _con->getConId() << " is deleted" << endl;
      delete _con;
    }
  }
};

// connections are maintained as shared_ptr so that when client socket is
// closed, and no one else is owning the connection block, it automatically
// deletes the memory
typedef boost::shared_ptr<sock_conn> sock_conn_shared_ptr;

#endif
