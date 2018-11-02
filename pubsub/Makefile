OBJS=pubsub_server_main.o pubsub_server.o pubsub_thread_pool.o \
                pubsub_app.o pubsub_sock_conn.o pubsub_queue.o
LIBS= -lboost_system -lpthread
LPATH= -L/home/vinod/test_dir/mathtest/boost_dir/lib
IPATH= -I/home/vinod/test_dir/mathtest/boost_dir/include
pubsub_server : $(OBJS)
	g++ -o pubsub_server $(OBJS) $(LPATH) $(LIBS)
DEP=pubsub_server.hpp pubsub_thread_pool.hpp pubsub_app.hpp pubsub_sock_conn.hpp pubsub_queue.hpp

pubsub_server_main.o : pubsub_server_main.cpp $(DEP)
	g++ -g -std=c++11 -c pubsub_server_main.cpp $(IPATH)
pubsub_server.o : pubsub_server.cpp $(DEP) 
	g++ -c -g -std=c++11 pubsub_server.cpp $(IPATH)
pubsub_app.o : pubsub_app.cpp $(DEP) 
	g++ -c -g -std=c++11 pubsub_app.cpp $(IPATH)
pubsub_thread_pool.o : pubsub_thread_pool.cpp $(DEP) 
	g++ -c -g -std=c++11  pubsub_thread_pool.cpp $(IPATH)
pubsub_sock_conn.o : pubsub_sock_conn.cpp $(DEP) 
	g++ -c -g -std=c++11 pubsub_sock_conn.cpp $(IPATH)
pubsub_queue.o : pubsub_queue.cpp $(DEP) 
	g++ -c -g -std=c++11 pubsub_queue.cpp $(IPATH)
clean :
	rm pubsub_server pubsub_server_main.o pubsub_server.o pubsub_thread_pool.o \
           pubsub_app.o pubsub_sock_conn.o pubsub_queue.o
