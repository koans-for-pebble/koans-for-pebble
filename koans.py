# -*- coding: latin-1 -*-

# Copyright (c) 2015 Johannes Neubrand
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function

# -------------------------- Initial Setup -----------------------------------

import sys
try:
    assert sys.hexversion >= 0x03030000
except AssertionError as e:
    print("Python version too low. Requires 3.3 or later.")
    raise SystemExit()  # Close.


class Sensei:
    def evaluateStudent(self, verbosity=0):
        import os

        from koan_lib.koans import Koans
        from koan_lib.errors import BuildError
        from koan_lib.errors import TestError
        from koan_lib.builder import Builder
        from koan_lib.logger import Logger
        from koan_lib.wisdoms import Wisdom

        pebbleBinLocation = '/usr/local/bin/pebble'
            # Location of the pebble launcher.
        logger = Logger(verbosity)
        koans = Koans()
        thiskoan = koans.getNextSolvable()
        builder = Builder()
        koans.unsolveAll()

        logger.log('dbg', 'Running in verbose mode.')

        # ------------- Make sure that pebble is installed. ------------------
        try:
            assert os.path.exists(pebbleBinLocation)  # Pebble installed via homebrew
        except AssertionError as e:
            logger.log('err', "pebble-tool not found! Checked at " + pebbleBinLocation)
            raise SystemExit()  # Close.

        pebblePath = ''

        with open(pebbleBinLocation) as pebbleBin:
            data = pebbleBin.read()
            paths = data.split('"')[1].split(':')
            if 'vendor' in paths[0]:
                pebblePath = paths[1]
            else:
                pebblePath = paths[0]

        # -------------------- Check the tool version. -----------------------

        # Find the `version.py` file
        versionLoc = os.path.join(pebblePath, 'pebble_tool', 'version.py')

        # Execute the version file against a dictionary called `variables`.
        variables = {}
        with open(versionLoc) as versionFile:
            exec(versionFile.read(), variables)
        # The pebble-tool version is stored in `variables['version_base']`
        tool_version = (variables['version_base'])

        try:
            assert tool_version[0] >= 4  # Version should be above 4.0
        except AssertionError as e:
            logger.log('err', "Upgrade your pebble-tool! Current version is", tool_version)
            logger.log('err', "                          Minimum version is", (4, 0, 0))
            raise SystemExit()  # Close.

        # ----------------------- Actual building. ---------------------------

        try:
            i = 0
            while koans.getNextSolvable() is not None:
                i += 1
                if i > 100:
                    # If something crazy is going on
                    logger.log('dbg', 'Maximum reached.')
                thiskoan = koans.getNextSolvable()
                builder.build(thiskoan)
                logger.log('pass', '                                 ')
                logger.log('pass', '  Your Meditation was fruitful.  ')  # Tell the user that
                logger.log('pass', '                                 ')  # the build passed :D
                logger.line()
                koans.setSolved(thiskoan)
                solved = koans.getSolvedAmount()
                logger.log('normal', 'Solved: ' + str(solved[0]) + ' of ' + str(solved[1]) +
                           '. Meditate ' + (koans.getNextSolvable() or
                                            'about something else') + '.')
                logger.line()
                logger.log(('wisdom' if koans.getNextSolvable() else 'experience'),
                           (Wisdom().getWisdom()
                            if koans.getNextSolvable() else
                            Wisdom().getExperience()))
                logger.line()
                if koans.getNextSolvable() is not None:
                    logger.log('normal', '-=' * 30 + '-')
        except (BuildError, TestError) as e:
            if e.__class__ == BuildError:
                logger.log('fail', '                    ')
                logger.log('fail', '  Building failed.  ')
                logger.log('fail', '                    ')
            elif e.__class__ == TestError:
                logger.log('fail', '                   ')
                logger.log('fail', '  Testing failed.  ')
                logger.log('fail', '                   ')
            elif e.__class__ == TestError:
                logger.log('fail', '                     ')
                logger.log('fail', '  Something failed.  ')
                logger.log('fail', '                     ')
            logger.line()
            solved = koans.getSolvedAmount()
            logger.log('normal', 'Solved: ' + str(solved[0]) + ' of ' + str(solved[1]) +
                       '. Meditate ' + koans.getNextSolvable() + '.')
            logger.line()
            logger.log('wisdom', Wisdom().getFailure())
            logger.line()

        if thiskoan is None:
            logger.line()
            logger.log('win', '                              ')
            logger.log('win', '  There is nothing to solve.  ')  # Tell the user that
            logger.log('win', '                              ')  # the build passed :D
            logger.line()
            solved = koans.getSolvedAmount()
            logger.log('normal', 'Solved: ' + str(solved[0]) + ' of ' + str(solved[1]) +
                       '. Meditate about something else.')
            logger.line()
            logger.log('experience', Wisdom().getExperience())
            logger.line()

import argparse

parser = argparse.ArgumentParser(description='Learn the ways of C and Pebble\'s SDK!')
parser.add_argument('-v', '--verbose', action='count')
args = parser.parse_args()

sensei = Sensei()
sensei.evaluateStudent(verbosity=args.verbose)
