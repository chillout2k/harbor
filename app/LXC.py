import requests
import json
from Host import Host
from Container import Container, ContainerException

class LXCContainer(Container):
  def __init__(self, uri_prefixes, host_name, name, state, nics):
    if not name:
      raise ContainerException("'name' is mandatory!")
    self.container_name = name
    if not state:
      raise ContainerException("'state' is mandatory!")
    self.container_state = state
    self.container_nics = nics
    self.container_type = 'LXC'
    self.host['href'] = uri_prefixes['hosts'] + '/' + host_name
    self.href = self.host['href'] + '/containers/' + self.container_name

class LXChostException(Exception):
  message = None
  
  def __init__(self, message):
    self.message = message

class LXChost(Host):
#  def __init__(self,uri_prefixes,scheme,host,port):
#    self.scheme = scheme
#    self.host = host
#    self.port = str(port)
#    self.uri_prefixes = uri_prefixes
#    self.href = uri_prefixes['hosts'] + '/' + self.host
  
#  def get_host(self):
#    return self.__dict__

  def get_containers(self):
    try:
      uri = self.scheme + '://' + self.host + ':' + self.port + '/api/v1/containers'
      resp = requests.get(uri).text
      resp = json.loads(resp)
      containers = []
      for container in resp:
        containers.append(LXCContainer(
          self.uri_prefixes,
          self.host,
          container['container_name'],
          container['container_state'],
          container['container_nics']
        ).__dict__)
      return containers
    except:
      ex = str(sys.exc_info())
      print("LXChost Exception: " + ex)
      raise LXChostException(ex)

