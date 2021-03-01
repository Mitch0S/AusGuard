import requests
import socket
import time


###############   FOR CLOUDFLARE API INTEGRATION   ###################
authEmail = ''
authKey = ''
ZONE = ''
Australia = ['PERTH', 'SYDNEY', 'BRISBANE', 'MELBOURNE', 'ADELAIDE']
location = 'PERTH'
######################################################################


########   FOR HOST PINGING INTEGRATION   ##########
port = 25565
retry = 1               # Amount of times to retry the ping
delay = 1              # Seconds
timeout = 1            # Seconds
ping_list_interval = 1  # Seconds
####################################################



TITLE = '''
   ________  _____    ____  ____  _______    _   __
  / ____/ / / /   |  / __ \/ __ \/  _/   |  / | / /
 / / __/ / / / /| | / /_/ / / / // // /| | /  |/ / 
/ /_/ / /_/ / ___ |/ _, _/ /_/ // // ___ |/ /|  /  
\____/\____/_/  |_/_/ |_/_____/___/_/  |_/_/ |_/                                                      
                                v0.3 by Mitch0S     
---------------------------------------------------\n'''

print(TITLE, '\n\n')


if location.upper() in Australia:
    country = 'au'
    location = location.lower()
else:
    country = 'nz'

IPS = open("hosts.txt", "r+")

def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def checkHost(IP, port):
        ipup = False
        for i in range(retry):
            if isOpen(ip, port):
                    ipup = True
                    break
            else:
                    time.sleep(delay)
        return ipup

while True:
    IPS = open("hosts.txt", "r+")
    try:
        for line in IPS:
           ip, status = line.split(', ')
           ip = ip.rstrip()
           status = status.rstrip()
           if not checkHost(ip, port) and status == 'offline':  # If status is offline and node is down
               a = ""

           if checkHost(ip, port) and status == 'offline':                        # If status is offline and node is up
               print(ip, 'Is now online, adding to the load balancer.')
               get_zone_domain = 'GET zones/:' + ZONE + '/dns_records'

               url = 'https://api.cloudflare.com/client/v4/zones/' + ZONE + '/dns_records'
               headers = {'X-Auth-Email': authEmail,
                          'X-Auth-Key': authKey,
                          'Content-Type': 'application/json'
                          }

               json = {
                   "type": "A",
                   "name": country + '.ipv4.' + location + '.',
                   'content': ip,
                   'ttl': 1,
                   'priority': 0,
                   'proxied': False
               }
               requests.post(url, headers=headers, json=json)

               replace = (ip + ', ' + status)
               replaceWith = (ip + ', online')

               with open("hosts.txt") as f:
                   newText = f.read().replace(replace, replaceWith) ###################

               with open("hosts.txt", "w") as f:
                   f.write(newText)

           if not checkHost(ip, port) and status == 'offline':  # If status is online and node is online
               a = ""

           if not checkHost(ip, port) and status == 'online':                 # If status is online and node is down
               print(ip, 'is offline, removing from load balancer.')
               find_record = 'https://api.cloudflare.com/client/v4/zones/' + ZONE + '/dns_records?type=A&content=' + ip
               delete_url = 'https://api.cloudflare.com/client/v4/zones/' + ZONE + '/dns_records/'

               headers = {'X-Auth-Email': authEmail,
                          'X-Auth-Key': authKey,
                          'Content-Type': 'application/json'
                          }

               payload = requests.get(find_record, headers=headers).json()
               id = payload["result"][0]["id"]
               id = id.strip()
               x = requests.delete(delete_url + id, headers=headers)
               replace = (ip + ', ' + status)
               replaceWith = (ip + ', offline')

               with open("hosts.txt") as f:
                   newText = f.read().replace(replace, replaceWith)

               with open("hosts.txt", "w") as f:
                   f.write(newText)


    except Exception as e:
        print(e)

    IPS = open("hosts.txt", "rt")
    time.sleep(ping_list_interval)