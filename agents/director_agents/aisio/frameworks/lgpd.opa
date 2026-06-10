package aisio.lgpd

import future.keywords.if
import future.keywords.contains

# ==========================================
# LGPD Compliance Policies for Aísio
# ==========================================

valid_legal_bases := {
    "consent", "legal_obligation", "public_policy", "research",
    "contract", "regular_rights_exercise", "life_protection",
    "health_protection", "legitimate_interest", "credit_protection",
}

sensitive_data_types := {
    "racial_origin", "religious_conviction", "health",
    "biometric", "sexual_orientation", "union_membership",
}

default allow := false

allow if { count(violations) == 0 }

violations contains msg if { msg := legal_basis_check() }
violations contains msg if { msg := sensitive_data_check() }
violations contains msg if { msg := consent_check() }
violations contains msg if { msg := dpia_check() }
violations contains msg if { msg := retention_check() }
violations contains msg if { msg := international_transfer_check() }
violations contains msg if { msg := incident_response_check() }
violations contains msg if { msg := dpo_check() }

legal_basis_check := "No valid legal basis provided" if {
    not input.legal_basis in valid_legal_bases
}

sensitive_data_check := "Sensitive data without specific legal basis (art. 11)" if {
    input.data_type == "sensitive"
    not input.legal_basis in {"consent", "legal_obligation", "life_protection", "health_protection"}
}

consent_check := "Consent not freely given" if {
    input.legal_basis == "consent"
    not input.consent.freely_given
}

consent_check := "Consent response exceeds 15-day deadline" if {
    input.response_days > 15
}

dpia_check := "DPIA required but not conducted (art. 38)" if {
    input.dpia_required == true
    input.dpia_conducted == false
}

dpia_check := "DPIA required for large-scale sensitive data" if {
    input.data_type == "sensitive"
    input.data_scale == "large"
    input.dpia_conducted == false
}

retention_check := "Retention exceeds necessity principle (art. 15)" if {
    input.retention_days > 3650
}

international_transfer_check := "Transfer without adequate safeguards (art. 33)" if {
    input.transfer_international == true
    not input.transfer_safeguards in {"adequacy", "scc", "bcr", "consent", "contract"}
}

incident_response_check := "Incident not communicated within reasonable period" if {
    input.incident_occurred == true
    input.incident_notified == false
}

incident_response_check := "Incident notification exceeds 2 business days" if {
    input.incident_occurred == true
    input.incident_notification_days > 2
}

dpo_check := "DPO not appointed (art. 41)" if {
    input.dpo_appointed == false
}

summary := {
    "compliant": allow,
    "violations": violations,
    "framework": "LGPD",
    "version": "Lei 13.709/2018",
}

report := {"status": "PASS"} if allow
report := {"status": "FAIL", "violations": violations} if not allow
