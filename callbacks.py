from tasks import print_task, add

msg = "############ Signature callbacks ############"
print_task.delay(msg)
print(msg)

msg = "1 - assign callback through s.link"
print_task.delay(msg)
print(msg)
s = add.s(2,2)
s.link(add.s(4)) # cannot chain s.link on the same line, i.e. cannot do: add.s(2,2).link(add.s(4))
result = s.delay() # note: the result is 4, does not collect the callback sum
print(result.get())


msg = "2 - calling signature and setting its callback in apply_async"
print_task.delay(msg)
print(msg)
s = add.s(2,2)
result = s.apply_async(link=add.s(4))
print(result.get()) # note: the result is 4, does not collect the callback sum

msg = "3 - setting a callback both in the signature and in apply_async"
print_task.delay(msg)
print(msg)
s = add.s(2,2)
s.link(add.s(2)) # >>> 6
s.link(add.s(4)) # >>> 8
result = s.apply_async(link=add.s(8)) # >>> 12
print(result.get()) 
result = s.apply_async()
print(result.get()) 

print("EXPERIMENTAL NOTES:")
print("1) Callbacks can be set through the signature.link() method or within apply_async")
print("2) Callbacks are overridden, i.e. the last declaration of callbacks substitutes all the previous declarations")
print("3) Callbacks output is not transfered in the signature result")


