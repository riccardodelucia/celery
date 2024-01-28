from tasks import print_task, raise_exception, error_handler, error_handler_1, error_handler_2, error_handler_forward_error, add, mul, receive_many_params, tsum, group_error_handler, forward_error
from celery import signature, chain, group, chord

msg = "########### Mixed primitives ###########"
print_task.delay(msg)
print(msg)
msg = "1 - chain a group to a chain: the following groups receives the results and add them to the final result array"
print_task.delay(msg)
print(msg)
g = group(add.s(10), mul.s(10))
c = (add.s(4) | mul.s(8) | mul.s(2) | g)
result = c(16) # [((16 + 4) * 8 * 2) + 10 , ((16 + 4) * 8 * 2)*10] = [330, 3200]
print(result.get())

msg = "2 - assign a group callback to a chain: the group is executed but their outcomes are not sent to the results"
print_task.delay(msg)
print(msg)
g = group(add.s(10), mul.s(10))
c = (add.s(4) | mul.s(8) | mul.s(2))
c.link(g) # the group is executed but the chain result contains only 320
result = c(16) 
print(result.get())


msg = "3 - assign a group errback to a chain: the exception is not actually passed to the group"
print_task.delay(msg)
print(msg)
try:
    g = group(group_error_handler.s(), group_error_handler.s())
    c = (add.s(4) | raise_exception.si() | mul.s(2))
    c.on_error(g) # in this case the group will only receive the request id and no info about the exception
    result = c(16) 
    print(result.get()) 
except Exception as e:
    print(e)  


msg = "4 - assign a group interceptor errback to pass errors to a group: useless approach since the errbacks are executed in the same task where they have been raised"
print_task.delay(msg)
print(msg)
try:
    errback = forward_error.s()
    g = group(error_handler.s(), error_handler.s())
    errback.link(g) # this group will never called back from errback
    c = (add.s(4) | raise_exception.si() | mul.s(2))
    c.on_error(errback) 
    result = c(16) 
    print(result.get()) 
except Exception as e:
    print(e) 

  
msg = "5 - Passing a chain as an errback: since errbacks are executed in the same task where they are raised this approach doesn't work"
print_task.delay(msg)
print(msg)
try:
    c = (add.s(4,4) | raise_exception.si()| add.s(4))
    ceb = (forward_error.s() | error_handler.s())
    c.on_error(ceb)
    result = c()
    print(result.get())
except Exception as e:
    print(e)


print("EXPERIMENTAL NOTES:")
print("1) groups and chains can be combined to obtain complex flows")
print("2) when groups and chains are combined without the link, computed data is injected into the final result")
print("3) when groups and chains are are explicitly declared as link callbacks, they are executed but computed data is not injected into the final result")
print("4) managing errbacks in complex flows must happen on the single primitives/ tasks taking into account previous errbacks considerations")