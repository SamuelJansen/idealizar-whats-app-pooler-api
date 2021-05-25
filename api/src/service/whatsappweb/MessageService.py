from python_helper import log, ObjectHelper
from python_framework import Service, ServiceMethod

from dto import MessageScanDto, MessageWriteDto, ContactDto

@Service()
class MessageService:

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto, str, int, dict])
    def scanAllAndReturnIsLastMessage(self, contactRequestDto, lastMessageKey, iteration, messageResponseDtoDictionary) :
        rawMessageList = self.service.whatsAppWeb.getMessageList(contactRequestDto)
        log.debug(self.scanAllAndReturnIsLastMessage, f'Iteration: {iteration}, rawMessageList lenght: {len(rawMessageList)}')
        isLastMessage = False
        for rawMessage in rawMessageList :
            errorList = []
            messageKey = self.getMessageKey(errorList, rawMessage=rawMessage, muteLogs=True)
            isLastMessage = self.isLastScannedMessage(messageKey, lastMessageKey)
            if isLastMessage :
                break
            elif self.isNewMessage(messageKey, messageResponseDtoDictionary) :
                messageResponseDtoDictionary[messageKey] = self.converter.message.toReadResponseDto(
                    messageKey,
                    self.getMessageHtml(errorList, rawMessage=rawMessage, muteLogs=True),
                    errorList
                )
        return isLastMessage

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto, [MessageWriteDto.MessageWriteRequestDto]])
    def writeContent(self, contact, requestDtoList) :
        textBox = self.service.whatsAppWeb.getInputTextBox(contact)
        self.service.whatsAppWeb.access(element=textBox)
        responseDtoList = []
        for requestDto in requestDtoList :
            errorList = []
            self.writeText(errorList, contact, requestDto, textBox=textBox)
            responseDtoList.append(self.converter.message.toWriteResponseDto(errorList))
        return responseDtoList

    @ServiceMethod(requestClass=[[str], ContactDto.ContactRequestDto, MessageWriteDto.MessageWriteRequestDto])
    def writeText(self, errorList, contact, requestDto, textBox=None):
        errorList = []
        try :
            if ObjectHelper.isNotNone(requestDto.text) :
                self.service.whatsAppWeb.typeTextAndSend(contact, requestDto.text, element=textBox)
            else :
                log.warning(self.writeText, f'Text cannot be none')
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.writeText, f'Not possible to write message to {contact.key} properly', exception=exception)

    @ServiceMethod(requestClass=[[str]])
    def getMessageKey(self, errorList, rawMessage=None, muteLogs=False) :
        messageKey = None
        try :
            messageKey = self.service.whatsAppWeb.getMessageKey(message=rawMessage)
        except Exception as exception :
            errorList.append(str(exception))
            if not muteLogs :
                log.failure(self.getMessageKey, 'Not possible to get messageKey', exception=exception)
        return messageKey

    @ServiceMethod(requestClass=[[str]])
    def getMessageHtml(self, errorList, rawMessage=None, muteLogs=False) :
        html = None
        try :
            html = self.service.whatsAppWeb.getHtml(element=rawMessage)
        except Exception as exception :
            errorList.append(str(exception))
            if not muteLogs :
                log.failure(self.getMessageHtml, 'Not possible to get message as HTML', exception=exception)
        return html

    @ServiceMethod(requestClass=[str, dict])
    def isNewMessage(self, messageKey, messageResponseDtoDictionary) :
        return ObjectHelper.isNotNone(messageKey) and messageKey not in messageResponseDtoDictionary

    @ServiceMethod(requestClass=[str, str])
    def isLastScannedMessage(self, messageKey, lastMessageKey) :
        isLastScannedMessage = False
        try :
            isLastScannedMessage = ObjectHelper.isNotNone(lastMessageKey) and lastMessageKey == messageKey
        except Exception as exception :
            log.failure(self.scanAll, 'Not possible to evaluate "isLastScannedMessage" properly', exception=exception)
        return isLastScannedMessage
