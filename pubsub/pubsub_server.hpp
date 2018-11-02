#ifndef __PUBSUB_SERVER_HPP__
#define __PUBSUB_SERVER_HPP__
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
#include "pubsub_thread_pool.hpp"

using namespace std;

//server class responsible for opening listening socket and maintaing
//thread-pool to use for multiple clients data connections.
// When the server accept the new connection  a sock_conn obj is created who
// will be responsible for managing specific data connection with a client
// it is a shared_ptr because the obj will be alive as long as it is being used.
// If some reason socket is closed and not more events are waiting, the
// connection object will be removed automatically
//each connection is given a ID by server when it accepts a connection.

class pubsub_server
{
public:
  pubsub_server(boost::asio::io_service& _io_service, uint16_t _port, int32_t num_of_threads);
  ~pubsub_server();
  pubsubApp_t & getPubSubAppObj(void);
  void threadpool_run();
  void threadpool_join();

private:
  void start_accept();
  void handle_accept(sock_conn_shared_ptr new_connection, const boost::system::error_code& error);
  sock_conn_shared_ptr newCon;
  tcp::acceptor acceptor_;
  pubsubApp_t pubSubApp;
  pubSubServerThreadPool_t threadPool;
  uint64_t conIdGenerator;
};
#endif
