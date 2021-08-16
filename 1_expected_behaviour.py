"""Throw and catch an exception.

The code is arranged in the same manner as would be found in a gui environment with a menu,
a menu handler module, a gui module, and a file IO module.
"""


#  Copyright ©2021. Stephen Rigden.
#  Last modified 8/16/21, 7:29 AM by stephen.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from collections.abc import Callable


class TheSpanishInquisition(IOError):
    pass


def file_io():
    pass
    raise TheSpanishInquisition('Nobody excepts to see the Spanish Inquisition.')
    # raise ValueError(42)


def not_tkinter(file_io_callback: Callable):
    file_io_callback()


def menu_handler():
    try:
        not_tkinter(file_io)
    except TheSpanishInquisition:
        print(f"I handled TheSpanishInquisition")
    else:
        print(f"No sign of TheSpanishInquisition")


def main():
    menu_handler()


if __name__ == '__main__':
    sys.exit(main())
