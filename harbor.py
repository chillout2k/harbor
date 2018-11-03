#!/usr/bin/python3

import argparse, os, sys, fcntl, time, signal, json
from flask import Flask
from flask_restful import Api
from DBUpdater import DBUpdater, DBUpdaterException
from Resources import ResAny,ResHosts,ResHost,ResHostContainers,ResHostContainer

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', required=True, help="Path to config file")
  args = parser.parse_args()

  config = {}
  try:
    with open(args.config, 'r') as f:
      config = json.load(f)
    f.close()
  except:
    print("CONFIG-FILE-Exception: " + str(sys.exc_info()))
    sys.exit(1) 

  dbupdater_pid = os.fork()
  if(dbupdater_pid == 0):
    # Child: DB-Updater
    db_updater = DBUpdater(config)
    while True:
      db_updater.update_db()
      time.sleep(config['db_updater']['update_interval'])
  else:
    # Parent: Harbor-API
    try:
      app = Flask(__name__)
      api = Api(app)
      api.add_resource(ResHosts,
        '/api/v1/hosts',
        resource_class_kwargs={'config': config}
      )
      api.add_resource(ResHost, 
        '/api/v1/hosts/<host_name>',
        resource_class_kwargs={'config': config}
      )
      api.add_resource(ResHostContainers, 
        '/api/v1/hosts/<host_name>/containers',
        resource_class_kwargs={'config': config}
      )
      api.add_resource(ResHostContainer, 
        '/api/v1/hosts/<host_name>/containers/<container_name>',
        resource_class_kwargs={'config': config}
      )
      api.add_resource(ResAny, 
        '/api/v1/',
        resource_class_kwargs={'config': config}
      )
      # SIGUSR1 handler nach Fork
#      signal.signal(signal.SIGUSR1, handle_sigusr1)
      app.run(debug=False, 
        host=config['daemon']['listen_host'], 
        port=config['daemon']['listen_port']
      )
    except:
      print("MAIN-EXCEPTION: " + str(sys.exc_info()))
      # Destroy child process
      os.kill(dbupdater_pid, signal.SIGTERM)

