# Name: Miguel Angel Bruni Montero
# OSU Email: brunimom@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6. Hash Map Implementation 
# Due Date: March 17th 2023
# Description: Exercise related to implementing a Hash Map
# and the methods needed to work with it using open addresing
# with quadratic probing for collision resolution.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        '''
        Updates the key/value pair in the hash map. If the key is
        already in the hash map, updates its value. If not, it adds
        a new key/value pair.

        :param key:     key to be inserted or updated.
        :param value:   value to be associated with the key.
        '''
        # Resizes the hash map if the table load is 0.5 or higher.
        if self.table_load() >= 0.5: 
            new_capacity = self._next_prime(self._capacity * 2)
            self.resize_table(new_capacity)
        
        # Calculates initial index using the hash function.
        hash = self._hash_function(key)
        index = hash % self._capacity
        new_index = index
        quadratic_factor = 1

        data_at_index = self._buckets.get_at_index(index)

        # Iterates though the buckets in the hash map looking for 
        # an empty bucket. If initial bucket is not empty, uses 
        # quadratic probing for finding a new index.
        while data_at_index is not None:
            # If key is already in the hash map, updates its value.
            if data_at_index.key == key and data_at_index.is_tombstone == False:
                data_at_index.value = value
                return
            # If key is in the hash map but it is a tombstone, 
            # updates value and size and changes the flag to False.
            elif data_at_index.key == key and data_at_index.is_tombstone == True:
                data_at_index.value = value
                data_at_index.is_tombstone = False
                self._size += 1
                return
            # Uses quadratic probing for finding next empty bucket.
            else:
                new_index = (index + quadratic_factor**2) % self._capacity
                quadratic_factor += 1
                data_at_index = self._buckets.get_at_index(new_index)

        # Inserts new hash entry in the empty bucket and updates
        # the hash map size.
        self._buckets.set_at_index(new_index, HashEntry(key, value))
        self._size += 1


    def table_load(self) -> float:
        '''
        Returns the load factor of the hash map.

        :return:    a float representing the load factor. 
        '''
        load_factor = float(self._size / self._capacity)
        return load_factor

    def empty_buckets(self) -> int:
        '''
        Returns the number of empty buckets in the hash table.

        :return:    an integer representing number of empty buckets.
        '''
        count = 0

        # Looks for buckets that are empty or have a tombstone.
        for number in range(self._buckets.length()):
            if self._buckets.get_at_index(number) == None or self._buckets.get_at_index(number).is_tombstone == True:
                count += 1
        
        return count

    def resize_table(self, new_capacity: int) -> None:
        '''
        Changes the capacity of the internal hash table. Key/value
        pairs are maintained but hash table links are rehashed.

        :param new_capacity:    new capacity for the hash map.
        '''
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initializes a variable to store original buckets, changes
        # the capacity to the new one and clears the hash map.            
        temp_buckets = self._buckets
        self._capacity = new_capacity
        self.clear()

        # Iterates through the buckets in the old hash map and puts
        # them in the new one (this rehashes all hash table links).
        for number in range(temp_buckets.length()):
            if temp_buckets.get_at_index(number) and temp_buckets.get_at_index(number).is_tombstone == False:
                self.put(temp_buckets.get_at_index(number).key, temp_buckets.get_at_index(number).value)

    def get(self, key: str) -> object:
        '''
        Returns the value associated with the key if it exists
        on the hash map.

        :param key: key for the value we are searching for.
        '''
        # Calculates the initial index for the key we are looking 
        # for using the hash function.
        hash = self._hash_function(key)
        index = hash % self._capacity
        new_index = index
        quadratic_factor = 1

        data_at_index = self._buckets.get_at_index(index)

        # Looks for the key in the hash map, if found returns the 
        # value, else None.
        while data_at_index is not None:
            # If the key is found and it is not a tombstone, returns
            # the value.
            if data_at_index.key == key and data_at_index.is_tombstone == False:
                return data_at_index.value
            # If the key is found and it is a tombstone, returns None.
            elif data_at_index.key == key and data_at_index.is_tombstone == True:
                return None
            # If not found, continues looking using the quadratic
            # probing until it founds an empty bucket.
            else:
                new_index = (index + quadratic_factor**2) % self._capacity
                quadratic_factor += 1
                data_at_index = self._buckets.get_at_index(new_index)

        # If the while loop arrives at an empty bucket, returns None.
        return None

    def contains_key(self, key: str) -> bool:
        '''
        Looks for the presence of the key in the hash map.

        :param key: key to look for in the hash map.

        :return:    True if the key is found
                    False otherwise.
        '''
        # Hash map is empty.
        if self._size == 0:
            return False

        # Calculates the initial index for the key we are looking 
        # for using the hash function.
        hash = self._hash_function(key)
        index = hash % self._capacity
        new_index = index
        quadratic_factor = 1

        data_at_index = self._buckets.get_at_index(index)

        # Looks for the key in the hash map.
        while data_at_index is not None:
            # If the key is found and it is not a tombstone, returns
            # True.
            if data_at_index.key == key and data_at_index.is_tombstone == False:
                return True
            # If the key is found and it is a tombstone, returns False.
            elif data_at_index.key == key and data_at_index.is_tombstone == True:
                return False
            # If not found, continues looking using the quadratic
            # probing until it founds an empty bucket.
            else:
                new_index = (index + quadratic_factor**2) % self._capacity
                quadratic_factor += 1
                data_at_index = self._buckets.get_at_index(new_index)

        return False

    def remove(self, key: str) -> None:
        '''
        Removes the given key and its value from the hash map.

        :param key: key to remove from the hash map.
        '''
        # Calculates the initial index for the key we are looking 
        # for using the hash function.
        hash = self._hash_function(key)
        index = hash % self._capacity
        new_index = index
        quadratic_factor = 1

        data_at_index = self._buckets.get_at_index(index)

        # Looks for the key in the hash map using the quadratic
        # probing.
        while data_at_index and data_at_index.key != key:
            new_index = (index + quadratic_factor**2) % self._capacity
            quadratic_factor += 1
            data_at_index = self._buckets.get_at_index(new_index)

        # If the bucket with the key is found, sets the tombstone
        # value as True and updates size.
        if data_at_index and data_at_index.is_tombstone == False:
            data_at_index.is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        '''
        Clears the contents of the hash map while maintaining 
        the current capacity.
        '''
        # Creates a new empty array with as many buckets as capacity.
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        '''
        Returns an array containing tuples of all key/value pairs
        stored in the hash map.

        :return:    a dynamic array with tuples of key/value pairs.
        '''
        # Initializes the new array and the variable to keep track
        # of the position in it.
        array = DynamicArray()
        array_index = 0

        # Iterates through the buckets of the hash map. 
        for number in range(self._buckets.length()):
            data_at_index = self._buckets.get_at_index(number)
            # If there is an entry in the bucket and does not have
            # a tombstone, adds the key/value pair to our array.      
            if data_at_index and data_at_index.is_tombstone == False:
                array.append((data_at_index.key, data_at_index.value))
                array_index += 1
        
        return array

    def __iter__(self):
        '''
        Returns the iterator.
        '''
        self._index = 0

        return self

    def __next__(self):
        '''
        Return next hash entry and advances the iterator.
        '''
        try:
            hash_entry = self._buckets.get_at_index(self._index)
            while hash_entry is None or hash_entry.is_tombstone == True:
                self._index += 1
                hash_entry = self._buckets.get_at_index(self._index)

            self._index += 1
            return hash_entry
            
        except DynamicArrayException:
            raise StopIteration
        

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
