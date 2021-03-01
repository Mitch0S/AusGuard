from flask import request
import flask, glob, yaml, os, json, hashlib  # API server
import glob  # View all configs
import yaml  # read yaml and send off as credidentials
import os
import json

server_side_key = 'test'

app = flask.Flask(__name__)

example_server = 'DomainName: "example.com"\nProxyTo: "123.123.123.123:25565"\nProxyProtocol: True'


@app.route('/get/', methods=['POST'])
def get_config():
    credidentials = request.headers
    iUsername = (credidentials['Username']).upper()  # i = input
    iPassword = (credidentials['Password']).encode('utf-8')
    iPassword = str(hashlib.sha512(iPassword).hexdigest())  # i = input
    users = open('ausguard.db', 'r+')
    for line in users:
        username, email, password, server, null = line.split(', ')
        username = username.upper()
        if iUsername == username and iPassword == password:
            server = server
            server = (server.replace('.', '_')) + '.yml'
            servers = glob.glob('*.yml')
            if server in servers:
                servers = glob.glob('/proxy/configs/*.yml')
                a_yaml_file = open(server)
                parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
                return (parsed_yaml_file)
            else:
                return 'The server config file is missing, please contact Mitch.'
    return 'Your API credidentials are invalid.'


@app.route('/edit/', methods=['POST'])
def write_config():
    credidentials = request.headers
    iUsername = (credidentials['Username']).upper()  # i = input
    iPassword = (credidentials['Password']).encode('utf-8')
    iPassword = str(hashlib.sha512(iPassword).hexdigest())  # i = input
    db = open('ausguard.db', 'r+')
    for line in db:
        username, email, password, server, null = line.split(', ')
        if iUsername == username and iPassword == password:
            match = True
        else:
            match = 'nup'

    if match:
        server = (server.replace('.', '_')) + '.yml'
        servers = glob.glob('/proxy/configs/*.yml')
        config = open(server, 'w+')
        domain_name = server.replace("_", ".")
        domain_name = domain_name.replace('.yml', '')
        config.truncate(0)
        data = request.json
        config.write(yaml.dump(data))
        config.write('DomainName: ' + domain_name)
        return ('Config Successfully edited.')
    else:
        return 'Your API credidentials are invalid.'



@app.route('/new/', methods=['POST'])
def create_config():
    credidentials = request.headers
    iUsername = (credidentials['Username']).upper()  # i = input
    iPassword = (credidentials['Password']).encode('utf-8')
    iPassword = str(hashlib.sha512(iPassword).hexdigest())  # i = input
    iEmail = (credidentials['Email']).upper()  # i = input
    iServer = (credidentials['Server'])  # i = input
    users = open('ausguard.db', 'r+')
    servers = glob.glob('/proxy/configs/*.yml')
    if len(iUsername) > 16:
        return "Your username exceeds 16 characters."
    for line in users:
        username, email, password, server, null = line.split(', ')
        #print(username, email, password, server)
        file = (iServer.replace('.', '_')) + '.yml'
        if os.path.isfile(file):
            return ('This server already exists.')
        if username == iUsername:
            return 'This Username is taken.'
        if email == iEmail:
            return 'This Email is already in use.'
    file = (iServer.replace('.', '_')) + '.yml'
    db = open('ausguard.db', 'a')
    db.write('\n' + iUsername + ', ' + iEmail + ', ' + iPassword + ', ' + iServer + ', null')
    db.close()
    a = open(file, 'w+')
    a.write(example_server)
    return 'Successfully signed up and created server.'



"""@app.route('/edit_credidentials/', methods=['POST'])
def edit_credidentials():
    credidentials = request.headers
    jsonCredidentials = request.json
    #
    jsonPassword = jsonCredidentials["Password"].encode('utf-8')
    jsonPassword = str(hashlib.sha512(jsonPassword).hexdigest())
    jsonEmail = jsonCredidentials["Email"]
    iUsername = (credidentials['Username']).upper()  # i = input
    iPassword = (credidentials['Password']).encode('utf-8')
    iPassword = str(hashlib.sha512(iPassword).hexdigest())  # i = input
    iEmail = (credidentials['Email']).upper()  # i = input
    iServer = (credidentials['Server'])  # i = input
    users = open('ausguard.db', 'r+')
    #
    for line in users:
        username, email, password, server, null = line.split(', ')
        newline = ('\n' + iUsername + ', ' + jsonEmail + ', ' + jsonPassword + ', ' + iServer + ', null')
        oldline = ('\n' + iUsername + ', ' + iEmail + ', ' + iPassword + ', ' + iServer + ', null')
        if iUsername == username and iEmail == email and iPassword == password:
            line.replace(oldline, newline)
            return ('Successfully edited your account credidentials.')"""




app.run(host='0.0.0.0', port=80)