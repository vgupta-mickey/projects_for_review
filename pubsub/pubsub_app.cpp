#include "pubsub_app.hpp"

pubsubApp_t::pubsubApp_t() {}

pubsubApp_t::~pubsubApp_t() {}

void pubsubApp_t::publishMsgToSubscriber (const string& _channel, sock_conn_shared_ptr _conn, msg_shared_ptr msg)
{
   _conn->enque_msg(_channel, msg);
}

void pubsubApp_t::publishChannelMsg(const std::string& _channel, msg_shared_ptr msg)
{
   //send this message to all the subscribers
   //get subscriber list
   subscriber_list_mtx.lock();
   auto it_list = channel_subscriber_list_map.find(_channel);

   if (it_list == channel_subscriber_list_map.end())
   {
     //cout << "no one is subscribed for this msg" << endl;
     subscriber_list_mtx.unlock();
     return;
   }
   else
   {
	  //take a copy of the set and unlock it so that other clients can
	  // subscribe/unsubscribe while the messages are published to all the
      // clients
      SubSet_t _set = it_list->second;
      subscriber_list_mtx.unlock();
      for (auto value: _set)
      {
          publishMsgToSubscriber(_channel, value, msg);
      }
   }
   return;
}

void pubsubApp_t::addSubscriber (const std::string& _channel, sock_conn_shared_ptr _conn)
{
    subscriber_list_mtx.lock();
    auto it = channel_subscriber_list_map.find(_channel);
    if (it != channel_subscriber_list_map.end())
    {
       SubSet_t &_set = it->second;
       _set.insert(_conn);
    }
    else
    {
       SubSet_t _set;
       _set.insert(_conn);
       channel_subscriber_list_map.insert({_channel, _set});
    }
    subscriber_list_mtx.unlock();
}

void pubsubApp_t::deleteSubscriber (const std::string& _channel, sock_conn_shared_ptr _conn)
{
    subscriber_list_mtx.lock();
    auto it = channel_subscriber_list_map.find(_channel);

    if (it != channel_subscriber_list_map.end())
    {
       SubSet_t &_set = it->second;
       _set.erase(_conn);
       if (_set.size() == 0)
       {
          channel_subscriber_list_map.erase(it);
          //cout << "deleted the entire channel: " << _channel << endl;
       }
    }
    else
    {
       //cout << "nothing to delete" << endl;
    }
    subscriber_list_mtx.unlock();
}
