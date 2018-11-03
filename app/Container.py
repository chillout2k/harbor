class ContainerException(Exception):
  message = None

  def __init__(self, message):
    self.message = message

class Container:
  uri_prefixes = {} 
  host = {}
  container_type = 'NOT_OVERRIDEN!'
  container_name = 'AbstractContainer'
  container_state = 'UNDEAD'
  # nic = {name: eth0, ips: [ip1, ip2, ...]}
  container_nics = ()

  def __init__(self, uri_prefixes, host_name, name, state, nics):
    if not uri_prefixes:
      raise ContainerException("'uri_prefixes' is mandatory")
    self.uri_prefixes = uri_prefixes
    if not name:
      raise ContainerException("'name' is mandatory!")
    self.container_name = name
    if not state:
      raise ContainerException("'state' is mandatory!")
    self.container_state = state
    self.container_nics = nics
    self.container_type = 'NOT_OVERRIDEN!'
    self.host['href'] = uri_prefixes['hosts'] + '/' + host_name
    self.href = self.host['href'] + '/containers/' + self.container_name
