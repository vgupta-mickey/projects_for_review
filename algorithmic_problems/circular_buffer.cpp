#include <iostream>
#include <mutex>
#include <assert.h>

using namespace std;

class circular_buffer
{

private:

	int head;
	int tail;
	int *data;
	int capacity;
	int totElements;
    mutex read_write_lock;

public:

	circular_buffer(int _capacity):
		capacity(_capacity+1),
		head(0),
		tail(0),
        totElements(0)
	{
	  data = new int[capacity];
	  assert(data);
	}

	~circular_buffer()
	{
	  delete [] data;
	}

	int addElement(int element)
	{
	  read_write_lock.lock();
	  if (is_buffer_full())
	  {
		cout << "buffer full" << endl;

		tail = (tail +1) % capacity;
		data[head] = element; 
		head = (head +1) % capacity;
        cout << "head = " << head << "tail = " << tail << endl;
	  }
      else
      {
		data[head] = element; 
		head = (head +1) % capacity;
	    totElements += 1;
      }
	  read_write_lock.unlock();
	}

	int removeElement (int &_data)
	{
	  read_write_lock.lock();
      cout << "head" << head << "tail" << tail << endl;
	  if (is_buffer_empty())
	  {
		return false;
	  }
      else
	  {
		_data = data[tail];
		tail = (tail +1) % capacity;
	    totElements -= 1;
		assert(totElements >= 0);
	    return true;
	  }
	  read_write_lock.unlock();

	}
	bool is_buffer_full()
	{
	  return ((head + 1) % capacity == tail);
	}

	bool is_buffer_empty()
	{
	  return head == tail;
	}
	int totalElements()
	{
	  return totElements;
	}
};


int main()
{
	circular_buffer buf(3);

	cout << buf.totalElements() << endl;
	buf.addElement(1);
	cout << buf.totalElements() << endl;
	buf.addElement(2);
	cout << buf.totalElements() << endl;
	buf.addElement(3);
	cout << buf.totalElements() << endl;
	buf.addElement(4);
	cout << buf.totalElements() << endl;
	int _data;
	buf.removeElement(_data);
	cout << _data << endl;
	cout << buf.totalElements() << endl;
	buf.removeElement(_data);
	cout << _data << endl;
	cout << buf.totalElements() << endl;
	buf.removeElement(_data);
	cout << _data << endl;
	cout << buf.totalElements() << endl;
	buf.removeElement(_data);
	cout << _data << endl;
	cout << buf.totalElements() << endl;
}
