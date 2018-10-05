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



if __name__ == '__main__':
    
    """ MTU send {IDS, N, R}"""
    # Initial Variable (All of variables are 4*8=32 bits)
    MTU_IDS_New = 0x11001001000011111101101010100010  # 第一次執行隨便設(但MTU與RTU要一樣)
    MTU_IDS_Old = 0
    MTU_K_New = 0x10101101111110000101010001011000    # 第一次執行隨便設(但MTU與RTU要一樣)
    MTU_K_Old = 0
    MTU_n = 0
    pi = 11001001000011111101101010100010  # pi = 11.001001000011111101101010100010 去掉小數點取32位
    e  = 10101101111110000101010001011000  # e  = 10.101101111110000101010001011000 去掉小數點取32位
    
    # use random to set value (use "New" one to shake hand)
    MTU_n = random.randint(0, 2**96)
    
    # divide "K, n" in 3 parts
    MTU_K_list = divide_in_parts(MTU_K_New, 3)
    MTU_n_list = divide_in_parts(MTU_n, 3)
    
    # Calculate "N, a, b"
    MTU_N = MTU_IDS_New ^ MTU_K_New ^ MTU_n
    MTU_a = MQR([pi, MTU_K_list[0], MTU_n_list[1], MTU_K_list[2]]) #MTU_a has 128bits
    MTU_b = MQR([MTU_n_list[0], MTU_K_list[1], MTU_n_list[2], e])
    
    # divide "a, b" in 4 parts
    MTU_a_list = divide_in_parts(MTU_a, 4)
    MTU_b_list = divide_in_parts(MTU_b, 4)
    
    # Calculate "R" 
    MTU_R = and32(MTU_a_list[0], MTU_b_list[0]) | and32(MTU_a_list[2], MTU_b_list[2]) | and32(MTU_a_list[3], MTU_b_list[3])
    
###### Use flask to send {IDS, N, R} to RTU
    
    
    
    """ RTU Obtain {IDS, N, R}""" 
    # Initial Variable (All of variables are 4*8=32 bits)
    MTU_IDS = MTU_IDS_New
    RTU_IDS_New = 0x11001001000011111101101010100010  # 第一次執行隨便設(但MTU與RTU要一樣)
    RTU_IDS_Old = 0
    RTU_K_New = 0x10101101111110000101010001011000    # 第一次執行隨便設(但MTU與RTU要一樣)
    RTU_K_Old = 0
    RTU_N = MTU_N
    pi = 11001001000011111101101010100010  # pi = 11.001001000011111101101010100010 去掉小數點取32位
    e  = 10101101111110000101010001011000  # e  = 10.101101111110000101010001011000 去掉小數點取32位    
 
    # Check MTU use IDS_New or IDS_Old
    if (RTU_IDS_New != MTU_IDS):
        RTU_IDS_New, RTU_IDS_Old = RTU_IDS_Old, RTU_IDS_New
    
    # Calculate "n"
    RTU_n = RTU_N ^ RTU_K_New ^ RTU_IDS_New
    
    # divide "K, n" in 3 parts
    RTU_K_list = divide_in_parts(RTU_K_New, 3)
    RTU_n_list = divide_in_parts(RTU_n, 3)
    
    # Calculate "a, b"
    RTU_a = MQR([pi, RTU_K_list[0], RTU_n_list[1], RTU_K_list[2]])
    RTU_b = MQR([RTU_n_list[0], RTU_K_list[1], RTU_n_list[2], e])
    
    # divide "a, b" in 4 parts
    RTU_a_list = divide_in_parts(RTU_a, 4)
    RTU_b_list = divide_in_parts(RTU_b, 4)
    
    # Calculate "R" 
    RTU_R = and32(RTU_a_list[0], RTU_b_list[0]) | and32(RTU_a_list[2], RTU_b_list[2]) | and32(RTU_a_list[3], RTU_b_list[3])
    
    
    # verify RTU_R == MTU_R
    if(RTU_R != MTU_R):
        print("R' != R\n")
    else:
        # Calculate "c, d"
        RTU_c = MQR([pi, RTU_n_list[0], RTU_K_list[1], RTU_n_list[2]])
        RTU_d = MQR([RTU_K_list[0], RTU_n_list[1], RTU_K_list[2], e])
        
        # divide "c, d" in 4 parts
        RTU_c_list = divide_in_parts(RTU_c, 4)
        RTU_d_list = divide_in_parts(RTU_d, 4)
        
        # Calculate "S"
        RTU_S = and32(RTU_c_list[0], RTU_d_list[0]) | and32(RTU_c_list[2], RTU_d_list[2]) | and32(RTU_c_list[3], RTU_d_list[3])
    
###### Use flask to send {S} to MTU
    
    
    ## Update IDS and K
    # divide "IDS" in 4 parts
    RTU_IDS_list = divide_in_parts(RTU_IDS_New, 4)
        
    # Calculate "A, B"
    RTU_A = QR([RTU_IDS_list[0], RTU_IDS_list[1], RTU_IDS_list[2], RTU_a_list[1]]) #不確定這裡是不是兩個MTU_IDS_list[2]
    RTU_B = QR([RTU_K_list[0], RTU_K_list[1], RTU_K_list[2], RTU_c_list[1]])        
        
    # divide "A, B" in 3 parts
    RTU_A_list = divide_in_parts(RTU_A, 3)
    RTU_B_list = divide_in_parts(RTU_B, 3)
        
    # Transfer IDS_New, K_New into IDS_Old, K_Old
    RTU_IDS_Old, RTU_K_Old = RTU_IDS_New, RTU_K_New
        
    # Calculate "IDS_New, K_New"
    RTU_IDS_New = RTU_A_list[0] ^ RTU_A_list[1] ^ RTU_A_list[2]
    RTU_K_New = RTU_B_list[0] ^ RTU_B_list[1] ^ RTU_B_list[2]
    
    
    
    """ MTU Obtain {S}"""
    # Calculate "c, d"
    MTU_c = MQR([pi, MTU_n_list[0], MTU_K_list[1], MTU_n_list[2]])
    MTU_d = MQR([MTU_K_list[0], MTU_n_list[1], MTU_K_list[2], e])
    
    # divide "c, d" in 4 parts
    MTU_c_list = divide_in_parts(MTU_c, 4)
    MTU_d_list = divide_in_parts(MTU_d, 4)
        
    # Calculate "S"
    MTU_S = and32(MTU_c_list[0], MTU_d_list[0]) | and32(MTU_c_list[2], MTU_d_list[2]) | and32(MTU_c_list[3], MTU_d_list[3])
    
    
    # verify RTU_S == MTU_S
    if(RTU_S != MTU_S):
        print("RTU_S != MTU_S")
    else:
        ## Update IDS and K
        # divide "IDS" in 4 parts
        MTU_IDS_list = divide_in_parts(MTU_IDS_New, 4)
        
        # Calculate "A, B"
        MTU_A = QR([MTU_IDS_list[0], MTU_IDS_list[1], MTU_IDS_list[2], MTU_a_list[1]]) #不確定這裡是不是兩個MTU_IDS_list[2]
        MTU_B = QR([MTU_K_list[0], MTU_K_list[1], MTU_K_list[2], MTU_c_list[1]])        
        
        # divide "A, B" in 3 parts
        MTU_A_list = divide_in_parts(MTU_A, 3)
        MTU_B_list = divide_in_parts(MTU_B, 3)
        
        # Transfer IDS_New, K_New into IDS_Old, K_Old
        MTU_IDS_Old, MTU_K_Old = MTU_IDS_New, MTU_K_New
        
        # Calculate "IDS_New, K_New"
        MTU_IDS_New = MTU_A_list[0] ^ MTU_A_list[1] ^ MTU_A_list[2]
        MTU_K_New = MTU_B_list[0] ^ MTU_B_list[1] ^ MTU_B_list[2]
        
        
    


'''
Reference:
    1. random.randint()  ->  https://dotblogs.com.tw/chris0920/2010/10/25/18560
    2. print in hex      ->  https://blog.csdn.net/u010918541/article/details/51485189
    3. print in binary   ->  https://stackoverflow.com/questions/699866/python-int-to-binary
    4. xor compute       ->  https://blog.csdn.net/AI_S_YE/article/details/45150477
    5. pi and e binary   ->  https://www.exploringbinary.com/pi-and-e-in-binary/
    備註: 由於96位數太大，故不能用取餘數(%)這個方法來擷取32bit，只能用&這個方法
'''