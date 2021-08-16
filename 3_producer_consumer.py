"""Producer and Consumer Pattern."""


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
from types import TracebackType
from typing import Type


tk_root = tk.Tk()
exception_queue = []
hold_callback_exception = None


class TheSpanishInquisition(IOError):
    pass


def file_io():
    pass
    raise TheSpanishInquisition('Nobody excepts to see the Spanish Inquisition.')
    # raise ValueError(42)


def gui(file_io_op: Callable):
    # Simulate a widget callback.
    tk_root.after(0, file_io_op)


def menu_handler():
    patch_report_callback_exception()
    # This call will raise an exception which will be handled by Tkinter but only after
    #   control has been returned to Tkinter.
    gui(file_io)
    # Schedule work to be done after Tkinter has handled the return from this menu_handler function.
    tk_root.after(0, restore_report_callback_exception)
    tk_root.after(0, consumer)


def consumer():
    try:
        if exception_queue:
            _, val, _ = exception_queue.pop()
            raise val
    except TheSpanishInquisition:
        print(f"I handled TheSpanishInquisition")
    else:
        print(f"No sign of TheSpanishInquisition")
    

def producer(exc: Type[BaseException], val: BaseException, traceback: TracebackType):
    exception_queue.append((exc, val, traceback))
    
    
def patch_report_callback_exception():
    global hold_callback_exception
    hold_callback_exception = tk_root.report_callback_exception
    tk_root.report_callback_exception = producer


def restore_report_callback_exception():
    tk_root.report_callback_exception = hold_callback_exception


def main():
    tk_root.after(0, menu_handler)
    tk_root.after(1000, tk_root.destroy)
    tk_root.mainloop()


if __name__ == '__main__':
    sys.exit(main())
