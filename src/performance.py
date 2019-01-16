import datetime
import json
import random
import time

import redis
import requests
import threading

def construct_json():
    #  延时运行
    base_time = int(time.time() + 40)
    base_id = 1000000000000000

    def generate_body():
        random.seed(time.time())
        second = random.randrange(0, 10)
        second = 0
        to_run_at = base_time + second
        to_run_str = str(to_run_at)
        nonlocal base_id
        base_id += 1

        d =  {
            "ID": str(base_id),
            "Name": "OncePingTask",
            "ToRunAt": to_run_str,
            "ToRunAfter": "10",
            "Timeout": "1",
            "Url": "http://www.baidu.com"
        }
        return json.dumps(d)
    return generate_body


def send_json_task():
    conn = redis.from_url(url="redis://:uestc12345@127.0.0.1:6379",db=4)
    # p = conn.pubsub(conn)
    generator = construct_json()
    for i in range(0,500):
        conn.publish("remote-task0:messageQ",generator())


def test():
    conn = redis.from_url(url="redis://:uestc12345@127.0.0.1:6379", db=4)
    sub = conn.pubsub()
    p.subscribe("remote-task0:messageQ")
    while True:
        message = p.get_message()
        if message:
            print(message)

        sub.close()



if __name__ == "__main__":
    # t = threading.Thread(target=test,args=())
    # t.start()
    send_json_task()