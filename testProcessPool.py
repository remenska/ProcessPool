#!/usr/bin/python

import random
import time


class RequestTask:
  def __init__(self, id):
    self.__id = id
    print "Create %s"%id

  def __call__(self):
    randomNumber = random.randint(0,2000000)
    #print "Req %s sleep %s"%(self.__id, sleepTime)
    #while randomNumber!=10:
    while True: 
     randomNumber = random.randint(0,2000000)
    print "Req %s finished"%self.__id

  #  original:
  #def __call__(self):
    #sleepTime = random.randint(0,20)
    #print "Req %s sleep %s"%(self.__id, sleepTime)
    #time.sleep(sleepTime)
    #print "Req %s finished"%self.__id
    
from ProcessPool import ProcessPool

def resultCallback( self, taskID, taskResult ):
  print "callback taskID %s result %s"%(taskID, taskResult)

def exceptCallback( self, taskID, taskResult ):
  print "except callback taskID %s result %s"%(taskID, taskResult)

random.seed(0)

__processPool = None

def processPool(  ):
  """ facade for ProcessPool """
  global __processPool
  if not __processPool:

    __processPool = ProcessPool( 1,
                                      8,
                                      10,
                                      poolCallback = resultCallback,
                                      poolExceptionCallback = exceptCallback )
    __processPool.daemonize()
  return __processPool




idPool = range(2)
retried = 0
taskCounter = 0
requestsPerCycle = 20
while taskCounter < requestsPerCycle:

  while True:
    print "processPool tasks idle = %s working = %s" % ( processPool().getNumIdleProcesses(), processPool().getNumWorkingProcesses() )
    reqId = 0
    try:
      reqId = idPool.pop()
    except:
      if retried > 3 :
        break
      retried += 1
      print "Empty, we wait"
      time.sleep(25)
      #idPool = range(2)
      continue

      if not processPool().getFreeSlots():
        print "No free slots available in processPool, will wait %d seconds to proceed" % 1
        time.sleep( 1 )
    else:
      print "spawning task for request %s"%reqId
      enqueue = processPool().createAndQueueTask( RequestTask,
	                                           kwargs = { "id": reqId}, 
	                                           taskID = reqId,
	                                           blocking = True,
	                                           usePoolCallbacks = True,
	                                           timeOut = 2 )
    taskCounter += 1

processPool().finalize( timeout = 10 )



