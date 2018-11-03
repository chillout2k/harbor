from flask import request
from flask_restful import Resource, Api, abort
import json 

class HarborResource(Resource):
  config = {}
  def __init__(self,config):
    self.config = config
    self.check_trusted_proxy()
    self.check_auth()

  def get_db(self):
    # TODO: Exception-Handling!
    f = open(self.config['db_file'], 'r')
    db = json.load(f)
    f.close()
    return db

  def check_trusted_proxy(self):
    remote_ip = request.remote_addr
    if 'trusted_proxies' not in self.config:
      return True
    for proxy in self.config['trusted_proxies']:
      for trusted_proxy_ip in self.config['trusted_proxies'][proxy]:
        if(remote_ip == trusted_proxy_ip):
          return True
    abort(403, message="Untrusted client IP-address!")

  def check_auth(self):
    if not 'API-KEY' in request.headers:
      abort(400, message="API-KEY header missing!")
    api_key = request.headers['API-KEY']
    if api_key not in self.config['api_keys']:
      abort(401, message="NOT AUTHORIZED!")

class ResAny(HarborResource):
  def get(self):
    return self.get_db()

class ResHosts(HarborResource):
  def get(self):
    return self.config['hosts'] 

class ResHost(HarborResource):
  def get(self, host_name):
    db = self.get_db() 
    if host_name not in db:
      abort(404, message="Host " + host_name + "not found in DB!")
    db[host_name]['containers'] = self.config['uri_prefixes']['hosts'] + '/' + host_name + '/containers'
    return db[host_name]

class ResHostContainers(HarborResource):
  def get(self, host_name):
    db = self.get_db()
    if host_name not in db:
      abort(404, message="Unknown host: " + host_name)
    return db[host_name]['containers']

class ResHostContainer(HarborResource):
  def get(self, host_name, container_name):
    db = self.get_db()
    if host_name not in db:
      abort(404, message="Unknown host: " + host_name)
    for container in db[host_name]['containers']:
      if(container['container_name'] == container_name):
        return container
    abort(404, message="Container " + container_name + 
      " not found on host " + host_name
    )

