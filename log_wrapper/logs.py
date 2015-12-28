# This file uses excerpts from the pebble-tool
# code, which is under the following license:

#    The MIT License (MIT)
#
#    Copyright (c) 2015 Pebble Technology
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

import time
import sys
import os
vendorPath = '/usr/local/Cellar/pebble-sdk/4.0/libexec/vendor/lib/python2.7/site-packages'
assert os.path.isdir(vendorPath)
sys.path.append(vendorPath)

toolPath = '/usr/local/Cellar/pebble-sdk/4.0/libexec/lib/python2.7/site-packages/'
assert os.path.isdir(toolPath)
sys.path.append(toolPath)

from pebble_tool.util.logs import PebbleLogPrinter
from pebble_tool.sdk.emulator import ManagedEmulatorTransport
from libpebble2.communication import PebbleConnection
from libpebble2.protocol.system import TimeMessage, SetUTC


class LogPrinter(PebbleLogPrinter):
    def _print(self, packet, message):
        sys.stdout.write(message.encode('utf-8') + '\n')
        sys.stdout.flush()


def connect_emulator(platform, sdk):
    connection = PebbleConnection(ManagedEmulatorTransport(platform, sdk), None)
    connection.connect()
    connection.run_async()
    # Make sure the timezone is set usefully.
    if connection.firmware_version.major >= 3:
        ts = time.time()
        tz_offset = -time.altzone if time.localtime(ts).tm_isdst and time.daylight else -time.altzone
        tz_offset_minutes = tz_offset // 60
        tz_name = "UTC%+d" % (tz_offset_minutes / 60)
        connection.send_packet(TimeMessage(message=SetUTC(unix_time=ts, utc_offset=tz_offset_minutes, tz_name=tz_name)))
    return connection

if __name__ == "__main__":
    emu = connect_emulator(sys.argv[1] or 'aplite', sys.argv[2] or '3.8.2')
    LogPrinter(emu, False).wait()
