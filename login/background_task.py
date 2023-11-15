import time

def run_background_task():
    # Simulate a task that takes 10 seconds
    print('Background task started')

    # raise Exception 
    time.sleep(10)
    # Perform the background work here
    return "Background task completed"
