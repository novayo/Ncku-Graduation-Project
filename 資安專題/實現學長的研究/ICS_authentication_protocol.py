'''
下次目標: 用封包傳給其他電腦
'''
import random

# To prevent over 32 bits after calculating, rewrite by myself
def rotate_left32(number, bits):
    tmp = (((number << bits)&(2**32-1)) | (number >> (32-bits)))
    return tmp&(2**32-1)

# To prevent over 32 bits after calculating, rewrite by myself
def rotate_right32(number, bits):
    tmp = (((number << 32-bits)&(2**32-1)) | (number >> (bits)))
    return tmp&(2**32-1)

# To prevent over 32 bits after calculating, rewrite by myself
def and32(i1, i2):  
    tmp = i1 + i2
    return tmp&(2**32-1)

def divide_in_parts(i, parts): 
    tmplist = []
    for times in range(parts):
        tmplist.append(i&(int((2**(96/parts))-1)))
        i = i >> int(96/parts)
    return tmplist

# return 128bits
def QR(list): 
    list[1] = list[1] ^ (rotate_left32(and32(list[0], list[3]), 7))
    list[2] = list[2] ^ (rotate_left32(and32(list[1], list[0]), 9))
    list[3] = list[3] ^ (rotate_left32(and32(list[2], list[1]), 13))
    list[0] = list[0] ^ (rotate_left32(and32(list[3], list[2]), 18))
    return (list[0]*2**0) + (list[1]*2**32) + (list[2]*2**64) + (list[3]*2**96)

# return 128bits    
def MQR(list): 
    list[1] = and32(list[0],list[1]) ^ (rotate_left32(and32(list[0], list[3]), 7))
    list[2] = and32(list[2],list[1]) ^ (rotate_left32(and32(list[1], list[0]), 9))
    list[3] = and32(list[3],list[2]) ^ (rotate_left32(and32(list[2], list[1]), 13))
    list[0] = and32(list[0],list[3]) ^ (rotate_left32(and32(list[3], list[2]), 18))
    return (list[0]*2**0) + (list[1]*2**32) + (list[2]*2**64) + (list[3]*2**96)


'''
Reference:
    1. random.randint()  ->  https://dotblogs.com.tw/chris0920/2010/10/25/18560
    2. print in hex      ->  https://blog.csdn.net/u010918541/article/details/51485189
    3. print in binary   ->  https://stackoverflow.com/questions/699866/python-int-to-binary
    4. xor compute       ->  https://blog.csdn.net/AI_S_YE/article/details/45150477
    5. pi and e binary   ->  https://www.exploringbinary.com/pi-and-e-in-binary/
    備註: 由於96位數太大，故不能用取餘數(%)這個方法來擷取32bit，只能用&這個方法
'''