#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <queue>
#include <unordered_map>
#include <assert.h>

using namespace std;

struct heap_node 
{
    int rank;
    string word;
};
class heap_comparator
{
public:
    bool operator() (const heap_node& n1, const heap_node& n2) const
    {
       return n1.rank < n2.rank;
    }
};
class compare_node
{
public:
    bool operator() (const heap_node& n1, const heap_node& n2) const
    {
       return n1.rank < n2.rank;
    }
};

class node {

  //priority_queue<heap_node, vector<heap_node>, heap_comparator> ranked_autofil_words;
  set<heap_node, compare_node> ranked_autofil_words;
  bool  marker;
  int  data;
  unordered_map<char, node*> childrens;

public:

  node():
  marker(false),
  data(0)
  {

  }

  node* addChildren(const char c, const int d = 0)
  {
     node* new_node = NULL;
     auto it = childrens.find(c);
     if (it == childrens.end())
     {
        new_node = new node;
        new_node->data = d;
        childrens.insert({c, new_node});
     }
     else
     {
       new_node = it->second;
     }
     return new_node;
  }
  node* findChildren(const char c)
  {
     auto it = childrens.find(c);
     if (it == childrens.end())
     {
       return NULL;
     }
     return it->second;
  }
  int deleteChildren(const char c)
  {
     childrens.erase(c);
     return true;
  }
  int totalChildren()
  {
     return childrens.size();
  }

  int updateData(int d)
  {
    data = d;
    return true;
  }

  void setMarker(bool f)
  {
    marker = f;
  }

  void addRank(string word, const int rank)
  {
    if (ranked_autofil_words.size() < 3)
    ranked_autofil_words.insert({rank, word});
    else
    {
      auto it = ranked_autofil_words.begin();
      if ((*it).rank < data)
      {
        ranked_autofil_words.erase(it);
        ranked_autofil_words.insert({rank, word});
      }
    }
  }

  void deleteRank(string word, const int rank)
  {
    ranked_autofil_words.erase({rank, word});
  }
  friend class trie;
};

class trie
{
   node *root;

public:

   trie() 
   {
      root = new node;
   }

   int insertWord(const string &word, const int rank)
   {
      node *tmp = root;
      assert(tmp);

      for (int i =0; i < word.length(); i++)
      {
         tmp = tmp->addChildren(word.at(i));
         tmp->addRank(word, rank);
      }
      tmp->setMarker(true);
      tmp->data = 0; //just put zero - it is not imporant for the algorithm
      return true;
   }
   int deleteWord(const string &word, int rank)
   {
      node *tmp = root;
      assert(tmp);
      node * parent  = tmp;
      char tmp_char;
      for (int i =0; i < word.length(); i++)
      {
         parent = tmp;
         tmp_char = word.at(i);

         tmp = tmp->findChildren(word.at(i));
         if (tmp == NULL)
           return false;
         else
         {
           tmp->deleteRank(word, rank);
         }
      }
      if(tmp->totalChildren() == 0)
      {
        parent->deleteChildren(tmp_char);
        delete tmp;
      }
      else
      {
        tmp->setMarker(false);
      }
      return true;
   }

   int searchWord(const string &word)
   {
      node *tmp = root;
      assert(tmp);

      for (int i =0; i < word.length(); i++)
      {
         tmp = tmp->findChildren(word.at(i));
         if (tmp == NULL)
           return false;
      }
      if (tmp->marker == true)
      return true;
      else
      return false;
   }
   int giveBest3RankedWords(const string &word, vector<string>&
                            autoFillWords)
   {
      node *tmp = root;
      assert(tmp);

      for (int i =0; i < word.length(); i++)
      {
         tmp = tmp->findChildren(word.at(i));
         if (tmp == NULL)
           return false;
      }

      for (const heap_node& n: tmp->ranked_autofil_words)
      {
        autoFillWords.push_back(n.word);
      }

      return true;
   }
};

int main()

{

    trie _trie;
    _trie.insertWord("banana", 50);
    _trie.insertWord("banglore", 30);
    _trie.insertWord("ban", 23);
    _trie.insertWord("banner", 1);
    _trie.insertWord("banny", 2);
    _trie.insertWord("bang", 3);
    _trie.insertWord("banned", 4);

    cout << _trie.searchWord("vinod") << endl;

    _trie.deleteWord("banned", 4);
    cout << "result: " << _trie.searchWord("banana") << endl;
    cout << "result: " << _trie.searchWord("na") << endl;
    cout <<  "result: " <<_trie.searchWord("ana") << endl;
    cout << "result: " << _trie.searchWord("") << endl;
    _trie.deleteWord("banana", 50);
    cout << "result: " << _trie.searchWord("banana") << endl;
    cout <<  "result: " <<_trie.searchWord("bananae") << endl;

    vector<string> _ranklist;
    _trie.giveBest3RankedWords("ban", _ranklist);

    for (auto it = _ranklist.rbegin(); it != _ranklist.rend(); it++)
    {
      cout << "word: " << (*it) << endl;
    }
}

