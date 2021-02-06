# -*- coding: utf-8 -*-
import socket
from subprocess import Popen, PIPE
import time
import os
from threading import Thread
import signal
import traceback
import configparser
from utility.LogCommon import *

SERVER_IP_PORT = ('0.0.0.0', 8000)
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_EXECUTABLE = None


def stdout_callback(pout, wfile, rfile, conn):
    try:
        while True:
            b = pout.read(1)
            if len(b) == 0:
                break
            while True:
                tellval = pout.tell()
                if tellval < 0:
                    b += pout.read(-tellval)
                else:
                    break
            wfile.write(b)
    except Exception as e:
        error_print(f"stdout/stderr_callback break loop with {e}.")

    try:
        pout.close()
    except Exception as e:
        error_print(
            f"stdout/stderr_callback close stdout/stderr of subprocess with {e}.")

    try:
        wfile.close()
    except Exception as e:
        error_print(f"stdout/stderr_callback close wfile with {e}.")

    try:
        rfile.close()
    except Exception as e:
        error_print(f"stdout/stderr_callback close rfile with {e}.")

    try:
        conn.close()
    except Exception as e:
        error_print(f"stdout/stderr_callback close socket with {e}.")

    warning_print(f"exiting stdout/stderr_callback ...")


def thd_callback(conn, addr):
    try:
        rfile = conn.makefile('rb', -1)
        wfile = conn.makefile('wb', 0)

        p = Popen(SERVER_EXECUTABLE, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        pin = p.stdin
        pout = p.stdout
        perr = p.stderr

        thdout = Thread(target=stdout_callback,
                        args=(pout, wfile, rfile, conn))
        thdout.setDaemon(True)
        thdout.start()
        info_print(
            f"starting a thread for recv stdout from subprocess, at {addr} ...")

        thdout2 = Thread(target=stdout_callback,
                         args=(perr, wfile, rfile, conn))
        thdout2.setDaemon(True)
        thdout2.start()
        info_print(
            f"starting a thread for recv stderr from subprocess, at {addr} ...")

        while not rfile.closed:
            data = rfile.readline()
            if len(data) == 0:
                break
            verbose_print(f"recv {(data)} from {addr}.")

            if rfile.closed:
                break
            pin.write(data)

            if rfile.closed:
                break
            pin.flush()

    except Exception as e:
        error_print(f"thd_callback recv socket with {e}.")
        # traceback.print_exc()

    try:
        p.terminate()
    except Exception as e:
        error_print(f"thd_callback close subprocess with {e}.")

    try:
        pin.close()
    except Exception as e:
        error_print(f"thd_callback close stdin of subprocess with {e}.")

    warning_print(f"exiting thd_callback ...")


def exit(signum, frame):
    try:
        warning_print(f"closing server socket at exit ...")
        SERVER_SOCKET.close()
    except:
        pass

    raise KeyboardInterrupt


def server_accept_callback():
    sk = SERVER_SOCKET
    try:
        while True:
            conn, addr = sk.accept()
            # conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, 0)
            info_print(f"accept a connection from {addr}.")

            thd = Thread(target=thd_callback, args=(conn, addr))
            thd.setDaemon(True)
            thd.start()
            debug_print(f"starting a recv thread for peer {addr} ...")
    except OSError:
        pass
    except Exception as e:
        error_print(f"server_accept_callback break loop with {e}.")
    warning_print(f"exiting server_accept_callback ...")


class TcpShellServer:
    def __init__(self, fil):
        self.cfg_path = fil

    def run(self):
        global SERVER_IP_PORT, SERVER_SOCKET, SERVER_EXECUTABLE

        cfg = configparser.ConfigParser()

        # open config.ini
        cfg.read(self.cfg_path)
        assert cfg.has_option("Shell", "ListenIpv4Address")
        assert cfg.has_option("Shell", "ListenPort")
        assert cfg.has_option("Shell", "Executable")
        SERVER_IP_PORT = (cfg.get("Shell", "ListenIpv4Address"),
                          cfg.getint("Shell", "ListenPort"))
        SERVER_EXECUTABLE = cfg.get("Shell", "Executable")

        sk = SERVER_SOCKET
        sk.bind(SERVER_IP_PORT)
        debug_print(f"binding {SERVER_IP_PORT} ...")
        sk.listen(50)
        warning_print('listening ...')

        signal.signal(signal.SIGINT, exit)
        signal.signal(signal.SIGTERM, exit)

        thd = Thread(target=server_accept_callback)
        thd.setDaemon(True)
        thd.start()
        verbose_print(f"starting a accept thread for server ...")

        while True:
            try:
                if thd.is_alive() == False:
                    break
                time.sleep(1e6)
            except KeyboardInterrupt:
                break

        warning_print('bye.')
