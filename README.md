# Bloom-Filter

When we wish to store numerous keys, especially very large keys in a hash table and query, we run into a big problem of not enough RAM to hold them all.

We can solve this issue by implementing a Bloom Filter, a probabilistic data structure supporting insertion and query.

A Bloom Filter is an array of 'N' bits, which here uses Purdue's BitVector, a custom bit array class. It uses a total of 'd' hash functions. They can be independent
or simulated by multiple functions using just one BitHash function by rehashing, providing the prior BitHash value as the seed for the next call. This approach uses less RAM per key.

Keys can be any size, but all keys of all sizes consume the same small number of bits! 
Practically, applying this data structure allows one to efficiently check if you've encountered the same text, name, image, and even the same text of an entire book.

Set membership method (searching for the key in the Bloom Filter) is guaranteed to succeed if the same key has been previously inserted.
There is a small and tunable probability that the Bloom Filter will return true even though the key was never inserted. This false-positive rate is very rare.
Bloom Filters have a zero false-negative rate. If it returns False that the key has been inserted, then it definitely has never been inserted.

My implementation allows one to pass in:
- The number of keys we want to store.
- The number of hash functions.
- The desired false positive rate.





