# Application settings
DEBUG = False
RESULT_LIMIT = 100

# Don't show transfer and download options
DEMO = True

# Location of where the image data should be downloaded to (Full path!)
IMAGE_FOLDER = '/tmp/images'
# TASKS_DB = 'tasks.db'
REPORT_SHOW_URL = 'http://meqpacscrllt01.uhbs.ch:9000/show?accession_number='

# Solr settings
SOLR_HOSTNAME = 'localhost'
SOLR_CORE_NAME = 'pacs'

# DCMTK settings
DCMIN = '/home/giga/dev/usb/meta/dcm.in'
DCMTK_BIN = '/usr/bin/'

AE_TITLE = 'SNOWFOX'
AE_CALLED = 'AE_ARCH2_4PR'
PEER_ADDRESS = '10.5.66.74'
PEER_PORT = 104
INCOMING_PORT = 11110

TESTING=True

SQLALCHEMY_DATABASE_URI = "sqlite://"
SQLALCHEMY_TRACK_MODIFICATIONS = False

