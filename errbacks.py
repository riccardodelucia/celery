from tasks import print_task, raise_exception, error_handler, error_handler_1, error_handler_2

msg = "############ Signature errbacks ############"
print_task.delay(msg)
print(msg)

msg = "1 - assign errback through s.link_error"
print_task.delay(msg)
print(msg)
try:
    s = raise_exception.s()
    s.link_error(error_handler.s()) 
    result = s.delay()
    print(result.get())
except Exception as e:
    print(e)

msg = "2 - assign errback through s.on_error"
print_task.delay(msg)
print(msg)
try:
    s = raise_exception.s()
    s.on_error(error_handler.s())
    result = s.delay()
    print(result.get())
except Exception as e:
    print(e)

msg = "3 - calling signature and setting its errback in the apply_async method"
print_task.delay(msg)
print(msg)
try:
    s = raise_exception.s()
    result = s.apply_async(link_error=error_handler.s())
    print(result.get())
except Exception as e:
    print(e)

msg = "4 - testing errbacks additional parameters"
print_task.delay(msg)
print(msg)
try:
    # can add additional arguments after request, exc, traceback
    result = raise_exception.apply_async((), link_error=error_handler.s(param="hello"))
    print(result.get())
except Exception as e:
    print(e) 



msg = "5 - setting up an errback list within signature.link_error"
print_task.delay(msg)
print(msg)

msg = "setting up a list of errbacks declaring an errbacks array in signature.link_error: NOT WORKING"
print_task.delay(msg)
print(msg)
s.link_error([error_handler_1.s(), error_handler_2.s()])
try:
    result = s.apply_async()
    print(result.get())
except Exception as e:
    print(e)

msg = "setting up a list of errbacks declaring errbacks as an ellipsis in signature.link_error: NOT WORKING"
print_task.delay(msg)
print(msg)
try:
    s.link_error(error_handler_1.s(), error_handler_2.s())
    result = s.apply_async()
    print(result.get())
except Exception as e:
    print(e)

msg = "setting up multiple errbacks calling on_error/link_error multiple times: NOT WORKING"
print_task.delay(msg)
print(msg)
try:
    s.on_error(error_handler_1.s()) # same wtih link_error
    s.on_error(error_handler_2.s())

    result = s.apply_async()
    print(result.get())
except Exception as e:
    print(e)

msg = "setting up a list of errbacks declaring a list of errbacks in apply_async: WORKING!"
print_task.delay(msg)
print(msg)
try:
    result = s.apply_async(link_error=[error_handler_1.s(), error_handler_2.s()])
    print(result.get())
except Exception as e:
    print(e)


print("EXPERIMENTAL NOTES:")
print("1) link_error() and on_error() behave the same for declaring one single callback")
print("2) The only way to declare multiple callbacks is through a list declared in link_error as a parameter in apply_async. All other strategies won't work")



""" msg = "5 - setting up multiple errbacks: it is not possible to assign a callback/ errback to an errback"
print_task.delay(msg)
print(msg)
# This doesn't work neither by declaring an on_error and throwing the exception within the first errback, neither returning everything as a callback
err1 = error_handler_forward_error.s()
err2 = error_handler.s(args=[""])

err1.link(err2) #err1.on_error(err2) doesn't work as well

s = raise_exception.s()
s.on_error(err1)

result = s.delay()
print(result.get) """