import threading

from koan_lib.errors import TestError, BuildError, InstallError


class LogReader(threading.Thread):
    def __init__(self, timeout, platform):
        self.timeout = timeout
        self.output = ""
        self.platform = platform
        threading.Thread.__init__(self)

    def run(self):
        # This should be called via threading.
        import subprocess
        import os
        from tempfile import TemporaryFile

        logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               '..', 'log_wrapper', 'logs.py')
        self.logCmd = ['python', logFile, self.platform, '3.8.2']
        with TemporaryFile() as tfile:
            logProcess = subprocess.Popen(
                self.logCmd,
                stdout=tfile,
                stderr=tfile,
                universal_newlines=True
            )
            try:
                logProcess.wait(timeout=self.timeout)
            except subprocess.TimeoutExpired:
                pass
            if logProcess.returncode is None:
                logProcess.terminate()
            tfile.seek(0)
            output = tfile.read()
        if output.__class__ is bytes:
            self.output = output.decode('utf-8')


class Tester(threading.Thread):
    def __init__(self, test):
        import os
        self.test = test['name']
        self.assertions = test['assertions']
        self.projectLocation = '/tmp/koansforpebble/project'
        self.logLocation = os.path.join(self.projectLocation, '..', 'runlogs')
        self.passed = None
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        # This should be called via threading.
        import subprocess
        import sys
        import tempfile
        from koan_lib.logger import Logger
        logger = Logger()
        tmpfile = tempfile.TemporaryFile()
        if self.test[:4] == "emu-":
            self.platform = self.test[4:]

            installCmd = ['pebble', 'install', '--emulator', self.platform]
            logger.log('info', 'Installing to ' + self.platform + '.')
            logger.log('wisdom', '┏━━━━━━━━━━━━━━━━━━━━━ Install Output')
            installProcess = subprocess.Popen(installCmd,
                                              stderr=subprocess.PIPE,
                                              cwd=self.projectLocation)
            try:
                installProcess.wait(timeout=30)
            except subprocess.TimeoutExpired:
                logger.log('fail', 'Install Timeout Expired!!!')
                logger.log('fail', 'If this keeps happening, consider ' +
                           'running `pebble wipe`')
                self.result = InstallError()
            else:
                logger.log('wisdom', '┗━━━━━━━━━━━━━━━━━━━━━ Install Output')
                stderr = installProcess.stderr.read()\
                                              .decode('utf-8').split('\n')
                if stderr != ['']:
                    logger.log('err', '┏━━━━━━━━━━━━━━━━━━━━━ Install Errors')
                    logger.log('err', '\n'.join(stderr))
                    logger.log('err', '┗━━━━━━━━━━━━━━━━━━━━━ Install Errors')
                if 'TimeoutError' in stderr[-1] or\
                   (len(stderr) > 1 and 'TimeoutError' in stderr[-2]):
                    self.result = InstallError('Installer timed out')
                    return
                logger.log('info', 'Installed to ' + self.platform +
                                   ' - Getting logs...')

            if installProcess.returncode != 0:
                self.result = InstallError('Return code nonzero')
                return

            logger.line()
            if installProcess.poll() is None:
                installProcess.kill()

            self.logThread = LogReader(timeout=3, platform=self.platform)
            self.logThread.start()
            self.logThread.join()

            self.assertionsPassed = []
            logger.log('dbg', self.logThread.output)
            for line in self.logThread.output.split('\n'):
                data = line.split()
                if len(data) < 3:
                    pass  # Don't do anything.
                elif data[-2] == 'pass':
                    if data[-1] in self.assertions:
                        self.assertionsPassed.append(data[-1])
                    else:
                        logger.log('warn', 'Huh, weird. ' +
                                           'That test was never registered.')

            if len(self.assertions) == 0:
                logger.log('err', 'No test results found. ' +
                                  'To find out what\'s going wrong, try -v?')
                logger.line()
                self.passed = False
            else:
                allPass = True
                for test in self.assertions:
                    if test in self.assertionsPassed:
                        logger.log('wisdom', ('Test', test, 'passed.'))
                    else:
                        logger.log('err', ('Test', test, 'failed.'))
                        allPass = False
                logger.line()
                self.passed = allPass

            # print('>', self.logThread.output)

            # with open(self.logLocation) as fh:
            #     print("OUT:", fh.read()
        else:
            logger.log('info', ('Unsupported test type', self.test))


class Builder:
    def __init__(self):
        self.tempLocation = '/tmp/koansforpebble/'
        # Location of temporary files.
        self.projectLocation = '/tmp/koansforpebble/project'
        # Location of the temp project
        pass

    def build(self, koanName):
        import subprocess
        import os
        import shutil
        import re
        from koan_lib.koans import Koans
        from koan_lib.logger import Logger
        koans = Koans()
        logger = Logger()

        if not os.path.isdir(self.tempLocation):
            # If the temporary dir doesn't exist, create it.
            os.mkdir(self.tempLocation)

        if os.path.isdir(self.projectLocation):
            shutil.rmtree(self.projectLocation)

        assert os.path.isdir(koans.getKoanDir(koanName))

        shutil.copytree(koans.getKoanDir(koanName), self.projectLocation)

        logger.line()
        logger.log('info', 'Meditating ' + koanName + '...')
        logger.line()

        # Build the project (remember, we moved to the project's directory)
        temp = subprocess.Popen(['pebble', 'build'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=self.projectLocation)
        tempin, tempout = temp.communicate(timeout=30)
        tempout = tempout.decode('utf-8')

        logger.log('dbg', "-" * 30 + "  Dumping raw build info  " + "-" * 30)
        logger.log('dbg', tempout)  # Dump the build log (if running verbosely)

        platform = ''
        platforms = {}
        for x in tempout.split('\n'):
            if 'Start build for' in x:
                platform = str(re.findall('Start build for (.+):', x)[0])
                platforms[platform] = {'problemCount': 0, 'problems': []}
                logger.log('info', ('-> Building', platform.upper()))
            if ('error' in x or 'warning' in x) and x[0] != '[':
                platforms[platform]['problemCount'] += 1
                platforms[platform]['problems'].append(x)

        for platform in platforms.keys():
            if platforms[platform]['problemCount'] != 0:
                logger.line()
                if True in ['error' in problem for
                            problem in platforms[platform]['problems']]:
                    logger.log('err', 'Build errors when building for ' +
                               platform.upper())
                else:
                    logger.log('warn', 'Build warnings when building for ' +
                               platform.upper())
                for problem in platforms[platform]['problems']:
                    logger.log(('err' if 'error' in problem else 'warn'),
                               '-----> ' + problem)

        if temp.returncode != 0:  # If building didn't return 0 (failure)
            logger.line()
            raise BuildError()  # Close.

        # Now that building is done, on to testing!

        testsPass = True

        tests = koans.getTests(koanName)
        # Make sure there's no duplicate tests because then things would break.
        if len(tests) > 0:
            logger.line()
            for test in tests:
                logger.log('wisdom', 'Running test: ' + test['name'])
                logger.line()
                testThread = Tester(test)
                testThread.start()
                testThread.join()
                if testThread.result is not None:
                    raise testThread.result
                if not testThread.passed:
                    testsPass = False
        if not testsPass:
            raise TestError("Tests failed.")
