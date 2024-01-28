from tasks import print_task, raise_exception, error_handler, error_handler_1, error_handler_2, add, mul

msg = "############ Chains ############"
print_task.delay(msg)
print(msg)
msg = "1 - simple tasks chain"
print_task.delay(msg)
print(msg)
c = (add.s(4) | mul.s(8) | mul.s(2))
result = c(16) # (16 + 4) * 8 * 2
print(result.get())

msg = "2 - chain + callback: the callback result is not sent to the chain result"
print_task.delay(msg)
print(msg)
c = (add.s(4) | mul.s(8))
c.link(mul.s(2)) # executed but does not affect the chain result
result = c(16) # (16 + 4) * 8
print(result.get())

msg ="3 - chain + errback"
print_task.delay(msg)
print(msg)
try:
    c = (raise_exception.s() | add.s(8))
    c.on_error(error_handler.s())
    result = c()
    print(result.get())
except Exception as e:
    print(e)

msg ="4 - chain + errback list"
print_task.delay(msg)
print(msg)
try:
    c = (raise_exception.s() | add.s(8))
    result = c.apply_async(link_error=[error_handler_1.s(), error_handler_2.s()])
    print(result.get())
except Exception as e:
    print(e)

print("EXPERIMENTAL NOTES AND CONSIDERATIONS:")
print("1) Chains are different from callbacks since they allow to send the output to the same result object")
print("2) Calling a chain always converts into sending the chain to a worker. It is never executed locally")
print("3) Chains are not usable as errback primitives, since the errback is called on the same task which raised the exception")
print("4) Errbacks list can be declared for chains as well within the link_error parameter of apply_async")