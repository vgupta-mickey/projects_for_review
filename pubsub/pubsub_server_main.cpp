#include "pubsub_server.hpp"

int main(int32_t argc, char* argv[])
{
    //this will be used for listening the connections
    boost::asio::io_service io_service;

    if (argc != 4)
    {
      cerr << "Usage: ./pubsub_server <tcpproto> <port>\n";
      cerr << "  For IPv4:\n";
      
      cerr << "   ./pubsub_server ipv4 port loadtype.\n";
      cerr << "Example:  ./pubsub_server ipv4 2500 low.\n";
      cerr << "Example:  ./pubsub_server ipv4 2500 med.\n";
      cerr << "Example:  ./pubsub_server ipv4 2500 high.\n";
      return 1;
    }

    string   protoType = argv[1];
    uint16_t port = atoi(argv[2]);
    string   loadType = argv[3];
    int32_t  numOfThreads = 1;

    cout << "protoType: " << protoType << "  port: " << port << " loadType: " << loadType << endl;
    if (loadType == "low")
      numOfThreads = 1;
    else if (loadType == "med")
      numOfThreads = 4;
    else if (loadType == "high")
      numOfThreads  = 8;

    if(protoType == "ipv4")
    {
      //create listen socket amd start listening
      //create threadpool
      //The idea is that - the main thread will listen new connections using its
      //own io_service and will not be blocked by anything on data sockets.
      //Each thread in the thread pool will have its own io_service object and it
      //will be responsible to handle all data sockets in async mode handled by
      //that specific thread.
      pubsub_server _server(io_service,port,numOfThreads);
      //start threads - create threads and io_service.run() of each thread starts 
      //as soon as a new connection is accepted, one of the thread in the
      //threadpool will start looking for messages on that socket
      _server.threadpool_run();
      // start main io_service to start accepting the connections
      io_service.run();
      //exit only after all threads are joined together
      _server.threadpool_join();
    }
    else
    {
      cout << "currently ipv6 is not supported" << endl;
    }

    return 0;
}
