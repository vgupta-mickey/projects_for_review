#ifndef __SERVER_THREAD_POOL_HPP__
#define __SERVER_THREAD_POOL_HPP__
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
#include "pubsub_app.hpp"

using namespace std;
using boost::asio::ip::tcp;

//Thread specific data
//io_service to manage data sockets handled by this thread

class pubSubServerThread_t
{
public:
   pubSubServerThread_t(pubsubApp_t *const _pubSubApp);
   ~pubSubServerThread_t();
   void handleConEntryFunc(void);
   std::thread* getThread(void);
   boost::asio::io_service& get_io_service(void);
   void run();
   void join();
   pubsubApp_t* getPubSubApp (void);
private:

   boost::asio::io_service io_service;
   boost::asio::io_service::work io_work;
   std::thread  *thandle;
   pubsubApp_t  *pPubSubApp;
};



//Threadpool
//connections are accepted in round robin fashion
//all the threads gets equal peice of connections

class pubSubServerThreadPool_t
{
public:
   pubSubServerThread_t* getNextThreadToUse();
   pubSubServerThreadPool_t(int32_t _size,pubsubApp_t *const pPubSubApp);
   void run(void);
   void join(void);
private:
   std::vector<pubSubServerThread_t*> conThreads;
   //The next io_service to use for a connection.
   int  next_thread_to_use;
};
#endif
