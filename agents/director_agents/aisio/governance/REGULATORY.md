# Regulatory Compliance Framework — BRACHÁT

## EU AI Act (Regulation 2024/1689)
**Risk categories:**
- Unacceptable (prohibited): social scoring, manipulative AI, real-time biometric surveillance → **BAN**
- High-risk: recruitment, credit, medical, law enforcement, critical infra, education, migration, justice → **STRICT COMPLIANCE**
- Limited: chatbots, deepfakes → **TRANSPARENCY**
- Minimal: spam filters, basic analytics → **GENERAL LAWS**

**High-risk requirements (Art. 9-15):**
- Risk management system (Art. 9) — documentado, contínuo
- Data governance (Art. 10) — qualidade, bias mitigation
- Technical documentation (Art. 11) — registro completo
- Record-keeping (Art. 12) — logging obrigatório
- Transparency (Art. 13) — explainability, instructions
- Human oversight (Art. 14) — trained supervisors, operational controls
- Accuracy/robustness/cybersecurity (Art. 15) — resilience, feedback loops

**Penalties:** até €35M ou 7% do faturamento global anual

## NIST AI RMF 1.0
**4 core functions:**
- GOVERN — policies, accountability, diversity, communication, supply chain risk
- MAP — document purpose, stakeholders, risk tolerance, categorize system, 3rd-party risks
- MEASURE — safety metrics, fairness/bias, feedback loops, performance monitoring
- MANAGE — determine fit, develop strategies, manage 3rd-party risks, document treatments

**7 trustworthiness characteristics:**
valid & reliable, safe, secure & resilient, accountable & transparent, explainable & interpretable, privacy-enhanced, fair with bias managed

## LGPD (Lei 13.709/2018)
**10 principles (Art. 6):** purpose, appropriateness, necessity, free access, data quality, transparency, security, prevention, non-discrimination, accountability

**Data subject rights (Art. 18):** confirmation, access, correction, anonymization/blocking/deletion, portability, deletion of consented data, sharing info, consequences of denial, revocation

**Enforcement:** ANPD, penalties até 2% do faturamento (limitado a R$50M)

## PL 2338/2023 (Brazilian AI Bill — in progress)
**Risk categories:** excessive (prohibited), high risk (strict governance), lower risk (proportionate)

**Key provisions:** transparency, security, data protection (aligned with LGPD), accountability, prohibition of harmful uses, SIA creation, regulatory sandbox, copyright for non-profit training

**Penalties:** até R$50M ou 2% do faturamento no Brasil

**Enforcement:** ANPD + sectoral regulators (BACEN, ANATEL, ANS)

## BRACHÁT Compliance Mapping
| Domain | Framework | Aísio Enforcement |
|--------|-----------|-------------------|
| Agent actions | AGCP L2+ | Commit-bound authorization |
| Agent lifecycle | QILIS | Interpretability trace |
| High-risk AI | EU AI Act | Risk classification + documentation per agent |
| Data privacy | LGPD | Data governance + subject rights |
| AI risk | NIST AI RMF | GOVERN/MAP/MEASURE/MANAGE cycle |
| AI regulation | PL 2338 | Tracking bill progress + gap analysis |
| Bias/fairness | NIST + EU AI Act | Bias metrics in agent evaluation |
| Security | NIST + AGCP L3+ | Invariant enforcement + replay validation |
| Transparency | EU AI Act + LGPD | Explainability output per action |
| Human oversight | EU AI Act Art. 14 | HITL approval gates (AGCP L4) |
