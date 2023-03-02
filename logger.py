# Logging allows you to maintain a record of how
# your program is working.
# setLevel determines what is saved to the logfile
# and what is ignored.


import logging
from datetime import datetime as dt

# This configuration can be done once in the program
logging.basicConfig(filename='logger.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# Get the logger at the top of each module where it is used
logger = logging.getLogger('__name__')
logger.setLevel(logging.WARNING)

# Example messages
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
