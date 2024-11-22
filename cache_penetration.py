import sys
import array
import csv
import math

def makeBitArray(bitSize, fill = 0):
    """
    Creates a bit array represented as an array of unsigned 32-bit integers.

    Parameters:
        - bitSize (int): The size of bit array.
        - fill (int): The initial value of bits (defaults to zero).
        
    Returns:
        - array.array: An array of unsigned 32-bit integers representing the bit array.
    """
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

def testBit(array_name, bit_num):
    """
    Checks if the bit at the specified position in the bit array is set to 1.
    
    Parameters:
        - array_name (array.array): The bit array.
        - bit_num (int): The position of the bit to check.
    
    Returns:
        - int: A nonzero value (2**offset) if the bit is set to 1, otherwise 0.
    """
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)


def setBit(array_name, bit_num):
    """
    Sets the bit at the specified position in the bit array to 1.
    
    Parameters:
        - array_name (array.array): The bit array.
        - bit_num (int): The position of the bit to set.
    
    Returns:
        - int: An integer with the bit at 'bit_num' set to 1.
    """
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

def hashing(data, bitArraySize, k):
    """
    Generates a hash value for the given data using a hash function.

    Parameters:
        - data (str): The data to hash.
        - bitArraySize (int): The size of the bit array.
        - k (int): A unique identifier for the hash function (seed).
    
    Returns:
        - int: The index within the range of the bit array.
    """
    hashValue = hash(f"{data}{k}")
    return hashValue % bitArraySize

def BloomFilterCalculator(n, p):
    """
    Calculates the optimal size and number of hash functions for a Bloom filter.
    
    Parameters:
        - n (int): Number of items in the Bloom filter.
        - p (float): Probability of false positives, fraction between 0 and 1 or a number indicating 1-in-p
    
    Returns:
        - m (int): The optimal size of the bit array (in bits).
        - k (int): The optimal number of hash functions.
    """
    m = math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))
    k = round((m / n) * math.log(2))
    return m, k

def addToBloomFilter(bitArray, element, bitArraySize, k):
    """
    Adds an element to the Bloom filter.

    Parameters:
        - bitArray (array.array): The bit array representing the Bloom filter.
        - element (str): The element to add to the Bloom filter.
        - bitArraySize (int): The size of the bit array (hash space).
        - k (int): The number of hash functions to apply.
    """
    for i in range(k):
        index = hashing(element, bitArraySize, i)
        setBit(bitArray, index)
   
def checkBloomFilter(emailToCheck, bitArray, bitArraySize, k):
    """
    Checks if an element is probably in the Bloom filter.
    
    Parameters:
        - emailToCheck (str): The element to check.
        - bitArray (array.array): The bit array representing the Bloom filter.
        - bitArraySize (int): The size of the bit array.
        - k (int): The number of hash functions applied.
    
    Returns:
        - None: Prints the result of the check:
                - "Probably in the DB" if the element might be in the filter.
                - "Not in the DB" if the element is definitely not in the filter.
    """
    for i in range(k):
        index = hashing(emailToCheck, bitArraySize, i)
        if testBit(bitArray, index) == 0: #if 0 not in DB
            print(f"{emailToCheck},Not in the DB")
            return
    print(f"{emailToCheck},Probably in the DB")

def readEmailsFromFile(filename):
    """
    Reads emails from the csv file.

    Parameters:
        - filename (str): Name of csv file containing emails.
        
    Returns:
        - emails (list): A list of emails extracted from the csv file.
    """
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        emails = []
        for row in reader:
            for email in row:
                emails.append(email)
    return emails

                    
if len(sys.argv) > 1:
    filename1 = sys.argv[1]  # file with emails data
    filename2 = sys.argv[2]  # file with emails to compare to
    
    emails = readEmailsFromFile(filename1)
    
    m, k = BloomFilterCalculator(len(emails), 0.0000001)  # calculates the number of bits that will be in the filter and the number of hash function to be used

    bloomArray  = makeBitArray(m) # creates an m-bit array

    for email in emails:
        addToBloomFilter(bloomArray, email, m, k) # add the emails to the bloom filter
    
    emailsToCompare = readEmailsFromFile(filename2)

    for email in emailsToCompare:
        checkBloomFilter(email, bloomArray, m, k) # checks whether the emails have a possibility of being in the DB or are definitely not in the DB