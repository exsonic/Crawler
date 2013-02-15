from dict2xml import dict2xml
import json, os

class threadsProcessor:
    
    def __init__(self, usersFileName):
        try:
            if os.path.isfile(usersFileName):
                jsonFile = open(usersFileName)
                self.output = []
                experts = json.load(jsonFile)[0]['experts']
                self.expertsDict = dict()
                #0 is for indicating question's reply ID
                self.postID = 1
                #assume there's no more than 1000 experts
                self.customerID = 1000  
                expertID = 0
                for expert in experts:
                    self.expertsDict[expert['name']] = expertID
                    expertID+=1
        except:
            jsonFile.close()
            
    def outpuXMLFile(self, jsonFileName):
        if os.path.isfile(jsonFileName):
            threadsFile = open(jsonFileName)
            try:
                threads = json.load(threadsFile)
                output = self.processThreads(threads)            
                xml = dict2xml(output, 'Thread')
                xmlFileName = jsonFileName.split('.')[0] + '.xml'
                xmlFile = open(xmlFileName, 'w')
                xmlFile.write(xml)
                xmlFile.close()
            finally:
                threadsFile.close()
        
    def processThreads(self, threads):
        for thread in threads:
            self.output.append(self.processThread(thread, self.customerID))
            self.customerID += 1
        return self.output
        
    def processThread(self, thread, threadID):
        outputThread = dict()
        for key,value in thread.items():
            if key == 'question':
                outputThread['Question'] = self.processQuestion(value, threadID)
            elif key == 'posts':
                #remove all the thread include chat, if include chat self.processPosts will return None
                result = self.processPosts(value, threadID)
                if result == None:
                    return None
                else:
                    outputThread['Posts'] = result
        
        #handle the ReplyID
        questionPostID = outputThread['Question']['PostID']
        prevCustomerPostID = 0
        prevExpertPostID = 0
        for post in outputThread['Posts']:
            if post['Subject'] == 'Customer Reply':
                if prevExpertPostID == 0:
                    post['ReplyToPostID'] = questionPostID
                else:
                    post['ReplyToPostID'] = prevExpertPostID
                prevCustomerPostID = post['PostID']
            else:
                if  prevCustomerPostID == 0:
                    post['ReplyToPostID'] = questionPostID
                else:
                    post['ReplyToPostID'] = prevCustomerPostID
                prevExpertPostID = post['PostID']
        
        #merge all the key, values into a list
        threadList = []
        threadList.append(outputThread['Question'])
        for key,value in outputThread.items():
            if key == 'Posts':
                for post in value:
                    threadList.append(post)
        outputThread = threadList
        return outputThread
    
    def processQuestion(self, question, threadID):
        outputQuestion = dict()
        for key,value in question.items():
            if key == 'title':
                outputQuestion['Subject'] = value
            elif key == 'content':
                outputQuestion['Message'] = value
            elif key == 'submitTime':
                outputQuestion['PostTime'] = value
            elif key == 'optionalInfo':
                outputQuestion['optionalInfo'] = value
            
        outputQuestion['UserID'] = threadID
        outputQuestion['PostID'] = self.postID
        outputQuestion['ReplyToPostID'] = 0
        self.postID += 1
        return outputQuestion

    def processPosts(self, posts, threadID):
        outputPosts = []
        for post in posts:
            outputPost = dict()
            for key,value in post.items():
                #remove all the threads include chat
                if (key == 'chatCustomer' or key == 'chatExpert') and value == '':
                    return None 
                
                if key == 'userName':
                    if value == 'Customer':
                        outputPost['UserID'] = threadID
                    else:
                        try:
                            outputPost['UserID'] = self.expertsDict[value]
                        except:
                            outputPost['UserID'] = threadID
                            
                elif key == 'title':
                    outputPost['Subject'] = value
                elif key == 'content':
                    outputPost['Message'] = value
                elif key == 'postTime':
                    outputPost['PostTime'] = value
                elif key == 'accepted':
                    if value == 'Accepted Answer':
                        outputPost['Accept'] = 'Yes'
                    else:
                        outputPost['Accept'] = 'No'
                
            outputPost['PostID'] = self.postID
            self.postID += 1
            outputPosts.append(outputPost)
        return outputPosts