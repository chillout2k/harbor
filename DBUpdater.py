import os, sys, fcntl, json, signal
from LXC import LXChost, LXChostException
from LXD import LXDhost, LXDhostException

class DBUpdaterException(Exception):
  message = None
  def __init__(self, message):
    self.message = message

class DBUpdater:
  config = {}
  def __init__(self, config):
    self.config = config

  def update_db(self):
    containers = {}
    for host in self.config['hosts']:
      if(host['type'] == 'lxc'):
        try:
          lxchost = LXChost(self.config['uri_prefixes'],
            host['scheme'],host['host'], host['port']
          )
          containers[host['host']] = {
            'self': lxchost.get_host(),
            'containers': lxchost.get_containers()
          }
        except LXChostException as e:
          print(e.message)
      elif(host['type'] == 'lxd'):
        try:
          lxdhost = LXDhost(self.config['uri_prefixes'],
            host['scheme'], host['host'], host['port'],
            host['ccert'], host['ckey']
          )
          containers[host['host']] = {
            'self': lxdhost.get_host(),
            'containers': lxdhost.get_containers()
          }
        except LXDhostException as e:
          print(e.message)
    try:
      f = open(self.config['db_file'], 'w')
      fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
      json.dump(containers, f)
      fcntl.flock(f, fcntl.LOCK_UN)
      f.close()
      # TODO: notify parent to read in new DB!
      #os.kill(os.getppid(), signal.SIGUSR1)
    except:
      print("DB-Updater-EXCEPTION: " + str(sys.exc_info()[0]))
      raise DBUpdaterException(sys.exc_info()[0])

