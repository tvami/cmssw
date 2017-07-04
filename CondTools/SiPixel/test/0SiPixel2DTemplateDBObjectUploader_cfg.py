#  Marc Osherson, Test Code for Pixel Template Uploader
#     Oct 2012

import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("SiPixel2DTemplateDBUpload")
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("FWCore.MessageService.MessageLogger_cfi")

process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

# ---------------------- PB Geometry -------------------
# --------------------- GlobalTag ----------------------
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '') # = 'MCRUN2_74_V7'
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

print process.GlobalTag.globaltag
import CalibTracker.Configuration.Common.PoolDBESSource_cfi

process.trackerGeometryDB.applyAlignment = cms.bool(False)
process.XMLFromDBSource.label=''
process.PoolDBESSourceGeometry = cms.ESSource("PoolDBESSource",
                               process.CondDBSetup,
                               timetype = cms.string('runnumber'),
                               toGet = cms.VPSet(
							cms.PSet(record = cms.string('GeometryFileRcd'),tag = cms.string('XMLFILE_Geometry_74YV2_Extended2015_mc')),
                                                        cms.PSet(record = cms.string('IdealGeometryRecord'),tag = cms.string('TKRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PGeometricDetExtraRcd'),tag = cms.string('TKExtra_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PTrackerParametersRcd'),tag = cms.string('TKParameters_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PEcalBarrelRcd'),   tag = cms.string('EBRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PEcalEndcapRcd'),   tag = cms.string('EERECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PEcalPreshowerRcd'),tag = cms.string('EPRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PHcalRcd'),         tag = cms.string('HCALRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PCaloTowerRcd'),    tag = cms.string('CTRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PZdcRcd'),          tag = cms.string('ZDCRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('PCastorRcd'),       tag = cms.string('CASTORRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('CSCRecoGeometryRcd'),tag = cms.string('CSCRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('CSCRecoDigiParametersRcd'),tag = cms.string('CSCRECODIGI_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('DTRecoGeometryRcd'),tag = cms.string('DTRECO_Geometry_74YV2')),
                                                        cms.PSet(record = cms.string('RPCRecoGeometryRcd'),tag = cms.string('RPCRECO_Geometry_74YV2'))
                                                        ),
                               connect = cms.string('sqlite_file:/data/vami/projects/PilotBlade/PilotGeometry.db')
                               )
process.es_prefer_geometry = cms.ESPrefer( "PoolDBESSource", "PoolDBESSourceGeometry" )
#-------------------------------------------------------


MagFieldValue = float(sys.argv[2])
#version = 'v2'
version = sys.argv[3]

# Removed all but mag = 3.8 for testing.
if ( MagFieldValue==3.8 or MagFieldValue==38 ):
    MagFieldString = '38'
    #file_path = "CalibTracker/SiPixelESProducers/data/template2D_IOV5/template_summary2D_"
    file_path = "CondTools/SiPixel/data/template2D_IOV5/template_summary2D_"
    suffix = ".out"
    files_to_upload = cms.vstring(
#	file_path + "zp2840" + suffix,
#	file_path + "zp2940" + suffix,	
#	file_path + "zp3641" + suffix,
#	file_path + "zp3741" + suffix,
#	file_path + "zp3242" + suffix,
#	file_path + "zp3342" + suffix,
#	file_path + "zp0940" + suffix,
#	file_path + "zp0941" + suffix,
	file_path + "zp0942" + suffix
)
### We must now ID each of these templates. Match each ID "zp####" in the appropriate array position below:
    theTemplateIds = cms.vuint32(2940,2940,2940,2940,2840,2840,2840,2840,3741,3741,3741,
#Corresponds to array position.	# 0    1     2    3    4    5    6    7    8    9   10
				 3741,3641,3641,3641,3641,3342,3342,3342,3342,3242,3242,
                               	#11    12   13   14   15   16   17   18   19   20   21
				 3242,3242,940,941,942,942,940,941,942,942,940,
                                #22   23    24    25   26  27   28   29   30    31    32
				 941,942,942,940,941,942,942,940,941,942,940,
                                #33   34   35   36   37   38   39   40   41   42    43
				 941,942,940,941,942,940,941,942)
                                #44   45    46   47   48   49   50    51

 			
else :
    print 'ERROR... please use values 38 and v3.'


template_base = 'SiPixel2DTemplateDBObject' + MagFieldString + 'T'
#theTemplateBaseString = cms.string(template_base)

print '\nUploading %s%s with record SiPixel2DTemplateDBObjectRcd in file siPixel2DTemplates%sT_IOV5.db\n' % (template_base,version,MagFieldString)

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
                                          connect = cms.string('sqlite_file:siPixel2DTemplates' + MagFieldString + 'T_IOV5.db'),
                                          toPut = cms.VPSet(cms.PSet(
    record = cms.string('SiPixel2DTemplateDBObjectRcd'),
    tag = cms.string(template_base + version)
    ))
                                          )

process.uploader = cms.EDAnalyzer("SiPixel2DTemplateDBObjectUploader",
                                  siPixelTemplateCalibrations = files_to_upload,
                                  theTemplateBaseString = cms.string(template_base),
                                  Version = cms.double("17.0"),
                                  MagField = cms.double(MagFieldValue),
                                  templateIds = theTemplateIds
)


process.myprint = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path(process.uploader)
process.CondDBCommon.connect = 'sqlite_file:siPixel2DTemplates' + MagFieldString + 'T.db'
process.CondDBCommon.DBParameters.messageLevel = 0
process.CondDBCommon.DBParameters.authenticationPath = './'
