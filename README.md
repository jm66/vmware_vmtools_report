vmware_vmtools_report
=====================

Another pysphere implementation to get a report of the VMware Tools package in each Virtual Machine. 
The script takes several arguments from the command line, such as server, username, 
password (not required), destination directory, filename of the report and finally verbose, 
debug,  and if set output to an specific log. Sorry, it is certainly better to show the help message:

``` bash
./vmware_vmtools_report.py -h
usage: vmware_vmtools_report.py [-h] -s SERVER -u USERNAME [-p PASSWORD] [-n]
                                [-D DIRECTORY] [-f FILENAME] [-v] [-d]
                                [-l LOGFILE] [-V]

Prints report of VMware tools version installed.

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        The vCenter or ESXi server to connect to
  -u USERNAME, --user USERNAME
                        The username with which to connect to the server
  -p PASSWORD, --password PASSWORD
                        The password with which to connect to the host. If not
                        specified, the user is prompted at runtime for a
                        password
  -n, --notools         No VMware Tools isntalled into separate file.
  -D DIRECTORY, --dir DIRECTORY
                        Written file(s) into a specific directory.
  -f FILENAME, --filename FILENAME
                        File name. If not set, will be asked.
  -v, --verbose         Enable verbose output
  -d, --debug           Enable debug output
  -l LOGFILE, --log-file LOGFILE
                        File to log to (default = stdout)
  -V, --version         show program's version number and exit
```
For instance, you can simply run the script with the minimum input parameters:

``` bash
./vmware_vmtools_report.py -s 192.100.200.192 -u vma -n -D `pwd` -f vmware_tools-2014-02-13 
Enter password for vCenter 192.100.200.192 for user vma: 
2014-02-13 16:09:35,776 WARNING Written CSV file to /home/vi-admin/scripts/pysphere
```

More info in my [blog] (http://jose-manuel.me/2014/02/reporting-vmware-tools-version-installed-vmware_vmtools-py/) 
