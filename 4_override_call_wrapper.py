"""Monkey patch tkinter's CallWrapper.

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
import time
import tkinter as tk
from collections.abc import Callable
from typing import Optional


tk_root = tk.Tk()
try_except_completed: Optional[time.time] = None
file_io_started: Optional[time.time] = None


class TheSpanishInquisition(IOError):
    pass


def file_io():
    global file_io_started
    file_io_started = time.time()
    
    raise TheSpanishInquisition('Nobody excepts to see the Spanish Inquisition.')
    # raise ValueError(42)


def gui(file_io_callback: Callable):
    # Simulate a widget callback.
    tk_root.after(0, file_io_callback)
    

def menu_handler():
    try:
        gui(file_io)
    except TheSpanishInquisition:
        print(f"I handled TheSpanishInquisition")
    else:
        print(f"No sign of TheSpanishInquisition")
    finally:
        global try_except_completed
        try_except_completed = time.time()


class MyCallWrapper:
    """Internal class. Stores function to call when some user
    defined Tcl function is called e.g. after an event occurred.
    
    THis has been copied from tkinter.__init__.py. The exception handling mechanism has been removed.
    """

    def __init__(self, func, subst, widget):
        """Store FUNC, SUBST and WIDGET as members."""
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        """Apply first function SUBST to arguments, than FUNC."""
        if self.subst:
            args = self.subst(*args)
        return self.func(*args)


tk.CallWrapper = MyCallWrapper


def main():
    tk_root.after(0, menu_handler)
    tk_root.after(1000, tk_root.destroy)
    tk_root.mainloop()

    delay = int((file_io_started - try_except_completed) * 1e6)
    print(f"The file_io function started {delay}ms after the exception handler had completed.")


if __name__ == '__main__':
    sys.exit(main())
