#!/bin/bash
#for light load
#./pubsub_server ipv4 2500 low &
#for medium load 
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/vinod/test_dir/mathtest/boost_dir/lib
./pubsub_server ipv4 2500 med &
#for high load 
#./pubsub_server ipv4 2500 high &

