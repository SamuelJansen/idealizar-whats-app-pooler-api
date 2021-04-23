from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod

from dto import ContactDto

@Service()
class ScanService:

    @ServiceMethod(requestClass=[[ContactDto.ContactRequestDto]])
    def scanMessageAll(self, contactList) :
        self.service.authentication.authenticateIfNeeded()
        messageList = []
        for contact in contactList :
            messageList.append(self.scan(contact))

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def scanMessage(self, contact) :
        try :
            self.service.whatsAppWeb.accessContact(contact)
            messageList = self.service.whatsAppWeb.getMessageList(contact)
        except Exception as exception :
            log.error(self.scan, f'Not possible to scan messages from {contact.name} properly', exception=exception)
            raise exception
