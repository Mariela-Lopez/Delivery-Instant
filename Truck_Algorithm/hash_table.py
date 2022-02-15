class HashTable:
    def __init__(self):
        self.size = 50
        self.positions = [None] * self.size
        self.values = [None] * self.size

    def insert(self,key,value):
      hashvalue = self.hashfn(key,len(self.positions))

      if self.positions[hashvalue] == None:
        self.positions[hashvalue] = key
        self.values[hashvalue] = value
      else:
        if self.positions[hashvalue] == key:
          self.values[hashvalue] = value #replace
        else:
          nextposition = self.rehash(hashvalue,len(self.positions))
          while self.positions[nextposition] != None and \
                          self.positions[nextposition] != key:
            nextposition = self.rehash(nextposition,len(self.positions))

          if self.positions[nextposition] == None:
            self.positions[nextposition]=key
            self.values[nextposition]=value
          else:
            self.values[nextposition] = value #replace

    def hashfn(self,key,size):
         return key%size

    def rehash(self,oldhash,size):
        return (oldhash+1)%size

    def get(self,key):
      startposition = self.hashfn(key,len(self.positions))

      value = None
      stop = False
      found = False
      position = startposition
      while self.positions[position] != None and not found and not stop:
         if self.positions[position] == key:
           found = True
           value = self.values[position]
         else:
           position=self.rehash(position,len(self.positions))
           if position == startposition:
               stop = True
      return value
