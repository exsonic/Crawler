from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from JA.items import JAPost, JAQuestion, JAThread, JAExpert, JAThreadLinks, JAUsers
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import json, os

class JALinkSpider(CrawlSpider):
    name = 'JALinks'
    start_urls = ['http://www.justanswer.com/cell-phones/questions.html']
    rules = [Rule(SgmlLinkExtractor(allow=[r'/cell-phones/\d{4}-\d{2}-questions.html']), 'parse_links'),
                 Rule(SgmlLinkExtractor(allow=[r'/cell-phones/\d{4}-\d{2}-p\d+-questions.html']), 'parse_links')]
    
    #start_urls also can include url from p1..., and add it into rules.
    def parse_links(self, response):
        x = HtmlXPathSelector(response)
        threadLinks = JAThreadLinks()
        threadLinks['links'] = x.select("//table[@class='JA_archiveQuestionsTable'][2]/tr[*]/td/a/@href").extract()
        return threadLinks
    
class JAThreadSpider(CrawlSpider):
    name = "JAThreads"
    start_urls = None
    
    def __init__(self):
        #urls read from json file
        if os.path.isfile('/Users/exsonic/Dropbox/Courses/Directed_Research/Crawler/JA/links.json'):
            jsonFile = open('/Users/exsonic/Dropbox/Courses/Directed_Research/Crawler/JA/links.json')
            try:
                jsonData = json.load(jsonFile)
                self.start_urls = jsonData[0]['links']
            except:
                jsonData = []
                self.start_urls = []
            jsonFile.close()

    def parse(self, response):   
        thread = JAThread()
        question = JAQuestion()
        posts = []
        
        thread['url'] = response.url
        thread['question'] = question
        thread['posts'] = posts
        
        x = HtmlXPathSelector(response)
        
        question['title'] = x.select("//div[@class='JA_questionSubjectHolder']/h1/text()").extract()
        question['content'] = x.select("//div[@id='JA_questionThread']/div/div/p/text()").extract()
        question['optionalInfo'] = x.select("//div[@id='JA_questionThread']/div/div/p[3]/jarootja/text()").extract()
        question['submitTime'] = x.select("//div[@class='JA_submission']/text()").extract()
        question['category'] = x.select("//div[@class='JA_qCategory']/text()").extract()
        question['value'] = x.select("//div[@class='JA_qValue']/text()").extract()
        question['status'] = x.select("//div[@class='JA_qStatus']/text()").extract()
        
        links = x.select("//div[@id='JA_topic']/div/div/div/div/p[@class='JA_content']")
        for link in links:
            post = JAPost()
            post['content'] = link.select("./../p/text()").extract() + link.select("./../ol/li/text()").extract() + link.select("./../div/text()").extract()
            #detect and remove the locked thread
            if post['content'] == [u'\r\n        ', u'\r\n        ', u'\r\n       \r\n            \r\n                    ', u' ', u'\r\n            \r\n            ', u'\r\n        ']:
                return None
            
            post['title'] = link.select("./../div[@class='JA_profile JA_other']/span[@class='JA_infoLabel']/text()").extract()
            #if title is empty, delete the question post
            if not post['title']:
                continue
            
            post['userName'] = link.select("./../div[@class='JA_profile JA_other']/a[@class='JA_authorName']/text()").extract()
            post['postTime'] = link.select("./../div[@class='JA_profile JA_other']/span[@class='JA_note']/text()").extract()
            post['chatExpert'] = link.select("./../div[@class='JA_chatExpertMessage'][*]/span/p/text()").extract()
            post['chatCustomer'] = link.select("./../div[@class='JA_chatAskerMessage'][*]/span/p/text()").extract()
            post['accepted'] = link.select("./../../../h3/text()").extract()
               
            posts.append(post)
        return thread

class JAExpertSpider(CrawlSpider):
    name = 'JAExperts'
    start_urls = None
    
    def __init__(self):
        self.start_urls = ['http://www.justanswer.com/cell-phones/experts.html#']
 
    def parse(self, response):
        x = HtmlXPathSelector(response)
        experts = []
        users = JAUsers()
        users['experts'] = experts
        
        links = x.select("//div[@class='expert_list']/div/div/div/div/a")
        for link in links:
            expert = JAExpert()
            expert['name'] = link.select("./text()").extract()
            expert['title'] = link.select("./../text()").extract()
            expert['acceptedAnswers'] = link.select("./../../div[@class='expert_rating JA_column_left']/text()").extract()[0]
            expert['posFeedback'] = link.select("./../../div[@class='expert_rating JA_column_left']/text()").extract()[1]
            expert['category'] = link.select("//h2[@id='JA_forumName']/text()").extract()
            expert['description'] = link.select("./../../../div[@class='expert_profile']/text()").extract()
            experts.append(expert)
        return users