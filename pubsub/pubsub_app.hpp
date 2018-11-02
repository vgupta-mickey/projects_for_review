#ifndef __PUBSUB_APP_HPP__
#define __PUBSUB_APP_HPP__
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
#include "pubsub_sock_conn.hpp"

using namespace std;

//functor for hashing entry in the set of all the connections for each channel  
struct SetKeyHash
{
  uint64_t operator() (const  sock_conn_shared_ptr &k) const {return hash<uint64_t>()(k->getConId()); }
};
 
//compare functor to find an entry in set
struct SetKeyCompare
{
  bool operator() (const sock_conn_shared_ptr &x, const sock_conn_shared_ptr &y) const 
  { 
 
      return x->getConId() == y->getConId();
  }
};

typedef unordered_set<sock_conn_shared_ptr, SetKeyHash, SetKeyCompare> SubSet_t;

//This class manages the pubsub application
//It maintains a list of client connections who are subscribed for a channel
//The list is global. Every client will register his subscription to this list 
//list is protected by mutex

class pubsubApp_t
{
  public:
      pubsubApp_t();
      ~pubsubApp_t();
      void addSubscriber (const  std::string& _channel, sock_conn_shared_ptr _conn);
      void deleteSubscriber (const std::string& _channel, sock_conn_shared_ptr _conn);
      void publishChannelMsg(const std::string& _channel, msg_shared_ptr msg);
  private:
  void publishMsgToSubscriber (const string& _channel, sock_conn_shared_ptr _conn, msg_shared_ptr msg);

  //channel name to list of connections who are looking for this channel messages
  unordered_map<string, SubSet_t>  channel_subscriber_list_map;
  //std::mutex mtx;
  std::mutex subscriber_list_mtx;
};

#endif
