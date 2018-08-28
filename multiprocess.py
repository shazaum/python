import datetime, time, random
from multiprocessing.pool import ThreadPool
from multiprocessing import TimeoutError

def getResult(client):
    '''Your code here'''
    time.sleep(random.randint(0,1))
    data = datetime.datetime.today()
    result = client + ' - ' + str(data)
    return result

pool = ThreadPool(processes=5)

# do some other stuff in the main process
clients = ['cliente1', 'cliente2', 'cliente3','cliente4','cliente5']
theList = []

for client in clients:
    try:
        asyncResult = pool.apply_async(getResult, args=(client,)) # tuple of args for foo
        returnValue = asyncResult.get(timeout=1)  # get the return value from your function.
        theList.append(returnValue) # just append
    except TimeoutError:
        print("Client: " + client + " is Timeout") #time is over...
        theList.append("Timeout") # append again, but with timeout

pool.close()
pool.join()
print(theList)
