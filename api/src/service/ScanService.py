from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod

from domain import WhatsAppWebConstants
from dto import ContactDto, ScanDto

MAX_MESSAGE_SEARCH_ITERATIONS = 20

@Service()
class ScanService:

    @ServiceMethod(requestClass=[[ScanDto.ScanRequestDto]])
    def scanMessageAll(self, dtoList) :
        self.validator.authentication.isAuthenticated()
        messageList = []
        for dto in dtoList :
            messageList.append(self.scanMessage(dto))

    @ServiceMethod(requestClass=[ScanDto.ScanRequestDto])
    def scanMessage(self, dto) :
        self.validator.authentication.isAuthenticated()
        responseDtoList = []
        try :
            self.service.whatsAppWeb.accessContact(dto.contact)
            messageList = self.getRawMessageList(dto)
            responseDtoList = self.mapper.scan.fromRawMessageListToResponseDtoList(dto, rawMessageList=messageList)
        except Exception as exception :
            log.debug(self.scanMessage, f'Not possible to scan messages from {dto.contact.key} properly', exception=exception)
            raise exception
        return responseDtoList

    @ServiceMethod(requestClass=[ScanDto.ScanRequestDto])
    def getRawMessageList(self, dto, iteration=1) :
        messageList = self.service.whatsAppWeb.getRawMessageList(dto.contact)
        log.debug(self.getRawMessageList, f'Iteration: {iteration}, messageList lenght: {len(messageList)}')
        if ObjectHelper.isNone(dto.lastMessageKey) or MAX_MESSAGE_SEARCH_ITERATIONS == iteration :
            return messageList
        for message in messageList :
            if self.isLastMessage(dto, message=message) :
                return self.service.whatsAppWeb.getRawMessageList(dto.contact)
        self.service.whatsAppWeb.moveUpConversation(dto.contact)
        return self.getRawMessageList(dto, iteration=iteration+1)

    @ServiceMethod(requestClass=[ScanDto.ScanRequestDto])
    def isLastMessage(self, dto, message=None) :
        isLastMessage = False
        try :
            isLastMessage = dto.lastMessageKey == self.getMessageKey([], message=message, muteLogs=True)
        except :
            ...
        return isLastMessage

    @ServiceMethod(requestClass=[[str]])
    def getMessageKey(self, errorList, message=None, muteLogs=False) :
        messageKey = None
        try :
            messageKey = self.service.whatsAppWeb.getMessageKey(message=message)
        except Exception as exception :
            errorList.append(str(exception))
            if not muteLogs :
                log.failure(self.getMessageKey, 'Not possible to get messageKey', exception=exception)
        return messageKey

    @ServiceMethod(requestClass=[[str]])
    def getMessageHtml(self, errorList, message=None, muteLogs=False) :
        html = None
        try :
            html = self.service.whatsAppWeb.getHtml(element=message)
        except Exception as exception :
            print(exception)
            errorList.append(str(exception))
            if not muteLogs :
                log.failure(self.getMessageKey, 'Not possible to get messageHtml', exception=exception)
        return html
