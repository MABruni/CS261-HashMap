# Name: Miguel Angel Bruni Montero
# OSU Email: brunimom@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6. Hash Map Implementation 
# Due Date: March 17th 2023
# Description: Exercise related to implementing a Hash Map
# and the methods needed to work with it using separate
# chaining for collision resolution.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        # Resizes the hash map if the table load is 1 or higher.
        if self.table_load() >= 1:
            new_capacity = self._capacity * 2
            if self._is_prime(new_capacity):
                self.resize_table(new_capacity)
            else:
                new_capacity = self._next_prime(new_capacity)
                self.resize_table(new_capacity)
        
        # Calculates new index using the hash function and capacity
        # of the hash map.
        hash = self._hash_function(key)
        index = hash % self._capacity

        sll_at_index = self._buckets.get_at_index(index)

        # If the key is in the hash map, updates the value, 
        # otherwise inserts the new key/value pair.
        if sll_at_index and sll_at_index.contains(key):
            sll_at_index.contains(key).value = value
        else:
            sll_at_index.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        '''
        Returns the number of empty buckets in the hash table.

        :return:    an integer representing number of empty buckets.
        '''
        count = 0

        # Looks for buckets that have an empty linked list.
        for number in range(self._buckets.length()):
            if self._buckets.get_at_index(number) and self._buckets.get_at_index(number).length() == 0:
                count += 1
        
        return count

    def table_load(self) -> float:
        '''
        Returns the load factor of the hash map.

        :return:    a float representing the load factor. 
        '''
        load_factor = float(self._size / self._capacity)
        return load_factor

    def clear(self) -> None:
        '''
        Clears the contents of the hash map while maintaining 
        the current capacity.
        '''
        # Creates a new empty array and populates it with empty
        # linked lists.
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        '''
        Changes the capacity of the internal hash table. Key/value
        pairs are maintained but hash table links are rehashed.

        :param new_capacity:    new capacity for the hash map.
        '''
        if new_capacity < 1:
            return
        
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initializes a variable to store original buckets, changes
        # the capacity to the new one and clears the hash map.            
        temp_buckets = self._buckets
        self._capacity = new_capacity
        self.clear()

        # Iterates through the buckets in the old hash map and puts
        # them back (this rehashes all hash table links with the new
        # capacity).
        for number in range(temp_buckets.length()):
            if temp_buckets.get_at_index(number) and temp_buckets.get_at_index(number).length() > 0:
                for node in temp_buckets.get_at_index(number):
                    self.put(node.key, node.value)
        

    def get(self, key: str):
        '''
        Returns the value associated with the key if it exists
        on the hash map.

        :param key: key for the value we are searching for.
        '''
        # Calculates the index for the key we are looking for.
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Looks for the key in the linked list at our index, if
        # found returns the value, else None.
        if self._buckets.get_at_index(index) and self._buckets.get_at_index(index).contains(key):
            return self._buckets.get_at_index(index).contains(key).value
        else:
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
        
        # Calculates the index for the key we are looking for.
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Looks for the key at the index, if found returns True
        # else, False.
        if self._buckets.get_at_index(index) and self._buckets.get_at_index(index).contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        '''
        Removes the given key and its value from the hash map.

        :param key: key to remove from the hash map.
        '''
        # Calculates the index for the key we want to delete.
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Removes the node from the linked list and updates the size.
        if self._buckets.get_at_index(index) and self._buckets.get_at_index(index).contains(key):
            self._buckets.get_at_index(index).remove(key)
            self._size -= 1

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

        # Iterates through the buckets of the hash map, if the
        # linked list in the bucket contains key/value pairs, 
        # adds them to our array.
        for number in range(self._buckets.length()):
            sll_at_index = self._buckets.get_at_index(number)
            if sll_at_index and sll_at_index.length() > 0:
                for node in sll_at_index:
                    array.append((node.key, node.value))
                    array_index += 1
        
        return array

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    '''
    Finds the mode of a dynamic array using a hash map.

    :param da:  dynamic array we want to find the mode of.

    :return:    a tuple containing (a dynamic array that stores 
    all the mode values, an integer showing the frequency).
    '''
    # Initializes a new hash map.
    map = HashMap()

    # Iterates through values in the array passed as an argument.
    for number in range(da.length()):
        key = da.get_at_index(number)

        # Looks for the array values in the hash map. If not found
        # creates a key/value pair with the value being the 
        # frequency of the key in the array. If found adds one
        # to the value to update the frequency.
        if map.contains_key(key):
            value = map.get(key)
            map.put(key, value+1)
        else:
            map.put(key, 1)
    
    # Creates an array with all key/value pairs in our hash map.
    map_array = map.get_keys_and_values()

    frequency = 0
    mode_value = DynamicArray()
    
    # Iterates through our map array.
    for number in range(map_array.length()):
        # Checks the value for frequency in the tuple, if the
        # frequency is higher than the previous value it clears the 
        # mode_value array and updates the frequency and mode_value
        # array.
        if map_array.get_at_index(number)[1] > frequency:
            frequency = map_array.get_at_index(number)[1]
            mode_value = DynamicArray()
            mode_value.append(map_array.get_at_index(number)[0])
        # If the frequency is the same as the previous highest, adds
        # the new key to the mode_value array.
        elif map_array.get_at_index(number)[1] == frequency:
            mode_value.append(map_array.get_at_index(number)[0])
    
    return (mode_value, frequency)


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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
