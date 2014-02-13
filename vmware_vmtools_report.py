#!/usr/bin/python
import logging, csv, sys, re, getpass, argparse, subprocess
from pysphere import MORTypes, VIServer, VITask, VIProperty, VIMor, VIException
from pysphere.vi_virtual_machine import VIVirtualMachine

def print_verbose(message):
        if verbose:
                print message
def set_dir():
	if directory: 
		return directory
	else:
		return '/tmp'
def set_filename():
	if filename:
		return filename
	else:
		csvfile = raw_input("csv filename: ")
		return csvfile

def get_admin(annotation):
        if annotation == "":
		return "No annotations found"
	else:
		vmadminemail = re.findall(r'[\w\.-]+@', annotation)
		if vmadminemail:
			return vmadminemail[0]
		else:
			return "No VM admin"

def write_vmw_tools(con, logger, c, cnt):
    # List properties to get
    property_names = ['name', 'guest.toolsVersion', 'config.files.vmPathName','config.annotation']
    try:
        logger.debug('Retrieving properties %s' % property_names )
        properties = con._retrieve_properties_traversal(property_names=property_names, obj_type="VirtualMachine")

        for propset in properties:
        	name = ""
        	tools_version = ""
        	path = ""
        	admin = ""
        	ann = ""
        	for prop in propset.PropSet:
        		if prop.Name == "name": 
        			name = prop.Val
        		elif prop.Name == "guest.toolsVersion": 
        			tools_version = prop.Val
        		elif prop.Name == "config.files.vmPathName": 
        			path = prop.Val
        		elif prop.Name == "config.annotation":
        			ann = prop.Val
	
        	admin = get_admin(ann)

        	if tools_version == "":
        		tools_version = "No tools installed"
        		if notools:
                    		if cnt is not None:
                               	    cnt.writerow([name, path, tools_version, admin])
                    		else:
                        	    logger.error('Somehow CSV writer is not available.')
                          	    return
            	if c is not None:
                   c.writerow([name, path, tools_version, admin])
        	   logger.debug(name+path+tools_version+admin)
                else:
                   logger.error('Somehow CSV writer is not available.')
                   return            
    except VIException as e:
        logger.error(e)
        return
        
def get_args():
    parser = argparse.ArgumentParser(description="Prints report of VMware tools version installed. ")
    parser.add_argument('-s', '--server', nargs=1, required=True, help='The vCenter or ESXi server to connect to', dest='server', type=str)
    parser.add_argument('-u', '--user', nargs=1, required=True, help='The username with which to connect to the server', dest='username', type=str)
    parser.add_argument('-p', '--password', nargs=1, required=False, help='The password with which to connect to the host. If not specified, the user is prompted at runtime for a password', dest='password', type=str)
    parser.add_argument('-n', '--notools', required=False, help='No VMware Tools isntalled into separate file.', dest='notools', action='store_true')
    parser.add_argument('-D', '--dir', required=False, help='Written file(s) into a specific directory.', dest='directory', type=str)
    parser.add_argument('-f', '--filename', required=False, help='File name. If not set, will be asked.', dest='filename', type=str)
    parser.add_argument('-v', '--verbose', required=False, help='Enable verbose output', dest='verbose', action='store_true')
    parser.add_argument('-d', '--debug', required=False, help='Enable debug output', dest='debug', action='store_true')
    parser.add_argument('-l', '--log-file', nargs=1, required=False, help='File to log to (default = stdout)', dest='logfile', type=str)
    parser.add_argument('-V', '--version', action='version', version="%(prog)s (version 0.2)")
	
    args = parser.parse_args()
    return args
    
# Parsing values
args = get_args()
argsdict = vars(args)
server 		= args.server[0]
username 	= args.username[0]
verbose		= args.verbose
debug		= args.debug
log_file	= None
password 	= None
notools 	= args.notools
directory	= args.directory
filename 	= args.filename

# Setting output filename
csvfile = set_filename()

# Setting output directory 
dir = set_dir()

if args.password:
	password = args.password[0]

if args.logfile:
        log_file = args.logfile[0]
# Logging settings
if debug:
	log_level = logging.DEBUG
elif verbose:
	log_level = logging.INFO
else:
	log_level = logging.WARNING
    
# Initializing logger
if log_file:
	logging.basicConfig(filename=log_file,format='%(asctime)s %(levelname)s %(message)s',level=log_level)
else:
	logging.basicConfig(filename=log_file,format='%(asctime)s %(levelname)s %(message)s',level=log_level)
	logger = logging.getLogger(__name__)
logger.debug('logger initialized')

# CSV formating file & Formatting
c = None
cnt = None
try:
    csv_header = ["VM Name", "Datastore Path", "Vmware Tools Version", "Admin"]
    c = csv.writer(open(dir+"/"+csvfile+".csv", "wb"))
    c.writerow(csv_header)
    pass
except IOException as e:
    logger.error(e)
    sys.exit()
    
# Enable additional file if "notools" flag is set
try:
    if notools:
	    cnt = csv.writer(open(dir+"/"+csvfile+"-notools.csv","wb"))
            cnt.writerow(csv_header)
    	    pass
except IOException as e:
    logger.error(e)
    sys.exit()

# Asking Users password for server
if password is None:
	logger.debug('No command line password received, requesting password from user')
        password = getpass.getpass(prompt='Enter password for vCenter %s for user %s: ' % (server,username))

# Connecting to server
logger.info('Connecting to server %s with username %s' % (server,username))

con = VIServer()
try:
	logger.debug('Trying to connect with provided credentials')
	con.connect(server,username,password)
	logger.info('Connected to server %s' % server)
	logger.debug('Server type: %s' % con.get_server_type())
	logger.debug('API version: %s' % con.get_api_version())
except VIException as ins:
	logger.error(ins)
	logger.debug('Loggin error. Program will exit now.')
	sys.exit()

# getting report
write_vmw_tools(con, logger, c, cnt)
logger.warning("Written CSV file to %s " %dir)

#disconnecting
try:
   con.disconnect()
   logger.info('Disconnected to server %s' % server)
except VIException as e:
   logger.error(e)
