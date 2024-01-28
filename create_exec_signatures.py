from tasks import print_task, add, receive_many_params
from celery import signature

msg = "############ Creating and executing signatures ############"
print_task.delay(msg)
print(msg)
msg = "1 - Creating signature using the Celery.signature method"
print_task.delay(msg)
print(msg)
s = signature("tasks.add", args=(2,2))
result = s.delay()
print(result.get())
result = s.apply_async()
print(result.get())

msg = "2 - Creating signature using the Task.signature method and passing the 'countdown' option as an example"
print_task.delay(msg)
print(msg)
# this method allows to set options for the signature (e.g. countdown -> the task waits 5 secs before starting)
s = add.signature(args=(2,2), countdown=5)
result = s.delay()
print(result.get())
s = add.signature()
result = s.apply_async(args=(2,2), countdown=5)
print(result.get())

msg = "3 - Creating signature using the Task.s method"
print_task.delay(msg)
print(msg)
# this method doesn't allow to set options for the signature
s = add.s(2,2)
result = s.delay()
print(result.get())
s = add.s()
result = s.delay(2,2)
print(result.get())

msg = "4 - Overriding params to the task"
print_task.delay(msg)
print(msg)
# in this example we can see that it is not allowed to override arguments and kwargs for a signature
try:
    s = add.s(2,2)
    result = s.apply_async(kwargs={"x":1}) 
    print(result.get())
except Exception as e:
    print(e) # exception! add() got multiple values for argument 'x' -> this is not even executed from the worker

print_task.delay(msg)
print(msg)


msg = "5 - executing a signature locally"
print_task.delay(msg)
print(msg)
s = add.s(2,2)()
print(s) # >>> 4 in this case the signature is executed as a plain function in the current scope


msg = "6 - Combining params from signature and call to the signature"
print_task.delay(msg)
print(msg)
# the relative order of parameters in one same declaration is ensured
s = receive_many_params.s(3,4)
result = s.delay(1,2) 
print(result.get()) # >>> a: 1, b: 2, c: 3, d: 4


print("EXPERIMENTAL NOTES:")
print("1) Both celery.signature(), Task.signature() are valid to create a new signature")
print("2) When declaring same options in multiple places (e.g. within the signature and in apply_async) the last declaration overrides all previous declaration of the same option")
print("3) Parameters cannot be overridden")
print("4) Calling a signature with () executes it in the current process without calling the worker")