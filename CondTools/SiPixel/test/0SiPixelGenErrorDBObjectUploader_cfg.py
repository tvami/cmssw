import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("SiPixelGenErrorDBUpload")
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


# --------------------- GlobalTag ----------------------
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '') 
# auto:run2_mc = 'MCRUN2_74_V7'
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

print process.GlobalTag.globaltag
import CalibTracker.Configuration.Common.PoolDBESSource_cfi

# ---------------------- PB Geometry -------------------
process.trackerGeometryDB.applyAlignment = cms.bool(False)
process.XMLFromDBSource.label=''
process.PoolDBESSourceGeometry = cms.ESSource("PoolDBESSource",
	process.CondDBSetup,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(
		cms.PSet(
			record = cms.string('GeometryFileRcd'),
			tag = cms.string('XMLFILE_Geometry_74YV2_Extended2015_mc')
		),
		cms.PSet(
			record = cms.string('IdealGeometryRecord'),
			tag = cms.string('TKRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PGeometricDetExtraRcd'),
			tag = cms.string('TKExtra_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PTrackerParametersRcd'),
			tag = cms.string('TKParameters_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PEcalBarrelRcd'),
			tag = cms.string('EBRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PEcalEndcapRcd'),
			tag = cms.string('EERECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PEcalPreshowerRcd'),
			tag = cms.string('EPRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PHcalRcd'),
			tag = cms.string('HCALRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PCaloTowerRcd'),
			tag = cms.string('CTRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PZdcRcd'),
			tag = cms.string('ZDCRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('PCastorRcd'),
			tag = cms.string('CASTORRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('CSCRecoGeometryRcd'),
			tag = cms.string('CSCRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('CSCRecoDigiParametersRcd'),
			tag = cms.string('CSCRECODIGI_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('DTRecoGeometryRcd'),
			tag = cms.string('DTRECO_Geometry_74YV2')
		),
		cms.PSet(
			record = cms.string('RPCRecoGeometryRcd'),
			tag = cms.string('RPCRECO_Geometry_74YV2')
		)
	),
	connect = cms.string('sqlite_file:/data/vami/projects/PilotBlade/PilotGeometry.db') 
		#PilotGeometry.db --> with PB and Fake PB
		#PilotGeometry0.db --> with PB only
)
process.es_prefer_geometry = cms.ESPrefer( "PoolDBESSource", "PoolDBESSourceGeometry" )
#-------------------------------------------------------

MagFieldValue = float(sys.argv[2])

print '\nMagField = %f \n' % (MagFieldValue)
#version = 'v2'
version = sys.argv[3]

if ( MagFieldValue==0 ):
    MagFieldString = '0T'
    files_to_upload = cms.vstring(
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0022.out",
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0023.out")
    theDetIds      = cms.vuint32( 1, 2) # 0 is for all, 1 is Barrel, 2 is EndCap theGenErrorIds = cms.vuint32(22,23)
elif ( MagFieldValue==4 or MagFieldValue==40 ):
    MagFieldString = '4T'
    files_to_upload = cms.vstring(
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0018.out",
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0019.out")
    theDetIds      = cms.vuint32( 1, 2)
    theGenErrorIds = cms.vuint32(18,19)
elif ( MagFieldValue==3.8 or MagFieldValue==38 ):
    MagFieldString = '38T'
    files_to_upload = cms.vstring(
#        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0020.out",
#        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0021.out")
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0030.out",
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0031.out")
    theDetIds      = cms.vuint32( 1, 2)
    theGenErrorIds = cms.vuint32(30,31)
elif ( MagFieldValue==2 or MagFieldValue==20 ):
    MagFieldString = '2T'
    files_to_upload = cms.vstring(
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0030.out",
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0031.out")
    theDetIds      = cms.vuint32( 1, 2)
    theGenErrorIds = cms.vuint32(30,31)
elif ( MagFieldValue==3 or MagFieldValue==30 ):
    MagFieldString = '3T'
    files_to_upload = cms.vstring(
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0032.out",
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0033.out")
    theDetIds      = cms.vuint32( 1, 2)
    theGenErrorIds = cms.vuint32(32,33)
elif( MagFieldValue==3.5 or MagFieldValue==35 ):
    MagFieldString = '35T'
    files_to_upload = cms.vstring(
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0034.out",
        "CalibTracker/SiPixelESProducers/data/generror_summary_zp0035.out")
    theDetIds      = cms.vuint32( 1, 2)
    theGenErrorIds = cms.vuint32(34,35)



generror_base = 'SiPixelGenErrorDBObject' + MagFieldString + version
#theGenErrorBaseString = cms.string(generic_base)

print '\nUploading %s with record SiPixelGenErrorDBObjectRcd in file siPixelGenErrors%s%s.db\n' % (generror_base,MagFieldString,version)

process.source = cms.Source("EmptyIOVSource",
                            timetype = cms.string('runnumber'),
                            firstValue = cms.uint64(1),
                            lastValue = cms.uint64(1),
                            interval = cms.uint64(1)
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
    )

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
                                          DBParameters = cms.PSet(
    messageLevel = cms.untracked.int32(0),
    authenticationPath = cms.untracked.string('.')
    ),
                                          timetype = cms.untracked.string('runnumber'),
                                          connect = cms.string('sqlite_file:siPixelGenErrors' + MagFieldString + version + '.db'),
                                          toPut = cms.VPSet(cms.PSet(
    record = cms.string('SiPixelGenErrorDBObjectRcd'),
    tag = cms.string(generror_base)
    ))
                                          )

process.uploader = cms.EDAnalyzer("SiPixelGenErrorDBObjectUploader",
                                  siPixelGenErrorCalibrations = files_to_upload,
                                  theGenErrorBaseString = cms.string(generror_base),
                                  Version = cms.double("3.0"),
                                  MagField = cms.double(MagFieldValue),
                                  detIds = theDetIds,
                                  generrorIds = theGenErrorIds
)


process.myprint = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path(process.uploader)
process.CondDBCommon.connect = 'sqlite_file:siPixelGenErrors' + MagFieldString + '.db'
process.CondDBCommon.DBParameters.messageLevel = 0
process.CondDBCommon.DBParameters.authenticationPath = './'
