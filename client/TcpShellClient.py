# -*- coding: utf-8 -*-
import socket
from chardet import detect
from threading import Thread
import configparser
from utility.LogCommon import *

SERVER_IP_PORT = None
SERVER_ENCODING = 'utf-8'
SERVER_ENCODING_CONFIDENCE = 0.0
IS_TERMINATED = False
MAX_CAPACITY = 256
CHARACTER_BUFFER = b''
BYTES_REMAINING = b''


def update_server_encoding(line_with_newline):
    global CHARACTER_BUFFER, SERVER_ENCODING, SERVER_ENCODING_CONFIDENCE
    if len(CHARACTER_BUFFER) >= MAX_CAPACITY:
        CHARACTER_BUFFER += line_with_newline
        try:
            dicts = detect(CHARACTER_BUFFER)
            encod = dicts["encoding"]
            confi = dicts["confidence"]
            if encod == None or encod == 'ascii':
                encod = 'utf-8'
        except:
            encod = 'utf-8'
            confi = 0.0
        if encod != SERVER_ENCODING:
            verbose_print('changing encoding: {} -> {} ({} -> {})'.format((SERVER_ENCODING), (encod), (SERVER_ENCODING_CONFIDENCE), (confi)), end='')
            SERVER_ENCODING = encod
            SERVER_ENCODING_CONFIDENCE = confi
        CHARACTER_BUFFER = b''
    else:
        CHARACTER_BUFFER += line_with_newline


def split_and_update(barr):
    global BYTES_REMAINING
    assert len(barr) > 0
    arr = barr.split(b'\n')
    if len(arr) == 1:
        BYTES_REMAINING += arr[0]
    else:
        arr[0] = BYTES_REMAINING + arr[0]
        for idx in range(0, len(arr)-1):
            update_server_encoding(arr[idx]+b'\n')
        BYTES_REMAINING = arr[-1]


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
            split_and_update(b)
            bs = convert_bytes_to_str(b)
            print(bs, end='')
    except OSError:
        pass
    except Exception as e:
        error_print("stdout_callback break loop with {}.".format((e)))
    warning_print("exiting stdout_callback ...".format())
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
                user_input = "{}\n".format((input()))
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
                error_print("stdin_callback break loop with {}.".format((repr(e))))
                break

        try:
            sk.close()
        except Exception as e:
            error_print("close client socket with {}.".format((e)))
        thda.join()

        warning_print("bye.")
