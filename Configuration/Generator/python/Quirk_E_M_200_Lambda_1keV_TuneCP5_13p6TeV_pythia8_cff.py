# Color-neutral "E" quirk pair, Drell-Yan gamma*/Z -> tau' tau'bar (PDG 17)
# with the tau' stable. The infracolor string is added in Geant4 by
# SimG4Core/CustomPhysics/Exotica_Quirk_SIM_cfi.customise.
# Cross sections: multiply by N_IC = 2 (and an NLO K-factor of 1.3 to 1.5).
QUIRK_MASS = 200.     # GeV
QUIRK_LAMBDA = 1000.  # eV, string tension F = Lambda^2 / (hbar c)
# From about 1 keV the pair moves as one object along its total momentum,
# mostly forward; keep events whose pair points into the tracker.
# Set to None below about 1 keV, where the quirks separate by more than a meter.
PAIR_ETA_MAX = 2.5

import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(-1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),
    crossSection = cms.untracked.double(-1),
    maxEventsToPrint = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            # SM gamma*/Z only (no Z'); the gmZ resonance code stops at PDG 16
            'NewGaugeBoson:ffbar2gmZZprime = on',
            'Zprime:gmZmode = 4',
            'Zprime:coup2gen4 = on',
            '32:mMin = %.1f' % (2 * QUIRK_MASS + 1.),
            '32:onMode = off',
            '32:onIfMatch = 17 -17',
            '17:m0 = %.1f' % QUIRK_MASS,
            '17:mWidth = 0.',
            '17:mayDecay = off',
            '17:isResonance = false',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters')
    )
)

generator.quirkMass = cms.untracked.double(QUIRK_MASS)
generator.quirkLambda = cms.untracked.double(QUIRK_LAMBDA)

if PAIR_ETA_MAX is None:
    ProductionFilterSequence = cms.Sequence(generator)
else:
    genParticlesForFilter = cms.EDProducer("GenParticleProducer",
        saveBarCodes = cms.untracked.bool(True),
        src = cms.InputTag("generator", "unsmeared"),
        abortOnUnknownPDGCode = cms.untracked.bool(False)
    )
    quirksForFilter = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticlesForFilter"),
        cut = cms.string("abs(pdgId) == 17 && status == 1"),
        filter = cms.bool(True)
    )
    quirkPairForFilter = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("quirksForFilter@+ quirksForFilter@-"),
        cut = cms.string("abs(eta) < %f" % PAIR_ETA_MAX),
        checkCharge = cms.bool(True)
    )
    quirkPairFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("quirkPairForFilter"),
        minNumber = cms.uint32(1)
    )
    ProductionFilterSequence = cms.Sequence(generator * genParticlesForFilter * quirksForFilter *
                                            quirkPairForFilter * quirkPairFilter)
