2022-2학기 데이터통신 4조 과제: CSMA/CD 구현

•조원 학번, 이름
 20180239 허현수
 20180240 황태겸
 20203046 김민규

•프로그램 구성요소 설명
 Server.py : 서버 컴퓨터에서 실행하여 클라이언트의 접속요청을 받은 후, backoff를 계산하여 파일을 Client.py로 전송하는 역할
 Client.py :  단말 기기에서 Thread로 동작하며 서버에 접속 요청을 전송한 후, Server.py에서 계산한 파일을 받는 역할

•프로그램 실행환경 및 실행방법 설명
 사용 프로그램 언어 : Python
 프로그램 제작 환경 : Windows 10
 사용한 서버 : AWS EC2를 이용한 Ubuntu 서버 구축

 실행 방법: AWS EC2를 이용해 Ubuntu로 인스턴스를 시작하고 해당 서버에 연결을 한다.
                 Ubuntu 서버에서 Server.py파일을 실행한 이후, 다른 단말 기기에서 Client.py파일을 실행한다.
                 
•Error or Additional Message Handling에 대한 사항 설명
 - Server.py 파일에서 AWS EC2 인스턴스의 Ubuntu 서버에서 파일을 읽는 과정에서 오류가 발생할 경우 ex를 출력한다.
 - Server.py 파일에서 클라이언트에서  파일을 받고 명령어로 넘기는 과정에서 오류가 발생할 경우 ex를 출력한다.
 - Server.py 파일에서  File_Class의 File_Send 함수에서 사용 리소스를 종료하기 위해 finally 구문을 이용한다.
 - Server.py 파일을 실행하던 도중 오류가 발생할 경우 e를 출력한다.
 - Server.py 파일의 main문에서 gracefully termination을 수행하기 위해 finally 구문을 이용해 소켓통신을 종료한다.
 - Server.py 파일의 main문에서 포트를 사용중일 때 발생하는 에러를 해결하기 위해
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)를 이용한다.
 - Client.py 파일에서 파일을 읽어오는 도중 오류가 발생하면 ex룰 출력한다.

•Additional Comments
 - Server.py의 사용하고자 하는 포트를 수정한다.
 - 실행한 AWS EC2 인스턴스의 퍼블릭 IPv4 DNS를 이용해 Client.py의 HOST 변수의 주소를 수정한다.
 - 실행한 AWS EC2 인스턴스의 보안 탭에서 Client.py파일에서 연결에 사용할 포트를 입력, 수정해야 한다.
