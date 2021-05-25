from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod

from domain import WhatsAppWebConstants
from dto import WriteDto

@Service()
class WriteService :

    @ServiceMethod(requestClass=[WriteDto.WriteRequestDto])
    def writeMessage(self, requestDto) :
        self.service.whatsAppWeb.setToBusy()
        responseDto = None
        exception = None
        try :
            self.service.whatsAppWeb.accessContact(requestDto.contact)
            responseDto = self.getResponseDto(requestDto)
        except Exception as runTimeException :
            log.debug(self.writeMessage, f'Not possible to write message to "{requestDto.contact.key}" properly', exception=exception)
            exception = runTimeException
        self.service.whatsAppWeb.setToAvailable()
        if ObjectHelper.isNotNone(exception) :
            raise exception
        # log.prettyPython(self.writeMessage, 'responseDto.messageWriteList', [e.errorList for e in responseDto.messageWriteList], logLevel=log.DEBUG)
        return responseDto

    @ServiceMethod(requestClass=[WriteDto.WriteRequestDto])
    def getResponseDto(self, requestDto) :
        messageResponseDtoList = self.service.message.writeContent(requestDto.contact, requestDto.messageWriteList)
        return self.converter.write.toResponseDto(messageResponseDtoList)
