import socket, threading
from os.path import exists
import sys, os, time, math, random

PORT = 5555

Accept_Flag = 0     #허용/거절 플래그
Node1_Flag = 0      #Accept 하는 동안 Node1 실행 금지 플래그
Node2_Flag = 0      #Accept 하는 동안 Node2 실행 금지 플래그
Node3_Flag = 0      #Accept 하는 동안 Node3 실행 금지 플래그
Node4_Flag = 0      #Accept 하는 동안 Node4 실행 금지 플래그
BackCount = 0       #BackCount횟수
CountNode = 0       #서버 과부하 막기 위한 Node 실행 횟수
CountTime = 0       #Time Count

class Link_Write:       #Link 관련 파일 쓰기 클레스
    def link_init(time, min, sec, ms): 
        with open("Link.txt", "w") as f:
            f.write(time + " Link Start //" + min + "min " + sec + "sec " + ms + "msec\n")

    def systime_init(time, min, sec, ms):
         with open("Link.txt", "a") as l:
            l.write(time + " System Clock Start //" + min + "min " + sec + "sec " + ms + "msec\n")

    def Send(NodeName, AfterNodeName, time):
        with open("Link.txt", "a") as a:
            a.write(time + ' ' + NodeName+ ' Data Send Request To '+AfterNodeName+'\n')
            
    def Accept(NodeName, AfterNodeName, time):
        with open("Link.txt", "a") as b:
            b.write(time + ' Accept : ' + NodeName+ ' Data Send Request To '+AfterNodeName + '\n')

    def Reject(NodeName, AfterNodeName, time):
        with open("Link.txt", "a") as c:
            c.write(time + ' Reject : ' + NodeName+ ' Data Send Request To '+AfterNodeName + '\n')
            
    def Finish(NodeName, AfterNodeName, time):
        with open("Link.txt", "a") as d:
            d.write(time+ ' '+ NodeName+' Data Send Finished To '+ AfterNodeName + '\n')

    def link_Finish(time):
        with open("Link.txt", "a") as f:
            f.write(time + " Link Finished\n")

    def systime_Finish(time):
         with open("Link.txt", "a") as f:
            f.write(time + " System Clock Finished\n")

class Node_Write:       #노드 관련 파일 쓰기 클레스
    def init(NodeName, time):
        with open(NodeName+'.txt', "w") as f:
            f.write(time + ' ' + NodeName + ' Start\n')

    def Send(NodeName, AfterNodeName, time):
        with open(NodeName+'.txt', "a") as e:
            e.write(time+' Data Send Request To '+ AfterNodeName + '\n')

    def Reject(NodeName, time):
        with open(NodeName+'.txt', "a") as g:
            g.write(time+ ' Data Send Request Reject from Link\n')

    def BackOff(NodeName, time, Retime):
        Retime = str(int(Retime * 1000))
        with open(NodeName+'.txt', "a") as h:
            h.write(time+' Exponential Back-off Time : '+ Retime + ' msec\n')

    def Accept(NodeName, time):
        with open(NodeName+'.txt', "a") as x:
            x.write(time+ ' Data Send Request Accept from Link\n')

    def Send_Finish(NodeName, AfterNodeName, time):
        with open(NodeName+'.txt', "a") as y:
            y.write(time+' Data Send Finished To '+ AfterNodeName+'\n')

    def Receive_Start(NodeName, AfterNodeName, time):
        with open(AfterNodeName+'.txt', "a") as z:
            z.write(time+' Data Receive Start from '+ NodeName+'\n')

    def Receive_Finish(NodeName, AfterNodeName, time):
        with open(AfterNodeName+'.txt', "a") as w:
            w.write(time+' Data Receive Finished from '+ NodeName+'\n')
    
    def Node_Finish(NodeName, time):
        with open(NodeName+'.txt', "a") as p:
            p.write(time + ' ' + NodeName + ' Finshed\n')

class NodeActive:       #노드 활동
    def send(NodeName, AfterNodeName):  #노드 처음 호출할 경우
        global BackCount, CountTime
        BackCount = 0
        Link_Write.Send(NodeName, AfterNodeName, Timer.min_sec_ms())
        Node_Write.Send(NodeName, AfterNodeName, Timer.min_sec_ms())
        if Accept_Flag == 0 :   # 노드 허용 플래그인 경우
            NodeActive.Accept(NodeName, AfterNodeName, Timer.min_sec_ms())
            CountTime += 5
            time.sleep(0.05)
            NodeActive.Finish(NodeName, AfterNodeName, Timer.min_sec_ms())
        elif Accept_Flag == 1:   #노드 거부 플래그인 경우
            NodeActive.Reject(NodeName, AfterNodeName, Timer.min_sec_ms())
            BackCount += 1       #노드 거부할때마다 횟수 증가
            Retime = NodeActive.BackOffTimer(BackCount)/1000    #BackOff실행
            CountTime += NodeActive.BackOffTimer(BackCount)
            time.sleep(Retime)
            Node_Write.BackOff(NodeName, Timer.min_sec_ms(), Retime)
            NodeActive.resend(NodeName, AfterNodeName)  #재전송

    def resend(NodeName, AfterNodeName):    #노드 재전송해야하는 경우
        global BackCount, CountTime
        BackCount += 1
        if Accept_Flag == 0 :   #노드 허용 플래그인 경우
            NodeActive.Accept(NodeName, AfterNodeName, Timer.min_sec_ms())
            time.sleep(0.005)
            CountTime += 5
            NodeActive.Finish(NodeName, AfterNodeName, Timer.min_sec_ms())
        elif Accept_Flag == 1:  #노드 거부 플래그인 경우
            Retime = NodeActive.BackOffTimer(BackCount)/1000    #BackOff실행
            time.sleep(Retime)
            CountTime += NodeActive.BackOffTimer(BackCount)
            Node_Write.BackOff(NodeName, Timer.min_sec_ms(), Retime)
            NodeActive.resend(NodeName, AfterNodeName)  #계속해서 재전송

    def Accept(NodeName, AfterNodeName, tim):
        NodeFlagChange.NodeFlagChangeOne(NodeName)  #Node플래그 1로 바꿔 Finish할 때까지 똑같은 노드 생성이 안되도록 한다.
        global Accept_Flag
        Accept_Flag = 1     #Accept인 경우 플래그 1로 바꾼다
        Link_Write.Accept(NodeName, AfterNodeName, tim)
        Node_Write.Accept(NodeName, tim)
        Node_Write.Receive_Start(NodeName, AfterNodeName, tim)

    def Reject(NodeName, AfterNodeName, tim):
        Link_Write.Reject(NodeName,AfterNodeName, tim)
        Node_Write.Reject(NodeName, tim)

    def Finish(NodeName, AfterNodeName, tim):
        NodeFlagChange.NodeFlagChangeZero(NodeName)
        global Accept_Flag, CountNode
        Accept_Flag =  0    #허용 플래그 0으로 바꿈
        CountNode -= 1      #노드 허용 갯수 하나 제거
        Link_Write.Finish(NodeName, AfterNodeName, tim)
        Node_Write.Send_Finish(NodeName, AfterNodeName, tim)
        Node_Write.Receive_Finish(NodeName, AfterNodeName, tim)
        sys.exit(0)         #종료

    def BackOffTimer(trasNum):                  #transNum은 재전송 횟수를 말함
        temp = min(trasNum, 10)            
        rnd = int(random.random()*math.pow(2,temp) -1)
        return rnd          #BackCount 시간

class NodeFlagChange:   #NodeFlagChange -> Node 실행 여부
    def NodeFlagChangeZero(NodeName):           #Nodei 실행 완료
        global Node1_Flag, Node2_Flag,  Node3_Flag, Node4_Flag
        if NodeName == "Node1" and Node1_Flag == 1 :
            Node1_Flag = 0
        elif NodeName == "Node2" and Node2_Flag == 1 :
            Node2_Flag = 0
        elif NodeName == "Node3" and Node3_Flag == 1 :
            Node3_Flag = 0
        elif NodeName == "Node4" and Node4_Flag == 1 :
            Node4_Flag = 0

    def NodeFlagChangeOne(NodeName):            #Nodei 실행 시작(실행 중)
        global Node1_Flag, Node2_Flag,  Node3_Flag, Node4_Flag
        if NodeName == "Node1" and Node1_Flag == 0 :
            Node1_Flag = 1
        elif NodeName == "Node2" and Node2_Flag == 0 :
            Node2_Flag = 1
        elif NodeName == "Node3" and Node3_Flag == 0 :
            Node3_Flag = 1
        elif NodeName == "Node4" and Node4_Flag == 0 :
            Node4_Flag = 1   

class Timer:            #시간 형식 (분, 초, 밀리초, 전체적인 형식)
    def min_sec_ms():
        result_min = int((CountTime/ (1000 * 60)) % 60)
        result_sec = int((CountTime/1000)%60)
        result_ms = int((CountTime%1000))

        time_result = '{:02}:{:02}:{:03}'.format(result_min, result_sec, result_ms)
        return time_result

    def min():
        result_min = int((CountTime/ (1000 * 60)) % 60)
        time_result = '{:02}'.format(result_min)
        
        return  time_result

    def sec():
        result_sec = int((CountTime/1000)%60)
        time_result = '{:02}'.format(result_sec)
        
        return  time_result

    def ms():
        result_ms = int((CountTime%1000))
        time_result = '{:03}'.format(result_ms)
        
        return  time_result


class File_Class:       #파일 관련 클레스
    def File_System(fileName, client_socket, addr):         #파일을 찾고, 파일을 읽고 바이트를 보냄
        data_transferred = 0
        if not exists(fileName):
            sys.exit()
        with open(fileName, 'rb') as f:
            try:
                if(fileName == "Link.txt"):
                    Link_Write.link_Finish(Timer.min_sec_ms())
                data = f.read(1024)
                while True:
                    if not data :
                        break
                    data_transferred += client_socket.send(data)
                    data = f.read(1024)
            except Exception as ex:
                print(ex)

    def File_Send(client_socket, addr):         #클라이언트에서 파일명을 받고, 파일 명령어로 넘김
        try:
            while True:
                data = client_socket.recv(1024)
                msg = data.decode()
                if not data :
                    break
                File_Class.File_System(msg, client_socket, addr)
                data = msg.encode()
                client_socket.sendall(data)
                print(msg)
        except Exception as ex:
            print(ex)
        finally:
            pid = os.getpid()
            os.kill(pid, 2)
            client_socket.close()

#소켓 네트워크 연결 준비
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', PORT))
server_socket.listen(1)

try:
    #2 클라이언트 접속 메시지 수신
    client_socket, addr = server_socket.accept()
    socketAccept = client_socket.recv(1024)
    msg = socketAccept.decode()
    print("Link Success")
    print(msg)
    
    #3 계산 완료할때까지 기다리라는 메시지 송신
    msg = 'Wait'
    socketAccept = msg.encode()
    client_socket.sendall(socketAccept)

    #txt(로그)파일 초기화
    Link_Write.link_init(Timer.min_sec_ms(), Timer.min(), Timer.sec(), Timer.ms())
    Link_Write.systime_init(Timer.min_sec_ms(), Timer.min(), Timer.sec(), Timer.ms())
    for i in range(1,5):
        Node_Write.init('Node%d' %i, Timer.min_sec_ms())
    

    while True:
        CountTime += 1      #0.001초씩 돌아감
        time.sleep(0.001)   #0.001초 정지
        if CountTime >= 60000:  #1분이 되면 while문 종료
            th1.join()
            th2.join()
            th3.join()
            th4.join()          #join으로 전체 스레드 종료 기다림
            Link_Write.systime_Finish(Timer.min_sec_ms())
            for i in range(1, 5):
                Node_Write.Node_Finish('Node%d' %i, Timer.min_sec_ms())
            print("CSMA/CD Finish")
            break

        if CountNode < 4:   #Node최대 실행횟수 : 4개  #만약 없는 경우 서버 과부하(CPU사용량 증가)
            CountNode += 1
            first = random.choice(["Node1", "Node2", "Node4","Node3"])  #처음에 보내는 Node를 선택
            if(first == "Node1" and Node1_Flag == 0):                   #Node1이면서, Node1_Flag가 실행 시작하기 전이면 if문에 들어감
                second = random.choice(["Node2", "Node3", "Node4"])     #Node1제외된 남은 2,3,4 노드 랜덤 선택한다.
                th1 = threading.Thread(target=NodeActive.send, args=(first, second)) 
                th1.start()
            elif(first == "Node2"and Node2_Flag == 0):
                second = random.choice(["Node1", "Node3", "Node4"])
                th2 = threading.Thread(target=NodeActive.send, args=(first, second)) 
                th2.start()
            elif(first == "Node3"and Node3_Flag == 0):
                second = random.choice(["Node2", "Node1", "Node4"])
                th3 = threading.Thread(target=NodeActive.send, args=(first, second)) 
                th3.start()
            elif(first == "Node4"and Node4_Flag == 0):
                second = random.choice(["Node2", "Node3", "Node1"])
                th4 = threading.Thread(target=NodeActive.send, args=(first, second)) 
                th4.start()
    
    #6  파일 전송 시작
    data = client_socket.recv(1024)
    msg = data.decode()
    print(msg)
    
    #7  파일 전송을 시작한다는 메시지를 보냄
    data = 'File Receive Start'
    msg = data.encode()
    client_socket.sendall(msg)
    
    #파일 전송 시작
    print("==File_List==")
    for i in range(0, 5):
        time.sleep(0.28)
        th = threading.Thread(target=File_Class.File_Send, args=(client_socket, addr))
        th.start()
except Exception as e :
    print(e)
finally:
    print("=============")
    print("File Send END")
    print("Link End")
    server_socket.close()
    os._exit(0)