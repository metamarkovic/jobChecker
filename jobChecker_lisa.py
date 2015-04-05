from pexpect import pxssh
import ConfigParser


class jobChecker():
    config_path = './config.lisa.ini'
    s = pxssh.pxssh()

    def readConfig(self):

        self.config.read(self.config_path)

        self.hostname = self.config.get('Credentials', 'hostname')
        self.username = self.config.get('Credentials', 'username')
        self.password = self.config.get('Credentials', 'password')
        self.email = self.config.get('Credentials', 'email')

        self.command1 = self.config.get('Commands', 'command1')
        self.command2 = self.config.get('Commands', 'command2')

        self.experimentDown = self.config.get('Message', 'experimentDown')
        self.checkerFailed = self.config.get('Message', 'checkerFailed')

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()


    def retrieveOutput(self):
        """Connects to ssh server and inputs commands specified in the config file
        """
        self.readConfig()
        try:
            self.s.login(self.hostname, self.username, self.password)

            self.s.sendline(self.command1)   # run a command
            self.s.prompt()             # match the prompt
            # print self.s.before
            # outputEmpty1 = 'Total Jobs: 0   Active Jobs: 0   Idle Jobs: 0   Blocked Jobs: 0'
            # if outputEmpty1 in output1:
            #     self.errorAlert()

            self.s.sendline(self.command2)   # run a command
            self.s.prompt()             # match the prompt
            print self.s.before
            self.matchIndex()
            # outputEmpty2 = ''
            # if outputEmpty2 in output2:
            #     self.errorAlert()


        except pxssh.ExceptionPxssh, e:
            print "pxssh failed on login."
            print str(e)

    def matchIndex(self):
        index = self.s.getwinsize()
        print index[0]
        print index[1]
        if index[1] < 8:
            self.errorAlert(self.experimentDown)
        else:
            pass

        # except EOF:
        #     self.errorAlert(self.checkerFailed)
        # except TIMEOUT:
        #     self.errorAlert(self.checkerFailed)

    def errorAlert(self, emailSubject):
        """Sends an email if there are no jobs running
        """
        self.s.sendline('date | mail -s "' + emailSubject + '" ' + self.email)
        self.s.prompt()


    def initialize(self):
        self.readConfig()
        self.retrieveOutput()

checker = jobChecker()
checker.initialize()