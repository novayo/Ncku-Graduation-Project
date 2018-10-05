import socket
import ICS_authentication_protocol as ap

def sendint(i):
    return bin(i).encode("utf-8")

def sendstr(i):
    return i.encode("utf-8")



if __name__ == '__main__':
    
    # Initial Variable (All of variables are 4*8=32 bits)
    IDS_New = 2**(96-1)  # 第一次執行隨便設(但MTU與RTU要一樣)
    IDS_Old = 0
    K_New = 2**48    # 第一次執行隨便設(但MTU與RTU要一樣)
    K_Old = 0
    pi = 11001001000011111101101010100010  # pi = 11.001001000011111101101010100010 去掉小數點取32位
    e  = 10101101111110000101010001011000  # e  = 10.101101111110000101010001011000 去掉小數點取32位    
    
    # Create RTU Server
    RTU_Socket = socket.socket()         
    host = socket.gethostname()
    port = 12345                
    RTU_Socket.bind((host, port))        

    RTU_Socket.listen(5)  # 可接受客戶端個數為5
    print("RTU Server Start!")
    while True:
        RTU_Client, addr = RTU_Socket.accept()
        print('連結地址：', addr)
        
        RTU_Client.send(sendstr("Connect to RTU!"))
        
        ##### receive IDS N R #####
        MTU_IDS = int(RTU_Client.recv(1024).decode('ascii')[2:], 2) # int(RTU_Client.recv(1024), 2)
        MTU_N   = int(RTU_Client.recv(1024).decode('ascii')[2:], 2) # int(RTU_Client.recv(1024), 2)
        print("MTU_N = ", bin(MTU_N))      ############################################################### 這裡MTU案太多次有時候會收到 N跟R 連起來的數值
        MTU_R   = int(RTU_Client.recv(1024).decode('ascii')[2:], 2) # int(RTU_Client.recv(1024), 2)
        print("\n\nMTU_R = ", bin(MTU_R))
        
        
        """ RTU Obtain {IDS, N, R}""" 
        # Check MTU use IDS_New or IDS_Old
        if (IDS_New != MTU_IDS):
            IDS_New, IDS_Old = IDS_Old, IDS_New
    
        # Calculate "n"
        n = MTU_N ^ K_New ^ IDS_New
        
        # divide "K, n" in 3 parts
        K_list = ap.divide_in_parts(K_New, 3)
        n_list = ap.divide_in_parts(n, 3)
        
        # Calculate "a, b"
        a = ap.MQR([pi, K_list[0], n_list[1], K_list[2]])
        b = ap.MQR([n_list[0], K_list[1], n_list[2], e])
        
        # divide "a, b" in 4 parts
        a_list = ap.divide_in_parts(a, 4)
        b_list = ap.divide_in_parts(b, 4)
        
        # Calculate "R" 
        R = ap.and32(a_list[0], b_list[0]) | ap.and32(a_list[2], b_list[2]) | ap.and32(a_list[3], b_list[3])
        
        
        ''' verify RTU_R == MTU_R '''
        if(R != MTU_R):
            RTU_Client.send(sendstr("Mismatch R"))
        else:
            # Calculate "c, d"
            c = ap.MQR([pi, n_list[0], K_list[1], n_list[2]])
            d = ap.MQR([K_list[0], n_list[1], K_list[2], e])
            
            # divide "c, d" in 4 parts
            c_list = ap.divide_in_parts(c, 4)
            d_list = ap.divide_in_parts(d, 4)
            
            # Calculate "S"
            S = ap.and32(c_list[0], d_list[0]) | ap.and32(c_list[2], d_list[2]) | ap.and32(c_list[3], d_list[3])
    
    
            ##### send {S} to MTU #####
            RTU_Client.send(sendint(S))     ##### send S #####
        
        
            ''' Update IDS K '''
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
            IDS_New = A_list[0] ^ A_list[1] ^ A_list[2]
            K_New = B_list[0] ^ B_list[1] ^ B_list[2]
            
            print("IDS_New : " , IDS_New)
            print("\n\nK_New : " , K_New)
            print("----------------------------")
        
        
        
        
        RTU_Client.close()
    
    
'''
Reference:
    1. Socket usage                                ->  http://www.runoob.com/python/python-socket.html
    2. Convert base-2 binary number string to int  ->  https://stackoverflow.com/questions/8928240/convert-base-2-binary-number-string-to-int
    
'''