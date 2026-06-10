package aisio.nist_ai_rmf

import future.keywords.if
import future.keywords.contains

# ==========================================
# NIST AI RMF 1.0 Compliance Policies for Aísio
# ==========================================

default allow := false
allow if { count(violations) == 0 }

violations contains msg if { msg := govern_check() }
violations contains msg if { msg := map_check() }
violations contains msg if { msg := measure_check() }
violations contains msg if { msg := manage_check() }
violations contains msg if { msg := trustworthy_check() }
violations contains msg if { msg := third_party_check() }

# GOVERN
govern_check := "GOV-1: No AI risk management policy" if { input.govern.policy_established == false }
govern_check := "GOV-2: No accountability structure" if { input.govern.accountability_assigned == false }
govern_check := "GOV-3: Third-party risk not managed" if { input.govern.third_party_risk_managed == false }
govern_check := "GOV-4: No multidisciplinary team" if { input.govern.multidisciplinary_team == false }
govern_check := "GOV-5: Not integrated into ERM" if { input.govern.erm_integrated == false }

# MAP
map_check := "MAP-1: System purpose not defined" if { input.map.purpose_defined == false }
map_check := "MAP-2: Laws/regs not mapped" if { input.map.laws_mapped == false }
map_check := "MAP-3: Impacts not mapped" if { input.map.impacts_mapped == false }
map_check := "MAP-4: Components/lifecycle not mapped" if { input.map.components_mapped == false }
map_check := "MAP-5: Risks not identified" if { input.map.risks_identified == false }

# MEASURE
measure_check := "MEAS-1: No trustworthiness metrics" if { input.measure.trustworthiness_metrics == false }
measure_check := "MEAS-2: System not risk-evaluated" if { input.measure.risk_evaluated == false }
measure_check := "MEAS-3: No baseline monitoring" if { input.measure.baseline_monitored == false }
measure_check := "MEAS-4: No feedback mechanisms" if { input.measure.feedback_mechanisms == false }
measure_check := "MEAS-5: No testing protocols" if { input.measure.testing_protocols == false }

# MANAGE
manage_check := "MAN-1: No risk response strategy" if { input.manage.risk_response_strategy == false }
manage_check := "MAN-2: No treatment plan" if { input.manage.treatment_plan == false }
manage_check := "MAN-3: No ongoing monitoring" if { input.manage.ongoing_monitoring == false }
manage_check := "MAN-4: No incident response plan" if { input.manage.incident_response_plan == false }
manage_check := "MAN-5: Risks not documented" if { input.manage.risk_documentation == false }

# TRUSTWORTHINESS
trustworthy_check := "Trust: validity/reliability not shown" if { not input.trustworthy.valid_reliable }
trustworthy_check := "Trust: safety not assured" if { not input.trustworthy.safe }
trustworthy_check := "Trust: security/resilience not addressed" if { not input.trustworthy.secure_resilient }
trustworthy_check := "Trust: accountability/transparency lacking" if { not input.trustworthy.accountable_transparent }
trustworthy_check := "Trust: explainability not addressed" if { not input.trustworthy.explainable_interpretable }
trustworthy_check := "Trust: privacy not enhanced" if { not input.trustworthy.privacy_enhanced }
trustworthy_check := "Trust: fairness/bias not managed" if { not input.trustworthy.fair_bias_managed }

# THIRD PARTY
third_party_check := "Third-party: supplier not assessed" if {
    input.third_party.used == true
    input.third_party.supplier_assessed == false
}
third_party_check := "Third-party: no contractual safeguards" if {
    input.third_party.used == true
    input.third_party.contractual_safeguards == false
}

# GENERATIVE AI PROFILE (NIST AI 600-1)
genai_check := "GenAI: hallucination risk not mitigated" if {
    input.genai_profile == true
    input.genai.hallucination_mitigated == false
}
genai_check := "GenAI: no content provenance" if {
    input.genai_profile == true
    input.genai.content_provenance == false
}
genai_check := "GenAI: misuse not assessed" if {
    input.genai_profile == true
    input.genai.misuse_assessed == false
}

summary := {
    "compliant": allow,
    "violations": violations,
    "framework": "NIST AI RMF",
    "version": "1.0",
}

report := {"status": "PASS"} if allow
report := {"status": "FAIL", "violations": violations} if not allow
