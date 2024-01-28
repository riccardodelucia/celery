from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost')

@app.task(name="tasks.raise_exception")
def raise_exception():
    raise Exception("raised exception!")

@app.task(name="tasks.print_task")
def print_task(msg):
    print(msg)

@app.task(name="tasks.error_handler_forward_error")
def error_handler_forward_error(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))
    print(f"forwarding error")
    #raise exc
    return request, exc, traceback

@app.task(name="tasks.error_handler")
def error_handler(request, exc, traceback, param=""):
    print("error_handler")
    print(f"param: {param}")
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))

@app.task(name="tasks.error_handler_1")
def error_handler_1(request, exc, traceback):
    print("error_handler 11111111111111")
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))

@app.task(name="tasks.error_handler_2")
def error_handler_2(request, exc, traceback):
    print("error_handler 2222222222")
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))

@app.task(name="tasks.group_error_handler")
def group_error_handler(request):
    print(f"request: {request}")

@app.task(name="tasks.forward_error")
def forward_error(request, exc, traceback):
    print("forward_error!")
    return request, exc, traceback
    
@app.task(name="tasks.add")
def add(x, y):
    return x + y

@app.task(name="tasks.mul")
def mul(x, y):
    return x * y

@app.task(name="tasks.receive_many_params")
def receive_many_params(a,b,c,d):
    return f"a: {a}, b: {b}, c: {c}, d: {d}"

@app.task(name="tasks.tsum")
def tsum(numbers):
    result = sum(numbers)
    print(f"tsum computed: {result}")
    return result
