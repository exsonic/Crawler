from scrapy.item import Item, Field

class JAThread(Item):
    url = Field()
    question = Field()
    posts = Field()
    
class JAQuestion(Item):
    title = Field()
    content = Field()
    submitTime = Field()
    category = Field()
    value = Field()
    status = Field()
    optionalInfo = Field()
    
    
class JAPost(Item):
    title = Field()
    accepted = Field()
    userName = Field()
    postTime = Field()
    content = Field()
    chatExpert = Field()
    chatCustomer = Field()

class JAExpert(Item):
    name = Field()
    title = Field()
    description = Field()
    category = Field()
    posFeedback = Field()
    acceptedAnswers = Field()
    
class JAThreadLinks(Item):
    links = Field()

class JAExperts(Item):
    experts = Field()    