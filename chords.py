from tasks import print_task, raise_exception, error_handler, add, tsum
from celery import chord, group


msg = "########### Chords ###########"
print_task.delay(msg)
print(msg)
msg = "1 - simple chord: the callback receives the header tasks outcome -> the callback result is set as chord result!!!"
print_task.delay(msg)
print(msg)
header = [add.s(10, 10), add.s(20, 20)]
body = tsum.s()
result = chord(header)(body)
print(result.get())

msg = "2 - declaring the chord callback through chord.link(): raised 'NoneType' object has no attribute 'link'"
print_task.delay(msg)
print(msg)
try:
    header = [add.s(10, 10), add.s(20, 20)]
    c = chord(header)
    c.link(tsum.s())
except Exception as e:
    print(e) 

msg = "3 - declaring the chord errback"
print_task.delay(msg)
print(msg)
# Note: a double exception is raised internally in the worker, but the errback is called correctly
try:
    header = [add.s(10, 10), add.s(20, 20), raise_exception.si()]
    body = tsum.s()
    body.on_error(error_handler.s())
    result = chord(header)(body)
    print(result.get())
except Exception as e:
    print(e)

msg = "4 - calling a group chained to a task promotes it to a chord (here also specifying an errback)"
print_task.delay(msg)
print(msg)
# Note: a double exception is reaised internally in the worker, but the errback is called correctly
try:
    result =(group(add.s(10, 10), add.s(20, 20), raise_exception.si()) | tsum.s().on_error(error_handler.s())).delay()
    print(result.get())
except Exception as e:
    print(e)


print("EXPERIMENTAL NOTES:")
print("1) Chords need a header=(list of tasks) + a body (single task + optional errback)")
print("2) Chords callback put their result in the result object. This is the only case in ceery")
print("3) Chords can be created out of a group chained to another task. An errback can be added to the chained task as well")
