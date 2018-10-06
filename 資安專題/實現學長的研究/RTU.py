import socket
import ICS_authentication_protocol as ap

def sendint(i):
    return bin(i).encode("utf-8")

def sendstr(i):
    return i.encode("utf-8")



if __name__ == '__main__':
    
    # Constant Variable
    IDS_New = 2**(96-1)   # 第一次執行隨便設(但MTU與RTU要一樣)
    K_New = 2**48         # 第一次執行隨便設(但MTU與RTU要一樣)
    a1_New = 0
    c1_New = 0
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
        
        # Initial Variable
        IDS = IDS_New
        K = K_New 
        a1 = a1_New
        c1 = c1_New
        
        # Reset all var
        MTU_IDS = MTU_N = MTU_R = n = a = b = R = c = d = S = -1
        d_list = c_list = a_list = b_list = n_list = K_list = IDS_list = [-1, -1, -1, -1]
        
        
        RTU_Client.send(sendstr("Connect to RTU!"))
        
        ##### receive IDS N R #####
        MTU_IDS = int(RTU_Client.recv(1024).decode('ascii')[2:], 2) # int(RTU_Client.recv(1024), 2)
        MTU_N   = int(RTU_Client.recv(1024).decode('ascii')[2:], 2) # int(RTU_Client.recv(1024), 2)
        MTU_R   = int(RTU_Client.recv(1024).decode('ascii')[2:], 2) # int(RTU_Client.recv(1024), 2)
        
        
        """ RTU Obtain {IDS, N, R}""" 
        # Check MTU use IDS or IDS_Old
        if ((IDS != MTU_IDS)): #if rtu ide new and old mismatch MTU ide
            RTU_Client.send(sendstr("Mismatch IDS!"))
            IDS_list = ap.divide_in_parts(IDS, 3)
            IDS = ap.QR_Reverse([IDS_list[0], IDS_list[1], IDS_list[2], a1])
        
        # Calculate "n"
        n = MTU_N ^ K ^ IDS
            
        # divide "K, n" in 3 parts
        K_list = ap.divide_in_parts(K, 3)
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
            RTU_Client.send(sendstr("Mismatch R!"))
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
        IDS_list = ap.divide_in_parts(IDS, 4)
                        
        # Calculate "A, B"
        A = ap.QR([IDS_list[0], IDS_list[1], IDS_list[2], a_list[1]]) 
        B = ap.QR([K_list[0], K_list[1], K_list[2], c_list[1]])        
                        
        # divide "A, B" in 3 parts
        A_list = ap.divide_in_parts(A, 3)
        B_list = ap.divide_in_parts(B, 3)
                        
        # Calculate "IDS, K"
        IDS = A_list[0] + A_list[1] + A_list[2]
        K = B_list[0] + B_list[1] + B_list[2]
        a1_New = a_list[1]
        c1_New = c_list[1]
                    
        print("IDS : " , IDS)
        print("\n\nK : " , K)
        print("----------------------------")              
        
        
        RTU_Client.close()
    
    
'''
Reference:
    1. Socket usage                                ->  http://www.runoob.com/python/python-socket.html
    2. Convert base-2 binary number string to int  ->  https://stackoverflow.com/questions/8928240/convert-base-2-binary-number-string-to-int
    
'''