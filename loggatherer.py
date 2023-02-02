import paramiko
import json
from copy import deepcopy
import os
from sys import platform


def readSettings(file):
    global selfCFG
    global baseDirDict
    baseDirDict=dict()
    if not os.path.exists(file):
        settingTemplate=open(file,'x')
        settingTemplate.write(json.dumps({"baseDirDict":["gateway","toolpack_engine","tbuctwriter"], "tmgIP":"[IP ADDRESS]", "tmgSSHPort":22, "tmgUN":"[USERNAME]", "tmgPW":"[PASSWORD]", "remoteDir":"/lib/tb/toolpack/setup/12358/3.2/apps"}, indent=3))
        print('Please modify the settings file that has just been created: '+file)
        quit()
    else:
        with open('settings.json') as json_file:
            selfCFG=json.load(json_file)
        for i in selfCFG['baseDirDict']:
            baseDirDict.update({i:[]})
    selfCFG['slashDir']='\\' if platform=='win32' else '/'


def paramikoSetup(): #Setup SFTP/SSH Communication
    global sftpTrans
    global sftp
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys() # Load SSH host keys.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Add SSH host key automatically if needed.
    sftpTrans=paramiko.Transport((selfCFG['tmgIP'],selfCFG['tmgSSHPort']))
    sftpTrans.connect(username=selfCFG['tmgUN'],password=selfCFG['tmgPW'])
    sftp = paramiko.SFTPClient.from_transport(sftpTrans)

def makeFolders(folder):
    if not os.path.exists(folder): #make log directory if doesn't exist
        os.makedirs(folder)

def localDirList():
    global localDir
    localDir=os.getcwd()+selfCFG['slashDir']+'logfiles'+selfCFG['slashDir']
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
            relativeDir=i[0].split(selfCFG['slashDir'])
            localLogList[relativeDir[-1]].append(i[2])
            localLogList[relativeDir[-1]]=localLogList[relativeDir[-1]][0]
 
def remoteDirList():
    paramikoSetup()
    global remoteLogList
    remoteLogList=deepcopy(baseDirDict)
    for i in baseDirDict:
        sftp.chdir(path=selfCFG['remoteDir']+'/'+i)
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
        localPget=localDir+i+selfCFG['slashDir']
        remotePget=selfCFG['remoteDir']+'/'+i+'/'
        for ii in grabLogList[i]:
            print('Downloading: '+i+'/'+ii)
            sftp.get(remotePget+ii,localPget+ii)
    sftpTrans.close()

if __name__ == "__main__":
    readSettings('settings.json')
    getGrabbing()
