import sys
import mmh3
import hashlib
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

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])

def hashing(data, bitArraySize, k):
    # salted_data = f"{data}{seed}".encode()
    # hash_object = hashlib.sha256(salted_data)
    # hash_value = int(hash_object.hexdigest(), 16)
    # return hash_value % bitArraySize
    hash_value = mmh3.hash(data, k)
    return hash_value % bitArraySize

def placeElementInBitArray(bitArray, element, bitArraySize, k):
    for function in range(k):
        index = hashing(element, bitArraySize, function)
        setBit(bitArray, index)
    #FOR TESTING
    #print(f"Email: '{element}' ; index: {index}")

def BloomFilter(emailToCheck,bitArray, bitArraySize, k):
    for function in range(k):
        index = hashing(emailToCheck, bitArraySize, function)
        if not testBit(bitArray, index):
            print(f"{emailToCheck},Not in the DB")
            return
    print(f"{emailToCheck},Probably in the DB")
            

def BloomFilterCalculator(n, p):
    m = math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))
    k = round((m / n) * math.log(2))
    return m, k
    
if len(sys.argv) > 1:
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    
    with open(filename1, "r") as file:
        reader = csv.reader(file)
        next(reader)
        emails = []
        for row in reader:
            for email in row:
                emails.append(email)
        m, k = BloomFilterCalculator(len(emails),0.0000001)
        bloomArray  = makeBitArray(m) #Creates an m-bit array
        for email in emails:
            placeElementInBitArray(bloomArray, email, m, k)
    
    with open(filename2, "r") as file:
        reader = csv.reader(file)
        next(reader)
        emailsToCompare = []
        for row in reader:
            for email in row:
                emailsToCompare.append(email)
        for email in emailsToCompare:
            BloomFilter(email, bloomArray, m, k)

    

        

