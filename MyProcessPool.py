import multiprocessing
import sys
import time
import threading
import os
import signal
import Queue

class WorkingProcess( multiprocessing.Process ):
  def __init__( self , pendingQueue):
    """ c'tor

    :param self: self refernce
    :param multiprocessing.Queue pendingQueue: queue storing ProcessTask before exection
    :param multiprocessing.Queue resultsQueue: queue storing callbacks and exceptionCallbacks
    :param multiprocessing.Event stopEvent: event to stop processing
    """
    multiprocessing.Process.__init__( self )
    self.__pendingQueue = pendingQueue
    ## daemonize
    self.daemon = True
    self.__working = multiprocessing.Value( 'i', 0 )
    self.__watchdogThread = None

    self.start()  
  def __watchdog( self ):
    print "Entered the watchdog....."
    """ watchdog thread target

    terminating/killing WorkingProcess when parent process is dead

    :param self: self reference
    """
    while True:      
      ## parent is dead,  commit suicide
      if os.getppid() == 1: # NOTE: getppid() is not monitoring the Working process, it's monitoring the agent
        os.kill( self.pid, signal.SIGTERM )
        ## wait for half a minute and if worker is still alive use REAL silencer
        time.sleep(30)
        ## now you're dead
        os.kill( self.pid, signal.SIGKILL )
      ## wake me up in 5 seconds
      print "gonna sleep for 5 seconds, wake me up"
      time.sleep(50)
      
  def run( self ):
  
    ## main loop
    print "Worker:Entered run()"
    self.__watchdogThread = threading.Thread( target = self.__watchdog )
    self.__watchdogThread.daemon = True
    self.__watchdogThread.start()    
    idleLoopCount = 0
    while True:

      ## read from queue
      try:
        task = self.__pendingQueue.get( block = True, timeout = 2 )   
      except Queue.Empty:
        ## idle loop?
        idleLoopCount += 1
        print "Worker:Idling... %s " %(idleLoopCount)
        ## 10th idle loop - exit, nothing to do 
        if idleLoopCount == 4:
	  print "Worker:Gonna exit now!"
	  print time.clock()
          return 
        continue

      ## toggle __working flag
      self.__working.value = 1    
      for i in range(1,5):
        print "Worker:Workin on something... %s " %(i)
      
      print "Worker:Finished working.."
      self.__working.value = 0
      
  def isWorking( self ):
    """ check if process is being executed

    :param self: self reference
    """
    return self.__working.value == 1

class ProcessPool( object ):
  def __init__( self ):
    self.__workersDict = {}
    self.done = False
    self.__pendingQueue =  multiprocessing.Queue(2)
  
  def spawnWorkingProcess( self ):
    print "Pool:gonna create a Worker!"
    worker = WorkingProcess(self.__pendingQueue)
    while worker.pid == None:
      time.sleep(0.1)
    print "Pool:Created a worker! PID = %s " % (worker.pid)  
    self.__workersDict[ worker.pid ] = worker
  
  def areWorkersAlive( self ):
    for pid, worker in self.__workersDict.items():
      if not worker.is_alive():
	print "Pool:My worker is dead!"
	print time.clock()
        del self.__workersDict[pid]
        print "WorkersDict %s " % (self.__workersDict)
        pool.done = True
      else:
        print "Pool:My worker still alive and kicking"
        #print "WorkersDict %s " % (self.__workersDict)        
        time.sleep(1)
        self.__pendingQueue.put(33)
        
if __name__ == "__main__":
  pool = ProcessPool()
  pool.spawnWorkingProcess()
  
  while True:
    pool.areWorkersAlive()
    if pool.done:
      break
      