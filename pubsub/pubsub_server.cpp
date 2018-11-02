#include "pubsub_server.hpp"
#include "pubsub_app.hpp"

pubsub_server::pubsub_server(boost::asio::io_service& _io_service, uint16_t _port, int32_t num_of_threads)
    : acceptor_(_io_service),
      pubSubApp(),
	  threadPool(num_of_threads,&pubSubApp),
	  conIdGenerator(1)
{
    boost::asio::ip::tcp::endpoint endpoint(boost::asio::ip::tcp::v4(), _port);
    acceptor_.open(endpoint.protocol());
    acceptor_.set_option(boost::asio::ip::tcp::acceptor::reuse_address(true));
    acceptor_.bind(endpoint);
    acceptor_.listen();
    start_accept();
}

pubsub_server::~pubsub_server() {}

void pubsub_server::start_accept()
{
    sock_conn_shared_ptr new_connection(new
                                        sock_conn(threadPool.getNextThreadToUse(), conIdGenerator++),
                                        delete_sock_conn());

    //save this new connection
    newCon = new_connection;


    acceptor_.async_accept(new_connection->socket(),
        boost::bind(&pubsub_server::handle_accept, this, new_connection,
          boost::asio::placeholders::error));
}

void pubsub_server::threadpool_run()
{
    threadPool.run();
}

void pubsub_server::threadpool_join()
{
    threadPool.join();
}

void pubsub_server::handle_accept(sock_conn_shared_ptr new_connection,
      const boost::system::error_code& error)
{
    if (!error)
    {
      new_connection->start();
    }

    start_accept();
}
