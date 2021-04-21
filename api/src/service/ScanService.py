from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod, WebBrowser, Serializer

import WhatsAppConstants

@Service()
class PoolerService:

    @ServiceMethod(requestClass=[[ContactDto.ContactRequestDto]])
    def scanMessageAll(self, contactList) :
        messageList = []
        for contact in contactList :
            messageList.append(self.scan(contact))

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def scanMessage(self, contact) :
        try :
            self.accessContact(contact)
            messageList = self.getMessageList(contact)
        except Exception as exception :
            log.error(self.scan, f'Not possible to scan messages from {contact.name} properly', exception=exception)
            raise exception

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def accessContact(self, contact) :
        contactConversationXPath = self.helper.whatsApp.getContactConversationXPath(contact)
        self.service.broser.accessXPath(contactConversationXPath)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def getMessageList(self, contact) :
        return self.service.browser.findAllByXPath(WhatsAppConstants.XPATH_GROUP_MESSAGE_LIST)
