# from scrapy.item import Item, Field

# class JAThread(Item):
#     url = Field()
#     question = Field()
#     posts = Field()
#     expert = Field()
    

# class JAQuestion(Item):
#     title = Field()
#     content = Field()
#     submitTime = Field()
#     category = Field()
#     value = Field()
#     status = Field()
#     optionalInfo = Field()
    
    
# class JAPost(Item):
#     title = Field()
#     expertName = Field()
#     postTime = Field()
#     content = Field()
#     chatExpert = Field()
#     chatCustomer = Field()

# class JAExpert(Item):
#     name = Field()
#     title = Field()
#     description = Field()
#     category = Field()
#     posFeedback = Field()
#     accepts = Field()
#     answeredDate = Field()
    
# class JAThreadLinks(Item):
#     links = Field()
    


# from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
# from scrapy.selector import HtmlXPathSelector
# from tutorial.items import JAPost, JAQuestion, JAThread, JAExpert, JAThreadLinks
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# import json, os
# from stat import ST_SIZE

# class JALinkSpider(CrawlSpider):
#     name = 'JALinks'
#     start_urls = ['http://www.justanswer.com/cell-phones/questions.html',
#                   'http://www.justanswer.com/email/questions.html']
#     rules = [Rule(SgmlLinkExtractor(allow=[r'/cell-phones/\d{4}-\d{2}-questions.html']), 'parse_links'),
#              Rule(SgmlLinkExtractor(allow=[r'/cell-phones/\d{4}-\d{2}-p\d+-questions.html']), 'parse_links')]
#     #start_urls also can include url from p1..., and add it into rules.
#     def parse_links(self, response):
#         print response
#         x = HtmlXPathSelector(response)
#         threadLinks = JAThreadLinks()
#         threadLinks['links'] = x.select("//table[@class='JA_archiveQuestionsTable'][2]/tr[*]/td/a/@href").extract()
#         print threadLinks
#         return threadLinks
    
# class JAThreadSpider(CrawlSpider):
#     name = "JAThread"
#     #urls read from json file
#     if os.path.isfile('/Users/exsonic/Dropbox/Courses/Directed_Research/Project/JA_Crawler/tutorial/links.json') and os.stat('/Users/exsonic/Dropbox/Courses/Directed_Research/Project/JA_Crawler/tutorial/links.json')[ST_SIZE] > 20:
#         jsonFile = open('/Users/exsonic/Dropbox/Courses/Directed_Research/Project/JA_Crawler/tutorial/links.json')
#         try:
#             jsonData = json.load(jsonFile)
#             start_urls = jsonData[0]['links']
#         except:
#             jsonData = []
#             start_urls = []
#         jsonFile.close()

#     def parse(self, response):   
#         thread = JAThread()
#         question = JAQuestion()
#         expert = JAExpert()
#         posts = []
        
#         thread['url'] = response.url
#         thread['question'] = question
#         thread['expert'] = expert
#         thread['posts'] = posts
        
#         x = HtmlXPathSelector(response)
        
#         question['title'] = x.select("//div[@class='JA_questionSubjectHolder']/h1/text()").extract()
#         question['content'] = x.select("//div[@id='JA_questionThread']/div/div/p/text()").extract()
#         question['optionalInfo'] = x.select("//div[@id='JA_questionThread']/div/div/p[3]/jarootja/text()").extract()
#         question['submitTime'] = x.select("//div[@class='JA_submission']/text()").extract()
#         question['category'] = x.select("//div[@class='JA_qCategory']/text()").extract()
#         question['value'] = x.select("//div[@class='JA_qValue']/text()").extract()
#         question['status'] = x.select("//div[@class='JA_qStatus']/text()").extract()
        
#         expert['name'] = x.select("//div[@id='JA_answerThread']/div/div/div/table/tr[1]/td/a/text()").extract()
#         expert['title'] = x.select("//div[@id='JA_answerThread']/div/div/div/div/p[1]/strong/text()").extract()
#         expert['category'] = x.select("//div[@id='JA_answerThread']/div/div/div/table/tr[2]/td/a/text()").extract()
#         expert['posFeedback'] = x.select("//div[@id='JA_answerThread']/div/div/div/table/tr[3]/td/text()").extract()
#         expert['description'] = x.select("//div[@id='JA_answerThread']/div/div/div/div/p[2]/text()").extract()
#         expert['accepts'] = x.select("//div[@id='JA_answerThread']/div/div/div/table/tr[4]/td/text()").extract()
#         expert['answeredDate'] = x.select("//div[@id='JA_answerThread']/div/div/div/table/tr[5]/td/text()").extract()
        

#         links = x.select("//div[@id='JA_topic']/div[4]/div/div/div/p[@class='JA_content']")
#         for link in links:
#             post = JAPost()
#             post['content'] = link.select("./../p[*]/text()").extract()
#             #to handle /p & /p[*]
#             if len(post.get('content')) == 0:
#                 post['content'] += link.select("./../p/text()").extract()
#             print post['content']

#             #locked content feature check 
#             if post['content'] == [u'\r\n        ', u'\r\n    ']:
#                 return None
            
#             post['title'] = link.select("./../div/div/h3/text()").extract()
#             post['expertName'] = link.select("./../div/a[@class='JA_authorName']/text()").extract()
#             post['postTime'] = link.select("./../div[@class='JA_profile JA_other']/text()").extract()
#             post['chatExpert'] = link.select("./../div[@class='JA_chatExpertMessage'][*]/span[@class='JA_chatMessage']/p/text()").extract()
#             post['chatCustomer'] = link.select("./../div[@class='JA_chatAskerMessage'][*]/span[@class='JA_chatMessage']/p/text()").extract()
#             posts.append(post)
#         return thread








# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/topics/item-pipeline.html
# from tutorial.items import JAThread

# class TutorialPipeline(object):
    
#     def process_item(self, item, spider):
#         if  isinstance(item, JAThread):
#             for key in item['question']:
#                 item['question'][key] = [''.join(item['question'][key])]
#                 item['question'][key] = item['question'][key][0].replace(u'\xa0', u' ').replace(u'\r\n', u' ').replace('\"', "'").strip()
                
            
#             for postDict in item['posts']:
#                 for key in postDict:
#                     print postDict[key]
#                     if  key == 'charCustomer' or key == 'chatExpert' or len(postDict[key]) == 0:
#                         continue
#                     #delete 'Posted by' that element
#                     if key == 'postTime' and len(postDict[key]) == 2:
#                         del postDict[key][0]
#                     #concatenate, clean \n\r, and strip all the additional spaces, replace all the \" to '
#                     postDict[key] = [''.join(postDict[key])]
#                     postDict[key] = postDict[key][0].replace(u'\xa0', u' ').replace(u'\r\n', u' ').replace('\"', "'").strip()
#         return item
