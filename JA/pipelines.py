from JA.items import JAThread, JAUsers
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
                if  key == 'submitTime' and len(item['question'][key]) == 4:
                    print item['question'][key]
                    days = int(item['question'][key].split()[0])
                    hours = int(item['question'][key].split()[3])
                    item['question'][key] = str(int(time.time() - (days * 3600 * 24) - (hours * 3600)))
                       
            for post in item['posts']:
                for key in post:
                    if  key == 'chatCustomer' or key == 'chatExpert' or len(post[key]) == 0:
                        continue
                    
                    if key == 'title' and cmp(post[key], 'Expert:'):
                        post[key] = 'Expert'
                                            
                    post[key] = self.cleanString(post[key])
                    #convert to absolute time
                    if key == 'postTime':
                        days = int(post[key].split()[1])
                        hours = int(post[key].split()[4])
                        post[key] = str(int(time.time() - (days * 3600 * 24) - (hours * 3600)))
        
        if isinstance(item, JAUsers):
            for expert in item['experts']:
                for key in expert:
                    if key == 'acceptedAnswers' or key == 'posFeedback':
                        expert[key] = [expert[key].split()[2]]
                    expert[key] = self.cleanString(expert[key])
        return item
    