#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <utility>
#include <boost/algorithm/string.hpp>
#include <unordered_set>
#include <vector>

/*
 *
 *
 * Insert all suffixes of each word, insert index number at each node 
 * example:   "vinod is great"
 *
 * insert v index 0
 *        i index 1
 *        n index 2
 *        o index 3
 *        d index 4
 *
 *        another suffis: "inod"
 *
 *        i index 1
 *        n index 2
 *        o index 3 
 *        d index 4
 *
 *        similarly 
 *        "nod" and "od" and "d"
 *
 *        Insert "is"
 *        i index 5
 *        s index 6
 *
 *        Insert "s"
 *        s index 6
 *
 *
 *  when you search for pharase "vinod is great"
 *  vinod search will return the list of indexes where vinod ends. in this case:
 *  4
 *  is search will return the list of indexs where is ends. in this case:
 *  6
 *
 *  great will return indexes where great ends. in this case:
 *  11
 *
 *  now when you find vinod at index 4, you must find is and great at index 6
 *  and 11 to match the full pharase.
 */
 
using namespace std;

class remove_extra_space
{
public:
    static string& removeDuplicateSpaces (string & str)
    {
       auto lambda_func = [](char lhs, char rhs){ return (lhs == rhs) && (lhs == ' '); };
       auto new_end = unique(str.begin(), str.end(), lambda_func);
       str.erase(new_end, str.end());
       return str;
    }
};

class Node
{
    unordered_set<int> indexes;
    Node* children[26];
public:
    Node():
        children{0}
    {
    }

    int getIndex (char _c)
    {

      return _c - 'a';
    }

    Node* getChildren (char _c)
    {
      if (_c >= 'a' || _c <= 'z')
      {
        int index = getIndex(_c);
        return children[index];
      }
      else
        return 0;
    }
    int setChildren (char _c)
    {
      if (_c >= 'a' || _c <= 'z')
      {
        int index = getIndex(_c);
        children[index] = new Node;
        return 1;
      }
      else
        return 0;
    }
    int getIndex(int index)
    {
      auto it = indexes.find(index);
      return *it;
    }
    bool IsIndexFoundgetIndex(int index)
    {
      auto it = indexes.find(index);
      if (it == indexes.end())
        return false;
      else
        return true;
    }

    unordered_set<int>&  getSet()
    {
      
      return indexes;
    }
    void addIndex (int  _index)
    {
      cout << "add index " << _index << endl;
      indexes.insert(_index); 
    }
};

class trie
{
    Node *root;

public:

    trie()
    {
      root = new Node;
    }
    ~trie()
    {
    }
    Node *  getNode()
    {
      Node * n = new Node;
      return  n;
    }


    int insert_word(const string& word, const int data)
    {
      cout << "insert " << word << " at " << data << endl;
      if (root == NULL)
        return 0;
      Node *tmp = root;
      for (int i =0; i < word.length(); i++)
      {
        Node *child = tmp->getChildren(word[i]);
        if (child == NULL)
        {
          tmp->setChildren(word[i]);
          //cout << "insert one node" << endl;
        }
        tmp = tmp->getChildren(word[i]);
        tmp->addIndex(data + i);
      }
      return true;
    }
    int search_word(string &word, unordered_set<int>& _set)
    {
      if (root == NULL)
        return 0;
      Node *tmp = root;

      for (int i =0; i < word.length(); i++)
      {
        Node *child = tmp->getChildren(word[i]);
        if (child == NULL)
        {
          return 0;
        }
        tmp = child;
      }
      _set = tmp->getSet();
      return true;
    }
};

int main()
{

    string str = "vinod is great tom is good vinod tom dan vinod is great vinod is doing hardword";

    str = remove_extra_space::removeDuplicateSpaces(str);

    cout << str << endl;

    vector<string> list_of_words;

 
    boost::split(list_of_words, str, [](char c){return c == ' ';});


    trie dict; 

    int index = 0;
    for (auto &s: list_of_words)
    {
        cout << s << endl;
        int i = 0;
        for (i = 0; i < s.length(); i++)
          dict.insert_word(s.substr(i), index + i);
        index += i;
    }

    string pharase = "nod is great";
    vector<string> pharase_words;

 
    boost::split(pharase_words, pharase, [](char c){return c == ' ';});


    vector<unordered_set<int>> indexes_list(pharase_words.size());

    index = 0;
    for (auto &s: pharase_words)
    {
        cout << s << endl;
        dict.search_word(s, indexes_list[index]);
        index++;
    }

   int occurance = 0;
   auto _set1 = indexes_list[0];

   for (auto index: _set1)
   {
        cout << index << endl;


        int found = true;
        int search_index = index;
        for (int i = 1; i < indexes_list.size(); i++)
        {
          cout << "next pharase word: " << pharase_words[i] << endl;
          cout << "next pharase word: " << pharase_words[i].length() << endl;
          search_index = search_index + pharase_words[i].length();
          cout << "search_index " << search_index << endl;
          if  (indexes_list[i].find(search_index) != indexes_list[i].end())
          {
            cout << "found index " << search_index << endl;
            continue;
          }
          else
          {
            found = false;
            break;
          }
        }

        if (found == true)
        {
           occurance++;
        }
    }

    cout << "occurance = " << occurance <<endl;
}
