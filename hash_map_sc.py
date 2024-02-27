# Name: Casey Lowe
# OSU Email: lowecas@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Portfolio Project - Assignment 6 - Hash Maps
# Due Date: December 10th, 2023
# Description: Implementing the following methods through open addressing hash maps: put(), empty_buckets(),
# table_load(), clear(), resize_table(), get(), contains_key(), remove(), get_keys_and_values(), find_mode()


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
        """
        Method that updates the key-value pair in a hash map and any existing keys given will have their
        value replaced with the new one. Otherwise, the key-value pair is added into the hash map.

        Table resizes are doubled from its capacity and the load factor is greater than or equal to 1.0.
        """

        # resize if load factor is at or exceeds 1.0
        load_factor = self.table_load()

        if load_factor >= 1.0:
            double_capacity = self.get_capacity() * 2
            self.resize_table(double_capacity)

        # get hash value and its' index
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()

        # find the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # existing key -- replace value with new value
        for item in bucket:
            if item.key == key:
                bucket.remove(key)
                bucket.insert(key, value)
                return

        # key does not exist, add key-value pair into hash map
        bucket.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that changes the capacity of the hash table and rehashes existing key-value pairs into
        the new hash map.
        """

        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) is not True:
            self._capacity = self._next_prime(new_capacity)
        else:
            self._capacity = new_capacity
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._size = 0
        for index in range(self._capacity):
            self._buckets.append(LinkedList())
        for index in range(old_buckets.length()):
            for i in old_buckets[index]:
                self.put(i.key, i.value)

    def table_load(self) -> float:
        """
        Return the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        """
        count = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Method that returns the value using the key and returns None if the key does not exist within
        the hash map.
        """
        # get the hash using key
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()

        # get the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # traverse through the bucket to find the key
        for item in bucket:
            if item.key == key:
                return item.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map, and return False otherwise.
        """
        if self.get(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Method that simply removes the given key-value pair from the hash map.
        """
        # get hash value and its' index
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()  # index = hash % array_size

        # find the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # existing key -- remove
        for item in bucket:
            if item.key == key:
                bucket.remove(key)
                self._size -= 1

        # sets size back to 0 if it goes to negative
        if self._size < 0:
            self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Create a new DynamicArray object where each index contains a tuple of
        all key/value pair stored in a HashMap.
        """
        hashmap = DynamicArray()
        for i in range(self._capacity):
            sll = self._buckets[i]
            if sll.length() > 0:
                for node in sll:
                    hashmap.append((node.key, node.value))
        return hashmap

    def clear(self) -> None:
        """
        Clear the contents of the hash map but do not change the underlying hash table capacity.
        """
        for index in range(self._buckets.length()):
            self._buckets[index] = LinkedList()
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Method that takes in a dynamic array that is either sorted or unsorted and returns a tuple of
    a dynamic array that establishes the mode and frequency for the mode in O(n) runtime complexity.
    There can be multiple modes if they are the same frequencies.
    """
    frequency = HashMap()
    highest_frequency = 0

    for index in range(da.length()):
        key = da[index]

        # number exists, increment frequency
        if frequency.contains_key(key):
            value = frequency.get(key) + 1
            frequency.put(key, value)

        # number doesn't exist, add it into hash map
        else:
            frequency.put(key, 1)

    # establish a mode array and key-value pairs from hash map
    mode = DynamicArray()
    hash_map = frequency.get_keys_and_values()

    # traverse through to collect highest frequency
    for num in range(hash_map.length()):
        value = hash_map[num][1]

        # replace if there is a higher frequency
        if value > highest_frequency:
            highest_frequency = value

    # append keys that have the same highest frequency
    for index in range(hash_map.length()):
        key = hash_map[index][0]
        value = hash_map[index][1]

        if value == highest_frequency:
            mode.append(key)

    return mode, highest_frequency


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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
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
