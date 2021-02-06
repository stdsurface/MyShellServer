# MyShellServer
Shell Servers used to Share Your Shells

## How to Run
- ### Windows NT (x86)
```bat
cd dist
REM modify `config.ini` to match your requirements.
myshellserver_nt32
```
- ### Windows NT (AMD64)
```bat
cd dist
REM modify `config.ini` to match your requirements.
myshellserver_nt32
```

## How when Running
- ### Windows NT
```console
Debug: binding ('127.0.0.1', 18362) ...
Warning: listening ...
Verbose: starting a accept thread for server ...
Info: accept a connection from ('127.0.0.1', 52940).
Debug: starting a recv thread for peer ('127.0.0.1', 52940) ...
Info: starting a thread for recv stdout from subprocess, at ('127.0.0.1', 52940) ...
Info: starting a thread for recv stderr from subprocess, at ('127.0.0.1', 52940) ...
Verbose: recv b'help\n' from ('127.0.0.1', 52940).
Verbose: recv b'exit\n' from ('127.0.0.1', 52940).
Warning: exiting stdout/stderr_callback ...
Verbose: recv b'\n' from ('127.0.0.1', 52940).
Warning: exiting stdout/stderr_callback ...
Warning: exiting thd_callback ...
Warning: closing server socket at exit ...
Warning: exiting server_accept_callback ...
Warning: bye.
```
