from python_helper import ObjectHelper
from python_framework import Converter, ConverterMethod

from dto import MessageScanDto, MessageWriteDto

@Converter()
class MessageConverter:

    @ConverterMethod(requestClass=[str, str, [str]])
    def toReadResponseDto(self, key, html, errorList) :
        return MessageScanDto.MessageScanResponseDto(
            key = key,
            html = html,
            errorList = errorList
        )

    @ConverterMethod(requestClass=[[str]])
    def toWriteResponseDto(self, errorList) :
        return MessageWriteDto.MessageWriteResponseDto(
            errorList = errorList
        )
