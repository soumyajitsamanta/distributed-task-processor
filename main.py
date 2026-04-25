# Copyright 2026 Soumyajit Samanta

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import network
import espnow
import json
import socket

# VERSION format = 'YYYY.MM.SEQ', SEQ is the incremented sequentially.
VERSION='2026.4.1'
workers = True

def parseJson(string):
    try:
        return json.loads(string)
    except:
        return None

def performTask(payloadJsonString):
    """
    Given a payload perform a task and resturn a json string to be returned as result.
    Payload format should be like {"action":".....", .....}

    Returns: Result should be valid json string.
    """
    payload = parseJson(payloadJsonString)
    if payload == None:
        return json.dumps({"error":"Could not parse the request sent."})

    action = payload["action"]

    # All handlers for task actions
    if action == 'get_version':
        return json.dumps({"version": VERSION})

    # Default handler when nothing else triggers
    return json.dumps({"result":"UnknownAction", "request": action})

def performConnectWifi(payload_dict, espNowObj, wifiObj):
    ssid = payload_dict["ssid"]
    password = payload_dict["password"]
    if e:
        e.active(False)
    if wifiObj:
        if wifiObj.isconnected():
            wifiObj.disconnect()
        wifiObj.connect(ssid, password)

def performSocketMessageProcess():
    # Start Socket Server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8000))
    s.listen(5)
    
    while True:
        c, addr = s.accept()
        message = c.recv(1000, 0)
        print('Got connection from', addr)
        result = performTask(message)
        c.send(result.encode())
        c.close()

    s.close()

sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True)
e = espnow.ESPNow()
e.active(True)

# For workers only.
while True and workers:
    host, msg = e.recv()
    # msg == None if timeout in recv()
    if msg == None:
        continue
    print(host, msg)
    message_content = parseJson(msg)
    if message_content == None:
        continue
    if message_content["action"] == 'connect_wifi':
        performConnectWifi(message_content, e, sta)
    if message_content["action"] == 'get_version':
        e.add_peer(host)
        e.send(host, json.dumps({"version": VERSION}), False)
    if message_content["action"] == 'start_socket_server':
        performSocketMessageProcess()
        break

# For orchestrator only.
# Insert the peer ids of all boards to be used.
# peers = [b'\x']

# for peer in peers:
#     e.add_peer(peer)

# for peer in peers:
#     e.send(
#         peer,
#         json.dumps({
#             "action":"connect_wifi",
#             "ssid":"SSID",
#             "password":"PASSWORD"})
#     )
#     e.send(
#         peer,
#         json.dumps({"action":"start_socket_server"})
#     )
