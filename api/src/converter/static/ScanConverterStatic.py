from python_framework import ConverterStatic

from domain import ScanConstants

def getMaxScanIterations(maxScanIterations) :
    return ConverterStatic.getValueOrDefault(maxScanIterations, ScanConstants.DEFAULT_MAX_SCAN_ITERATIONS)
