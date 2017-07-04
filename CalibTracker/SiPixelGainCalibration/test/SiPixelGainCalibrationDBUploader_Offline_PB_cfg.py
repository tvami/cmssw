import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process("PixelGainDB",eras.Run2_25ns)

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

# GlobalTag
# --------------------- GlobalTag ----------------------
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v11', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
from Configuration.StandardSequences.FrontierConditions_GlobalTag_cff import*
import CalibTracker.Configuration.Common.PoolDBESSource_cfi

# ---------------------- PB Geometry -------------------
process.trackerGeometryDB.applyAlignment = cms.bool(True)
# should it be False?
process.XMLFromDBSource.label=''
process.PoolDBESSourceGeometry = cms.ESSource("PoolDBESSource",
  timetype = cms.string('runnumber'),
  connect = cms.string('frontier://FrontierPrep/CMS_CONDITIONS'),
  toGet = cms.VPSet(
    cms.PSet(
      record = cms.string('GeometryFileRcd'),
      tag = cms.string('SiPixelPilotGeometry_v1')
    ),
    cms.PSet(
      record = cms.string('IdealGeometryRecord'),
      tag = cms.string('TKRECO_Geometry_forPilotBlade_v1')
    ),
    cms.PSet(
      record = cms.string('PGeometricDetExtraRcd'),
      tag = cms.string('TKExtra_Geometry_forPilotBlade_v1')
    ),
    cms.PSet(
      record = cms.string('PTrackerParametersRcd'),
      tag = cms.string('TKParameters_Geometry_forPilotBlade_v1')
    ),
  )
)
process.es_prefer_geometry = cms.ESPrefer( "PoolDBESSource", "PoolDBESSourceGeometry" )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.TFileService = cms.Service("TFileService", fileName = cms.string('./Summary_payload.root') )

process.source = cms.Source("EmptyIOVSource",                            
    #lastRun = cms.untracked.uint32(1),
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(1),
    lastValue = cms.uint64(1),
    interval = cms.uint64(1)
    )

process.gainDBOffline = cms.EDAnalyzer("SiPixelGainCalibrationDBUploader",
    #inputrootfile = cms.untracked.string('/data/vami/projects/pilotBlade/GainDB/GainCalibration.root'),
    inputrootfile = cms.untracked.string('/data/vami/projects/pilotBlade/GainDB/GainRun_2734/GainCalibration1240.root'),
    record = cms.untracked.string('SiPixelGainCalibrationOfflineRcd'),
    useMeanWhenEmpty = cms.untracked.bool(True),
    badChi2Prob = cms.untracked.double(0.00001)                                    
    )

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(10),
        authenticationPath = cms.untracked.string('.')
        ),
    toPut = cms.VPSet(
        cms.PSet(
            record = cms.string('SiPixelGainCalibrationOfflineRcd'),
            tag = cms.string('GainCalib_PilotBlade_offline_data_v1')
            )
        ),
    connect = cms.string('sqlite_file:./GainDB_Offline.db')
)
process.p = cms.Path(process.gainDBOffline)

