import socket, os

HOST = 'ec2-43-201-65-73.ap-northeast-2.compute.amazonaws.com'
PORT = 5555

#파일을 받는 함수
def file_Reader(fileName, client_socket):  
    data = client_socket.recv(1024)
    data_transferred = 0
    byte_index = 0
    if (fileName == "Link.txt"):
        byte_index = -8
    else:
        byte_index = -9

    nowdir = os.getcwd()
    with open(nowdir+"\\"+fileName, 'wb') as f:
        try:
            while True:
                f.write(data)
                data_transferred += len(data)
                byte_name = data[byte_index:]
                if(fileName == byte_name.decode()):
                    break
                data = client_socket.recv(1024)
        except Exception as ex:
            print(ex)
 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

#1  서버에 CSMA/CD 연산 요청
msg = 'CSMA/CD Start'
print("Link Start")
msg = msg.encode()
data = client_socket.sendall(msg)

#4  wait 메시지 받고 표시
msg = client_socket.recv(1024)
wait = msg.decode()
print(wait)

#5  서버에 파일 전송 시작 요청
msg = 'File Send Start'
msg = msg.encode()
data = client_socket.sendall(msg)

#8  서버 메시지를 받고 파일 리스트를 표시
msg = client_socket.recv(1024)
msg = msg.decode()
print(msg)
print("======File_List=======")

# 파일 이름 보내고, 요청
for i in range(1,6) :
        if i == 5:
            filename = "Link.txt"
            print("ReceveFile : " + filename)
            data = filename.encode()
            client_socket.send(data)
            file_Reader(filename, client_socket)
        else :
            filename = "Node%d.txt" % i
            print("ReceveFile : " + filename)
            data = filename.encode()
            client_socket.send(data)
            file_Reader(filename, client_socket)

#종료 후, 종료텍스트 출력
print("======================")
print("File Receive End")
print("Link End")
client_socket.close()