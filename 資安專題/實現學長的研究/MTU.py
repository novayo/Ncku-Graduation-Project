import sys
import socket
from time import sleep
import ICS_authentication_protocol as ap

def sendint(i):
    return bin(i).encode("utf-8")

def sendstr(i):
    return i.encode("utf-8")



if __name__ == '__main__':
    
    # Try if connect to RTU
    try:
        MTU_Socket = socket.socket()
        target_host = '140.116.103.51'     # Server端的ip
        target_port = 12345                # Server端的port

        MTU_Socket.connect((target_host, target_port))      # s.send(sendstr("Hello"))
        print(MTU_Socket.recv(1024).decode('ascii'))       ##### receive "Connect to RTU!" #####
    except:
        print("Fail to connect RTU!\n")
        MTU_Socket.close()
        sys.exit(1)
    
    """ MTU send {IDS, N, R}"""
    # Initial Variable (All of variables are 96 bits)
    IDS_New = 2**(96-1)  # 第一次執行隨便設(但MTU與RTU要一樣)
    IDS_Old = 2**40
    K_New = 2**48    # 第一次執行隨便設(但MTU與RTU要一樣)
    K_Old = 2**20
    n = 0
    pi = 11001001000011111101101010100010  # pi = 11.001001000011111101101010100010 去掉小數點取32位
    e  = 10101101111110000101010001011000  # e  = 10.101101111110000101010001011000 去掉小數點取32位
    
    # use random to set value (use "New" one to shake hand)
    n = ap.random.randint(0, 2**(96-1))
    
    # divide "K, n" in 3 parts
    K_list = ap.divide_in_parts(K_New, 3)
    n_list = ap.divide_in_parts(n, 3)
    
    # Calculate "N, a, b"
    N = IDS_New ^ K_New ^ n
    a = ap.MQR([pi, K_list[0], n_list[1], K_list[2]]) #MTU_a has 128bits
    b = ap.MQR([n_list[0], K_list[1], n_list[2], e])
    
    # divide "a, b" in 4 parts
    a_list = ap.divide_in_parts(a, 4)
    b_list = ap.divide_in_parts(b, 4)
    
    # Calculate "R" 
    R = ap.and32(a_list[0], b_list[0]) | ap.and32(a_list[2], b_list[2]) | ap.and32(a_list[3], b_list[3])
    
    ##### Send IDS N R #####
    MTU_Socket.send(sendint(IDS_New))
    sleep(0.1)
    MTU_Socket.send(sendint(N))
    sleep(0.1)
    MTU_Socket.send(sendint(R))
    
    
    ##### Receive S #####
    RTU_S = MTU_Socket.recv(1024).decode('ascii')
    if ((RTU_S == "Mismatch IDS!") | (RTU_S == "Mismatch R!")):
        print(RTU_S + "\n") ##### receive "Mismatch R!" #####
        sys.exit(2)


    RTU_S = int(RTU_S[2:], 2) ##### receive S #####    
    """ MTU Obtain {S}"""
    # Calculate "c, d"
    c = ap.MQR([pi, n_list[0], K_list[1], n_list[2]])
    d = ap.MQR([K_list[0], n_list[1], K_list[2], e])
    
    # divide "c, d" in 4 parts
    c_list = ap.divide_in_parts(c, 4)
    d_list = ap.divide_in_parts(d, 4)
        
    # Calculate "S"
    S = ap.and32(c_list[0], d_list[0]) | ap.and32(c_list[2], d_list[2]) | ap.and32(c_list[3], d_list[3])
    
    
    ''' verify RTU_S == MTU_S '''
    if(RTU_S != S):
        print("RTU_S != MTU_S")
    else:
        ''' Update IDS and K '''
        # divide "IDS" in 4 parts
        IDS_list = ap.divide_in_parts(IDS_New, 4)
        
        # Calculate "A, B"
        A = ap.QR([IDS_list[0], IDS_list[1], IDS_list[2], a_list[1]]) #不確定這裡是不是兩個MTU_IDS_list[2]
        B = ap.QR([K_list[0], K_list[1], K_list[2], c_list[1]])        
        
        # divide "A, B" in 3 parts
        A_list = ap.divide_in_parts(A, 3)
        B_list = ap.divide_in_parts(B, 3)
        
        # Transfer IDS_New, K_New into IDS_Old, K_Old
        IDS_Old, K_Old = IDS_New, K_New
        
        # Calculate "IDS_New, K_New"
        IDS_New = A_list[0] + A_list[1] + A_list[2]
        K_New = B_list[0] + B_list[1] + B_list[2]
    
    print("IDS_New : " , IDS_New)
    print("\n\nK_New : " , K_New)
    print("----------------------------")
    
    
    
    MTU_Socket.close()
    
    
'''
Reference:
    1. Socket usage                                ->  http://www.runoob.com/python/python-socket.html
    2. Convert base-2 binary number string to int  ->  https://stackoverflow.com/questions/8928240/convert-base-2-binary-number-string-to-int
    
'''