"""Simulate selection of a menu item using tkinter.

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
from typing import Optional, Callable


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
    # Simulate a widget command by scheduling a call for *later* invocation by the event handler.
    tk_root.after(0, file_io_callback)
    

def menu_handler():
    try:
        gui(file_io)
    except TheSpanishInquisition:
        print(f"I handled TheSpanishInquisition", flush=True)
    else:
        print(f"No sign of TheSpanishInquisition", flush=True)
    finally:
        global try_except_completed
        try_except_completed = time.time()
        
    
def main():
    # Simulate the callback from a menu widget
    tk_root.after(0, menu_handler)
    
    tk_root.after(1000, tk_root.destroy)
    tk_root.mainloop()
    
    delay = int((file_io_started - try_except_completed) * 1e6)
    print(f"The file_io function started {delay}ms after the exception handler had completed.")


if __name__ == '__main__':
    sys.exit(main())
