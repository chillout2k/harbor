class Host:
  uri_prefixes = {}
  scheme = None
  host = None
  port = None
  href = None

  def __init__(self,uri_prefixes,scheme,host,port):
    self.uri_prefixes = uri_prefixes
    self.scheme = scheme
    self.host = host
    self.port = str(port)
    self.href = uri_prefixes['hosts'] + '/' + self.host

  def get_host(self):
    return self.__dict__ 

  def get_containers(self):
    pass
