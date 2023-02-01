# TB Log Gatherer

This script is made to assist users of TelcoBridges' Tmedia products, including the TSG devices, the TMG devices, and of course the ProSBC.


## WHAT IT DOES
This script is meant to be run from a remote device to connect to the TMedia Product. 

This script will check log folders of tbtoolpack apps, compare them with the logs saved on the local device, and download all new files.

This script will perform these functions via SFTP

This script will wait until a log is in a `*.log.gz` format for all logs with an exception of tbuctwriter

This script will only collect `*.uct.gz` logs from tbuctwriter.  



## HOW TO USE
When you run this script for the first time it will create a file 'settings.json' in the home directory.
You must modify this file to configure the Log Gatherer.

This .json file consists of keys and values in the following format

`{ 'key1' : 'value1' , 'key2' : 'value2'}`

*Note the colon seperates a key from a value, and the comma seperates different key:value pairs.*

The key names are essential to the functioning of the app and should not be modified, though their order does not matter as long as they are coordinated with the correct values.

Currently there are 7 configuration settings and all fields are mandetory, below is a description of each one and an example of what should be put in it.

1. **baseDirDict** is a *list* of directories the script will check to collect logs, the entire list should be enclosed in square brackets `[]` also each directory should be enclosed in quotation marks and seperated by a comma. Valid directories are as follows:
   - ```
        gateway
        tbdebug
        tblogtrace
        tboamapp
        tbrouter
        tbsigtrace
        tbsip
        tbsnmpagent
        tbstreamserver
        tbsyslog
        tbtelnetdump
        tbuctwriter
        toolpack_engine
        toolpack_sys_manager```

1. **tmgIP** is a *string* of an ip address. The IP Address should be enclosed in quotation marks such as `"127.0.0.1"`

1. **tmgSSHPort** is an *integer* is the port for SSH/SFTP communication, this integer should be entered without quotation marks.

1. **tmgUN** is a *string* for the sftp username to your device, which should be enclosed in quotes.

1. **tmgPW** is a *string* for the sftp password to your device, which should be enclosed in quotes.

1. **remoteDir** is a *string* for the application directory of tbtoolpack, which should be enclosed in quotes.
   - *Note it can be found by enterering `tbsetup` on your device and printing the working directory with `pwd`*

1. **slashDir** is a *string* for direction of the slashes on the local filesystem. There are only two possible values:
   - `"\\"` for Windows or NT Machines, double slashes are needed to escape the escape character.
   - `"/"` for Unix devices.

## EXAMPLE settings.json FILE
```
{
   "baseDirDict": [
      "gateway",
      "toolpack_engine",
      "tbuctwriter"
   ],
   "tmgIP": "192.168.50.155",
   "tmgSSHPort": 22,
   "tmgUN": "sftpusr",
   "tmgPW": "s3cUr1ty15m3",
   "remoteDir": "/lib/tb/toolpack/setup/12358/3.2/apps",
   "slashDir": "\\"
}
```
