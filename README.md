# Exception Handling in Tkinter


## Scenario: The File Handler

Consider a scenario where a user wants to carry out a file operation. 
She selects the menu item, completes an input form, clicks an 'Open' button, 
and sits back and waits for the file operation to complete.

Meanwhile, under the hood, the menu item is serviced by a handler function. 
It calls the GUI's input form and supplies the file IO function as a callback. 
When the user clicks the 'Open' button the callback is used to start the actual file operation.

File IO operations can produce exceptions. The handler wrapped the call to the gui in 
a try-except block which could catch and deal with the exception.

Sadly, if the GUI happens to be Tkinter this handler will fail. Python's exception handling patterns 
***will*** work with Tkinter but ***only*** if the try-except statements are located in the correct 
place.

This article explains how to successfully integrate Python's exception patterns and Tkinter.

## Expected and Actual Behaviour.

### Expected Behaviour

See program `1_expected_behaviour`. 

The try-except handler prints the expected messages depending on whether 
function `file_io` raises the handled exception or not.

Unhandled exceptions cause three things to happen:

- The exception is reported: For example `ValueError: 42`.
- A full stack trace is reported from `<module> sys.exit)main())` to `file_io raise ValueError(42)`
- The program terminates immediately and abnormally with exit code 1.

### Actual Behaviour with Tkinter

See program `2_tkinter_behaviour`.

#### Behavior if no exception is raised.

If both of the exceptions in function `file_io` are commented out you'll see this on the console:
- No sign of TheSpanishInquisition
- The `file_io` function started ~200ms after the exception handler had completed. 

The first line of the console output shows the try-except block ran.

In the second line the timer says 
the exception was raised about 200ms after the try_except statements were executed.
(The actual time you see will depend on the speed of your computer.)
It's important to understand that either Python is running or 
Tk/Tcl is running. They cannot run concurrently. 
The call to `file_io` is sitting in Tk/Tcl's event queue. It will stay there until Tk/Tcl is able to run its event loop. That won't happen until Python cedes control to Tk/Tcl and that won't happen until after `menu_handler` has finished.


#### Behavior when an unhandled exception is raised.

If `raise ValueError(42)` is uncommented and the program rerun then that unhandled exception is raised. 

The stack trace is unexpected: It starts with `__call__ return self.func(*args)`and 
ends with `file_io raise ValueError(42)`. The timer reports that the error was raised sometime after the try-except handler had finished. Sometime later the program terminates normally with exit code 0. 

The `else` clause of the try-except handler correctly reports that the expected and handled exception was not encountered.

#### Behaviour when a handled exception is raised.

If the handled exception `TheSpanishInquisition` is uncommented and the program rerun then that exception will be raised instead of `ValueError`. 
The `else` clause of the try_except handler reports that `TheSpanishInquisition` was not raised. 
Tkinter produces an excpetion stack trace which says it was raised.

#### Conclusion

There are two distinct problems:

- Tk/Tcl's event loop can create a race condition which breaks exception handlers.
- For unhandled exceptions Tkinter replaces Python's exception handling 
mechanism with its own inferior version. (See footnote)

### A Model pattern

#### Tkinter threads

To simplify the language of this section I'm going to define a new term "tkinter thread". 
A tkinter thread begins when a callback is invoked from Tk/Tcl's event loop. 
It ends when the Python code has finished running and control is allowed to return to Tk/Tcl.

Using Python code to create tkinter widgets or anything else which places callbacks into the Tk/Tcl 
event queue does not end the tkinter thread.

A tkinter thread has nothing to do with either the threads created using Python's 
threading module or a subprocess created in Python's subprocess module. 
Tkinter threads are created by the tkinter module. Tkinter threads **do not** run concurrently. 

Understanding that Tkinter creates its own threads is crucial to understanding how to write 
correct Tkinter code.

#### A Correctly Designed Exception Handler

See program `5_model_solution.py`

In the present failing case the exception handler is run in one thread. 
That thread completes and control is returned to Tk/Tcl. 
Tk/Tcl starts a second tkinter thread and it is in that thread that the exception is raised. 

In the model solution the try-except handler has been moved from the first thread into the second.

The golden rule is that the exception handler must be in the same Tkinter thread as the exception which it is handling.

#### Footnote: Tkinter's exception handling mechanism.

See program `4_override_call_wrapper.py`.

Tkinter's `class CallWrapper.__call__`  wraps the callback in a try-except block which has a bare `except:`suite. This intercepts and handles exceptions raised in callbacks which were raised and not intercepted within the Tkinter thread.
Tkinter handles the exception by calling `_report_exception()`. This removes the exception from Python's exception stack. 
The removed exception is passed to `report_callback_exception` and that calls 
Python's `traceback. print_exception` to print the exception on stderr. 

It is not clear why TKinter supresses Python's excellent exception handling. Full Python fuctionality can be restored by overriding `CallWrapper` and removing the try-except statements handler. 

`CallWrapper` is marked as a private class although without a leading underscore. No gross problems were noticed as a result of this override although does not preclude the possibility of unseen edge cases. 
