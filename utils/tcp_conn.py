import socket
import json
import time
from utils.logger import get_logger


class TcpConnection:
    def __init__(self, host, port):
        self.conn_timeout = 10
        self.wait_time_to_reconnect = 60
        self.sent_event_number = 0
        self.logger = get_logger()
        self.tcp_host = host
        self.tcp_port = int(port)
        self.set_tcp_conn()

    def set_tcp_conn(self):
        self.close_tcp_conn()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.tcp_host, self.tcp_port))
            self.sock.settimeout(self.conn_timeout)
        except Exception as err:
            self.logger.error('Can not connect to tcp socket. {}'.format(err))
            raise Exception

    def close_tcp_conn(self):
        try:
            self.sock.close()
        except:
            pass

    def send_event(self, event):
        while True:
            try:
                if event:
                    if isinstance(event, dict):
                        event = json.dumps(event, default=str)
                    self.sock.send(event.encode() + b'\n')
                    self.sent_event_number += 1
                break
            except Exception as err:
                self.logger.warning('Can not send event to tcp socket. Sleeping {} seconds. {}'.format(self.wait_time_to_reconnect, err))
                time.sleep(self.wait_time_to_reconnect)
                try:
                    self.close_tcp_conn()
                    self.set_tcp_conn()
                except:
                    pass
                self.send_event(event)
                break
