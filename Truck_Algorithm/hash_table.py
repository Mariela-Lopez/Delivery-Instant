# hash function
# spacetime complexity -> O(1)
def hashfn(key, size):
    return key % size


# function that rehashes
# spacetime complexity -> O(1)
def rehash(oldhash, size):
    return (oldhash + 1) % size


# initializes the hashtable class
# spacetime complexity -> O(1)
class HashTable:
    def __init__(self):
        self.size = 50
        self.positions = [None] * self.size
        self.values = [None] * self.size

    # insertion function for hashtable
    # spacetime complexity -> O(n)
    def insert(self, key, value):
        hashvalue = hashfn(key, len(self.positions))

        if self.positions[hashvalue] is None:
            self.positions[hashvalue] = key
            self.values[hashvalue] = value
        else:
            if self.positions[hashvalue] == key:
                self.values[hashvalue] = value  # replace
            else:
                nextposition = rehash(hashvalue, len(self.positions))

                # spacetime complexity -> O(n)
                while self.positions[nextposition] is not None and \
                        self.positions[nextposition] != key:
                    nextposition = rehash(nextposition, len(self.positions))

                # spacetime complexity -> O(1)
                if self.positions[nextposition] is None:
                    self.positions[nextposition] = key
                    self.values[nextposition] = value
                else:
                    self.values[nextposition] = value  # replace

    # function that gets value from hashtable based on key
    # spacetime complexity -> O(n)
    def get_package(self, key):
        startposition = hashfn(key, len(self.positions))

        value = None
        stop = False
        found = False
        position = startposition

        # spacetime complexity -> O(n)
        while self.positions[position] is not None and not found and not stop:
            if self.positions[position] == key:
                found = True
                value = self.values[position]
            else:
                position = rehash(position, len(self.positions))
                if position == startposition:
                    stop = True
        return value

    # function that returns values for all packages
    # spacetime complexity -> O(n)
    def getAllPackages(self):
        return [package for package in self.values if package]
