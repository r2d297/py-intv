
# Online Python - IDE, Editor, Compiler, Interpreter
import threading
import time
from random import randint
from readerwriterlock import rwlock

class HitCounter:

    def __init__(self):
        self.times = [0]*300
        self.hits=[0]*300
        self.lock = rwlock.RWLockFair()

    def hit(self, timestamp: int) -> None:
        index=timestamp % 300

        with self.lock.gen_wlock():
            if self.times[index] != timestamp:
                self.times[index]=timestamp
                self.hits[index] = 1
            else:
                self.hits[index]+=1


    def getHits(self, timestamp: int) -> int:
        total = 0
        with self.lock.gen_rlock():
            for i in range(300):
                if timestamp - self.times[i]<300:
                    total+=self.hits[i]

        return total

def hit_worker(counter,id):
    for _ in range(20):
        current_time = int(time.time())
        counter.hit(current_time)
        time.sleep(randint(1,3) * 0.1)

def get_worker(counter):
    for _ in range(10):
        current_time = int(time.time())
        print(f"[get] Total hits: {counter.getHits(current_time)}")
        time.sleep(0.5)

if __name__ == "__main__":
    counter = HitCounter()
    
    threads=[]
    
    for i in range(5):
        t= threading.Thread(target=hit_worker, args=(counter,i))
        threads.append(t)
        t.start()
    
    t = threading.Thread(target=get_worker, args=(counter,))
    threads.append(t)
    t.start()
    
    for t in threads:
        t.join()
    print("All threads are done")
    
        
        
        