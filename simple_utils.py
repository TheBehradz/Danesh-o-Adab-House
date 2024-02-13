from consts import RunningEnviroments

import logging




def get_environment():
  print('Enter environment : prod, dev')
  e = input()
  if e.upper() == RunningEnviroments.PRODUCTION:
    return RunningEnviroments.PRODUCTION
  else:
    return RunningEnviroments.DEVELOPMENT

def init_loggers():
  main_log = logging.getLogger('main_log')
  debug_log = logging.getLogger('debug_log')
  file_handler = logging.FileHandler('main.log')
  file_handler1 = logging.FileHandler('debug.log')
  stream_handler = logging.StreamHandler()
  formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
  file_handler.setLevel(logging.DEBUG)
  file_handler1.setLevel(logging.DEBUG)
  stream_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  file_handler1.setFormatter(formatter)
  stream_handler.setFormatter(formatter)
  main_log.addHandler(file_handler)
  main_log.addHandler(stream_handler)
  debug_log.addHandler(file_handler1)
