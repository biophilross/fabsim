import os, sys

user = os.getlogin()
userPath = '/home/' + user

print 'Pick a username: '
username = raw_input()
print 'Please provide an email: '
email = raw_input()

def checkForRootAccess():
  if not os.geteuid() == 0:
    sys.exit("root access required to run this script\n")

def installPackages():
  os.system('sudo apt-get install git')
  os.system('sudo apt-get install xclip')
  os.system('sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose')

def getSSHKey():
  sshKeyPath = userPath + '/.ssh'
  if not os.path.exists(sshKeyPath):
    os.system('mkdir ' + sshKeyPath)
  if not (os.path.exists(sshKeyPath + '/id_rsa.pub') or os.path.exists(sshKeyPath + '/id_dsa.pub')):
    os.system('ssh-keygen -t rsa -C "' + email + '"')

def gitSetup():
  os.system('git config --global user.name "' + username + '"') 
  os.system('git config --global user.email ' + email)
  os.system('xclip -sel clip < ~/.ssh/id_rsa.pub')
  print 'please add add your ssh key to git hub\n'
  print 'directions can be found in step 3 and 4 at https://help.github.com/articles/generating-ssh-keys\n'
  print 'your key should already be in your clipboard' 
  print 'please press enter to continue'
  entered = raw_input()

def cloneRepo():
#  os.system('git clone git@github.com:thephilross/fabsim.git')
  os.system('ssh -T git@github.com')
 
def main():
  checkForRootAccess()
  installPackages()
  getSSHKey()
  gitSetup()
  cloneRepo()

main()
