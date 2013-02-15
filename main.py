import os
from threadsProcessor import threadsProcessor
from usersProcessor import usersProcessor

threadsFileName = os.getcwd() + '/JA/threads.json'
usersFileName = os.getcwd() + '/JA/users.json'
tp = threadsProcessor(usersFileName)
tp.outpuXMLFile(threadsFileName)
up = usersProcessor(30000)
up.outpuXMLFile(usersFileName)
