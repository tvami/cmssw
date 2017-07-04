import FWCore.ParameterSet.Config as cms

process = cms.Process("MapWriter")
process.load("CondCore.DBCommon.CondDBCommon_cfi")

#process.load("Configuration.StandardSequences.GeometryDB_cff")
#process.load("Configuration.Geometry.GeometryExtended2017Reco_cff")

#from Configuration.AlCa.autoCond_condDBv2 import autoCond
#process.GlobalTag.globaltag = autoCond['phase1_2017_design']
#process.GlobalTag = GlobalTag(process.GlobalTag, 'phase1_2017_design', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '76X_upgrade2017_design_v8', '')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


# ---------------------- PB Geometry -------------------
process.trackerGeometryDB.applyAlignment = cms.bool(True)
#process.XMLFromDBSource.label=''
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
#-------------------------------------------------------

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v11', '')

process.source = cms.Source("EmptyIOVSource",
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(1),
    lastValue = cms.uint64(1),
    interval = cms.uint64(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(
     messageLevel = cms.untracked.int32(0),
     authenticationPath = cms.untracked.string('.')
    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string("sqlite_file:/data/vami/projects/pilotBlade/pp2016miniDAQ_v2/CMSSW_8_0_9/src/SiPixelFedCablingMap_FED1240_v1.db"),
    #process.CondDBCommon,
    toPut = cms.VPSet(cms.PSet(
        record =  cms.string('SiPixelFedCablingMapRcd'),
		label = cms.untracked.string('pilotBlade'),
        tag = cms.string('SiPixelFedCablingMap_FED1240_v1')
    )),
    # loadBlobStreamer = cms.untracked.bool(False)
)

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('*'),
    destinations = cms.untracked.vstring('log'),
    #log = cms.untracked.PSet( threshold = cms.untracked.string('DEBUG'))
    log = cms.untracked.PSet( threshold = cms.untracked.string('WARNING'))
)

#process.load("CalibTracker.SiPixelConnectivity.PixelToLNKAssociateFromAsciiESProducer_cfi")

process.mapwriter = cms.EDAnalyzer("SiPixelFedCablingMapWriter",
  record = cms.string('SiPixelFedCablingMapRcd'),
  fileName = cms.untracked.string('pixelToLNK_pilot.ascii')
  #phase1 = cms.untracked.bool(True),
  #associator = cms.untracked.string('PixelToLNKAssociateFromAscii')
)

process.p1 = cms.Path(process.mapwriter)
