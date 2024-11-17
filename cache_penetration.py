import sys
import array
import csv
import math

def makeBitArray(bitSize, fill = 0):
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

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

def hashing(data, bitArraySize, k):
    hashValue = hash(f"{data}{k}")
    return hashValue % bitArraySize

def addToBloomFilter(bitArray, element, bitArraySize, k):
    for variationOfHash in range(k):
        index = hashing(element, bitArraySize, variationOfHash)
        setBit(bitArray, index)

def BloomFilterCalculator(n, p):
    m = math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))
    k = round((m / n) * math.log(2))
    return m, k
   
def checkBloomFilter(emailToCheck,bitArray, bitArraySize, k):
    for variationOfHash in range(k):
        index = hashing(emailToCheck, bitArraySize, variationOfHash)
        if testBit(bitArray, index) == 0: #if 0 not in DB
            print(f"{emailToCheck},Not in the DB")
            return
    print(f"{emailToCheck},Probably in the DB")

def readEmailsFromFile(filename):
    """
    Reads emails from csv file.

    Args:
        arg1 (str): Name of csv file containing emails.
        
    Returns:
        list: A list of emails extracted from the csv file.
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
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    
    emails = readEmailsFromFile(filename1)
    
    m, k = BloomFilterCalculator(len(emails), 0.0000001)

    bloomArray  = makeBitArray(m) #Creates an m-bit array

    for email in emails:
        addToBloomFilter(bloomArray, email, m, k)
    
    emailsToCompare = readEmailsFromFile(filename2)

    for email in emailsToCompare:
        checkBloomFilter(email, bloomArray, m, k)