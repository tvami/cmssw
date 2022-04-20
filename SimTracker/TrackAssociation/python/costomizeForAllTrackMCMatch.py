import FWCore.ParameterSet.Config as cms

def costomizeForAllTrackMCMatch(process):
   process.load("SimGeneral.TrackingAnalysis.simHitTPAssociation_cfi")
   process.load('SimTracker.TrackAssociation.trackMCMatchSequence_cff')

   if hasattr(process, 'reconstruction'):
      process.trackMCMatchSequenceWithTPAssociation = cms.Sequence(quickTrackAssociatorByHits*trackAssociatorByHits*trackMCMatch*standAloneMuonsMCMatch*globalMuonsMCMatch*allTrackMCMatch*quickTrackAssociatorByHits*trackingParticleRecoTrackAsssociation*assoc2secStepTk*assoc2thStepTk*assoc2GsfTracks*assocOutInConversionTracks*assocInOutConversionTracks*simHitTPAssocProducer)
      process.MCMatch_step = cms.Path(process.trackMCMatchSequenceWithTPAssociation)
      process.schedule.append(process.MCMatch_step)

   return process
