import json
from decimal import *
from ocpp_datatypes import *
from ocpp_datatypes_enum import *
from ocpp_datatype_parser import *
import status_notification_pb2
import authorize_pb2
import transaction_event_pb2

getcontext().prec = 6

def getEnumValue(enumTypeObj, protobufEnumType):
    return protobufEnumType.Value(enumTypeObj.name)

def statusNotificationRequest(
        timestamp: str,
        connectorStatus: ConnectorStatusEnumType,
        evseId: int,
        connectorId: int):
    request = status_notification_pb2.StatusNotificationRequest()
    request.timestamp = timestamp
    if connectorStatus in ConnectorStatusEnumType:
        request.connectorStatus = getEnumValue(connectorStatus,
                                               status_notification_pb2.StatusNotificationRequest.ConnectorStatusEnumType)
    else:
        return -1
    request.evseId = evseId
    request.connectorId = connectorId
    return request

def statusNotificationResponse():
    response = status_notification_pb2.StatusNotificationResponse()
    return response

def transactionEventRequest(
        eventType: TransactionEventEnumType,
        timestamp: str,
        triggerReason: TriggerReasonEnumType,
        seqNo: int,
        offline: bool = None,
        numberOfPhasesUsed: int = None,
        cableMaxCurrent: Decimal = None,
        reservationId: int = None,
        transactionData: TransactionType = None, # is required
        idToken: IdTokenType = None,
        evse: EVSEType = None,
        meterValue: MeterValueType = None
):
    request = transaction_event_pb2.TransactionEventRequest()
    if eventType in TransactionEventEnumType:
        request.eventType = getEnumValue(eventType,
                                         transaction_event_pb2.TransactionEventRequest.TransactionEventEnumType)
    else:
        return -1
    request.timestamp = timestamp
    if triggerReason in TriggerReasonEnumType:
        request.triggerReason = getEnumValue(triggerReason,
                                             transaction_event_pb2.TransactionEventRequest.TriggerReasonEnumType)
    else:
        return -1
    request.seqNo = seqNo

    if offline != None:
        request.offline = offline
    if numberOfPhasesUsed != None:
        request.numberOfPhasesUsed = numberOfPhasesUsed
    if cableMaxCurrent != None:
        request.cableMaxCurrent = str(cableMaxCurrent)
    if reservationId != None:
        request.reservationId = reservationId

    request.transactionData.id = transactionData.id
    if transactionData.chargingState in ChargingStateEnumType:
        request.transactionData.chargingState = getEnumValue(transactionData.chargingState,
                                                             transaction_event_pb2.TransactionEventRequest.TransactionType.ChargingStateEnumType)
    if transactionData.timeSpentCharging != None:
        request.timeSpentCharging = transactionData.timeSpentCharging
    if transactionData.stoppedReason in ReasonEnumType:
        request.transactionData.stoppedReason = getEnumValue(transactionData.stoppedReason,
                                                             transaction_event_pb2.TransactionEventRequest.TransactionType.ReasonEnumType)
    if transactionData.remoteStartId != None:
        request.transactionData.remoteStartId = transactionData.remoteStartId

    if idToken != None:
        request.idToken.idToken = idToken.idToken
        request.idToken.type = getEnumValue(idToken.type,
                                            transaction_event_pb2.TransactionEventRequest.IdTokenType.IdTokenEnumType)
        if idToken.additionalInfo != None:
            request.idToken.additionalInfo = getEnumValue(idToken.additionalInfo,
                                                          transaction_event_pb2.TransactionEventRequest.IdTokenType.AdditionalInfoType)

    if evse != None:
        request.evse.id = evse.id
        if evse.connectorId != None:
            request.evse.connectorId = evse.connectorId

    if meterValue != None:
        request.meterValue.timestamp = meterValue.timestamp
        request.meterValue.sampledValue.value = str(meterValue.sampledValue.value)
        if meterValue.sampledValue.context in ReasonEnumType:
            request.meterValue.sampledValue.context = getEnumValue(meterValue.sampledValue.context,
                    transaction_event_pb2.TransactionEventRequest.MeterValueType.SampledValueType.ReadingContextEnumType)
        if meterValue.sampledValue.measurand in MeasurandEnumType:
            request.meterValue.sampledValue.measurand = getEnumValue(meterValue.sampledValue.measurand,
                    transaction_event_pb2.TransactionEventRequest.MeterValueType.SampledValueType.MeasurandEnumType)
        if meterValue.sampledValue.phase in PhaseEnumType:
            request.meterValue.sampledValue.phase = getEnumValue(meterValue.sampledValue.phase,
                    transaction_event_pb2.TransactionEventRequest.MeterValueType.SampledValueType.PhaseEnumType)
        if meterValue.sampledValue.location in LocationEnumType:
            request.meterValue.sampledValue.location = getEnumValue(meterValue.sampledValue.location,
                    transaction_event_pb2.TransactionEventRequest.MeterValueType.SampledValueType.LocationEnumType)
        if meterValue.sampledValue.signedMeterValue != None:
            request.meterValue.sampledValue.signedMeterValue.meterValueSignature = meterValue.sampledValue.signedMeterValue.meterValueSignature
            request.meterValue.sampledValue.signedMeterValue.signatureMethod = getEnumValue(meterValue.sampledValue.signedMeterValue.signatureMethod,
                    transaction_event_pb2.TransactionEventRequest.MeterValueType.SampledValueType.SignedMeterValueType.SignatureMethodEnumType)
            request.meterValue.sampledValue.signedMeterValue.encodingMethod = getEnumValue(meterValue.sampledValue.signedMeterValue.encodingMethod,
                    transaction_event_pb2.TransactionEventRequest.MeterValueType.SampledValueType.SignedMeterValueType.EncodingMethodEnumType)
            request.meterValue.sampledValue.signedMeterValue.encodedMeterValue = meterValue.sampledValue.signedMeterValue.encodedMeterValue
        if meterValue.sampledValue.unitOfMeasure != None:
            if meterValue.sampledValue.unitOfMeasure.unit != None:
                request.meterValue.sampledValue.unitOfMeasure.unit = meterValue.sampledValue.unitOfMeasure.unit
            if meterValue.sampledValue.unitOfMeasure.multiplier != None:
                request.meterValue.sampledValue.unitOfMeasure.multiplier = meterValue.sampledValue.unitOfMeasure.multiplier

    return request

def transactionEventResponse(
        totalCost: Decimal = None,
        chargingPriority: int = None,
        idTokenInfo: IdTokenInfoType = None,
        updatedPersonalMessage: MessageContentType = None
):
    response = transaction_event_pb2.TransactionEventResponse()
    if totalCost != None:
        response.totalCost = totalCost

    if chargingPriority != None:
        response.chargingPriority = chargingPriority

    if idTokenInfo != None:
        if idTokenInfo.status in AuthorizationStatusEnumType:
            response.idTokenInfo.status = getEnumValue(idTokenInfo.status,
                    transaction_event_pb2.TransactionEventResponse.IdTokenInfoType.AuthorizationStatusEnumType)
        else:
            return -1
        if idTokenInfo.cacheExpiryDateTime != None:
            response.idTokenInfo.cacheExpiryDateTime = idTokenInfo.cacheExpiryDateTime
        if idTokenInfo.chargingPriority != None:
            response.idTokenInfo.chargingPriority = idTokenInfo.chargingPriority
        if idTokenInfo.language1 != None:
            response.idTokenInfo.language1 = idTokenInfo.language1
        if idTokenInfo.language2 != None:
            response.idTokenInfo.language2 = idTokenInfo.language2
        if idTokenInfo.groupIdToken != None:
            response.idTokenInfo.groupIdToken.idToken = idTokenInfo.groupIdToken.idToken
            response.idTokenInfo.groupIdToken.type = getEnumValue(idTokenInfo.groupIdToken.type,
                    transaction_event_pb2.TransactionEventResponse.IdTokenInfoType.GroupIdTokenType.IdTokenEnumType)
        if idTokenInfo.personalMessage != None:
            response.idTokenInfo.personalMessage.format = getEnumValue(idTokenInfo.personalMessage.format,
                    transaction_event_pb2.TransactionEventResponse.IdTokenInfo.MessageContentType.MessageFormatEnumType)
            if idTokenInfo.personalMessage.language != None:
                response.idTokenInfo.personalMessage.language = idTokenInfo.personalMessage.language
            response.idTokenInfo.personalMessage.content = idTokenInfo.personalMessage.content

    if updatedPersonalMessage != None:
        response.updatedPersonalMessage.format = getEnumValue(updatedPersonalMessage.format,
                transaction_event_pb2.TransactionEventResponse.MessageContentType.MessageFormatEnumType)
        if updatedPersonalMessage.language != None:
            response.updatedPersonalMessage.language = updatedPersonalMessage.language
        response.updatedPersonalMessage.content = updatedPersonalMessage.content

    return response

def authorizeRequest(
        evseId: int = None,
        idToken: IdTokenType = None, # idToken is required
        _15118CertificateHashData: OCSPRequestDataType = None
):
    request = authorize_pb2.AuthorizeRequest()

    if evseId != None:
        request.evseId = evseId

    request.idToken.idToken = idToken.idToken
    if idToken.type in IdTokenEnumType:
        request.idToken.type = getEnumValue(idToken.type,
                authorize_pb2.AuthorizeRequest.IdTokenType.IdTokenEnumType)
    else:
        return -1

    if idToken.additionalInfo != None:
        request.idToken.additionalInfo.additionalIdToken = idToken.additionalInfo.additionalIdToken
        request.idToken.additionalInfo.type = idToken.additionalInfo.type

    if _15118CertificateHashData != None:
        if _15118CertificateHashData.hashAlgorithm in HashAlgorithmEnumType:
            request._15118CertificateHashData.hashAlgorithm = getEnumValue(_15118CertificateHashData.hashAlgorithm,
                    authorize_pb2.AuthorizeRequest.OCSPRequestDataType.HashAlgorithmEnumType)
        else:
            return -1
        request._15118CertificateHashData.issuerNameHash = _15118CertificateHashData.issuerNameHash
        request._15118CertificateHashData.issuerKeyHash = _15118CertificateHashData.issuerKeyHash
        request._15118CertificateHashData.serialNumber = _15118CertificateHashData.serialNumber
        if _15118CertificateHashData.responderURL != None:
            request._15118CertificateHashData.responderURL = _15118CertificateHashData.responderURL

    return request

def authorizeResponse(
        certificateStatus: CertificateStatusEnumType = None,
        evseId: int = None,
        idTokenInfo: IdTokenInfoType = None # idTokenInfo is required
):
    response = authorize_pb2.AuthorizeResponse()

    if certificateStatus != None:
        response.certificateStatus = getEnumValue(certificateStatus,
                authorize_pb2.AuthorizeResponse.CertificateStatusEnumType)

    if evseId != None:
        response.evseId = evseId

    if idTokenInfo.status in AuthorizationStatusEnumType:
        response.idTokenInfo.status = getEnumValue(idTokenInfo.status,
                authorize_pb2.AuthorizeResponse.IdTokenInfoType.AuthorizationStatusEnumType)
    else:
        return -1
    if idTokenInfo.cacheExpiryDateTime != None:
        response.idTokenInfo.cacheExpiryDateTime = idTokenInfo.cacheExpiryDateTime
    if idTokenInfo.chargingPriority != None:
        response.idTokenInfo.chargingPriority = idTokenInfo.chargingPriority
    if idTokenInfo.language1 != None:
        response.idTokenInfo.language1 = idTokenInfo.language1
    if idTokenInfo.language2 != None:
        response.idTokenInfo.language2 = idTokenInfo.language2
    if idTokenInfo.groupIdToken != None:
        response.idTokenInfo.groupIdToken.idToken = idTokenInfo.groupIdToken.idToken
        response.idTokenInfo.groupIdToken.type = getEnumValue(idTokenInfo.groupIdToken.type,
                authorize_pb2.AuthorizeResponse.IdTokenInfoType.GroupIdTokenType.IdTokenEnumType)
    if idTokenInfo.personalMessage != None:
        response.idTokenInfo.personalMessage.format = getEnumValue(idTokenInfo.personalMessage.format,
                authorize_pb2.AuthorizeResponse.IdTokenInfo.MessageContentType.MessageFormatEnumType)
        if idTokenInfo.personalMessage.language != None:
            response.idTokenInfo.personalMessage.language = idTokenInfo.personalMessage.language
        response.idTokenInfo.personalMessage.content = idTokenInfo.personalMessage.content

    return response