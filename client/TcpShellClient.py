# -*- coding: utf-8 -*-
import socket
from subprocess import Popen, PIPE
import time
import os
import sys
from threading import Thread
import configparser
from utility.LogCommon import *

SERVER_IP_PORT = ('127.0.0.1', 8000)
SERVER_ENCODING = 'utf-8'
IS_TERMINATED = False


def convert_str_to_bytes(s):
    return s.encode(encoding=SERVER_ENCODING, errors='replace')


def convert_bytes_to_str(b):
    return b.decode(encoding=SERVER_ENCODING, errors='replace')


def stdout_callback(sk):
    global IS_TERMINATED
    try:
        while True:
            b = sk.recv(4096)
            if len(b) == 0:
                break
            bs = convert_bytes_to_str(b)
            print(bs, end='')
    except OSError:
        pass
    except Exception as e:
        error_print(f"stdout_callback break loop with {e}.")
    warning_print(f"exiting stdout_callback ...")
    IS_TERMINATED = True


class TcpShellClient:
    def __init__(self, fil):
        self.cfg_path = fil

    def run(self):
        global SERVER_IP_PORT, SERVER_ENCODING, IS_TERMINATED

        cfg = configparser.ConfigParser()

        # open config.ini
        cfg.read(self.cfg_path)
        assert cfg.has_option("Shell", "ListenIpv4Address")
        assert cfg.has_option("Shell", "ListenPort")
        SERVER_IP_PORT = (cfg.get("Shell", "ListenIpv4Address"),
                          cfg.getint("Shell", "ListenPort"))
        if SERVER_IP_PORT[0].strip() == '0.0.0.0':
            SERVER_IP_PORT = ('127.0.0.1', SERVER_IP_PORT[1])

        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(SERVER_IP_PORT)

        thda = Thread(target=stdout_callback, args=(sk,))
        thda.setDaemon(True)
        thda.start()

        while not IS_TERMINATED:
            try:
                user_input = f"{input()}\n"
                if len(user_input) == 0:
                    break
                # verbose_print(repr(user_input))
                if IS_TERMINATED:
                    break
                input_bytes = convert_str_to_bytes(user_input)
                if IS_TERMINATED:
                    break
                sk.sendall(input_bytes)
            except KeyboardInterrupt:
                break
            except OSError:
                break
            except Exception as e:
                error_print(f"stdin_callback break loop with {repr(e)}.")
                break

        try:
            sk.close()
        except Exception as e:
            error_print(f"close client socket with {e}.")
        thda.join()

        warning_print("bye.")
