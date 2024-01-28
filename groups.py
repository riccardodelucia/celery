from tasks import print_task, raise_exception, error_handler, error_handler_1, error_handler_2, add, mul
from celery import group

msg = "########### Groups ###########"
print_task.delay(msg)
print(msg)
msg = "1 - simple tasks group"
print_task.delay(msg)
print(msg)
g = group(add.s(1, 1), add.s(1, 3))
result = g()
print(result.get()) # >>> [2, 4]

msg = "2 - group callback: it does not receive the task output"
print_task.delay(msg)
print(msg)
g = group(add.s(1, 1), add.s(1, 3))
g.link(add.s(2,2)) # since groups do not pass values to the callback, it must declare all parameters needed
result = g()
print(result.get())

msg = "3 - group callback list -> raises an exception: Cannot add link to group: use a chord"
print_task.delay(msg)
print(msg)
try:
    g = group(add.s(1, 1), add.s(1, 3))
    result = g.apply_async(link=[add.s(2,2), mul(2,5)])
    print(result.get())
except Exception as e:
    print(e)

msg = "4 - group errback: it DOES receive request, exc, traceback + it is called for every exception raised"
print_task.delay(msg)
print(msg)
try:
    # the errback is called for any exception raised
    g = group(raise_exception.s(), add.s(1, 1), raise_exception.s())
    g.on_error(error_handler.s()) # errbacks do receive error parameters from the group
    result = g()
    print(result.get())
except Exception as e:
    print(e)

msg = "5 - group errback list: NOT WORKING -> raised exception Cannot add link to group: do that on individual tasks"
print_task.delay(msg)
print(msg)
try:
    g = group(raise_exception.s(), add.s(1, 1), raise_exception.s())
    result = g.apply_async(link_error=[error_handler_1.s(), error_handler_2.s()])
    print(result.get())
except Exception as e:
    print(e)

msg = "6 - adding errbacks to individual tasks: this works fine but for limits in on_error I can assign one errback only to each task"
print_task.delay(msg)
print(msg)
try:
    # note: .on_error([error_handler_1.s(), error_handler_2.s()]) doesn't work -> TypeError: unhashable type: 'list'
    g = group(raise_exception.s().on_error(error_handler_1.s()), add.s(1, 1), raise_exception.s().on_error(error_handler_2.s()))
    result = g.apply_async() # adding a further link_error here throws: Cannot add link to group: do that on individual tasks
    print(result.get())
except Exception as e:
    print(e)



print("EXPERIMENTAL NOTES:")
print("1) Groups can only have ONE callback/ errback in the link/ error_link parameter")
print("2) The callback does not receive data from the parent tasks")
print("3) The errback DOES receive 'request', 'exc' and 'traceback' from the parent task")
print("4) The callback/errback is executed per each task of the group (according to whether it produced an error or terminated without errors)")
print("5) It is also possible to assign ONE SINGLE callback/ errback directly to one or more group's task")

