from ocpp_datatypes import *

def parse_AdditionalInfoType(obj: AdditionalInfoType):
    parsed_object = {"additionalIdToken": obj.additionalIdToken, "type": obj.type}
    return parsed_object

def parse_EVSEType(obj: EVSEType):
    parsed_object = {"id": obj.id, "connectorId": obj.connectorId}
    return parsed_object

def parse_IdTokenType(obj: IdTokenType):
    parsed_object = {"idToken": obj.idToken, "type": obj.type.value,
                     "additionalInfo": parse_AdditionalInfoType(obj.additionalInfo)}
    return parsed_object

def parse_MeterValueType(obj: MeterValueType):
    parsed_object = {"timestamp": obj.timestamp, "sampledValue": parse_SampledValueType(obj.sampledValue)}
    return parsed_object

def parse_SampledValueType(obj: SampledValueType):
    parsed_object = {"value": obj.value, "context": obj.context.value,
                     "measurand": obj.measurand.value, "phase": obj.phase.value,
                     "location": obj.location.value, "signedMeterValue": parse_SignedMeterValueType(obj.signedMeterValue),
                     "unitOfMeasure": parse_UnitOfMeasureType(obj.unitOfMeasure)}
    return parsed_object

def parse_SignedMeterValueType(obj: SignedMeterValueType):
    parsed_object = {"meterValueSignature": obj.meterValueSignature, "signatureMethod": obj.signatureMethod.value,
                     "encodingMethod": obj.encodingMethod.value, "encodedMeterValue": obj.encodedMeterValue}
    return parsed_object

def parse_TransactionType(obj: TransactionType):
    parsed_object = {"id": obj.id, "chargingState": obj.chargingState.value, "timeSpentCharging": obj.timeSpentCharging,
                     "stoppedReason": obj.stoppedReason.value, "remoteStartId": obj.remoteStartId}
    return parsed_object

def parse_UnitOfMeasureType(obj: UnitOfMeasureType):
    parsed_object = {"unit": obj.unit, "multiplier": obj.multiplier}
    return parsed_object