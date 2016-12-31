import time

from . import tasks


def call_dummy_task():
    result = tasks.dummy_task.delay(0, 1)
    result = tasks.dummy_task.delay(0, 10)
    result = tasks.dummy_task.delay(0, 100)
    result = tasks.dummy_task.delay(0, 1000)

    result = tasks.dummy_data.delay(1, 1)
    result = tasks.dummy_data.delay(2, 10)
    result = tasks.dummy_data.delay(3, 100)
    result = tasks.dummy_data.delay(4, 1000)


    # at this time, our task is not finished, so it will return False
    print 'Task finished? ', result.ready()
    print 'Task result: ', result.result
    # sleep 10 seconds to ensure the task has been finished
    # time.sleep(10)
    # now the task should be finished and ready method will return True
    print 'Task finished? ', result.ready()
    print 'Task result: ', result.result
    return True
