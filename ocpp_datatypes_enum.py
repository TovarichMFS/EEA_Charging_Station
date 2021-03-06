from enum import Enum

class AuthorizationStatusEnumType(Enum):
    Accepted = "Accepted"
    Blocked = "Blocked"
    ConcurrentTx = "ConcurrentTx"
    Expired = "Expired"
    Invalid = "Invalid"
    NoCredit = "NoCredit"
    NotAllowedTypeEVSE = "NotAllowedTypeEVSE"
    NotAtThisLocation = "NotAtThisLocation"
    NotAtThisTime = "NotAtThisTime"
    Unknown = "Unknown"

class CertificateStatusEnumType(Enum):
    Accepted = "Accepted"
    SignatureError = "SignatureError"
    CertificateExpired = "CertificateExpired"
    CertificateRevoked = "CertificateRevoked"
    NoCertificateAvailable = "NoCertificateAvailable"
    CertChainError = "CertChainError"
    ContractCancelled = "ContractCancelled"

class ChargingStateEnumType(Enum):
    Charging = "Charging"
    EVDetected = "EVDetected"
    SuspendedEV = "SuspendedEV"
    SuspendedEVSE = "SuspendedEVSE"

class ConnectorStatusEnumType(Enum):
    Available = "Available"
    Occupied = "Occupied"
    Reserved = "Reserved"
    Unavailable = "Unavailable"
    Faulted = "Faulted"

class EncodingMethodEnumType(Enum):
    Other = "Other"
    DLMSMessage = "DLMS Message"
    COSEMProtectedData = "COSEM ProtectedData"
    EDL = "EDL"

class HashAlgorithmEnumType(Enum):
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"

class IdTokenEnumType(Enum):
    Central = "Central"
    eMAID = "eMAID"
    ISO14443 = "ISO14443"
    KeyCode = "KeyCode"
    Local = "Local"
    NoAuthorization = "NoAuthorization"
    ISO15693 = "ISO15693"

class LocationEnumType(Enum):
    Body = "Body"
    Cable = "Cable"
    EV = "EV"
    Inlet = "Inlet"
    Outlet = "Outlet"

class MeasurandEnumType(Enum):
    CurrentExport = "Current.Export"
    CurrentImport = "Current.Import"
    CurrentOffered = "Current.Offered"
    EnergyActiveExportRegister = "Energy.Active.Export.Register"
    EnergyActiveImportRegister = "Energy.Active.Import.Register"
    EnergyReactiveExportRegister = "Energy.Reactive.Export.Register"
    EnergyReactiveImportRegister = "Energy.Reactive.Import.Register"
    EnergyActiveExportInterval = "Energy.Active.Export.Interval"
    EnergyActiveImportInterval = "Energy.Active.Import.Interval"
    EnergyActiveNet = "Energy.Active.Net"
    EnergyReactiveExportInterval = "Energy.Reactive.Export.Interval"
    EnergyReactiveImportInterval = "Energy.Reactive.Import.Interval"
    EnergyReactiveNet = "Energy.Reactive.Net"
    EnergyApparentNet = "Energy.Apparent.Net"
    EnergyApparentImport = "Energy.Apparent.Import"
    EnergyApparentExport = "Energy.Apparent.Export"
    Frequency = "Frequency"
    PowerActiveExport = "Power.Active.Export"
    PowerActiveImport = "Power.Active.Import"
    PowerFactor = "Power.Factor"
    PowerOffered = "Power.Offered"
    PowerReactiveExport = "Power.Reactive.Export"
    PowerReactiveImport = "Power.Reactive.Import"
    SoC = "SoC"
    Voltage = "Voltage"

class MessageFormatEnumType(Enum):
    ASCII = "ASCII"
    HTML = "HTML"
    URI = "URI"
    UTF8 = "UTF8"

class PhaseEnumType(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    N = "N"
    L1N = "L1-N"
    L2N = "L2-N"
    L3N = "L3-N"
    L1L2 = "L1-L2"
    L2L3 = "L2-L3"
    L3L1 = "L3-L1"

class ReadingContextEnumType(Enum):
    InterruptionBegin = "Interruption.Begin"
    InterruptionEnd = "Interruption.End"
    Other = "Other"
    SampleClock = "Sample.Clock"
    SamplePeriodic = "Sample.Periodic"
    TransactionBegin = "Transaction.Begin"
    TransactionEnd = "Transaction.End"
    Trigger = "Trigger"

class ReasonEnumType(Enum):
    DeAuthorized = "DeAuthorized"
    EmergencyStop = "EmergencyStop"
    EnergyLimitReached = "EnergyLimitReached"
    EVDisconnected = "EVDisconnected"
    GroundFault = "GroundFault"
    ImmediateReset = "ImmediateReset"
    Local = "Local"
    LocalOutOfCredit = "LocalOutOfCredit"
    MasterPass = "MasterPass"
    Other = "Other"
    OvercurrentFault = "OvercurrentFault"
    PowerLoss = "PowerLoss"
    PowerQuality = "PowerQuality"
    Reboot = "Reboot"
    Remote = "Remote"
    SOCLimitReached = "SOCLimitReached"
    StoppedByEV = "StoppedByEV"
    TimeLimitReached = "TimeLimitReached"
    Timeout = "Timeout"
    UnlockCommand = "UnlockCommand"

class SignatureMethodEnumType(Enum):
    ECDSAP256SHA256 = "ECDSAP256SHA256"
    ECDSAP384SHA384 = "ECDSAP384SHA384"
    ECDSA192SHA256 = "ECDSA192SHA256"

class TransactionEventEnumType(Enum):
    Ended = "Ended"
    Started = "Started"
    Updated = "Updated"

class TriggerReasonEnumType(Enum):
    Authorized = "Authorized"
    CablePluggedIn = "CablePluggedIn"
    ChargingRateChanged = "ChargingRateChanged"
    ChargingStateChanged = "ChargingStateChanged"
    Deauthorized = "Deauthorized"
    EnergyLimitReached = "EnergyLimitReached"
    EVCommunicationLost = "EVCommunicationLost"
    EVConnectTimeout = "EVConnectTimeout"
    MeterValueClock = "MeterValueClock"
    MeterValuePeriodic = "MeterValuePeriodic"
    TimeLimitReached = "TimeLimitReached"
    Trigger = "Trigger"
    UnlockCommand = "UnlockCommand"
    StopAuthorized = "StopAuthorized"
    EVDeparted = "EVDeparted"
    EVDetected = "EVDetected"
    RemoteStop = "RemoteStop"
    RemoteStart = "RemoteStart"