import paramiko
from copy import deepcopy
import os

########################################
#### Modify to fit your environment ####
########################################
baseDirDict={'gateway':[],'toolpack_engine':[],'tbuctwriter':[]} #Add keys to include other log files.
remoteDir='/root/test/joshua' #Play Directory

tmgIP='' #Modify this string to your IP
tmgSSHPort='' #Modify this string to your SSH Port
tmgUN='' #Modify this to your Username
tmgPW='' #Modify this to your SSH Password
#remoteDir='/lib/tb/toolpack/setup/12358/3.2/apps' #Real Test
slashDir='\\' #This should change to '/' in a linux machine and '\\' in a windows machine.



def paramikoSetup(): #Setup SFTP/SSH Communication
    global sftpTrans
    global sftp
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys() # Load SSH host keys.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Add SSH host key automatically if needed.
    sftpTrans=paramiko.Transport((tmgIP,tmgSSHPort))
    sftpTrans.connect(username=tmgUN,password=tmgPW)
    sftp = paramiko.SFTPClient.from_transport(sftpTrans)

def makeFolders(folder):
    if not os.path.exists(folder): #make log directory if doesn't exist
        os.makedirs(folder)

def localDirList():
    global localDir
    localDir=os.getcwd()+slashDir+'logfiles'+slashDir
    #Prepare log directories
    makeFolders(localDir)
    for i in baseDirDict:
        makeFolders(localDir+i)

    #Make list of local files
    global localLogList
    localLogList=deepcopy(baseDirDict)
    localLogWalk=os.walk(localDir, topdown=True)
    for i in localLogWalk:
        if(len(i[2])>0):
            relativeDir=i[0].split(slashDir)
            localLogList[relativeDir[-1]].append(i[2])
            localLogList[relativeDir[-1]]=localLogList[relativeDir[-1]][0]
 
def remoteDirList():
    paramikoSetup()
    global remoteLogList
    remoteLogList=deepcopy(baseDirDict)
    for i in baseDirDict:
        sftp.chdir(path=remoteDir+'/'+i)
        relativeDir=i.split('/')
        if relativeDir[-1]=='tbuctwriter':
            templist=sftp.listdir(path='.')
            for i in templist:
                if i[-6:] == 'uct.gz':
                    remoteLogList['tbuctwriter'].append(i)
        else:
            templist=sftp.listdir(path='.')
            for i in templist:
                if i[-6:] == 'log.gz':
                    remoteLogList[relativeDir[-1]].append(i)   

def toGrabList():
    remoteDirList()
    localDirList()            
    global grabLogList
    grabLogList=deepcopy(baseDirDict)
    for i in grabLogList:
        grabLogList[i]=set(remoteLogList[i])-set(localLogList[i])

def getGrabbing():
    toGrabList()
    for i in grabLogList:
        localPget=localDir+i+slashDir
        remotePget=remoteDir+'/'+i+'/'
        for ii in grabLogList[i]:
            print('Downloading: '+i+'/'+ii)
            sftp.get(remotePget+ii,localPget+ii)
    sftpTrans.close()

if __name__ == "__main__":
    getGrabbing()
