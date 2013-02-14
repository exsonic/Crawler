from JA.items import JAThread, JAExperts
import time

class ExportPipeline(object):
    
    def cleanString(self, strList):
        # concatenate, clean \n\r, and strip all the additional spaces, replace all the \" to '
        strList = [''.join(strList)]
        strList = strList[0].replace(u'\xa0', u'').replace(u'\r\n', u'').replace('\"', "'").strip()
        strList = ' '.join(strList.split())
        return strList
            
    def process_item(self, item, spider):

        if isinstance(item, JAThread):
            for key in item['question']:
                item['question'][key] = self.cleanString(item['question'][key])
                #convert to absolute time
                if  key == 'submitTime' and len(item['question'][key].split()) == 6:
                    days = int(item['question'][key].split()[0])
                    hours = int(item['question'][key].split()[3])
                    item['question'][key] = str(int(time.time() - (days * 3600 * 24) - (hours * 3600)))
                       
            for post in item['posts']:
                for key in post:
                    if  key == 'chatCustomer' or key == 'chatExpert' or len(post[key]) == 0:
                        continue
                                            
                    post[key] = self.cleanString(post[key])
                    #convert to absolute time
                    if key == 'postTime' and len(post[key].split()) == 7:
                        days = int(post[key].split()[1])
                        hours = int(post[key].split()[4])
                        post[key] = str(int(time.time() - (days * 3600 * 24) - (hours * 3600)))
                    elif key == 'postTime' and len(post[key].split()) == 4:
                        days = int(post[key].split()[1])
                        post[key] = str(int(time.time() - (days * 3600 * 24)))
                    
                    #handle the issue of unable to get the customer's user name
                    if key == 'title' and post[key] == 'Expert:':
                        post[key] = 'Expert Reply'
                        
                    if key == 'title' and post[key] == 'Customer':
                        post[key] = 'Customer Reply'
                        post['userName'] = 'Customer'
                    
                    
        if isinstance(item, JAExperts):
            for expert in item['experts']:
                for key in expert:
                    if key == 'acceptedAnswers' or key == 'posFeedback':
                        expert[key] = [expert[key].split()[2]]
                    expert[key] = self.cleanString(expert[key])
        return item
    