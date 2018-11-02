#include "pubsub_sock_conn.hpp"
#include "pubsub_thread_pool.hpp"
#include "pubsub_queue.hpp"

sock_conn::sock_conn(pubSubServerThread_t *_pThread, uint64_t _conId): socket_(_pThread->get_io_service()),
      pThread(_pThread),
      conId(_conId),
      outbuf(100),
      queue()
{
}

sock_conn::~sock_conn()
{
  //nothing to do
}

uint64_t sock_conn::getConId()
{
  return conId;
}

tcp::socket& sock_conn::socket()
{
  return socket_;
}

void sock_conn::start()
{
  boost::asio::async_read_until(socket_, buf, "\n",boost::bind(&sock_conn::handle_read, shared_from_this(), boost::asio::placeholders::error));
}

void sock_conn::handle_read(const boost::system::error_code& e)
{
   //cout << "handler called thread id:" << std::this_thread::get_id() << "conId: " << conId << endl;
   if (!e)
   {
     std::istream is(&buf);
     string _channel;
     switch (is.peek())
     {
        case '+': 
        {
            std::getline(is, _channel);
            //cout << _channel << endl;
            _channel.erase(0,1);
            //cout << _channel << endl;
            size_t  pos = _channel.find_first_of(" ");
            if (pos != std::string::npos)
            {
              cout << "white space error" << endl;
              break;
            }
            subscribedChannels.insert(_channel);
            pThread->getPubSubApp()->addSubscriber(_channel, shared_from_this());
         }
           break;
         case '-': 
         {
            std::getline(is, _channel);
            //cout << _channel << endl;
            _channel.erase(0,1);
            size_t  pos = _channel.find_first_of(" ");
            if (pos != std::string::npos)
            {
              cout << "white space error" << endl;
              break;
            }
            subscribedChannels.erase(_channel);
            pThread->getPubSubApp()->deleteSubscriber(_channel,shared_from_this());
         }
           break;
         case '!': 
         {
            //cout << " enter here" << endl;
            string _channel;
            string *msg = new string;
            std::getline(is, *msg);
            //cout << *msg <<endl;
            msg->erase(0,1);
            //cout << *msg <<endl;
            size_t  pos = msg->find_first_of(" ");
            if (pos != std::string::npos)
            {
              _channel = msg->substr(0, pos);
            }
            else
            {
              cout << "no white space error" << endl;
              break;
            }
            msg->erase (0, pos+1);
            msg_shared_ptr _ptr(msg);
            //cout << _channel << endl;
            //cout << *msg << endl;
            pThread->getPubSubApp()->publishChannelMsg(_channel, _ptr);
         }
           break;
         default:
            std::getline(is, _channel);
            cout << "unknown string: " << _channel << endl;
       }

       boost::asio::async_read_until(socket_, buf, "\n",boost::bind(&sock_conn::handle_read,
                                     shared_from_this(), boost::asio::placeholders::error));
     }
     else
     {
        //close the tcp connection
        if ((boost::asio::error::eof == e) ||
            (boost::asio::error::connection_reset == e))
        {
            cout << "socket closed for conId: " << conId << endl;
        }
        deleteAllChannels();
     }
}

void sock_conn::deleteAllChannels(void)

{
    auto it = subscribedChannels.begin();
    for (auto it = subscribedChannels.begin(); it != subscribedChannels.end(); it++)
    {
      cout << "erase channel: " << (*it) << " for conId: " << conId << endl;
      pThread->getPubSubApp()->deleteSubscriber(*it, shared_from_this()); 
    }
}

void sock_conn::sendMsg (const string & _channel, msg_shared_ptr _msg) 
{
    //cout << "publish message to a client with conId: "<< conId << " on channel:" << _channel << endl;

    int total_size = _msg->length() + _channel.length() + 4;
    //cout << "total size to write: " << total_size << endl;
    assert(total_size < 1024);
    if (total_size > 100)
      outbuf.resize(1024);
    
    char *data = outbuf.data();
    data[0] = '[';
    memcpy (data + 1, _channel.data(), _channel.length());
    data[_channel.length() +1] = ']';
    data[_channel.length() +2] = ' ';
    memcpy (data + _channel.length() + 3, _msg->data(), _msg->length());
    data[_msg->length() + _channel.length() + 3] = '\n';
    //cout << data << endl;

    boost::asio::async_write(socket_,                                           
                               boost::asio::buffer(data, total_size),       
                               boost::bind(&sock_conn::handle_write, this,boost::asio::placeholders::error));



    return;
}

void sock_conn::enque_msg (const string& _channel, msg_shared_ptr _msg)
{
    queue_msg msg;
    msg.channel = _channel;
    msg.msg = _msg;

    queue.enque_msg_protected(msg);
    pThread->get_io_service().post(boost::bind(&sock_conn::new_msg,
                                               shared_from_this()));
}

void sock_conn::new_msg(void)
{
   queue_msg msg;
   if (queue.deque_msg(msg))
   {
      sendMsg(msg.channel, msg.msg);
   }
}

void sock_conn::handle_write(const boost::system::error_code& e)
{

    if (!e)
    {
       queue_msg msg;
       if (queue.deque_msg(msg))
       {
         sendMsg(msg.channel, msg.msg);
       }
    }
    else
    {
      std::cout << "Error: in writing " << e.message() << endl;
    }
}
