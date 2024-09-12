import struct
from controller_data import ControllerData


class DTMHeaderReader:
    def __init__(self):
        return

    def get_inputs(self, dtm):
        if not self._read_dtm_header_id(dtm.read(4)):
            raise Exception("Bad header ID")

        GameID = dtm.read(6)
        IsWiiGame = bool.from_bytes(dtm.read(1), 'little')
        ConnectedControllers = int.from_bytes(dtm.read(1), 'little')
        IsFromSaveState = bool.from_bytes(dtm.read(1), 'little')

        FrameCount = struct.unpack('<Q', dtm.read(8))[0]
        InputFrameCount = struct.unpack('<Q', dtm.read(8))[0]
        LagFrameCount = struct.unpack('<Q', dtm.read(8))[0]

        UniqueID = struct.unpack('<Q', dtm.read(8))[0]
        NumRerecords = struct.unpack('<i', dtm.read(4))[0]
        Author = dtm.read(32)
        VideoBackEnd = dtm.read(16)
        AudioEmulator = dtm.read(16)
        MD5 = dtm.read(16)
        RecordingStartTime = struct.unpack('<Q', dtm.read(8))[0]
        IsSavedConfig = bool.from_bytes(dtm.read(1), 'little')
        UsingIdleSkip = bool.from_bytes(dtm.read(1), 'little')
        UsingDualCore = bool.from_bytes(dtm.read(1), 'little')
        UsingProgressiveScan = bool.from_bytes(dtm.read(1), 'little')
        UsingHLEDSP = bool.from_bytes(dtm.read(1), 'little')
        UsingFastDiscSpeed = bool.from_bytes(dtm.read(1), 'little')
        CPUCore = int.from_bytes(dtm.read(1), 'little')
        IsEFBAccessEnabled = bool.from_bytes(dtm.read(1), 'little')
        IsEFBCopiesEnabled = bool.from_bytes(dtm.read(1), 'little')
        UsingEFBToTexture = bool.from_bytes(dtm.read(1), 'little')
        IsEFBCopyCacheEnabled = bool.from_bytes(dtm.read(1), 'little')
        IsEmulatingEFBFormatChanges = bool.from_bytes(dtm.read(1), 'little')
        UsingXFB = bool.from_bytes(dtm.read(1), 'little')
        UsingRealXFB = bool.from_bytes(dtm.read(1), 'little')
        UsingMemoryCard = bool.from_bytes(dtm.read(1), 'little')
        UsingClearSaves = bool.from_bytes(dtm.read(1), 'little')
        NumBongos = int.from_bytes(dtm.read(1), 'little')
        SyncGPU = bool.from_bytes(dtm.read(1), 'little')
        UsingNetplay = bool.from_bytes(dtm.read(1), 'little')
        PAL60 = bool.from_bytes(dtm.read(1), 'little')

        #  Skip reserved bytes
        garbage = dtm.read(12)

        SecondDiscName = dtm.read(40)
        GitRevision = dtm.read(20)
        DSPIROMHash = struct.unpack('<i', dtm.read(4))[0]
        DSPCoefHash = struct.unpack('<i', dtm.read(4))[0]
        TickCount = struct.unpack('<Q', dtm.read(8))[0]

        MoreGarbage = dtm.read(11)

        # print(f"GameID : {GameID}")
        # print(f"IsWiiGame : {IsWiiGame}")
        # print(f"ConnectedControllers : {ConnectedControllers}")
        # print(f"IsFromSaveState : {IsFromSaveState}")
        # print(f"FrameCount : {FrameCount}")
        # print(f"InputFrameCount : {InputFrameCount}")
        # print(f"LagFrameCount : {LagFrameCount}")
        # print(f"UniqueID : {UniqueID}")
        # print(f"NumRerecords : {NumRerecords}")
        # print(f"Author : {Author}")
        # print(f"VideoBackEnd : {VideoBackEnd}")
        # print(f"AudioEmulator : {AudioEmulator}")
        # print(f"MD5 : {MD5}")
        # print(f"RecordingStartTime : {RecordingStartTime}")
        # print(f"IsSavedConfig : {IsSavedConfig}")
        # print(f"UsingIdleSkip : {UsingIdleSkip}")
        # print(f"UsingDualCore : {UsingDualCore}")
        # print(f"UsingProgressiveScan : {UsingProgressiveScan}")
        # print(f"UsingHLEDSP : {UsingHLEDSP}")
        # print(f"UsingFastDiscSpeed : {UsingFastDiscSpeed}")
        # print(f"CPUCore : {CPUCore}")
        # print(f"IsEFBAccessEnabled : {IsEFBAccessEnabled}")
        # print(f"IsEFBCopiesEnabled : {IsEFBCopiesEnabled}")
        # print(f"UsingEFBToTexture : {UsingEFBToTexture}")
        # print(f"IsEFBCopyCacheEnabled : {IsEFBCopyCacheEnabled}")
        # print(f"IsEmulatingEFBFormatChanges : {IsEmulatingEFBFormatChanges}")
        # print(f"UsingXFB : {UsingXFB}")
        # print(f"UsingRealXFB : {UsingRealXFB}")
        # print(f"UsingMemoryCard : {UsingMemoryCard}")
        # print(f"UsingClearSaves : {UsingClearSaves}")
        # print(f"NumBongos : {NumBongos}")
        # print(f"SyncGPU : {SyncGPU}")
        # print(f"UsingNetplay : {UsingNetplay}")
        # print(f"PAL60 : {PAL60}")
        # print(f"garbage : {garbage}")
        # print(f"SecondDiscName : {SecondDiscName}")
        # print(f"GitRevision : {GitRevision}")
        # print(f"DSPIROMHash : {DSPIROMHash}")
        # print(f"DSPCoefHash : {DSPCoefHash}")
        # print(f"TickCount : {TickCount}")
        # print(f"MoreGarbage : {MoreGarbage}")

        inputs = []

        for i in range(InputFrameCount):
            controller_data = self._convert_controller_data(*struct.unpack('<HBBBBBB', dtm.read(8)))
            inputs.append(controller_data)

        # print(f"FrameCount : {FrameCount}")
        # print(f"InputFrameCount : {InputFrameCount}")
        # print(f"LagFrameCount : {LagFrameCount}")

        return inputs

    @staticmethod
    def _read_dtm_header_id(header_id):
        return (header_id[0] == 68 and          # "D"
                header_id[1] == 84 and          # "T"
                header_id[2] == 77 and          # "M"
                header_id[3] == 0x1A)

    @staticmethod
    def _convert_controller_data(bits, LPressure, RPressure, XAxis, YAxis, CXAxis, CYAxis):
        Start = (1 << 0)
        A = (1 << 1)
        B = (1 << 2)
        X = (1 << 3)
        Y = (1 << 4)
        Z = (1 << 5)
        DPadUp = (1 << 6)
        DPadDown = (1 << 7)
        DPadLeft = (1 << 8)
        DPadRight = (1 << 9)
        L = (1 << 10)
        R = (1 << 11)

        Start = bits & Start
        A = bits & A
        B = bits & B
        X = bits & X
        Y = bits & Y
        Z = bits & Z
        DPadUp = bits & DPadUp
        DPadDown = bits & DPadDown
        DPadLeft = bits & DPadLeft
        DPadRight = bits & DPadRight
        L = bits & L
        R = bits & R

        return ControllerData(Start=bool(Start),
                              A=bool(A),
                              B=bool(B),
                              X=bool(X),
                              Y=bool(Y),
                              Z=bool(Z),
                              DPadUp=bool(DPadUp),
                              DPadDown=bool(DPadDown),
                              DPadLeft=bool(DPadLeft),
                              DPadRight=bool(DPadRight),
                              L=bool(L),
                              R=bool(R),
                              LPressure=LPressure,
                              RPressure=RPressure,
                              XAxis=XAxis,
                              YAxis=YAxis,
                              CXAxis=CXAxis,
                              CYAxis=CYAxis,
                              )
