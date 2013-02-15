from dict2xml import dict2xml
import os, json

class usersProcessor:
    
    def __init__(self, customerNumber):
        self.output = []
        self.experts = []
        self.customerNumber = customerNumber

    def outpuXMLFile(self, jsonFileName):
        if os.path.isfile(jsonFileName):
            jsonFile = open(jsonFileName)
            self.experts = json.load(jsonFile)[0]['experts']
            try:
                output = self.processUsers()            
                xml = dict2xml(output, 'User')
                xmlFileName = jsonFileName.split('.')[0] + '.xml'
                xmlFile = open(xmlFileName, 'w')
                xmlFile.write(xml)
            finally:
                jsonFile.close()
                xmlFile.close()
    
    def processUsers(self):
        expertID = 0
        for expert in self.experts:
            user = dict()
            for key,value in expert.items():
                if key == 'name':
                    user['Name'] = value
                elif key == 'category':
                    user['Category'] = value
                elif key == 'description':
                    user['Description'] = value
                elif key == 'posFeedback':
                    user['PosFeedback'] = value
                elif key == 'acceptedAnswers':
                    user['AcceptedAnswers'] = value
                
            user['Role'] = 'Expert'
            user['UserID'] = expertID
            expertID += 1
            self.output.append(user)
        
        customerID = 0
        while customerID < self.customerNumber:
            user = dict()
            user['UserID'] = customerID
            customerID += 1
            user['Role'] = 'Customer'
            self.output.append(user)
        return self.output