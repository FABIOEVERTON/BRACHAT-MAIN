package aisio.eu_ai_act

import future.keywords.if
import future.keywords.contains

# ==========================================
# EU AI Act Compliance Policies for Aísio
# ==========================================

prohibited_practices := {
    "manipulative_techniques", "social_scoring", "real_time_biometric_public",
    "criminal_prediction_profile_only", "biometric_categorization_sensitive",
    "facial_scraping", "emotion_recognition_workplace", "emotion_recognition_education",
}

default allow := false
allow if { count(violations) == 0 }

violations contains msg if { msg := prohibited_practice_check() }
violations contains msg if { msg := high_risk_requirements_check() }
violations contains msg if { msg := transparency_check() }
violations contains msg if { msg := gpai_check() }
violations contains msg if { msg := human_oversight_check() }
violations contains msg if { msg := conformity_check() }
violations contains msg if { msg := fundamental_rights_check() }

prohibited_practice_check := "Prohibited AI practice: " + input.practice if {
    input.risk_category == "unacceptable"
    input.practice in prohibited_practices
}

high_risk_requirements_check := "High-risk: no risk management system (Art. 9)" if {
    input.risk_category == "high"
    input.risk_management == false
}
high_risk_requirements_check := "High-risk: inadequate data governance (Art. 10)" if {
    input.risk_category == "high"
    not input.data_governance in {"adequate", "compliant"}
}
high_risk_requirements_check := "High-risk: missing technical documentation (Art. 11)" if {
    input.risk_category == "high"
    input.technical_documentation == false
}
high_risk_requirements_check := "High-risk: no record-keeping (Art. 12)" if {
    input.risk_category == "high"
    input.record_keeping == false
}
high_risk_requirements_check := "High-risk: insufficient transparency (Art. 13)" if {
    input.risk_category == "high"
    input.transparency_provided == false
}

transparency_check := "Chatbot without AI disclosure (Art. 50)" if {
    input.system_type == "chatbot"
    input.discloses_ai_interaction == false
}
transparency_check := "AI content not labeled (Art. 50)" if {
    input.creates_synthetic_content == true
    input.content_labeled == false
}
transparency_check := "Deepfake without disclosure (Art. 50)" if {
    input.system_type == "deepfake"
    input.discloses_manipulation == false
}

gpai_check := "GPAI: missing technical documentation (Art. 53)" if {
    input.system_type == "gpai"
    input.gpai_technical_documentation == false
}
gpai_check := "GPAI: no copyright policy (Art. 53)" if {
    input.system_type == "gpai"
    input.gpai_copyright_policy == false
}
gpai_check := "GPAI: no training data summary (Art. 53)" if {
    input.system_type == "gpai"
    input.gpai_training_data_summary == false
}
gpai_check := "GPAI systemic: missing model evaluation (Art. 55)" if {
    input.gpai_systemic_risk == true
    input.gpai_model_evaluation == false
}
gpai_check := "GPAI systemic: no adversarial testing (Art. 55)" if {
    input.gpai_systemic_risk == true
    input.gpai_adversarial_testing == false
}
gpai_check := "GPAI systemic: no incident reporting (Art. 55)" if {
    input.gpai_systemic_risk == true
    input.gpai_incident_reporting == false
}

human_oversight_check := "High-risk: no human oversight (Art. 14)" if {
    input.risk_category == "high"
    input.human_oversight == false
}

conformity_check := "High-risk: no CE conformity assessment (Art. 43)" if {
    input.risk_category == "high"
    input.conformity_assessment == false
}
conformity_check := "High-risk: not in EU database (Art. 49)" if {
    input.risk_category == "high"
    input.eu_database_registered == false
}
conformity_check := "High-risk Annex III: needs notified body (Art. 43)" if {
    input.annex_iii == true
    input.notified_body_assessment == false
}

fundamental_rights_check := "High-risk: missing FRIA (Art. 27)" if {
    input.risk_category == "high"
    input.fria_conducted == false
}

summary := {
    "compliant": allow,
    "violations": violations,
    "risk_category": input.risk_category,
    "framework": "EU AI Act",
    "version": "Regulation (EU) 2024/1689",
}

report := {"status": "PASS"} if allow
report := {"status": "FAIL", "violations": violations} if not allow
