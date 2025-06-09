import os
import sys
from datetime import datetime

LOGDIR = os.environ.get("LOGDIR", "./log/")


def sterilize_exe(cmd):
    return cmd.replace('.', '_').replace('/', '')


def log(prefix, host, cmd, message, do_print=False):
    ts = datetime.now().isoformat()
    cmd = sterilize_exe(cmd)
    if do_print:
        print(f"[ {ts} ] - {prefix} - {host} - {cmd} :: {message}")
    if message.strip():
        with open(f"{LOGDIR}/{prefix}.{cmd}.{host}.log", "ab", buffering=0) as f:  # noqa: E501
            f.write(f"[ {ts} ] - {message}\n".encode('utf-8'))


def simplog(msg, exename="cmdr"):
    log(exename, "local", sys.argv[0], msg, do_print=True)
