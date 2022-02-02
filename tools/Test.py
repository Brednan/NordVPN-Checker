import time, threading

class Test():
    def __init__(self, status):
        self.status = status
    
    def test(self):
        while True:
            if self.status.status_var.get() == 'In Progress':
                print('test')
                time.sleep(1)
            else:
                break
        self.status.finishing()
        self.status.update_status_display()
        print(threading.active_count())