---
id: ADR-004
title: Implementação do QILIS e Pivot para BTScan e BTMonitor
status: Accepted
date: 2026-09-24
author: Tony Stark (Arquiteto de Software) / Wizer (Produto)
---

# ADR-004: Implementação Matemática do QILIS e Reestruturação de Produto

## 1. Contexto e Problema
A auditoria de Inteligência Artificial usando outros modelos baseados em LLM cria um ciclo perigoso de "caixas pretas" validando caixas pretas, introduzindo alucinações e vieses algorítmicos na própria camada de segurança. Além disso, a divisão anterior do produto em 4 passos lógicos gerava atrito comercial.

## 2. Decisão Arquitetural e de Produto
Foi decidido realizar um "Pivot" na Governança de IA consolidando a oferta em dois produtos principais e incorporando a matemática do QILIS (Quantum-Inspired Lifecycle Interpretability System) de forma nativa.

### 2.1. Reestruturação do Produto
A plataforma passa a ser vendida estritamente através de:
- **BTScan:** Foco em Discovery, mapeamento de rede e auditoria histórica (Shadow AI) com uso retroativo do QILIS e custódia em Cofre.
- **BTMonitor:** Foco em Segurança Inline 24/7 (Commit-Bound). Atua como proxy reverso com latência zero, aplicando o QILIS "em voo".

### 2.2. O Motor Matemático (Engine A - QILIS)
- **Proibição de LLM para Auditoria Inline:** O BTMonitor **não** usará LLMs para avaliar se um prompt é seguro.
- **Abordagem Algébrica (Sem Viés):** A engenharia utilizará Álgebra Linear Clássica (via `numpy`/`scipy` em Python) para emular a Cognição Quântica.
- **Mecânica:** 
  1. Extração do Embedding vetorial bruto.
  2. Transformação do vetor em uma **Matriz de Densidade** (representando o Espaço de Hilbert da requisição).
  3. Cálculo determinístico de *Fidelidade Quântica* e *Entropia de von Neumann* para detectar anomalias (Data Drift, Injeção de Prompts).
- **Justificativa Legal:** A matemática fornece prova determinística, sem o viés inerente aos modelos de linguagem treinados na internet.

### 2.3. O Cofre Criptográfico (Engine B - WORM/SHA-256)
A arquitetura "Time-Travel" passa a ser o motor de armazenamento unificado. O banco de dados PostgreSQL isolado (schema-per-tenant) deve garantir a cadeia de custódia inquebrável.

## 3. Consequências e Requisitos Técnicos
1. **Schema do Banco de Dados:** TODAS as tabelas de logs (ex: `forensic_ledger`) devem obrigatoriamente possuir as seguintes colunas:
   - `previous_hash` (VARCHAR 64)
   - `current_hash` (VARCHAR 64)
   - `qilis_signature_vector` (JSONB ou ARRAY de Float representando a assinatura matemática).
2. **Performance Backend:** O microsserviço em FastAPI deve executar o cálculo matricial do QILIS em menos de 20ms para não degradar a experiência do BTMonitor.
