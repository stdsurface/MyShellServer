# -*- coding: utf-8 -*-
from server.TcpShellServer import TcpShellServer
from utility.LogCommon import *
import configparser  # pip install configparser
import sys
import os

if __name__ == "__main__":
    dirname, exename = os.path.split(sys.executable)
    if 'python' in exename.lower():
        dir = os.path.dirname(os.path.realpath(__file__))
    else:
        dir = dirname
    fil = os.path.join(dir, "config.ini")
    cfg = configparser.ConfigParser()

    # open config.ini
    cfg.read(fil)
    assert cfg.has_option("Shell", "Method")
    method = cfg.get("Shell", "Method")

    if method == "Tcp":
        server_instance = TcpShellServer(fil)
        server_instance.run()
    else:
        critical_print(f"Method = `{method}` is unsupported.")
