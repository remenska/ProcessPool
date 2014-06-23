import multiprocessing
import sys
import time
import threading
import os
import signal
import Queue

class WorkingProcess( multiprocessing.Process ):
  def __init__( self ):
    """ c'tor

    :param self: self refernce
    :param multiprocessing.Queue pendingQueue: queue storing ProcessTask before exection
    :param multiprocessing.Queue resultsQueue: queue storing callbacks and exceptionCallbacks
    :param multiprocessing.Event stopEvent: event to stop processing
    """
    multiprocessing.Process.__init__( self )
    self.__pendingQueue = multiprocessing.Queue(4)
    ## daemonize
    self.daemon = True
    self.__working = multiprocessing.Value( 'i', 0 )
    self.start()  
    
  def run( self ):
  
    ## main loop
    print "Worker:Entered run()"
    idleLoopCount = 0
    while True:

      ## read from queue
      try:
        task = self.__pendingQueue.get( block = True, timeout = 1 )   
      except Queue.Empty:
        ## idle loop?
        idleLoopCount += 1
        print "Worker:Idling... %s " %(idleLoopCount)
        ## 10th idle loop - exit, nothing to do 
        if idleLoopCount == 10:
	  print "Worker:Gonna exit now!"
	  print time.clock()
          return 
        continue

      ## toggle __working flag
      self.__working.value = 1    
      for i in range(1,10):
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
  
  
  def spawnWorkingProcess( self ):
    print "Pool:gonna create a Worker!"
    worker = WorkingProcess()
    while worker.pid == None:
      time.sleep(0.1)
    print "Pool:Created a worker!"  
    self.__workersDict[ worker.pid ] = worker
  
  def areWorkersAlive( self ):
    for pid, worker in self.__workersDict.items():
      if not worker.is_alive():
	print "Pool:My worker is dead!"
	print time.clock()
        del self.__workersDict[pid]
      else:
        print "Pool:My worker still alive and kicking"
        time.sleep(1)
        
if __name__ == "__main__":
  pool = ProcessPool()
  pool.spawnWorkingProcess()
  
  while True:
    pool.areWorkersAlive()
    