import sys

# Cache is a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library (e.g., collections.OrderedDict).
#       Implement the data structure yourself.


class Cache:
  # Initializes the cache.
  # |n|: The size of the cache.
    def __init__(self, n):
        self.hash_table = {}
        self.n = n
        # Top is most recently.
        self.top_url = None
        # bottom is most old.
        self.bottom_url = None
    

  # Access a page and update the cache so that it stores the most
  # recently accessed N pages. This needs to be done with mostly O(1).
  # |url|: The accessed URL
  # |contents|: The contents of the URL
    def access_page(self, url, contents):
        if url in self.hash_table:
            self.hit_cache(url, contents)
        else:
            self.non_hit_cache(url, contents)

    def hit_cache(self, url, contents):
        if self.top_url == url:
            # When the top URL and the URL are the same, No change required
            pass
        else:
            self.remove_from_list(url, contents)
            self.insert_top(url, contents)


    def non_hit_cache(self, url, contents):
        if self.hash_table == {}:
            # Nothing in the cache
            self.insert_top(url, contents)
        elif len(self.hash_table) < self.n:
            # When the cache capacity is not exceeded
            self.insert_top(url, contents)
        else:
            # When the cache is full
            self.insert_top(url, contents)
            self.delete_bottom()


    def remove_from_list(self, url, contents):
        if self.hash_table[url] == None:
            # Exception handling
            pass
        elif url == self.bottom_url:
            self.delete_bottom()
        else:
            # Remove the middle node
            before_overwriting_prev_url = self.hash_table[url]["prev_URL"]
            before_overwriting_next_url = self.hash_table[url]["next_URL"]
            self.hash_table[before_overwriting_prev_url]["next_URL"] = before_overwriting_next_url
            self.hash_table[before_overwriting_next_url]["prev_URL"] = before_overwriting_prev_url


    def insert_top(self, url, contents):
        if self.top_url == url:
            # exception handling
            pass
        else:
            self.hash_table[url] = {}
            self.hash_table[url]["Web_page"] = contents
            self.hash_table[url]["prev_URL"] = self.top_url
            self.hash_table[url]["next_URL"] = None
            if self.top_url == None:
                # Change retained variables
                self.top_url = url
                self.bottom_url = url
            else:
                # Change list structure
                self.hash_table[self.top_url]["next_URL"] = url
                # Change retained variables
                self.top_url = url



    def delete_bottom(self):
        # Change list structure
        before_overwriting_bottom_url = self.bottom_url
        self.bottom_url = self.hash_table[before_overwriting_bottom_url]["next_URL"]
        self.hash_table[self.bottom_url]["prev_URL"] = None
        # Delete from hash_table
        self.hash_table[before_overwriting_bottom_url] = None


  # Return the URLs stored in the cache. The URLs are ordered
  # in the order in which the URLs are mostly recently accessed.
    def get_pages(self):
        result = []
        top_url = self.top_url
        if top_url == None:
            # Nothing in the cache
            return result
        else:
            result.append(top_url)
        now_url = self.hash_table[top_url]["prev_URL"]
        # Store in list order
        while now_url != None:
            result.append(now_url)
            now_url = self.hash_table[now_url]["prev_URL"]
        return result



# Does your code pass all test cases? :)
def cache_test():
  # Set the size of the cache to 4.
  cache = Cache(4)
  # Initially, no page is cached.
  equal(cache.get_pages(), [])
  # Access "a.com".
  cache.access_page("a.com", "AAA")
  # "a.com" is cached.
  equal(cache.get_pages(), ["a.com"])
  # Access "b.com".
  cache.access_page("b.com", "BBB")
  # The cache is updated to:
  #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["b.com", "a.com"])
  # Access "c.com".
  cache.access_page("c.com", "CCC")
  # The cache is updated to:
  #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
  # Access "d.com".
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "d.com" again.
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "a.com" again.
  cache.access_page("a.com", "AAA")
  # The cache is updated to:
  #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
  equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
  cache.access_page("c.com", "CCC")
  equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  # Access "e.com".
  cache.access_page("e.com", "EEE")
  # The cache is full, so we need to remove the least recently accessed page "b.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
  equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
  # Access "f.com".
  cache.access_page("f.com", "FFF")
  # The cache is full, so we need to remove the least recently accessed page "c.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
  print("OK!")

# A helper function to check if the contents of the two lists is the same.
def equal(list1, list2):
  assert(list1 == list2)

if __name__ == "__main__":
  cache_test()

