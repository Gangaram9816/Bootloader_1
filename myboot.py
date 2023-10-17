
import time
import serial
import os

def main():

    ser1=serial.Serial()
    ser1.baudrate=9600
    ser1.port='COM4'
    ser1.timeout=12
    ser1.open()

    def bms_update():
        
        try:
            file_size = os.path.getsize('EMO_BMS_V03.bin')
            file = open('EMO_BMS_V03.bin', 'rb')
            global end_index, start_index

            loop_n=file_size//64
            last_n=file_size%64

            start_index=0
            end_index=0

            c=0
            
            print(ser1.write(b'AT+BOOT=1\r\n'))
            print('boot1 send')
            
            
            time.sleep(3)
            bms=ser1.readline().decode('utf-8', 'ignore')
            
            def send_data():
                global end_index, start_index
                end_index=end_index+64
                file.seek(start_index)
                print('start_index',start_index)

                chunk_data=file.read(end_index-start_index)
                
                start_index=end_index
                print('end_index',end_index)

                
                ser1.write(b'AT+BOOT=3,64')
                time.sleep(0.1)
                ser1.write(chunk_data)
                time.sleep(0.1)
                ser1.write(b'\r\n')
                time.sleep(0.1)
                print('.bin data send')
                
            try:
                if 'AT+DONE' in bms:
                    print('Got Done')
                    time.sleep(0.8)
                    ser1.write(b'AT+BOOT=2\r\n')
                    
                    if 'BOOTLOA' in ser1.readline().decode('utf-8', 'ignore'):
                        while c<loop_n:
                            

                            send_data()

                            time.sleep(0.3)
                            if 'AT+DONE' in ser1.readline().decode('utf-8', 'ignore'):
                                c=c+1
                            else:
                                
                                print('NOt get AT+DONE after sending chun_data ,Failed')
                                break

                        file.seek(start_index)
                        print('last start index',start_index)
                        
                        end_index=end_index+last_n
                        print('last end index',end_index)

                        chunk_data=file.read(end_index-start_index)

                        time.sleep(0.3)

                        valu='AT+BOOT=3,'+str(last_n)
                        valu1=valu.encode()
                        
                        ser1.write(valu1)
                        ser1.write(chunk_data)
                        ser1.write(b'\r\n')
                        print('send last data')

                        time.sleep(0.3)
                        
                        if ser1.write(b'AT+BOOT=4\r\n'):
                            print('Data send Successfully')
                            
                    else:
                        
                        print('not get response after sending AT+BOOT=2')
                        
                else:
                    
                    print('NOt get AT+DONE after sending AT+BOOT=1 ,Failed')
                    
            except:
                pass

        except:
            pass
    inpu=input('Enter y ::: ')
    if inpu=='y':
        bms_update()

if __name__=="__main__":
    main()



    


