#include "pubsub_thread_pool.hpp"


pubSubServerThread_t::pubSubServerThread_t(pubsubApp_t* const _pubSubApp):
    io_service(),
    io_work(io_service),
    pPubSubApp(_pubSubApp)
{
      //thandle = new std:thread (boost::bind(&pubSubServerThread_t::entryFunction, this));
}
pubSubServerThread_t::~pubSubServerThread_t()
{
     delete thandle;
}
   
void pubSubServerThread_t::handleConEntryFunc(void)
{
    cout << "thread created with ID: " << thandle->get_id() << endl;
    io_service.run();
}

std::thread* pubSubServerThread_t::getThread(void)
{
    return thandle;
}

boost::asio::io_service& pubSubServerThread_t::get_io_service(void)
{
     return io_service;
}

void pubSubServerThread_t::run()
{
      thandle = new std::thread (boost::bind(&pubSubServerThread_t::handleConEntryFunc, this));
      return;
}

void pubSubServerThread_t::join()
{
     thandle->join();
     return;
}

pubsubApp_t* pubSubServerThread_t::getPubSubApp (void)
{
	  return pPubSubApp;
}


pubSubServerThreadPool_t::pubSubServerThreadPool_t(int32_t _size, pubsubApp_t *const _pPubSubApp)
     : next_thread_to_use(0)
{
	     if (_size == 0)
         {
            cerr << "create at least one thread"; 
            exit(0);
         }

         for (size_t i = 0; i < _size; i++)
         {
            
            pubSubServerThread_t *pThread = new pubSubServerThread_t(_pPubSubApp);

            conThreads.push_back (pThread);
         }
}

void pubSubServerThreadPool_t::run(void)
{
         for (int i = 0; i < conThreads.size(); i++)
         {
            conThreads[i]->run(); 
         }
}
void pubSubServerThreadPool_t::join(void)
{
         for (int i = 0; i < conThreads.size(); i++)
         {
            conThreads[i]->join(); 
         }
}

pubSubServerThread_t* pubSubServerThreadPool_t::getNextThreadToUse()
{
         pubSubServerThread_t *pThread = conThreads[next_thread_to_use++];
         next_thread_to_use = next_thread_to_use % conThreads.size();
         return pThread;
}
