import requests, json
from Host import Host
from Container import Container, ContainerException

class LXDContainer(Container):
  def __init__(self, uri_prefixes, host_name, name, state, nics):
    if not name:
      raise ContainerException("'name' is mandatory!")
    self.container_name = name
    if not state:
      raise ContainerException("'state' is mandatory!")
    self.container_state = state
    self.container_nics = nics
    self.host['href'] = uri_prefixes['hosts'] + '/' + host_name
    self.href = self.host['href'] + '/containers/' + name
    self.container_type = 'LXD'

class LXDhostException(Exception):
  message = None
  def __init__(self, message):
    self.message = message

class LXDhost(Host):
  client_crt = None
  client_key = None

  def __init__(self,uri_prefixes,scheme,host,port,client_crt,client_key):
    self.scheme = scheme
    self.host = host
    self.port = str(port)
    self.client_crt = client_crt
    self.client_key = client_key
    self.uri_prefixes = uri_prefixes
    self.href = uri_prefixes['hosts'] + '/' + host

#  def get_host(self):
#    return self.__dict__

  def get_containers(self):
    resp = requests.get(
      self.scheme + '://' + self.host + ':' + self.port + '/1.0/containers', 
      verify=False, 
      cert=(self.client_crt, self.client_key)
    ).text
    resp = json.loads(resp)
    containers = []
    for container in resp['metadata']:
      container_name = container.split('/')[3]
      tmp_cnt = requests.get(
        'https://' + self.host + ':' + self.port + container + "/state", 
        verify=False, 
        cert=(self.client_crt, self.client_key)
      ).text
      tmp_cnt = json.loads(tmp_cnt)
      nics = []
      for nic in tmp_cnt['metadata']['network'].items():
        if nic[0] == "lo":
          continue
        nic_ips = []
        for addr in tmp_cnt['metadata']['network'][nic[0]]['addresses']:
          nic_ips.append(addr['address'])
        nics.append({
          'nic_name': nic[0],
          'nic_ips': nic_ips
        })
      containers.append(LXDContainer(
        self.uri_prefixes,
        self.host,
        container_name,
        tmp_cnt['metadata']['status'],
        nics
      ).__dict__);
    return containers

