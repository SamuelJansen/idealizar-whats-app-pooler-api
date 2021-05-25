from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod

from domain import WhatsAppWebConstants
from dto import ScanDto

@Service()
class ScanService:

    @ServiceMethod(requestClass=[[ScanDto.ScanRequestDto]])
    def scanAllMessages(self, dtoList) :
        messageList = []
        for dto in dtoList :
            messageList.append(self.scanMessage(dto))

    @ServiceMethod(requestClass=[ScanDto.ScanRequestDto])
    def scanMessage(self, requestDto) :
        self.service.whatsAppWeb.setToBusy()
        exception = None
        responseDto = None
        try :
            self.service.whatsAppWeb.accessContact(requestDto.contact)
            responseDto = self.getResponseDto(requestDto)
        except Exception as runTimeException :
            log.debug(self.scanMessage, f'Not possible to scan messages from "{requestDto.contact.key}" properly', exception=exception)
            exception = runTimeException
        self.service.whatsAppWeb.setToAvailable()
        if ObjectHelper.isNotNone(exception) :
            raise exception
        # log.prettyPython(self.scanMessage, 'messageKeyList', [message.key for message in responseDto.messageScanList], logLevel=log.DEBUG)
        return responseDto

    @ServiceMethod(requestClass=[ScanDto.ScanRequestDto])
    def getResponseDto(self, requestDto, messageResponseDtoDictionary=None, iteration=1) :
        if ObjectHelper.isNone(messageResponseDtoDictionary) :
            messageResponseDtoDictionary = {}
        isLastMessage = self.service.message.scanAllAndReturnIsLastMessage(
            requestDto.contact,
            requestDto.lastMessageKey,
            iteration,
            messageResponseDtoDictionary
        )
        if (
            isLastMessage or
            ObjectHelper.isNotNone(requestDto.maxScanIterations) and requestDto.maxScanIterations <= 0 or
            ObjectHelper.equals(requestDto.maxScanIterations, iteration)
        ):
            return self.converter.scan.toResponseDto(list(messageResponseDtoDictionary.values())[::-1])
        self.service.whatsAppWeb.moveUpConversation(requestDto.contact)
        return self.getResponseDto(
            requestDto,
            messageResponseDtoDictionary = messageResponseDtoDictionary,
            iteration = iteration + 1
        )
