Socket examples

simple examples:
 - echo-client.py: simple echo client 
 - echo-server.py: simple echo server (talks to echo-client.py)

echo-server.py variations (all talk to echo-client.py clients)
 - thread-server.py: spawn thread for each echo-client request [most platforms]
 - fork-server.py:   fork a process for each echo-client request [not Windows]
 - class-server.py:  use SocketServer module to emulate thread-server.py

file transfer examples:
 - getfile.py: client and server file-transfer implementation
 - getfile-noeoln.py: minor variation that doesn't send file names in lines

other
 - *.out.txt: test results/logs
 - testdir: files used to test getfile.py
 - testecho.py: spawn multiple echo-client.py programs to test servers
 - testechowait.py: minor variation of testecho.py with execfile()

----
Note that you can run all of these on any machine with TCP/IP support,
even without an Internet feed--just use 'localhost' and '' for the host
name in clients and servers, respectively, and run in distinct console
windows on your local macine.  If you use a remote server machine name,
your machine will use whatever socket interface you have (e.g., it will
dial out to your ISP automatically to connect, if needed).  See also:

- Python select module documentation 
- ftplib, smtplib, and other standard library modules' socket usage
- thread and fork material and examples in operating system chapter
- ftp, email, and cgi examples in .. (higher-level protocols based on sockets)

