from ocpp_datatypes_enum import *
from decimal import Decimal

class AdditionalInfoType:
    def __init__(self, additionalIdToken: str, type:str):
        self.additionalIdToken = additionalIdToken
        self.type = type

class EVSEType:
    def __init__(self, id: int, connectorId: int = None):
        self.id = id
        self.connectorId = connectorId

class IdTokenType:
    def __init__(self, idToken: str, type: IdTokenEnumType, additionalInfo: AdditionalInfoType = None):
        self.idToken = idToken
        self.type = type
        self.additionalInfo = additionalInfo

class GroupIdTokenType:
    def __init__(self, idToken: str, type: IdTokenEnumType):
        self.idToken = idToken
        self.type = type

class MessageContentType:
    def __init__(self, format: MessageFormatEnumType, language: str = None, content: str = None): # content is required
        self.format = format
        self.language = language
        self.content = content

class IdTokenInfoType:
    def __init__(
            self,
            status: AuthorizationStatusEnumType,
            cacheExpiryDateTime: str = None,
            chargingPriority: int = None,
            language1: str = None,
            language2: str = None,
            groupIdToken: GroupIdTokenType = None,
            personalMessage: MessageContentType = None
    ):
        self.status = status
        self.cacheExpiryDateTime = cacheExpiryDateTime
        self.chargingPriority = chargingPriority
        self.language1 = language1
        self.language2 = language2
        self.groupIdToken = groupIdToken
        self.personalMessage = personalMessage

class UnitOfMeasureType:
    def __init__(self, unit: str = None, multiplier: int = None):
        self.unit = unit
        self.multiplier = multiplier

class OCSPRequestDataType:
    def __init__(
            self,
            hashAlgorithm: HashAlgorithmEnumType,
            issuerNameHash: str,
            issuerKeyHash: str,
            serialNumber: str,
            responderURL: str = None
    ):
        self.hashAlgorithm = hashAlgorithm
        self.issuerNameHash = issuerNameHash
        self.issuerKeyHash = issuerKeyHash
        self.serialNumber = serialNumber
        self.responderURL = responderURL

class SignedMeterValueType:
    def __init__(
            self,
            meterValueSignature: str,
            signatureMethod: SignatureMethodEnumType,
            encodingMethod: EncodingMethodEnumType,
            encodedMeterValue: int
    ):
        self.meterValueSignature = meterValueSignature
        self.signatureMethod = signatureMethod
        self.encodingMethod = encodingMethod
        self.encodedMeterValue = encodedMeterValue

class SampledValueType:
    def __init__(
            self,
            value: Decimal,
            context: ReadingContextEnumType = None,
            measurand: MeasurandEnumType = None,
            phase: PhaseEnumType = None,
            location: LocationEnumType = None,
            signedMeterValue: SignedMeterValueType = None,
            unitOfMeasure: UnitOfMeasureType = None
    ):
        self.value = value
        self.context = context
        self.measurand = measurand
        self.phase = phase
        self.location = location
        self.signedMeterValue = signedMeterValue
        self.unitOfMeasure = unitOfMeasure

class MeterValueType:
    def __init__(self, timestamp: str, sampledValue: SampledValueType):
        self.timestamp = timestamp
        self.sampledValue = sampledValue

class TransactionType:
    def __init__(
            self,
            id: str,
            chargingState: ChargingStateEnumType = None,
            timeSpentCharging: int = None,
            stoppedReason: ReasonEnumType = None,
            remoteStartId: int = None
    ):
        self.id = id
        self.chargingState = chargingState
        self.timeSpentCharging = timeSpentCharging
        self.stoppedReason = stoppedReason
        self.remoteStartId = remoteStartId
