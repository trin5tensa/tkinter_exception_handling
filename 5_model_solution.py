"""A Model Pattern for Exception Handling with Tkinter.

The code is arranged in the same manner as would be found in a gui environment with a menu,
a menu handler module, a gui module, and a file IO module.
"""

#  Copyright ©2021. Stephen Rigden.
#  Last modified 8/16/21, 7:30 AM by stephen.
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
import tkinter as tk
from collections.abc import Callable


tk_root = tk.Tk()


class TheSpanishInquisition(IOError):
    pass


def file_io():
    """Part of Tkinter thread 2"""
    pass
    raise TheSpanishInquisition('Nobody excepts to see the Spanish Inquisition.')
    # raise ValueError(42)
    # End Tkinter thread 2 and return control to Tk/Tcl via Tkinter


def menu_handler_callback():
    """Part of Tkinter thread 2"""
    try:
        file_io()
    except TheSpanishInquisition:
        print(f"I handled the TheSpanishInquisition")
    else:
        print(f"No sign of TheSpanishInquisition")


def gui(file_io_callback: Callable):
    """Part of Tkinter thread 1"""
    # Schedule a call which will start Tkinter thread 2
    tk_root.after(0, file_io_callback)
    # End Tkinter thread 1 and return control to Tk/Tcl via Tkinter


def menu_handler():
    """Part of Tkinter thread 1"""
    gui(menu_handler_callback)


def main():
    # Schedule a call which will start Tkinter thread 1
    tk_root.after(0, menu_handler)
    
    tk_root.after(1000, tk_root.destroy)
    tk_root.mainloop()


if __name__ == '__main__':
    # Trying to pass 'None' to sys.exit has stopped working for reasons which have not yet been discovered.
    # sys.exit(main())
    
    main()
    # Tk does not relinquish control unless sys.exit runs. (Not clear if it is tkinter, Tk, or Tcl)
    sys.exit()
