from BitHash import BitHash
from BitVector import BitVector 
import math

class BloomFilter(object):
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        P = maxFalsePositive               # our false posotive rate
        d = numHashes                      # amount of hashes we want to make
        n = numKeys                        # amount of keys we want to store
        phi = (1-P**(1/d))
        N = math.ceil(d/(1-phi**(1/n)))    # round the float
        return N                           # the estimated number of bits needed
    
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        self.__N = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)  # N, how big array should be
        self.__bitVec = BitVector(size = self.__N)                          # the bit vector itself
        self.__numHashes = numHashes
        self.__numBitsSet = 0
        
    def insert(self, key):                 # insert the specified key into the Bloom Filter.
        seed = 0
        for i in range(self.__numHashes):
            hashing = BitHash(key, seed) 
            index = hashing % self.__N     # hashes position in the array
            seed = hashing                 # set the seed to that hash for the next time around
            if self.__bitVec[index] == 0:   
                self.__bitVec[index] = 1   # set the bit to 1 to indicate insertion
                self.__numBitsSet += 1      
        
    def find(self, key):
        seed = 0
        for i in range(self.__numHashes):
            hashing = BitHash(key, seed)
            index = hashing % self.__N
            seed = hashing
            if self.__bitVec[index] == 0:  # if any of the hashed positions = 0 then the key can't be there
                return False
            return True                    # otherwise we found it
    
    def numBitsSet(self):
        return self.__numBitsSet           # the number of bits ACTUALLY set in this Bloom Filter    
        
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # Phi is the ACTUAL measured current proportion of bits in the bit vector that are still 0. 
    def falsePositiveRate(self):
        propBitsSet = self.__numBitsSet/self.__N
        phi = 1 - propBitsSet
        P = (1 - phi)**self.__numHashes
        return P
       
   
       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    bf = BloomFilter(numKeys, numHashes, maxFalse)
    
    fin = open("wordlist.txt")
    lines = fin.read().splitlines()
    fin.close()
    
    firstWords = lines[:numKeys] # store the first 100,000 words of the file
    for i in firstWords:
        bf.insert(i)             # insert them into the Bloom Filter
        
        
    projectedFalseP = bf.falsePositiveRate()
    print("The projected False Posotive Rate is:", projectedFalseP) # based on the number of bits that ACTUALLY ended up being set
    
    # Now re-read the same bunch of the first numKeys and count how many are missing from 
    # the Bloom Filter. This should report that 0 words are missing from the Bloom Filter

    missing = 0
    for i in firstWords:
        searching = bf.find(i)
        if searching != True:
            missing += 1
    print("Missing from the first part (should be 0):", missing)
    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    secondWords = lines[numKeys:2*numKeys]
    numMissing = 0
    for i in secondWords:
        searching = bf.find(i)
        if searching == True:
            numMissing += 1
    
    percentRateFalsePos = numMissing/numKeys
    
    print("Percentage rate of false positives:", percentRateFalsePos)
    
if __name__ == '__main__':
    __main()       

