# Workflow Automation
## 26 skills
---

## ai-agent-development
*AI agent development workflow for building autonomous agents, multi-agent systems, and agent orchestration with CrewAI, LangGraph, and custom agents.*

Risk: safe

# AI Agent Development Workflow

## Overview

Specialized workflow for building AI agents including single autonomous agents, multi-agent systems, agent orchestration, tool integration, and human-in-the-loop patterns.

## When to Use This Workflow

Use this workflow when:
- Building autonomous AI agents
- Creating multi-agent systems
- Implementing agent orchestration
- Adding tool integration to agents
- Setting up agent memory

## Workflow Phases

### Phase 1: Agent Design

#### Skills to Invoke
- `ai-agents-architect` - Agent architecture
- `autonomous-agents` - Autonomous patterns

#### Actions
1. Define agent purpose
2. Design agent capabilities
3. Plan tool integration
4. Design memory system
5. Define success metrics

#### Copy-Paste Prompts
```
Use @ai-agents-architect to design AI agent architecture
```

### Phase 2: Single Agent Implementation

#### Skills to Invoke
- `autonomous-agent-patterns` - Agent patterns
- `autonomous-agents` - Autonomous agents

#### Actions
1. Choose agent framework
2. Implement agent logic
3. Add tool integration
4. Configure memory
5. Test agent behavior

#### Copy-Paste Prompts
```
Use @autonomous-agent-patterns to implement single agent
```

### Phase 3: Multi-Agent System

#### Skills to Invoke
- `crewai` - CrewAI framework
- `multi-agent-patterns` - Multi-agent patterns

#### Actions
1. Define agent roles
2. Set up agent communication
3. Configure orchestration
4. Implement task delegation
5. Test coordination

#### Copy-Paste Prompts
```
Use @crewai to build multi-agent system with roles
```

### Phase 4: Agent Orchestration

#### Skills to Invoke
- `langgraph` - LangGraph orchestration
- `workflow-orchestration-patterns` - Orchestration

#### Actions
1. Design workflow graph
2. Implement state management
3. Add conditional branches
4. Configure persistence
5. Test workflows

#### Copy-Paste Prompts
```
Use @langgraph to create stateful agent workflows
```

### Phase 5: Tool Integration

#### Skills to Invoke
- `agent-tool-builder` - Tool building
- `tool-design` - Tool design

#### Actions
1. Identify tool needs
2. Design tool interfaces
3. Implement tools
4. Add error handling
5. Test tool usage

#### Copy-Paste Prompts
```
Use @agent-tool-builder to create agent tools
```

### Phase 6: Memory Systems

#### Skills to Invoke
- `agent-memory-systems` - Memory architecture
- `conversation-memory` - Conversation memory

#### Actions
1. Design memory structure
2. Implement short-term memory
3. Set up long-term memory
4. Add entity memory
5. Test memory retrieval

#### Copy-Paste Prompts
```
Use @agent-memory-systems to implement agent memory
```

### Phase 7: Evaluation

#### Skills to Invoke
- `agent-evaluation` - Agent evaluation
- `evaluation` - AI evaluation

#### Actions
1. Define evaluation criteria
2. Create test scenarios
3. Measure agent performance
4. Test edge cases
5. Iterate improvements

#### Copy-Paste Prompts
```
Use @agent-evaluation to evaluate agent performance
```

## Agent Architecture

```
User Input -> Planner -> Agent -> Tools -> Memory -> Response
              |          |        |        |
         Decompose   LLM Core  Actions  Short/Long-term
```

## Quality Gates

- [ ] Agent logic working
- [ ] Tools integrated
- [ ] Memory functional
- [ ] Orchestration tested
- [ ] Evaluation passing

## Related Workflow Bundles

- `ai-ml` - AI/ML development
- `rag-implementation` - RAG systems
- `workflow-automation` - Workflow patterns

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## ai-ml
*AI and machine learning workflow covering LLM application development, RAG implementation, agent architecture, ML pipelines, and AI-powered features.*

Risk: safe

# AI/ML Workflow Bundle

## Overview

Comprehensive AI/ML workflow for building LLM applications, implementing RAG systems, creating AI agents, and developing machine learning pipelines. This bundle orchestrates skills for production AI development.

## When to Use This Workflow

Use this workflow when:
- Building LLM-powered applications
- Implementing RAG (Retrieval-Augmented Generation)
- Creating AI agents
- Developing ML pipelines
- Adding AI features to applications
- Setting up AI observability

## Workflow Phases

### Phase 1: AI Application Design

#### Skills to Invoke
- `ai-product` - AI product development
- `ai-engineer` - AI engineering
- `ai-agents-architect` - Agent architecture
- `llm-app-patterns` - LLM patterns

#### Actions
1. Define AI use cases
2. Choose appropriate models
3. Design system architecture
4. Plan data flows
5. Define success metrics

#### Copy-Paste Prompts
```
Use @ai-product to design AI-powered features
```

```
Use @ai-agents-architect to design multi-agent system
```

### Phase 2: LLM Integration

#### Skills to Invoke
- `llm-application-dev-ai-assistant` - AI assistant development
- `llm-application-dev-langchain-agent` - LangChain agents
- `llm-application-dev-prompt-optimize` - Prompt engineering
- `gemini-api-dev` - Gemini API

#### Actions
1. Select LLM provider
2. Set up API access
3. Implement prompt templates
4. Configure model parameters
5. Add streaming support
6. Implement error handling

#### Copy-Paste Prompts
```
Use @llm-application-dev-ai-assistant to build conversational AI
```

```
Use @llm-application-dev-langchain-agent to create LangChain agents
```

```
Use @llm-application-dev-prompt-optimize to optimize prompts
```

### Phase 3: RAG Implementation

#### Skills to Invoke
- `rag-engineer` - RAG engineering
- `rag-implementation` - RAG implementation
- `embedding-strategies` - Embedding selection
- `vector-database-engineer` - Vector databases
- `similarity-search-patterns` - Similarity search
- `hybrid-search-implementation` - Hybrid search

#### Actions
1. Design data pipeline
2. Choose embedding model
3. Set up vector database
4. Implement chunking strategy
5. Configure retrieval
6. Add reranking
7. Implement caching

#### Copy-Paste Prompts
```
Use @rag-engineer to design RAG pipeline
```

```
Use @vector-database-engineer to set up vector search
```

```
Use @embedding-strategies to select optimal embeddings
```

### Phase 4: AI Agent Development

#### Skills to Invoke
- `autonomous-agents` - Autonomous agent patterns
- `autonomous-agent-patterns` - Agent patterns
- `crewai` - CrewAI framework
- `langgraph` - LangGraph
- `multi-agent-patterns` - Multi-agent systems
- `computer-use-agents` - Computer use agents

#### Actions
1. Design agent architecture
2. Define agent roles
3. Implement tool integration
4. Set up memory systems
5. Configure orchestration
6. Add human-in-the-loop

#### Copy-Paste Prompts
```
Use @crewai to build role-based multi-agent system
```

```
Use @langgraph to create stateful AI workflows
```

```
Use @autonomous-agents to design autonomous agent
```

### Phase 5: ML Pipeline Development

#### Skills to Invoke
- `ml-engineer` - ML engineering
- `mlops-engineer` - MLOps
- `machine-learning-ops-ml-pipeline` - ML pipelines
- `ml-pipeline-workflow` - ML workflows
- `data-engineer` - Data engineering

#### Actions
1. Design ML pipeline
2. Set up data processing
3. Implement model training
4. Configure evaluation
5. Set up model registry
6. Deploy models

#### Copy-Paste Prompts
```
Use @ml-engineer to build machine learning pipeline
```

```
Use @mlops-engineer to set up MLOps infrastructure
```

### Phase 6: AI Observability

#### Skills to Invoke
- `langfuse` - Langfuse observability
- `manifest` - Manifest telemetry
- `evaluation` - AI evaluation
- `llm-evaluation` - LLM evaluation

#### Actions
1. Set up tracing
2. Configure logging
3. Implement evaluation
4. Monitor performance
5. Track costs
6. Set up alerts

#### Copy-Paste Prompts
```
Use @langfuse to set up LLM observability
```

```
Use @evaluation to create evaluation framework
```

### Phase 7: AI Security

#### Skills to Invoke
- `prompt-engineering` - Prompt security
- `security-scanning-security-sast` - Security scanning

#### Actions
1. Implement input validation
2. Add output filtering
3. Configure rate limiting
4. Set up access controls
5. Monitor for abuse
6. Implement audit logging

## AI Development Checklist

### LLM Integration
- [ ] API keys secured
- [ ] Rate limiting configured
- [ ] Error handling implemented
- [ ] Streaming enabled
- [ ] Token usage tracked

### RAG System
- [ ] Data pipeline working
- [ ] Embeddings generated
- [ ] Vector search optimized
- [ ] Retrieval accuracy tested
- [ ] Caching implemented

### AI Agents
- [ ] Agent roles defined
- [ ] Tools integrated
- [ ] Memory working
- [ ] Orchestration tested
- [ ] Error handling robust

### Observability
- [ ] Tracing enabled
- [ ] Metrics collected
- [ ] Evaluation running
- [ ] Alerts configured
- [ ] Dashboards created

## Quality Gates

- [ ] All AI features tested
- [ ] Performance benchmarks met
- [ ] Security measures in place
- [ ] Observability configured
- [ ] Documentation complete

## Related Workflow Bundles

- `development` - Application development
- `database` - Data management
- `cloud-devops` - Infrastructure
- `testing-qa` - AI testing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## api-documentation
*API documentation workflow for generating OpenAPI specs, creating developer guides, and maintaining comprehensive API documentation.*

Risk: safe

# API Documentation Workflow

## Overview

Specialized workflow for creating comprehensive API documentation including OpenAPI/Swagger specs, developer guides, code examples, and interactive documentation.

## When to Use This Workflow

Use this workflow when:
- Creating API documentation
- Generating OpenAPI specs
- Writing developer guides
- Adding code examples
- Setting up API portals

## Workflow Phases

### Phase 1: API Discovery

#### Skills to Invoke
- `api-documenter` - API documentation
- `api-design-principles` - API design

#### Actions
1. Inventory endpoints
2. Document request/response
3. Identify authentication
4. Map error codes
5. Note rate limits

#### Copy-Paste Prompts
```
Use @api-documenter to discover and document API endpoints
```

### Phase 2: OpenAPI Specification

#### Skills to Invoke
- `openapi-spec-generation` - OpenAPI
- `api-documenter` - API specs

#### Actions
1. Create OpenAPI schema
2. Define paths
3. Add schemas
4. Configure security
5. Add examples

#### Copy-Paste Prompts
```
Use @openapi-spec-generation to create OpenAPI specification
```

### Phase 3: Developer Guide

#### Skills to Invoke
- `api-documentation-generator` - Documentation
- `documentation-templates` - Templates

#### Actions
1. Create getting started
2. Write authentication guide
3. Document common patterns
4. Add troubleshooting
5. Create FAQ

#### Copy-Paste Prompts
```
Use @api-documentation-generator to create developer guide
```

### Phase 4: Code Examples

#### Skills to Invoke
- `api-documenter` - Code examples
- `tutorial-engineer` - Tutorials

#### Actions
1. Create example requests
2. Write SDK examples
3. Add curl examples
4. Create tutorials
5. Test examples

#### Copy-Paste Prompts
```
Use @api-documenter to generate code examples
```

### Phase 5: Interactive Docs

#### Skills to Invoke
- `api-documenter` - Interactive docs

#### Actions
1. Set up Swagger UI
2. Configure Redoc
3. Add try-it functionality
4. Test interactivity
5. Deploy docs

#### Copy-Paste Prompts
```
Use @api-documenter to set up interactive documentation
```

### Phase 6: Documentation Site

#### Skills to Invoke
- `docs-architect` - Documentation architecture
- `wiki-page-writer` - Documentation

#### Actions
1. Choose platform
2. Design structure
3. Create pages
4. Add navigation
5. Configure search

#### Copy-Paste Prompts
```
Use @docs-architect to design API documentation site
```

### Phase 7: Maintenance

#### Skills to Invoke
- `api-documenter` - Doc maintenance

#### Actions
1. Set up auto-generation
2. Configure validation
3. Add review process
4. Schedule updates
5. Monitor feedback

#### Copy-Paste Prompts
```
Use @api-documenter to set up automated doc generation
```

## Quality Gates

- [ ] OpenAPI spec complete
- [ ] Developer guide written
- [ ] Code examples working
- [ ] Interactive docs functional
- [ ] Documentation deployed

## Related Workflow Bundles

- `documentation` - Documentation
- `api-development` - API development
- `development` - Development

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## api-security-testing
*API security testing workflow for REST and GraphQL APIs covering authentication, authorization, rate limiting, input validation, and security best practices.*

Risk: safe

# API Security Testing Workflow

## Overview

Specialized workflow for testing REST and GraphQL API security including authentication, authorization, rate limiting, input validation, and API-specific vulnerabilities.

## When to Use This Workflow

Use this workflow when:
- Testing REST API security
- Assessing GraphQL endpoints
- Validating API authentication
- Testing API rate limiting
- Bug bounty API testing

## Workflow Phases

### Phase 1: API Discovery

#### Skills to Invoke
- `api-fuzzing-bug-bounty` - API fuzzing
- `scanning-tools` - API scanning

#### Actions
1. Enumerate endpoints
2. Document API methods
3. Identify parameters
4. Map data flows
5. Review documentation

#### Copy-Paste Prompts
```
Use @api-fuzzing-bug-bounty to discover API endpoints
```

### Phase 2: Authentication Testing

#### Skills to Invoke
- `broken-authentication` - Auth testing
- `api-security-best-practices` - API auth

#### Actions
1. Test API key validation
2. Test JWT tokens
3. Test OAuth2 flows
4. Test token expiration
5. Test refresh tokens

#### Copy-Paste Prompts
```
Use @broken-authentication to test API authentication
```

### Phase 3: Authorization Testing

#### Skills to Invoke
- `idor-testing` - IDOR testing

#### Actions
1. Test object-level authorization
2. Test function-level authorization
3. Test role-based access
4. Test privilege escalation
5. Test multi-tenant isolation

#### Copy-Paste Prompts
```
Use @idor-testing to test API authorization
```

### Phase 4: Input Validation

#### Skills to Invoke
- `api-fuzzing-bug-bounty` - API fuzzing
- `sql-injection-testing` - Injection testing

#### Actions
1. Test parameter validation
2. Test SQL injection
3. Test NoSQL injection
4. Test command injection
5. Test XXE injection

#### Copy-Paste Prompts
```
Use @api-fuzzing-bug-bounty to fuzz API parameters
```

### Phase 5: Rate Limiting

#### Skills to Invoke
- `api-security-best-practices` - Rate limiting

#### Actions
1. Test rate limit headers
2. Test brute force protection
3. Test resource exhaustion
4. Test bypass techniques
5. Document limitations

#### Copy-Paste Prompts
```
Use @api-security-best-practices to test rate limiting
```

### Phase 6: GraphQL Testing

#### Skills to Invoke
- `api-fuzzing-bug-bounty` - GraphQL fuzzing

#### Actions
1. Test introspection
2. Test query depth
3. Test query complexity
4. Test batch queries
5. Test field suggestions

#### Copy-Paste Prompts
```
Use @api-fuzzing-bug-bounty to test GraphQL security
```

### Phase 7: Error Handling

#### Skills to Invoke
- `api-security-best-practices` - Error handling

#### Actions
1. Test error messages
2. Check information disclosure
3. Test stack traces
4. Verify logging
5. Document findings

#### Copy-Paste Prompts
```
Use @api-security-best-practices to audit API error handling
```

## API Security Checklist

- [ ] Authentication working
- [ ] Authorization enforced
- [ ] Input validated
- [ ] Rate limiting active
- [ ] Errors sanitized
- [ ] Logging enabled
- [ ] CORS configured
- [ ] HTTPS enforced

## Quality Gates

- [ ] All endpoints tested
- [ ] Vulnerabilities documented
- [ ] Remediation provided
- [ ] Report generated

## Related Workflow Bundles

- `security-audit` - Security auditing
- `web-security-testing` - Web security
- `api-development` - API development

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## bash-scripting
*Bash scripting workflow for creating production-ready shell scripts with defensive patterns, error handling, and testing.*

Risk: safe

# Bash Scripting Workflow

## Overview

Specialized workflow for creating robust, production-ready bash scripts with defensive programming patterns, comprehensive error handling, and automated testing.

## When to Use This Workflow

Use this workflow when:
- Creating automation scripts
- Writing system administration tools
- Building deployment scripts
- Developing backup solutions
- Creating CI/CD scripts

## Workflow Phases

### Phase 1: Script Design

#### Skills to Invoke
- `bash-pro` - Professional scripting
- `bash-defensive-patterns` - Defensive patterns

#### Actions
1. Define script purpose
2. Identify inputs/outputs
3. Plan error handling
4. Design logging strategy
5. Document requirements

#### Copy-Paste Prompts
```
Use @bash-pro to design production-ready bash script
```

### Phase 2: Script Structure

#### Skills to Invoke
- `bash-pro` - Script structure
- `bash-defensive-patterns` - Safety patterns

#### Actions
1. Add shebang and strict mode
2. Create usage function
3. Implement argument parsing
4. Set up logging
5. Add cleanup handlers

#### Copy-Paste Prompts
```
Use @bash-defensive-patterns to implement strict mode and error handling
```

### Phase 3: Core Implementation

#### Skills to Invoke
- `bash-linux` - Linux commands
- `linux-shell-scripting` - Shell scripting

#### Actions
1. Implement main functions
2. Add input validation
3. Create helper functions
4. Handle edge cases
5. Add progress indicators

#### Copy-Paste Prompts
```
Use @bash-linux to implement system commands
```

### Phase 4: Error Handling

#### Skills to Invoke
- `bash-defensive-patterns` - Error handling
- `error-handling-patterns` - Error patterns

#### Actions
1. Add trap handlers
2. Implement retry logic
3. Create error messages
4. Set up exit codes
5. Add rollback capability

#### Copy-Paste Prompts
```
Use @bash-defensive-patterns to add comprehensive error handling
```

### Phase 5: Logging

#### Skills to Invoke
- `bash-pro` - Logging patterns

#### Actions
1. Create logging function
2. Add log levels
3. Implement timestamps
4. Configure log rotation
5. Add debug mode

#### Copy-Paste Prompts
```
Use @bash-pro to implement structured logging
```

### Phase 6: Testing

#### Skills to Invoke
- `bats-testing-patterns` - Bats testing
- `shellcheck-configuration` - ShellCheck

#### Actions
1. Write Bats tests
2. Run ShellCheck
3. Test edge cases
4. Verify error handling
5. Test with different inputs

#### Copy-Paste Prompts
```
Use @bats-testing-patterns to write script tests
```

```
Use @shellcheck-configuration to lint bash script
```

### Phase 7: Documentation

#### Skills to Invoke
- `documentation-templates` - Documentation

#### Actions
1. Add script header
2. Document functions
3. Create usage examples
4. List dependencies
5. Add troubleshooting section

#### Copy-Paste Prompts
```
Use @documentation-templates to document bash script
```

## Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { log "ERROR: $*" >&2; exit 1; }

usage() { cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]
Options:
    -h, --help      Show help
    -v, --verbose   Verbose output
EOF
}

main() {
    log "Script started"
    # Implementation
    log "Script completed"
}

main "$@"
```

## Quality Gates

- [ ] ShellCheck passes
- [ ] Bats tests pass
- [ ] Error handling works
- [ ] Logging functional
- [ ] Documentation complete

## Related Workflow Bundles

- `os-scripting` - OS scripting
- `linux-troubleshooting` - Linux troubleshooting
- `cloud-devops` - DevOps automation

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## cloud-devops
*Cloud infrastructure and DevOps workflow covering AWS, Azure, GCP, Kubernetes, Terraform, CI/CD, monitoring, and cloud-native development.*

Risk: safe

# Cloud/DevOps Workflow Bundle

## Overview

Comprehensive cloud and DevOps workflow for infrastructure provisioning, container orchestration, CI/CD pipelines, monitoring, and cloud-native application development.

## When to Use This Workflow

Use this workflow when:
- Setting up cloud infrastructure
- Implementing CI/CD pipelines
- Deploying Kubernetes applications
- Configuring monitoring and observability
- Managing cloud costs
- Implementing DevOps practices

## Workflow Phases

### Phase 1: Cloud Infrastructure Setup

#### Skills to Invoke
- `cloud-architect` - Cloud architecture
- `aws-skills` - AWS development
- `azure-functions` - Azure development
- `gcp-cloud-run` - GCP development
- `terraform-skill` - Terraform IaC
- `terraform-specialist` - Advanced Terraform

#### Actions
1. Design cloud architecture
2. Set up accounts and billing
3. Configure networking
4. Provision resources
5. Set up IAM

#### Copy-Paste Prompts
```
Use @cloud-architect to design multi-cloud architecture
```

```
Use @terraform-skill to provision AWS infrastructure
```

### Phase 2: Container Orchestration

#### Skills to Invoke
- `kubernetes-architect` - Kubernetes architecture
- `docker-expert` - Docker containerization
- `helm-chart-scaffolding` - Helm charts
- `k8s-manifest-generator` - K8s manifests
- `k8s-security-policies` - K8s security

#### Actions
1. Design container architecture
2. Create Dockerfiles
3. Build container images
4. Write K8s manifests
5. Deploy to cluster
6. Configure networking

#### Copy-Paste Prompts
```
Use @kubernetes-architect to design K8s architecture
```

```
Use @docker-expert to containerize application
```

```
Use @helm-chart-scaffolding to create Helm chart
```

### Phase 3: CI/CD Implementation

#### Skills to Invoke
- `deployment-engineer` - Deployment engineering
- `cicd-automation-workflow-automate` - CI/CD automation
- `github-actions-templates` - GitHub Actions
- `gitlab-ci-patterns` - GitLab CI
- `deployment-pipeline-design` - Pipeline design

#### Actions
1. Design deployment pipeline
2. Configure build automation
3. Set up test automation
4. Configure deployment stages
5. Implement rollback strategies
6. Set up notifications

#### Copy-Paste Prompts
```
Use @cicd-automation-workflow-automate to set up CI/CD pipeline
```

```
Use @github-actions-templates to create GitHub Actions workflow
```

### Phase 4: Monitoring and Observability

#### Skills to Invoke
- `observability-engineer` - Observability engineering
- `grafana-dashboards` - Grafana dashboards
- `prometheus-configuration` - Prometheus setup
- `datadog-automation` - Datadog integration
- `sentry-automation` - Sentry error tracking

#### Actions
1. Design monitoring strategy
2. Set up metrics collection
3. Configure log aggregation
4. Implement distributed tracing
5. Create dashboards
6. Set up alerts

#### Copy-Paste Prompts
```
Use @observability-engineer to set up observability stack
```

```
Use @grafana-dashboards to create monitoring dashboards
```

### Phase 5: Cloud Security

#### Skills to Invoke
- `cloud-penetration-testing` - Cloud pentesting
- `aws-penetration-testing` - AWS security
- `k8s-security-policies` - K8s security
- `secrets-management` - Secrets management
- `mtls-configuration` - mTLS setup

#### Actions
1. Assess cloud security
2. Configure security groups
3. Set up secrets management
4. Implement network policies
5. Configure encryption
6. Set up audit logging

#### Copy-Paste Prompts
```
Use @cloud-penetration-testing to assess cloud security
```

```
Use @secrets-management to configure secrets
```

### Phase 6: Cost Optimization

#### Skills to Invoke
- `cost-optimization` - Cloud cost optimization
- `database-cloud-optimization-cost-optimize` - Database cost optimization

#### Actions
1. Analyze cloud spending
2. Identify optimization opportunities
3. Right-size resources
4. Implement auto-scaling
5. Use reserved instances
6. Set up cost alerts

#### Copy-Paste Prompts
```
Use @cost-optimization to reduce cloud costs
```

### Phase 7: Disaster Recovery

#### Skills to Invoke
- `incident-responder` - Incident response
- `incident-runbook-templates` - Runbook creation
- `postmortem-writing` - Postmortem documentation

#### Actions
1. Design DR strategy
2. Set up backups
3. Create runbooks
4. Test failover
5. Document procedures
6. Train team

#### Copy-Paste Prompts
```
Use @incident-runbook-templates to create runbooks
```

## Cloud Provider Workflows

### AWS
```
Skills: aws-skills, aws-serverless, aws-penetration-testing
Services: EC2, Lambda, S3, RDS, ECS, EKS
```

### Azure
```
Skills: azure-functions, azure-ai-projects-py, azure-monitor-opentelemetry-py
Services: Functions, App Service, AKS, Cosmos DB
```

### GCP
```
Skills: gcp-cloud-run
Services: Cloud Run, GKE, Cloud Functions, BigQuery
```

## Quality Gates

- [ ] Infrastructure provisioned
- [ ] CI/CD pipeline working
- [ ] Monitoring configured
- [ ] Security measures in place
- [ ] Cost optimization applied
- [ ] DR procedures documented

## Related Workflow Bundles

- `development` - Application development
- `security-audit` - Security testing
- `database` - Database operations
- `testing-qa` - Testing workflows

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## database
*Database development and operations workflow covering SQL, NoSQL, database design, migrations, optimization, and data engineering.*

Risk: safe

# Database Workflow Bundle

## Overview

Comprehensive database workflow for database design, development, optimization, migrations, and data engineering. Covers SQL, NoSQL, and modern data platforms.

## When to Use This Workflow

Use this workflow when:
- Designing database schemas
- Implementing database migrations
- Optimizing query performance
- Setting up data pipelines
- Managing database operations
- Implementing data quality

## Workflow Phases

### Phase 1: Database Design

#### Skills to Invoke
- `database-architect` - Database architecture
- `database-design` - Schema design
- `postgresql` - PostgreSQL design
- `nosql-expert` - NoSQL design

#### Actions
1. Gather requirements
2. Design schema
3. Define relationships
4. Plan indexing strategy
5. Design for scalability

#### Copy-Paste Prompts
```
Use @database-architect to design database schema
```

```
Use @postgresql to design PostgreSQL schema
```

### Phase 2: Database Implementation

#### Skills to Invoke
- `prisma-expert` - Prisma ORM
- `database-migrations-sql-migrations` - SQL migrations
- `neon-postgres` - Serverless Postgres

#### Actions
1. Set up database connection
2. Configure ORM
3. Create migrations
4. Implement models
5. Set up seed data

#### Copy-Paste Prompts
```
Use @prisma-expert to set up Prisma ORM
```

```
Use @database-migrations-sql-migrations to create migrations
```

### Phase 3: Query Optimization

#### Skills to Invoke
- `database-optimizer` - Database optimization
- `sql-optimization-patterns` - SQL optimization
- `postgres-best-practices` - PostgreSQL optimization

#### Actions
1. Analyze slow queries
2. Review execution plans
3. Optimize indexes
4. Refactor queries
5. Implement caching

#### Copy-Paste Prompts
```
Use @database-optimizer to optimize database performance
```

```
Use @sql-optimization-patterns to optimize SQL queries
```

### Phase 4: Data Migration

#### Skills to Invoke
- `database-migration` - Database migration
- `framework-migration-code-migrate` - Code migration

#### Actions
1. Plan migration strategy
2. Create migration scripts
3. Test migration
4. Execute migration
5. Verify data integrity

#### Copy-Paste Prompts
```
Use @database-migration to plan database migration
```

### Phase 5: Data Pipeline Development

#### Skills to Invoke
- `data-engineer` - Data engineering
- `data-engineering-data-pipeline` - Data pipelines
- `airflow-dag-patterns` - Airflow workflows
- `dbt-transformation-patterns` - dbt transformations

#### Actions
1. Design data pipeline
2. Set up data ingestion
3. Implement transformations
4. Configure scheduling
5. Set up monitoring

#### Copy-Paste Prompts
```
Use @data-engineer to design data pipeline
```

```
Use @airflow-dag-patterns to create Airflow DAGs
```

### Phase 6: Data Quality

#### Skills to Invoke
- `data-quality-frameworks` - Data quality
- `data-engineering-data-driven-feature` - Data-driven features

#### Actions
1. Define quality metrics
2. Implement validation
3. Set up monitoring
4. Create alerts
5. Document standards

#### Copy-Paste Prompts
```
Use @data-quality-frameworks to implement data quality checks
```

### Phase 7: Database Operations

#### Skills to Invoke
- `database-admin` - Database administration
- `backup-automation` - Backup automation

#### Actions
1. Set up backups
2. Configure replication
3. Monitor performance
4. Plan capacity
5. Implement security

#### Copy-Paste Prompts
```
Use @database-admin to manage database operations
```

## Database Technology Workflows

### PostgreSQL
```
Skills: postgresql, postgres-best-practices, neon-postgres, prisma-expert
```

### MongoDB
```
Skills: nosql-expert, azure-cosmos-db-py
```

### Redis
```
Skills: bullmq-specialist, upstash-qstash
```

### Data Warehousing
```
Skills: clickhouse-io, dbt-transformation-patterns
```

## Quality Gates

- [ ] Schema designed and reviewed
- [ ] Migrations tested
- [ ] Performance benchmarks met
- [ ] Backups configured
- [ ] Monitoring in place
- [ ] Documentation complete

## Related Workflow Bundles

- `development` - Application development
- `cloud-devops` - Infrastructure
- `ai-ml` - AI/ML data pipelines
- `testing-qa` - Data testing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## development
*Comprehensive web, mobile, and backend development workflow bundling frontend, backend, full-stack, and mobile development skills for end-to-end application delivery.*

Risk: safe

# Development Workflow Bundle

## Overview

Consolidated workflow for end-to-end software development covering web, mobile, and backend development. This bundle orchestrates skills for building production-ready applications from scaffolding to deployment.

## When to Use This Workflow

Use this workflow when:
- Building new web or mobile applications
- Adding features to existing applications
- Refactoring or modernizing legacy code
- Setting up new projects with best practices
- Full-stack feature development
- Cross-platform application development

## Workflow Phases

### Phase 1: Project Setup and Scaffolding

#### Skills to Invoke
- `app-builder` - Main application building orchestrator
- `senior-fullstack` - Full-stack development guidance
- `environment-setup-guide` - Development environment setup
- `concise-planning` - Task planning and breakdown

#### Actions
1. Determine project type (web, mobile, full-stack)
2. Select technology stack
3. Scaffold project structure
4. Configure development environment
5. Set up version control and CI/CD

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new React + Node.js full-stack application
```

```
Use @senior-fullstack to set up a Next.js 14 project with App Router
```

```
Use @environment-setup-guide to configure my development environment
```

### Phase 2: Frontend Development

#### Skills to Invoke
- `frontend-developer` - React/Next.js component development
- `frontend-design` - UI/UX design implementation
- `react-patterns` - Modern React patterns
- `typescript-pro` - TypeScript best practices
- `tailwind-patterns` - Tailwind CSS styling
- `nextjs-app-router-patterns` - Next.js 14+ patterns

#### Actions
1. Design component architecture
2. Implement UI components
3. Set up state management
4. Configure routing
5. Apply styling and theming
6. Implement responsive design

#### Copy-Paste Prompts
```
Use @frontend-developer to create a dashboard component with React and TypeScript
```

```
Use @react-patterns to implement proper state management with Zustand
```

```
Use @tailwind-patterns to style components with a consistent design system
```

### Phase 3: Backend Development

#### Skills to Invoke
- `backend-architect` - Backend architecture design
- `backend-dev-guidelines` - Backend development standards
- `nodejs-backend-patterns` - Node.js/Express patterns
- `fastapi-pro` - FastAPI development
- `api-design-principles` - REST/GraphQL API design
- `auth-implementation-patterns` - Authentication implementation

#### Actions
1. Design API architecture
2. Implement REST/GraphQL endpoints
3. Set up database connections
4. Implement authentication/authorization
5. Configure middleware
6. Set up error handling

#### Copy-Paste Prompts
```
Use @backend-architect to design a microservices architecture for my application
```

```
Use @nodejs-backend-patterns to create Express.js API endpoints
```

```
Use @auth-implementation-patterns to implement JWT authentication
```

### Phase 4: Database Development

#### Skills to Invoke
- `database-architect` - Database design
- `database-design` - Schema design principles
- `prisma-expert` - Prisma ORM
- `postgresql` - PostgreSQL optimization
- `neon-postgres` - Serverless Postgres

#### Actions
1. Design database schema
2. Create migrations
3. Set up ORM
4. Optimize queries
5. Configure connection pooling

#### Copy-Paste Prompts
```
Use @database-architect to design a normalized schema for an e-commerce platform
```

```
Use @prisma-expert to set up Prisma ORM with TypeScript
```

### Phase 5: Testing

#### Skills to Invoke
- `test-driven-development` - TDD workflow
- `javascript-testing-patterns` - Jest/Vitest testing
- `python-testing-patterns` - pytest testing
- `e2e-testing-patterns` - Playwright/Cypress E2E
- `playwright-skill` - Browser automation testing

#### Actions
1. Write unit tests
2. Create integration tests
3. Set up E2E tests
4. Configure CI test runners
5. Achieve coverage targets

#### Copy-Paste Prompts
```
Use @test-driven-development to implement features with TDD
```

```
Use @playwright-skill to create E2E tests for critical user flows
```

### Phase 6: Code Quality and Review

#### Skills to Invoke
- `code-reviewer` - AI-powered code review
- `clean-code` - Clean code principles
- `lint-and-validate` - Linting and validation
- `security-scanning-security-sast` - Static security analysis

#### Actions
1. Run linters and formatters
2. Perform code review
3. Fix code quality issues
4. Run security scans
5. Address vulnerabilities

#### Copy-Paste Prompts
```
Use @code-reviewer to review my pull request
```

```
Use @lint-and-validate to check code quality
```

### Phase 7: Build and Deployment

#### Skills to Invoke
- `deployment-engineer` - Deployment orchestration
- `docker-expert` - Containerization
- `vercel-deployment` - Vercel deployment
- `github-actions-templates` - CI/CD workflows
- `cicd-automation-workflow-automate` - CI/CD automation

#### Actions
1. Create Dockerfiles
2. Configure build pipelines
3. Set up deployment workflows
4. Configure environment variables
5. Deploy to production

#### Copy-Paste Prompts
```
Use @docker-expert to containerize my application
```

```
Use @vercel-deployment to deploy my Next.js app to production
```

```
Use @github-actions-templates to set up CI/CD pipeline
```

## Technology-Specific Workflows

### React/Next.js Development
```
Skills: frontend-developer, react-patterns, nextjs-app-router-patterns, typescript-pro, tailwind-patterns
```

### Python/FastAPI Development
```
Skills: fastapi-pro, python-pro, python-patterns, pydantic-models-py
```

### Node.js/Express Development
```
Skills: nodejs-backend-patterns, javascript-pro, typescript-pro, express (via nodejs-backend-patterns)
```

### Full-Stack Development
```
Skills: senior-fullstack, app-builder, frontend-developer, backend-architect, database-architect
```

### Mobile Development
```
Skills: mobile-developer, react-native-architecture, flutter-expert, ios-developer
```

## Quality Gates

Before moving to next phase, verify:
- [ ] All tests passing
- [ ] Code review completed
- [ ] Security scan passed
- [ ] Linting/formatting clean
- [ ] Documentation updated

## Related Workflow Bundles

- `wordpress` - WordPress-specific development
- `security-audit` - Security testing workflow
- `testing-qa` - Comprehensive testing workflow
- `documentation` - Documentation generation workflow

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## documentation
*Documentation generation workflow covering API docs, architecture docs, README files, code comments, and technical writing.*

Risk: safe

# Documentation Workflow Bundle

## Overview

Comprehensive documentation workflow for generating API documentation, architecture documentation, README files, code comments, and technical content from codebases.

## When to Use This Workflow

Use this workflow when:
- Creating project documentation
- Generating API documentation
- Writing architecture docs
- Documenting code
- Creating user guides
- Maintaining wikis

## Workflow Phases

### Phase 1: Documentation Planning

#### Skills to Invoke
- `docs-architect` - Documentation architecture
- `documentation-templates` - Documentation templates

#### Actions
1. Identify documentation needs
2. Choose documentation tools
3. Plan documentation structure
4. Define style guidelines
5. Set up documentation site

#### Copy-Paste Prompts
```
Use @docs-architect to plan documentation structure
```

```
Use @documentation-templates to set up documentation
```

### Phase 2: API Documentation

#### Skills to Invoke
- `api-documenter` - API documentation
- `api-documentation-generator` - Auto-generation
- `openapi-spec-generation` - OpenAPI specs

#### Actions
1. Extract API endpoints
2. Generate OpenAPI specs
3. Create API reference
4. Add usage examples
5. Set up auto-generation

#### Copy-Paste Prompts
```
Use @api-documenter to generate API documentation
```

```
Use @openapi-spec-generation to create OpenAPI specs
```

### Phase 3: Architecture Documentation

#### Skills to Invoke
- `c4-architecture-c4-architecture` - C4 architecture
- `c4-context` - Context diagrams
- `c4-container` - Container diagrams
- `c4-component` - Component diagrams
- `c4-code` - Code diagrams
- `mermaid-expert` - Mermaid diagrams

#### Actions
1. Create C4 diagrams
2. Document architecture
3. Generate sequence diagrams
4. Document data flows
5. Create deployment docs

#### Copy-Paste Prompts
```
Use @c4-architecture-c4-architecture to create C4 diagrams
```

```
Use @mermaid-expert to create architecture diagrams
```

### Phase 4: Code Documentation

#### Skills to Invoke
- `code-documentation-code-explain` - Code explanation
- `code-documentation-doc-generate` - Doc generation
- `documentation-generation-doc-generate` - Auto-generation

#### Actions
1. Extract code comments
2. Generate JSDoc/TSDoc
3. Create type documentation
4. Document functions
5. Add usage examples

#### Copy-Paste Prompts
```
Use @code-documentation-code-explain to explain code
```

```
Use @code-documentation-doc-generate to generate docs
```

### Phase 5: README and Getting Started

#### Skills to Invoke
- `readme` - README generation
- `environment-setup-guide` - Setup guides
- `tutorial-engineer` - Tutorial creation

#### Actions
1. Create README
2. Write getting started guide
3. Document installation
4. Add usage examples
5. Create troubleshooting guide

#### Copy-Paste Prompts
```
Use @readme to create project README
```

```
Use @tutorial-engineer to create tutorials
```

### Phase 6: Wiki and Knowledge Base

#### Skills to Invoke
- `wiki-architect` - Wiki architecture
- `wiki-page-writer` - Wiki pages
- `wiki-onboarding` - Onboarding docs
- `wiki-qa` - Wiki Q&A
- `wiki-researcher` - Wiki research
- `wiki-vitepress` - VitePress wiki

#### Actions
1. Design wiki structure
2. Create wiki pages
3. Write onboarding guides
4. Document processes
5. Set up wiki site

#### Copy-Paste Prompts
```
Use @wiki-architect to design wiki structure
```

```
Use @wiki-page-writer to create wiki pages
```

```
Use @wiki-onboarding to create onboarding docs
```

### Phase 7: Changelog and Release Notes

#### Skills to Invoke
- `changelog-automation` - Changelog generation
- `wiki-changelog` - Changelog from git

#### Actions
1. Extract commit history
2. Categorize changes
3. Generate changelog
4. Create release notes
5. Publish updates

#### Copy-Paste Prompts
```
Use @changelog-automation to generate changelog
```

```
Use @wiki-changelog to create release notes
```

### Phase 8: Documentation Maintenance

#### Skills to Invoke
- `doc-coauthoring` - Collaborative writing
- `reference-builder` - Reference docs

#### Actions
1. Review documentation
2. Update outdated content
3. Fix broken links
4. Add new features
5. Gather feedback

#### Copy-Paste Prompts
```
Use @doc-coauthoring to collaborate on docs
```

## Documentation Types

### Code-Level
- JSDoc/TSDoc comments
- Function documentation
- Type definitions
- Example code

### API Documentation
- Endpoint reference
- Request/response schemas
- Authentication guides
- SDK documentation

### Architecture Documentation
- System overview
- Component diagrams
- Data flow diagrams
- Deployment architecture

### User Documentation
- Getting started guides
- User manuals
- Tutorials
- FAQs

### Process Documentation
- Runbooks
- Onboarding guides
- SOPs
- Decision records

## Quality Gates

- [ ] All APIs documented
- [ ] Architecture diagrams current
- [ ] README up to date
- [ ] Code comments helpful
- [ ] Examples working
- [ ] Links valid

## Related Workflow Bundles

- `development` - Development workflow
- `testing-qa` - Documentation testing
- `ai-ml` - AI documentation

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## e2e-testing
*End-to-end testing workflow with Playwright for browser automation, visual regression, cross-browser testing, and CI/CD integration.*

Risk: safe

# E2E Testing Workflow

## Overview

Specialized workflow for end-to-end testing using Playwright including browser automation, visual regression testing, cross-browser testing, and CI/CD integration.

## When to Use This Workflow

Use this workflow when:
- Setting up E2E testing
- Automating browser tests
- Implementing visual regression
- Testing across browsers
- Integrating tests with CI/CD

## Workflow Phases

### Phase 1: Test Setup

#### Skills to Invoke
- `playwright-skill` - Playwright setup
- `e2e-testing-patterns` - E2E patterns

#### Actions
1. Install Playwright
2. Configure test framework
3. Set up test directory
4. Configure browsers
5. Create base test setup

#### Copy-Paste Prompts
```
Use @playwright-skill to set up Playwright testing
```

### Phase 2: Test Design

#### Skills to Invoke
- `e2e-testing-patterns` - Test patterns
- `test-automator` - Test automation

#### Actions
1. Identify critical flows
2. Design test scenarios
3. Plan test data
4. Create page objects
5. Set up fixtures

#### Copy-Paste Prompts
```
Use @e2e-testing-patterns to design E2E test strategy
```

### Phase 3: Test Implementation

#### Skills to Invoke
- `playwright-skill` - Playwright tests
- `webapp-testing` - Web app testing

#### Actions
1. Write test scripts
2. Add assertions
3. Implement waits
4. Handle dynamic content
5. Add error handling

#### Copy-Paste Prompts
```
Use @playwright-skill to write E2E test scripts
```

### Phase 4: Browser Automation

#### Skills to Invoke
- `browser-automation` - Browser automation
- `playwright-skill` - Playwright features

#### Actions
1. Configure headless mode
2. Set up screenshots
3. Implement video recording
4. Add trace collection
5. Configure mobile emulation

#### Copy-Paste Prompts
```
Use @browser-automation to automate browser interactions
```

### Phase 5: Visual Regression

#### Skills to Invoke
- `playwright-skill` - Visual testing
- `ui-visual-validator` - Visual validation

#### Actions
1. Set up visual testing
2. Create baseline images
3. Add visual assertions
4. Configure thresholds
5. Review differences

#### Copy-Paste Prompts
```
Use @playwright-skill to implement visual regression testing
```

### Phase 6: Cross-Browser Testing

#### Skills to Invoke
- `playwright-skill` - Multi-browser
- `webapp-testing` - Browser testing

#### Actions
1. Configure Chromium
2. Add Firefox tests
3. Add WebKit tests
4. Test mobile browsers
5. Compare results

#### Copy-Paste Prompts
```
Use @playwright-skill to run cross-browser tests
```

### Phase 7: CI/CD Integration

#### Skills to Invoke
- `github-actions-templates` - GitHub Actions
- `cicd-automation-workflow-automate` - CI/CD

#### Actions
1. Create CI workflow
2. Configure parallel execution
3. Set up artifacts
4. Add reporting
5. Configure notifications

#### Copy-Paste Prompts
```
Use @github-actions-templates to integrate E2E tests with CI
```

## Quality Gates

- [ ] Tests passing
- [ ] Coverage adequate
- [ ] Visual tests stable
- [ ] Cross-browser verified
- [ ] CI integration working

## Related Workflow Bundles

- `testing-qa` - Testing workflow
- `development` - Development
- `web-performance-optimization` - Performance

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## kubernetes-deployment
*Kubernetes deployment workflow for container orchestration, Helm charts, service mesh, and production-ready K8s configurations.*

Risk: safe

# Kubernetes Deployment Workflow

## Overview

Specialized workflow for deploying applications to Kubernetes including container orchestration, Helm charts, service mesh configuration, and production-ready K8s patterns.

## When to Use This Workflow

Use this workflow when:
- Deploying to Kubernetes
- Creating Helm charts
- Configuring service mesh
- Setting up K8s networking
- Implementing K8s security

## Workflow Phases

### Phase 1: Container Preparation

#### Skills to Invoke
- `docker-expert` - Docker containerization
- `k8s-manifest-generator` - K8s manifests

#### Actions
1. Create Dockerfile
2. Build container image
3. Optimize image size
4. Push to registry
5. Test container

#### Copy-Paste Prompts
```
Use @docker-expert to containerize application for K8s
```

### Phase 2: K8s Manifests

#### Skills to Invoke
- `k8s-manifest-generator` - Manifest generation
- `kubernetes-architect` - K8s architecture

#### Actions
1. Create Deployment
2. Configure Service
3. Set up ConfigMap
4. Create Secrets
5. Add Ingress

#### Copy-Paste Prompts
```
Use @k8s-manifest-generator to create K8s manifests
```

### Phase 3: Helm Chart

#### Skills to Invoke
- `helm-chart-scaffolding` - Helm charts

#### Actions
1. Create chart structure
2. Define values.yaml
3. Add templates
4. Configure dependencies
5. Test chart

#### Copy-Paste Prompts
```
Use @helm-chart-scaffolding to create Helm chart
```

### Phase 4: Service Mesh

#### Skills to Invoke
- `istio-traffic-management` - Istio
- `linkerd-patterns` - Linkerd
- `service-mesh-expert` - Service mesh

#### Actions
1. Choose service mesh
2. Install mesh
3. Configure traffic management
4. Set up mTLS
5. Add observability

#### Copy-Paste Prompts
```
Use @istio-traffic-management to configure Istio
```

### Phase 5: Security

#### Skills to Invoke
- `k8s-security-policies` - K8s security
- `mtls-configuration` - mTLS

#### Actions
1. Configure RBAC
2. Set up NetworkPolicy
3. Enable PodSecurity
4. Configure secrets
5. Implement mTLS

#### Copy-Paste Prompts
```
Use @k8s-security-policies to secure Kubernetes cluster
```

### Phase 6: Observability

#### Skills to Invoke
- `grafana-dashboards` - Grafana
- `prometheus-configuration` - Prometheus

#### Actions
1. Install monitoring stack
2. Configure Prometheus
3. Create Grafana dashboards
4. Set up alerts
5. Add distributed tracing

#### Copy-Paste Prompts
```
Use @prometheus-configuration to set up K8s monitoring
```

### Phase 7: Deployment

#### Skills to Invoke
- `deployment-engineer` - Deployment
- `gitops-workflow` - GitOps

#### Actions
1. Configure CI/CD
2. Set up GitOps
3. Deploy to cluster
4. Verify deployment
5. Monitor rollout

#### Copy-Paste Prompts
```
Use @gitops-workflow to implement GitOps deployment
```

## Quality Gates

- [ ] Containers working
- [ ] Manifests valid
- [ ] Helm chart installs
- [ ] Security configured
- [ ] Monitoring active
- [ ] Deployment successful

## Related Workflow Bundles

- `cloud-devops` - Cloud/DevOps
- `terraform-infrastructure` - Infrastructure
- `docker-containerization` - Containers

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## linux-troubleshooting
*Linux system troubleshooting workflow for diagnosing and resolving system issues, performance problems, and service failures.*

Risk: safe

# Linux Troubleshooting Workflow

## Overview

Specialized workflow for diagnosing and resolving Linux system issues including performance problems, service failures, network issues, and resource constraints.

## When to Use This Workflow

Use this workflow when:
- Diagnosing system performance issues
- Troubleshooting service failures
- Investigating network problems
- Resolving disk space issues
- Debugging application errors

## Workflow Phases

### Phase 1: Initial Assessment

#### Skills to Invoke
- `bash-linux` - Linux commands
- `devops-troubleshooter` - Troubleshooting

#### Actions
1. Check system uptime
2. Review recent changes
3. Identify symptoms
4. Gather error messages
5. Document findings

#### Commands
```bash
uptime
hostnamectl
cat /etc/os-release
dmesg | tail -50
```

#### Copy-Paste Prompts
```
Use @bash-linux to gather system information
```

### Phase 2: Resource Analysis

#### Skills to Invoke
- `bash-linux` - Resource commands
- `performance-engineer` - Performance analysis

#### Actions
1. Check CPU usage
2. Analyze memory
3. Review disk space
4. Monitor I/O
5. Check network

#### Commands
```bash
top -bn1 | head -20
free -h
df -h
iostat -x 1 5
```

#### Copy-Paste Prompts
```
Use @performance-engineer to analyze system resources
```

### Phase 3: Process Investigation

#### Skills to Invoke
- `bash-linux` - Process commands
- `server-management` - Process management

#### Actions
1. List running processes
2. Identify resource hogs
3. Check process status
4. Review process trees
5. Analyze strace output

#### Commands
```bash
ps aux --sort=-%cpu | head -10
pstree -p
lsof -p PID
strace -p PID
```

#### Copy-Paste Prompts
```
Use @server-management to investigate processes
```

### Phase 4: Log Analysis

#### Skills to Invoke
- `bash-linux` - Log commands
- `error-detective` - Error detection

#### Actions
1. Check system logs
2. Review application logs
3. Search for errors
4. Analyze log patterns
5. Correlate events

#### Commands
```bash
journalctl -xe
tail -f /var/log/syslog
grep -i error /var/log/*
```

#### Copy-Paste Prompts
```
Use @error-detective to analyze log files
```

### Phase 5: Network Diagnostics

#### Skills to Invoke
- `bash-linux` - Network commands
- `network-engineer` - Network troubleshooting

#### Actions
1. Check network interfaces
2. Test connectivity
3. Analyze connections
4. Review firewall rules
5. Check DNS resolution

#### Commands
```bash
ip addr show
ss -tulpn
curl -v http://target
dig domain
```

#### Copy-Paste Prompts
```
Use @network-engineer to diagnose network issues
```

### Phase 6: Service Troubleshooting

#### Skills to Invoke
- `server-management` - Service management
- `systematic-debugging` - Debugging

#### Actions
1. Check service status
2. Review service logs
3. Test service restart
4. Verify dependencies
5. Check configuration

#### Commands
```bash
systemctl status service
journalctl -u service -f
systemctl restart service
```

#### Copy-Paste Prompts
```
Use @systematic-debugging to troubleshoot service issues
```

### Phase 7: Resolution

#### Skills to Invoke
- `incident-responder` - Incident response
- `bash-pro` - Fix implementation

#### Actions
1. Implement fix
2. Verify resolution
3. Monitor stability
4. Document solution
5. Create prevention plan

#### Copy-Paste Prompts
```
Use @incident-responder to implement resolution
```

## Troubleshooting Checklist

- [ ] System information gathered
- [ ] Resources analyzed
- [ ] Logs reviewed
- [ ] Network tested
- [ ] Services verified
- [ ] Issue resolved
- [ ] Documentation created

## Quality Gates

- [ ] Root cause identified
- [ ] Fix verified
- [ ] Monitoring in place
- [ ] Documentation complete

## Related Workflow Bundles

- `os-scripting` - OS scripting
- `bash-scripting` - Bash scripting
- `cloud-devops` - DevOps

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## office-productivity
*Office productivity workflow covering document creation, spreadsheet automation, presentation generation, and integration with LibreOffice and Microsoft Office formats.*

Risk: safe

# Office Productivity Workflow Bundle

## Overview

Comprehensive office productivity workflow for document creation, spreadsheet automation, presentation generation, and format conversion using LibreOffice and Microsoft Office tools.

## When to Use This Workflow

Use this workflow when:
- Creating office documents programmatically
- Automating document workflows
- Converting between document formats
- Generating reports
- Creating presentations from data
- Processing spreadsheets

## Workflow Phases

### Phase 1: Document Creation

#### Skills to Invoke
- `libreoffice-writer` - LibreOffice Writer
- `docx-official` - Microsoft Word
- `pdf-official` - PDF handling

#### Actions
1. Design document template
2. Create document structure
3. Add content programmatically
4. Apply formatting
5. Export to required formats

#### Copy-Paste Prompts
```
Use @libreoffice-writer to create ODT documents
```

```
Use @docx-official to create Word documents
```

### Phase 2: Spreadsheet Automation

#### Skills to Invoke
- `libreoffice-calc` - LibreOffice Calc
- `xlsx-official` - Excel spreadsheets
- `googlesheets-automation` - Google Sheets

#### Actions
1. Design spreadsheet structure
2. Create formulas
3. Import data
4. Generate charts
5. Export reports

#### Copy-Paste Prompts
```
Use @libreoffice-calc to create ODS spreadsheets
```

```
Use @xlsx-official to create Excel reports
```

### Phase 3: Presentation Generation

#### Skills to Invoke
- `libreoffice-impress` - LibreOffice Impress
- `pptx-official` - PowerPoint
- `frontend-slides` - HTML slides
- `nanobanana-ppt-skills` - AI PPT generation

#### Actions
1. Design slide template
2. Generate slides from data
3. Add charts and graphics
4. Apply animations
5. Export presentations

#### Copy-Paste Prompts
```
Use @libreoffice-impress to create ODP presentations
```

```
Use @pptx-official to create PowerPoint presentations
```

```
Use @frontend-slides to create HTML presentations
```

### Phase 4: Format Conversion

#### Skills to Invoke
- `libreoffice-writer` - Document conversion
- `libreoffice-calc` - Spreadsheet conversion
- `pdf-official` - PDF conversion

#### Actions
1. Identify source format
2. Choose target format
3. Perform conversion
4. Verify quality
5. Batch process files

#### Copy-Paste Prompts
```
Use @libreoffice-writer to convert documents
```

### Phase 5: Document Automation

#### Skills to Invoke
- `libreoffice-writer` - Mail merge
- `workflow-automation` - Workflow automation
- `file-organizer` - File organization

#### Actions
1. Design automation workflow
2. Create templates
3. Set up data sources
4. Generate documents
5. Distribute outputs

#### Copy-Paste Prompts
```
Use @libreoffice-writer to perform mail merge
```

```
Use @workflow-automation to automate document workflows
```

### Phase 6: Graphics and Diagrams

#### Skills to Invoke
- `libreoffice-draw` - Vector graphics
- `canvas-design` - Canvas design
- `mermaid-expert` - Diagram generation

#### Actions
1. Design graphics
2. Create diagrams
3. Generate charts
4. Export images
5. Integrate with documents

#### Copy-Paste Prompts
```
Use @libreoffice-draw to create vector graphics
```

```
Use @mermaid-expert to create diagrams
```

### Phase 7: Database Integration

#### Skills to Invoke
- `libreoffice-base` - LibreOffice Base
- `database-architect` - Database design

#### Actions
1. Connect to data sources
2. Create forms
3. Design reports
4. Automate queries
5. Generate output

#### Copy-Paste Prompts
```
Use @libreoffice-base to create database reports
```

## Office Application Workflows

### LibreOffice
```
Skills: libreoffice-writer, libreoffice-calc, libreoffice-impress, libreoffice-draw, libreoffice-base
Formats: ODT, ODS, ODP, ODG, ODB
```

### Microsoft Office
```
Skills: docx-official, xlsx-official, pptx-official
Formats: DOCX, XLSX, PPTX
```

### Google Workspace
```
Skills: googlesheets-automation, google-drive-automation, gmail-automation
Formats: Google Docs, Sheets, Slides
```

## Quality Gates

- [ ] Documents formatted correctly
- [ ] Formulas working
- [ ] Presentations complete
- [ ] Conversions successful
- [ ] Automation tested
- [ ] Files organized

## Related Workflow Bundles

- `development` - Application development
- `documentation` - Documentation generation
- `database` - Data integration

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## os-scripting
*Operating system and shell scripting troubleshooting workflow for Linux, macOS, and Windows. Covers bash scripting, system administration, debugging, and automation.*

Risk: safe

# OS/Shell Scripting Troubleshooting Workflow Bundle

## Overview

Comprehensive workflow for operating system troubleshooting, shell scripting, and system administration across Linux, macOS, and Windows. This bundle orchestrates skills for debugging system issues, creating robust scripts, and automating administrative tasks.

## When to Use This Workflow

Use this workflow when:
- Debugging shell script errors
- Creating production-ready bash scripts
- Troubleshooting system issues
- Automating system administration tasks
- Managing processes and services
- Configuring system resources

## Workflow Phases

### Phase 1: Environment Assessment

#### Skills to Invoke
- `bash-linux` - Linux bash patterns
- `bash-pro` - Professional bash scripting
- `bash-defensive-patterns` - Defensive scripting

#### Actions
1. Identify operating system and version
2. Check available tools and commands
3. Verify permissions and access
4. Assess system resources
5. Review logs and error messages

#### Diagnostic Commands
```bash
# System information
uname -a
cat /etc/os-release
hostnamectl

# Resource usage
top
htop
df -h
free -m

# Process information
ps aux
pgrep -f pattern
lsof -i :port

# Network status
netstat -tulpn
ss -tulpn
ip addr show
```

#### Copy-Paste Prompts
```
Use @bash-linux to diagnose system performance issues
```

### Phase 2: Script Analysis

#### Skills to Invoke
- `bash-defensive-patterns` - Defensive scripting
- `shellcheck-configuration` - ShellCheck linting
- `bats-testing-patterns` - Bats testing

#### Actions
1. Run ShellCheck for linting
2. Analyze script structure
3. Identify potential issues
4. Check error handling
5. Verify variable usage

#### ShellCheck Usage
```bash
# Install ShellCheck
sudo apt install shellcheck  # Debian/Ubuntu
brew install shellcheck      # macOS

# Run ShellCheck
shellcheck script.sh
shellcheck -f gcc script.sh

# Fix common issues
# - Use quotes around variables
# - Check exit codes
# - Handle errors properly
```

#### Copy-Paste Prompts
```
Use @shellcheck-configuration to lint and fix shell scripts
```

### Phase 3: Debugging

#### Skills to Invoke
- `systematic-debugging` - Systematic debugging
- `debugger` - Debugging specialist
- `error-detective` - Error pattern detection

#### Actions
1. Enable debug mode
2. Add logging statements
3. Trace execution flow
4. Isolate failing sections
5. Test components individually

#### Debug Techniques
```bash
# Enable debug mode
set -x  # Print commands
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Pipeline failure detection

# Add logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> /var/log/script.log
}

# Trap errors
trap 'echo "Error on line $LINENO"' ERR

# Test sections
bash -n script.sh  # Syntax check
bash -x script.sh  # Trace execution
```

#### Copy-Paste Prompts
```
Use @systematic-debugging to trace and fix shell script errors
```

### Phase 4: Script Development

#### Skills to Invoke
- `bash-pro` - Professional scripting
- `bash-defensive-patterns` - Defensive patterns
- `linux-shell-scripting` - Shell scripting

#### Actions
1. Design script structure
2. Implement functions
3. Add error handling
4. Include input validation
5. Add help documentation

#### Script Template
```bash
#!/usr/bin/env bash
set -euo pipefail

# Constants
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Logging
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; exit 1; }

# Usage
usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -d, --debug     Enable debug mode

Examples:
    $SCRIPT_NAME --verbose
    $SCRIPT_NAME -d
EOF
}

# Main function
main() {
    local verbose=false
    local debug=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -d|--debug)
                debug=true
                set -x
                shift
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    info "Script started"
    # Your code here
    info "Script completed"
}

main "$@"
```

#### Copy-Paste Prompts
```
Use @bash-pro to create a production-ready backup script
```

```
Use @linux-shell-scripting to automate system maintenance tasks
```

### Phase 5: Testing

#### Skills to Invoke
- `bats-testing-patterns` - Bats testing framework
- `test-automator` - Test automation

#### Actions
1. Write Bats tests
2. Test edge cases
3. Test error conditions
4. Verify expected outputs
5. Run test suite

#### Bats Test Example
```bash
#!/usr/bin/env bats

@test "script returns success" {
    run ./script.sh
    [ "$status" -eq 0 ]
}

@test "script handles missing arguments" {
    run ./script.sh
    [ "$status" -ne 0 ]
    [ "$output" == *"Usage:"* ]
}

@test "script creates expected output" {
    run ./script.sh --output test.txt
    [ -f "test.txt" ]
}
```

#### Copy-Paste Prompts
```
Use @bats-testing-patterns to write tests for shell scripts
```

### Phase 6: System Troubleshooting

#### Skills to Invoke
- `devops-troubleshooter` - DevOps troubleshooting
- `incident-responder` - Incident response
- `server-management` - Server management

#### Actions
1. Identify symptoms
2. Check system logs
3. Analyze resource usage
4. Test connectivity
5. Verify configurations
6. Implement fixes

#### Troubleshooting Commands
```bash
# Check logs
journalctl -xe
tail -f /var/log/syslog
dmesg | tail

# Network troubleshooting
ping host
traceroute host
curl -v http://host
dig domain
nslookup domain

# Process troubleshooting
strace -p PID
lsof -p PID
iotop

# Disk troubleshooting
du -sh /*
find / -type f -size +100M
lsof | grep deleted
```

#### Copy-Paste Prompts
```
Use @devops-troubleshooter to diagnose server connectivity issues
```

```
Use @incident-responder to investigate system outage
```

### Phase 7: Automation

#### Skills to Invoke
- `workflow-automation` - Workflow automation
- `cicd-automation-workflow-automate` - CI/CD automation
- `linux-shell-scripting` - Shell scripting

#### Actions
1. Identify automation opportunities
2. Design automation workflows
3. Implement scripts
4. Schedule with cron/systemd
5. Monitor automation health

#### Cron Examples
```bash
# Edit crontab
crontab -e

# Backup every day at 2 AM
0 2 * * * /path/to/backup.sh

# Clean logs weekly
0 3 * * 0 /path/to/cleanup.sh

# Monitor disk space hourly
0 * * * * /path/to/monitor.sh
```

#### Systemd Timer Example
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

#### Copy-Paste Prompts
```
Use @workflow-automation to create automated system maintenance workflow
```

## Common Troubleshooting Scenarios

### High CPU Usage
```bash
top -bn1 | head -20
ps aux --sort=-%cpu | head -10
pidstat 1 5
```

### Memory Issues
```bash
free -h
vmstat 1 10
cat /proc/meminfo
```

### Disk Space
```bash
df -h
du -sh /* 2>/dev/null | sort -h
find / -type f -size +500M 2>/dev/null
```

### Network Issues
```bash
ip addr show
ip route show
ss -tulpn
curl -v http://target
```

### Service Failures
```bash
systemctl status service-name
journalctl -u service-name -f
systemctl restart service-name
```

## Quality Gates

Before completing workflow, verify:
- [ ] All scripts pass ShellCheck
- [ ] Tests pass with Bats
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Documentation complete
- [ ] Automation scheduled

## Related Workflow Bundles

- `development` - Software development
- `cloud-devops` - Cloud and DevOps
- `security-audit` - Security testing
- `database` - Database operations

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## postgresql-optimization
*PostgreSQL database optimization workflow for query tuning, indexing strategies, performance analysis, and production database management.*

Risk: safe

# PostgreSQL Optimization Workflow

## Overview

Specialized workflow for PostgreSQL database optimization including query tuning, indexing strategies, performance analysis, vacuum management, and production database administration.

## When to Use This Workflow

Use this workflow when:
- Optimizing slow PostgreSQL queries
- Designing indexing strategies
- Analyzing database performance
- Tuning PostgreSQL configuration
- Managing production databases

## Workflow Phases

### Phase 1: Performance Assessment

#### Skills to Invoke
- `database-optimizer` - Database optimization
- `postgres-best-practices` - PostgreSQL best practices

#### Actions
1. Check database version
2. Review configuration
3. Analyze slow queries
4. Check resource usage
5. Identify bottlenecks

#### Copy-Paste Prompts
```
Use @database-optimizer to assess PostgreSQL performance
```

### Phase 2: Query Analysis

#### Skills to Invoke
- `sql-optimization-patterns` - SQL optimization
- `postgres-best-practices` - PostgreSQL patterns

#### Actions
1. Run EXPLAIN ANALYZE
2. Identify scan types
3. Check join strategies
4. Analyze execution time
5. Find optimization opportunities

#### Copy-Paste Prompts
```
Use @sql-optimization-patterns to analyze and optimize queries
```

### Phase 3: Indexing Strategy

#### Skills to Invoke
- `database-design` - Index design
- `postgresql` - PostgreSQL indexing

#### Actions
1. Identify missing indexes
2. Create B-tree indexes
3. Add composite indexes
4. Consider partial indexes
5. Review index usage

#### Copy-Paste Prompts
```
Use @database-design to design PostgreSQL indexing strategy
```

### Phase 4: Query Optimization

#### Skills to Invoke
- `sql-optimization-patterns` - Query tuning
- `sql-pro` - SQL expertise

#### Actions
1. Rewrite inefficient queries
2. Optimize joins
3. Add CTEs where helpful
4. Implement pagination
5. Test improvements

#### Copy-Paste Prompts
```
Use @sql-optimization-patterns to optimize SQL queries
```

### Phase 5: Configuration Tuning

#### Skills to Invoke
- `postgres-best-practices` - Configuration
- `database-admin` - Database administration

#### Actions
1. Tune shared_buffers
2. Configure work_mem
3. Set effective_cache_size
4. Adjust checkpoint settings
5. Configure autovacuum

#### Copy-Paste Prompts
```
Use @postgres-best-practices to tune PostgreSQL configuration
```

### Phase 6: Maintenance

#### Skills to Invoke
- `database-admin` - Database maintenance
- `postgresql` - PostgreSQL maintenance

#### Actions
1. Schedule VACUUM
2. Run ANALYZE
3. Check table bloat
4. Monitor autovacuum
5. Review statistics

#### Copy-Paste Prompts
```
Use @database-admin to schedule PostgreSQL maintenance
```

### Phase 7: Monitoring

#### Skills to Invoke
- `grafana-dashboards` - Monitoring dashboards
- `prometheus-configuration` - Metrics collection

#### Actions
1. Set up monitoring
2. Create dashboards
3. Configure alerts
4. Track key metrics
5. Review trends

#### Copy-Paste Prompts
```
Use @grafana-dashboards to create PostgreSQL monitoring
```

## Optimization Checklist

- [ ] Slow queries identified
- [ ] Indexes optimized
- [ ] Configuration tuned
- [ ] Maintenance scheduled
- [ ] Monitoring active
- [ ] Performance improved

## Quality Gates

- [ ] Query performance improved
- [ ] Indexes effective
- [ ] Configuration optimized
- [ ] Maintenance automated
- [ ] Monitoring in place

## Related Workflow Bundles

- `database` - Database operations
- `cloud-devops` - Infrastructure
- `performance-optimization` - Performance

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## python-fastapi-development
*Python FastAPI backend development with async patterns, SQLAlchemy, Pydantic, authentication, and production API patterns.*

Risk: safe

# Python/FastAPI Development Workflow

## Overview

Specialized workflow for building production-ready Python backends with FastAPI, featuring async patterns, SQLAlchemy ORM, Pydantic validation, and comprehensive API patterns.

## When to Use This Workflow

Use this workflow when:
- Building new REST APIs with FastAPI
- Creating async Python backends
- Implementing database integration with SQLAlchemy
- Setting up API authentication
- Developing microservices

## Workflow Phases

### Phase 1: Project Setup

#### Skills to Invoke
- `app-builder` - Application scaffolding
- `python-development-python-scaffold` - Python scaffolding
- `fastapi-templates` - FastAPI templates
- `uv-package-manager` - Package management

#### Actions
1. Set up Python environment (uv/poetry)
2. Create project structure
3. Configure FastAPI app
4. Set up logging
5. Configure environment variables

#### Copy-Paste Prompts
```
Use @fastapi-templates to scaffold a new FastAPI project
```

```
Use @python-development-python-scaffold to set up Python project structure
```

### Phase 2: Database Setup

#### Skills to Invoke
- `prisma-expert` - Prisma ORM (alternative)
- `database-design` - Schema design
- `postgresql` - PostgreSQL setup
- `pydantic-models-py` - Pydantic models

#### Actions
1. Design database schema
2. Set up SQLAlchemy models
3. Create database connection
4. Configure migrations (Alembic)
5. Set up session management

#### Copy-Paste Prompts
```
Use @database-design to design PostgreSQL schema
```

```
Use @pydantic-models-py to create Pydantic models for API
```

### Phase 3: API Routes

#### Skills to Invoke
- `fastapi-router-py` - FastAPI routers
- `api-design-principles` - API design
- `api-patterns` - API patterns

#### Actions
1. Design API endpoints
2. Create API routers
3. Implement CRUD operations
4. Add request validation
5. Configure response models

#### Copy-Paste Prompts
```
Use @fastapi-router-py to create API endpoints with CRUD operations
```

```
Use @api-design-principles to design RESTful API
```

### Phase 4: Authentication

#### Skills to Invoke
- `auth-implementation-patterns` - Authentication
- `api-security-best-practices` - API security

#### Actions
1. Choose auth strategy (JWT, OAuth2)
2. Implement user registration
3. Set up login endpoints
4. Create auth middleware
5. Add password hashing

#### Copy-Paste Prompts
```
Use @auth-implementation-patterns to implement JWT authentication
```

### Phase 5: Error Handling

#### Skills to Invoke
- `fastapi-pro` - FastAPI patterns
- `error-handling-patterns` - Error handling

#### Actions
1. Create custom exceptions
2. Set up exception handlers
3. Implement error responses
4. Add request logging
5. Configure error tracking

#### Copy-Paste Prompts
```
Use @fastapi-pro to implement comprehensive error handling
```

### Phase 6: Testing

#### Skills to Invoke
- `python-testing-patterns` - pytest testing
- `api-testing-observability-api-mock` - API testing

#### Actions
1. Set up pytest
2. Create test fixtures
3. Write unit tests
4. Implement integration tests
5. Configure test database

#### Copy-Paste Prompts
```
Use @python-testing-patterns to write pytest tests for FastAPI
```

### Phase 7: Documentation

#### Skills to Invoke
- `api-documenter` - API documentation
- `openapi-spec-generation` - OpenAPI specs

#### Actions
1. Configure OpenAPI schema
2. Add endpoint documentation
3. Create usage examples
4. Set up API versioning
5. Generate API docs

#### Copy-Paste Prompts
```
Use @api-documenter to generate comprehensive API documentation
```

### Phase 8: Deployment

#### Skills to Invoke
- `deployment-engineer` - Deployment
- `docker-expert` - Containerization

#### Actions
1. Create Dockerfile
2. Set up docker-compose
3. Configure production settings
4. Set up reverse proxy
5. Deploy to cloud

#### Copy-Paste Prompts
```
Use @docker-expert to containerize FastAPI application
```

## Technology Stack

| Category | Technology |
|----------|------------|
| Framework | FastAPI |
| Language | Python 3.11+ |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | JWT, OAuth2 |
| Testing | pytest |

## Quality Gates

- [ ] All tests passing (>80% coverage)
- [ ] Type checking passes (mypy)
- [ ] Linting clean (ruff, black)
- [ ] API documentation complete
- [ ] Security scan passed
- [ ] Performance benchmarks met

## Related Workflow Bundles

- `development` - General development
- `database` - Database operations
- `security-audit` - Security testing
- `api-development` - API patterns

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## rag-implementation
*RAG (Retrieval-Augmented Generation) implementation workflow covering embedding selection, vector database setup, chunking strategies, and retrieval optimization.*

Risk: safe

# RAG Implementation Workflow

## Overview

Specialized workflow for implementing RAG (Retrieval-Augmented Generation) systems including embedding model selection, vector database setup, chunking strategies, retrieval optimization, and evaluation.

## When to Use This Workflow

Use this workflow when:
- Building RAG-powered applications
- Implementing semantic search
- Creating knowledge-grounded AI
- Setting up document Q&A systems
- Optimizing retrieval quality

## Workflow Phases

### Phase 1: Requirements Analysis

#### Skills to Invoke
- `ai-product` - AI product design
- `rag-engineer` - RAG engineering

#### Actions
1. Define use case
2. Identify data sources
3. Set accuracy requirements
4. Determine latency targets
5. Plan evaluation metrics

#### Copy-Paste Prompts
```
Use @ai-product to define RAG application requirements
```

### Phase 2: Embedding Selection

#### Skills to Invoke
- `embedding-strategies` - Embedding selection
- `rag-engineer` - RAG patterns

#### Actions
1. Evaluate embedding models
2. Test domain relevance
3. Measure embedding quality
4. Consider cost/latency
5. Select model

#### Copy-Paste Prompts
```
Use @embedding-strategies to select optimal embedding model
```

### Phase 3: Vector Database Setup

#### Skills to Invoke
- `vector-database-engineer` - Vector DB
- `similarity-search-patterns` - Similarity search

#### Actions
1. Choose vector database
2. Design schema
3. Configure indexes
4. Set up connection
5. Test queries

#### Copy-Paste Prompts
```
Use @vector-database-engineer to set up vector database
```

### Phase 4: Chunking Strategy

#### Skills to Invoke
- `rag-engineer` - Chunking strategies
- `rag-implementation` - RAG implementation

#### Actions
1. Choose chunk size
2. Implement chunking
3. Add overlap handling
4. Create metadata
5. Test retrieval quality

#### Copy-Paste Prompts
```
Use @rag-engineer to implement chunking strategy
```

### Phase 5: Retrieval Implementation

#### Skills to Invoke
- `similarity-search-patterns` - Similarity search
- `hybrid-search-implementation` - Hybrid search

#### Actions
1. Implement vector search
2. Add keyword search
3. Configure hybrid search
4. Set up reranking
5. Optimize latency

#### Copy-Paste Prompts
```
Use @similarity-search-patterns to implement retrieval
```

```
Use @hybrid-search-implementation to add hybrid search
```

### Phase 6: LLM Integration

#### Skills to Invoke
- `llm-application-dev-ai-assistant` - LLM integration
- `llm-application-dev-prompt-optimize` - Prompt optimization

#### Actions
1. Select LLM provider
2. Design prompt template
3. Implement context injection
4. Add citation handling
5. Test generation quality

#### Copy-Paste Prompts
```
Use @llm-application-dev-ai-assistant to integrate LLM
```

### Phase 7: Caching

#### Skills to Invoke
- `prompt-caching` - Prompt caching
- `rag-engineer` - RAG optimization

#### Actions
1. Implement response caching
2. Set up embedding cache
3. Configure TTL
4. Add cache invalidation
5. Monitor hit rates

#### Copy-Paste Prompts
```
Use @prompt-caching to implement RAG caching
```

### Phase 8: Evaluation

#### Skills to Invoke
- `llm-evaluation` - LLM evaluation
- `evaluation` - AI evaluation

#### Actions
1. Define evaluation metrics
2. Create test dataset
3. Measure retrieval accuracy
4. Evaluate generation quality
5. Iterate on improvements

#### Copy-Paste Prompts
```
Use @llm-evaluation to evaluate RAG system
```

## RAG Architecture

```
User Query -> Embedding -> Vector Search -> Retrieved Docs -> LLM -> Response
                |              |              |              |
            Model         Vector DB     Chunk Store    Prompt + Context
```

## Quality Gates

- [ ] Embedding model selected
- [ ] Vector DB configured
- [ ] Chunking implemented
- [ ] Retrieval working
- [ ] LLM integrated
- [ ] Evaluation passing

## Related Workflow Bundles

- `ai-ml` - AI/ML development
- `ai-agent-development` - AI agents
- `database` - Vector databases

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## react-nextjs-development
*React and Next.js 14+ application development with App Router, Server Components, TypeScript, Tailwind CSS, and modern frontend patterns.*

Risk: safe

# React/Next.js Development Workflow

## Overview

Specialized workflow for building React and Next.js 14+ applications with modern patterns including App Router, Server Components, TypeScript, and Tailwind CSS.

## When to Use This Workflow

Use this workflow when:
- Building new React applications
- Creating Next.js 14+ projects with App Router
- Implementing Server Components
- Setting up TypeScript with React
- Styling with Tailwind CSS
- Building full-stack Next.js applications

## Workflow Phases

### Phase 1: Project Setup

#### Skills to Invoke
- `app-builder` - Application scaffolding
- `senior-fullstack` - Full-stack guidance
- `nextjs-app-router-patterns` - Next.js 14+ patterns
- `typescript-pro` - TypeScript setup

#### Actions
1. Choose project type (React SPA, Next.js app)
2. Select build tool (Vite, Next.js, Create React App)
3. Scaffold project structure
4. Configure TypeScript
5. Set up ESLint and Prettier

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new Next.js 14 project with App Router
```

```
Use @nextjs-app-router-patterns to set up Server Components
```

### Phase 2: Component Architecture

#### Skills to Invoke
- `frontend-developer` - Component development
- `react-patterns` - React patterns
- `react-state-management` - State management
- `react-ui-patterns` - UI patterns

#### Actions
1. Design component hierarchy
2. Create base components
3. Implement layout components
4. Set up state management
5. Create custom hooks

#### Copy-Paste Prompts
```
Use @frontend-developer to create reusable React components
```

```
Use @react-patterns to implement proper component composition
```

```
Use @react-state-management to set up Zustand store
```

### Phase 3: Styling and Design

#### Skills to Invoke
- `frontend-design` - UI design
- `tailwind-patterns` - Tailwind CSS
- `tailwind-design-system` - Design system
- `core-components` - Component library

#### Actions
1. Set up Tailwind CSS
2. Configure design tokens
3. Create utility classes
4. Build component styles
5. Implement responsive design

#### Copy-Paste Prompts
```
Use @tailwind-patterns to style components with Tailwind CSS v4
```

```
Use @frontend-design to create a modern dashboard UI
```

### Phase 4: Data Fetching

#### Skills to Invoke
- `nextjs-app-router-patterns` - Server Components
- `react-state-management` - React Query
- `api-patterns` - API integration

#### Actions
1. Implement Server Components
2. Set up React Query/SWR
3. Create API client
4. Handle loading states
5. Implement error boundaries

#### Copy-Paste Prompts
```
Use @nextjs-app-router-patterns to implement Server Components data fetching
```

### Phase 5: Routing and Navigation

#### Skills to Invoke
- `nextjs-app-router-patterns` - App Router
- `nextjs-best-practices` - Next.js patterns

#### Actions
1. Set up file-based routing
2. Create dynamic routes
3. Implement nested routes
4. Add route guards
5. Configure redirects

#### Copy-Paste Prompts
```
Use @nextjs-app-router-patterns to set up parallel routes and intercepting routes
```

### Phase 6: Forms and Validation

#### Skills to Invoke
- `frontend-developer` - Form development
- `typescript-advanced-types` - Type validation
- `react-ui-patterns` - Form patterns

#### Actions
1. Choose form library (React Hook Form, Formik)
2. Set up validation (Zod, Yup)
3. Create form components
4. Handle submissions
5. Implement error handling

#### Copy-Paste Prompts
```
Use @frontend-developer to create forms with React Hook Form and Zod
```

### Phase 7: Testing

#### Skills to Invoke
- `javascript-testing-patterns` - Jest/Vitest
- `playwright-skill` - E2E testing
- `e2e-testing-patterns` - E2E patterns

#### Actions
1. Set up testing framework
2. Write unit tests
3. Create component tests
4. Implement E2E tests
5. Configure CI integration

#### Copy-Paste Prompts
```
Use @javascript-testing-patterns to write Vitest tests
```

```
Use @playwright-skill to create E2E tests for critical flows
```

### Phase 8: Build and Deployment

#### Skills to Invoke
- `vercel-deployment` - Vercel deployment
- `vercel-deploy-claimable` - Vercel deployment
- `web-performance-optimization` - Performance

#### Actions
1. Configure build settings
2. Optimize bundle size
3. Set up environment variables
4. Deploy to Vercel
5. Configure preview deployments

#### Copy-Paste Prompts
```
Use @vercel-deployment to deploy Next.js app to production
```

## Technology Stack

| Category | Technology |
|----------|------------|
| Framework | Next.js 14+, React 18+ |
| Language | TypeScript 5+ |
| Styling | Tailwind CSS v4 |
| State | Zustand, React Query |
| Forms | React Hook Form, Zod |
| Testing | Vitest, Playwright |
| Deployment | Vercel |

## Quality Gates

- [ ] TypeScript compiles without errors
- [ ] All tests passing
- [ ] Linting clean
- [ ] Performance metrics met (LCP, CLS, FID)
- [ ] Accessibility checked (WCAG 2.1)
- [ ] Responsive design verified

## Related Workflow Bundles

- `development` - General development
- `testing-qa` - Testing workflow
- `documentation` - Documentation
- `typescript-development` - TypeScript patterns

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## security-audit
*Comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening.*

Risk: safe

# Security Auditing Workflow Bundle

## Overview

Comprehensive security auditing workflow for web applications, APIs, and infrastructure. This bundle orchestrates skills for penetration testing, vulnerability assessment, security scanning, and remediation.

## When to Use This Workflow

Use this workflow when:
- Performing security audits on web applications
- Testing API security
- Conducting penetration tests
- Scanning for vulnerabilities
- Hardening application security
- Compliance security assessments

## Workflow Phases

### Phase 1: Reconnaissance

#### Skills to Invoke
- `scanning-tools` - Security scanning
- `shodan-reconnaissance` - Shodan searches
- `top-web-vulnerabilities` - OWASP Top 10

#### Actions
1. Identify target scope
2. Gather intelligence
3. Map attack surface
4. Identify technologies
5. Document findings

#### Copy-Paste Prompts
```
Use @scanning-tools to perform initial reconnaissance
```

```
Use @shodan-reconnaissance to find exposed services
```

### Phase 2: Vulnerability Scanning

#### Skills to Invoke
- `vulnerability-scanner` - Vulnerability analysis
- `security-scanning-security-sast` - Static analysis
- `security-scanning-security-dependencies` - Dependency scanning

#### Actions
1. Run automated scanners
2. Perform static analysis
3. Scan dependencies
4. Identify misconfigurations
5. Document vulnerabilities

#### Copy-Paste Prompts
```
Use @vulnerability-scanner to scan for OWASP Top 10 vulnerabilities
```

```
Use @security-scanning-security-dependencies to audit dependencies
```

### Phase 3: Web Application Testing

#### Skills to Invoke
- `top-web-vulnerabilities` - OWASP vulnerabilities
- `sql-injection-testing` - SQL injection
- `xss-html-injection` - XSS testing
- `broken-authentication` - Authentication testing
- `idor-testing` - IDOR testing
- `file-path-traversal` - Path traversal
- `burp-suite-testing` - Burp Suite testing

#### Actions
1. Test for injection flaws
2. Test authentication mechanisms
3. Test session management
4. Test access controls
5. Test input validation
6. Test security headers

#### Copy-Paste Prompts
```
Use @sql-injection-testing to test for SQL injection vulnerabilities
```

```
Use @xss-html-injection to test for cross-site scripting
```

```
Use @broken-authentication to test authentication security
```

### Phase 4: API Security Testing

#### Skills to Invoke
- `api-fuzzing-bug-bounty` - API fuzzing
- `api-security-best-practices` - API security

#### Actions
1. Enumerate API endpoints
2. Test authentication/authorization
3. Test rate limiting
4. Test input validation
5. Test error handling
6. Document API vulnerabilities

#### Copy-Paste Prompts
```
Use @api-fuzzing-bug-bounty to fuzz API endpoints
```

### Phase 5: Penetration Testing

#### Skills to Invoke
- `pentest-commands` - Penetration testing commands
- `pentest-checklist` - Pentest planning
- `ethical-hacking-methodology` - Ethical hacking
- `metasploit-framework` - Metasploit

#### Actions
1. Plan penetration test
2. Execute attack scenarios
3. Exploit vulnerabilities
4. Document proof of concept
5. Assess impact

#### Copy-Paste Prompts
```
Use @pentest-checklist to plan penetration test
```

```
Use @pentest-commands to execute penetration testing
```

### Phase 6: Security Hardening

#### Skills to Invoke
- `security-scanning-security-hardening` - Security hardening
- `auth-implementation-patterns` - Authentication
- `api-security-best-practices` - API security

#### Actions
1. Implement security controls
2. Configure security headers
3. Set up authentication
4. Implement authorization
5. Configure logging
6. Apply patches

#### Copy-Paste Prompts
```
Use @security-scanning-security-hardening to harden application security
```

### Phase 7: Reporting

#### Skills to Invoke
- `reporting-standards` - Security reporting

#### Actions
1. Document findings
2. Assess risk levels
3. Provide remediation steps
4. Create executive summary
5. Generate technical report

## Security Testing Checklist

### OWASP Top 10
- [ ] Injection (SQL, NoSQL, OS, LDAP)
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XML External Entities (XXE)
- [ ] Broken Access Control
- [ ] Security Misconfiguration
- [ ] Cross-Site Scripting (XSS)
- [ ] Insecure Deserialization
- [ ] Using Components with Known Vulnerabilities
- [ ] Insufficient Logging & Monitoring

### API Security
- [ ] Authentication mechanisms
- [ ] Authorization checks
- [ ] Rate limiting
- [ ] Input validation
- [ ] Error handling
- [ ] Security headers

## Quality Gates

- [ ] All planned tests executed
- [ ] Vulnerabilities documented
- [ ] Proof of concepts captured
- [ ] Risk assessments completed
- [ ] Remediation steps provided
- [ ] Report generated

## Related Workflow Bundles

- `development` - Secure development practices
- `wordpress` - WordPress security
- `cloud-devops` - Cloud security
- `testing-qa` - Security testing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## terraform-infrastructure
*Terraform infrastructure as code workflow for provisioning cloud resources, creating reusable modules, and managing infrastructure at scale.*

Risk: safe

# Terraform Infrastructure Workflow

## Overview

Specialized workflow for infrastructure as code using Terraform including resource provisioning, module creation, state management, and multi-environment deployments.

## When to Use This Workflow

Use this workflow when:
- Provisioning cloud infrastructure
- Creating Terraform modules
- Managing multi-environment infra
- Implementing IaC best practices
- Setting up Terraform workflows

## Workflow Phases

### Phase 1: Terraform Setup

#### Skills to Invoke
- `terraform-skill` - Terraform basics
- `terraform-specialist` - Advanced Terraform

#### Actions
1. Initialize Terraform
2. Configure backend
3. Set up providers
4. Configure variables
5. Create outputs

#### Copy-Paste Prompts
```
Use @terraform-skill to set up Terraform project
```

### Phase 2: Resource Provisioning

#### Skills to Invoke
- `terraform-module-library` - Terraform modules
- `cloud-architect` - Cloud architecture

#### Actions
1. Design infrastructure
2. Create resource definitions
3. Configure networking
4. Set up compute
5. Add storage

#### Copy-Paste Prompts
```
Use @terraform-module-library to provision cloud resources
```

### Phase 3: Module Creation

#### Skills to Invoke
- `terraform-module-library` - Module creation

#### Actions
1. Design module interface
2. Create module structure
3. Define variables/outputs
4. Add documentation
5. Test module

#### Copy-Paste Prompts
```
Use @terraform-module-library to create reusable Terraform module
```

### Phase 4: State Management

#### Skills to Invoke
- `terraform-specialist` - State management

#### Actions
1. Configure remote backend
2. Set up state locking
3. Implement workspaces
4. Configure state access
5. Set up backup

#### Copy-Paste Prompts
```
Use @terraform-specialist to configure Terraform state
```

### Phase 5: Multi-Environment

#### Skills to Invoke
- `terraform-specialist` - Multi-environment

#### Actions
1. Design environment structure
2. Create environment configs
3. Set up variable files
4. Configure isolation
5. Test deployments

#### Copy-Paste Prompts
```
Use @terraform-specialist to set up multi-environment Terraform
```

### Phase 6: CI/CD Integration

#### Skills to Invoke
- `cicd-automation-workflow-automate` - CI/CD
- `github-actions-templates` - GitHub Actions

#### Actions
1. Create CI pipeline
2. Configure plan/apply
3. Set up approvals
4. Add validation
5. Test pipeline

#### Copy-Paste Prompts
```
Use @cicd-automation-workflow-automate to create Terraform CI/CD
```

### Phase 7: Security

#### Skills to Invoke
- `secrets-management` - Secrets management
- `terraform-specialist` - Security

#### Actions
1. Configure secrets
2. Set up encryption
3. Implement policies
4. Add compliance
5. Audit access

#### Copy-Paste Prompts
```
Use @secrets-management to secure Terraform secrets
```

## Quality Gates

- [ ] Resources provisioned
- [ ] Modules working
- [ ] State configured
- [ ] Multi-env tested
- [ ] CI/CD working
- [ ] Security verified

## Related Workflow Bundles

- `cloud-devops` - Cloud/DevOps
- `kubernetes-deployment` - Kubernetes
- `aws-infrastructure` - AWS specific

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## testing-qa
*Comprehensive testing and QA workflow covering unit testing, integration testing, E2E testing, browser automation, and quality assurance.*

Risk: safe

# Testing/QA Workflow Bundle

## Overview

Comprehensive testing and quality assurance workflow covering unit tests, integration tests, E2E tests, browser automation, and quality gates for production-ready software.

## When to Use This Workflow

Use this workflow when:
- Setting up testing infrastructure
- Writing unit and integration tests
- Implementing E2E tests
- Automating browser testing
- Establishing quality gates
- Performing code review

## Workflow Phases

### Phase 1: Test Strategy

#### Skills to Invoke
- `test-automator` - Test automation
- `test-driven-development` - TDD

#### Actions
1. Define testing strategy
2. Choose testing frameworks
3. Plan test coverage
4. Set up test infrastructure
5. Configure CI integration

#### Copy-Paste Prompts
```
Use @test-automator to design testing strategy
```

```
Use @test-driven-development to implement TDD workflow
```

### Phase 2: Unit Testing

#### Skills to Invoke
- `javascript-testing-patterns` - Jest/Vitest
- `python-testing-patterns` - pytest
- `unit-testing-test-generate` - Test generation
- `tdd-orchestrator` - TDD orchestration

#### Actions
1. Write unit tests
2. Set up test fixtures
3. Configure mocking
4. Measure coverage
5. Integrate with CI

#### Copy-Paste Prompts
```
Use @javascript-testing-patterns to write Jest tests
```

```
Use @python-testing-patterns to write pytest tests
```

```
Use @unit-testing-test-generate to generate unit tests
```

### Phase 3: Integration Testing

#### Skills to Invoke
- `api-testing-observability-api-mock` - API testing
- `e2e-testing-patterns` - Integration patterns

#### Actions
1. Design integration tests
2. Set up test databases
3. Configure API mocks
4. Test service interactions
5. Verify data flows

#### Copy-Paste Prompts
```
Use @api-testing-observability-api-mock to test APIs
```

### Phase 4: E2E Testing

#### Skills to Invoke
- `playwright-skill` - Playwright testing
- `e2e-testing-patterns` - E2E patterns
- `webapp-testing` - Web app testing

#### Actions
1. Design E2E scenarios
2. Write test scripts
3. Configure test data
4. Set up parallel execution
5. Implement visual regression

#### Copy-Paste Prompts
```
Use @playwright-skill to create E2E tests
```

```
Use @e2e-testing-patterns to design E2E strategy
```

### Phase 5: Browser Automation

#### Skills to Invoke
- `browser-automation` - Browser automation
- `webapp-testing` - Browser testing
- `screenshots` - Screenshot automation

#### Actions
1. Set up browser automation
2. Configure headless testing
3. Implement visual testing
4. Capture screenshots
5. Test responsive design

#### Copy-Paste Prompts
```
Use @browser-automation to automate browser tasks
```

```
Use @screenshots to capture marketing screenshots
```

### Phase 6: Performance Testing

#### Skills to Invoke
- `performance-engineer` - Performance engineering
- `performance-profiling` - Performance profiling
- `web-performance-optimization` - Web performance

#### Actions
1. Design performance tests
2. Set up load testing
3. Measure response times
4. Identify bottlenecks
5. Optimize performance

#### Copy-Paste Prompts
```
Use @performance-engineer to test application performance
```

### Phase 7: Code Review

#### Skills to Invoke
- `code-reviewer` - AI code review
- `code-review-excellence` - Review best practices
- `find-bugs` - Bug detection
- `security-scanning-security-sast` - Security scanning

#### Actions
1. Configure review tools
2. Run automated reviews
3. Check for bugs
4. Verify security
5. Approve changes

#### Copy-Paste Prompts
```
Use @code-reviewer to review pull requests
```

```
Use @find-bugs to detect bugs in code
```

### Phase 8: Quality Gates

#### Skills to Invoke
- `lint-and-validate` - Linting
- `verification-before-completion` - Verification

#### Actions
1. Configure linters
2. Set up formatters
3. Define quality metrics
4. Implement gates
5. Monitor compliance

#### Copy-Paste Prompts
```
Use @lint-and-validate to check code quality
```

```
Use @verification-before-completion to verify changes
```

## Testing Pyramid

```
        /       /  \    E2E Tests (10%)
      /----     /      \  Integration Tests (20%)
    /--------   /          \ Unit Tests (70%)
  /------------```

## Quality Gates Checklist

- [ ] Unit test coverage > 80%
- [ ] All tests passing
- [ ] E2E tests for critical paths
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Code review approved
- [ ] Linting clean

## Related Workflow Bundles

- `development` - Development workflow
- `security-audit` - Security testing
- `cloud-devops` - CI/CD integration
- `ai-ml` - AI testing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## web-security-testing
*Web application security testing workflow for OWASP Top 10 vulnerabilities including injection, XSS, authentication flaws, and access control issues.*

Risk: safe

# Web Security Testing Workflow

## Overview

Specialized workflow for testing web applications against OWASP Top 10 vulnerabilities including injection attacks, XSS, broken authentication, and access control issues.

## When to Use This Workflow

Use this workflow when:
- Testing web application security
- Performing OWASP Top 10 assessment
- Conducting penetration tests
- Validating security controls
- Bug bounty hunting

## Workflow Phases

### Phase 1: Reconnaissance

#### Skills to Invoke
- `scanning-tools` - Security scanning
- `top-web-vulnerabilities` - OWASP knowledge

#### Actions
1. Map application surface
2. Identify technologies
3. Discover endpoints
4. Find subdomains
5. Document findings

#### Copy-Paste Prompts
```
Use @scanning-tools to perform web application reconnaissance
```

### Phase 2: Injection Testing

#### Skills to Invoke
- `sql-injection-testing` - SQL injection
- `sqlmap-database-pentesting` - SQLMap

#### Actions
1. Test SQL injection
2. Test NoSQL injection
3. Test command injection
4. Test LDAP injection
5. Document vulnerabilities

#### Copy-Paste Prompts
```
Use @sql-injection-testing to test for SQL injection
```

```
Use @sqlmap-database-pentesting to automate SQL injection testing
```

### Phase 3: XSS Testing

#### Skills to Invoke
- `xss-html-injection` - XSS testing
- `html-injection-testing` - HTML injection

#### Actions
1. Test reflected XSS
2. Test stored XSS
3. Test DOM-based XSS
4. Test XSS filters
5. Document findings

#### Copy-Paste Prompts
```
Use @xss-html-injection to test for cross-site scripting
```

### Phase 4: Authentication Testing

#### Skills to Invoke
- `broken-authentication` - Authentication testing

#### Actions
1. Test credential stuffing
2. Test brute force protection
3. Test session management
4. Test password policies
5. Test MFA implementation

#### Copy-Paste Prompts
```
Use @broken-authentication to test authentication security
```

### Phase 5: Access Control Testing

#### Skills to Invoke
- `idor-testing` - IDOR testing
- `file-path-traversal` - Path traversal

#### Actions
1. Test vertical privilege escalation
2. Test horizontal privilege escalation
3. Test IDOR vulnerabilities
4. Test directory traversal
5. Test unauthorized access

#### Copy-Paste Prompts
```
Use @idor-testing to test for insecure direct object references
```

```
Use @file-path-traversal to test for path traversal
```

### Phase 6: Security Headers

#### Skills to Invoke
- `api-security-best-practices` - Security headers

#### Actions
1. Check CSP implementation
2. Verify HSTS configuration
3. Test X-Frame-Options
4. Check X-Content-Type-Options
5. Verify referrer policy

#### Copy-Paste Prompts
```
Use @api-security-best-practices to audit security headers
```

### Phase 7: Reporting

#### Skills to Invoke
- `reporting-standards` - Security reporting

#### Actions
1. Document vulnerabilities
2. Assess risk levels
3. Provide remediation
4. Create proof of concept
5. Generate report

#### Copy-Paste Prompts
```
Use @reporting-standards to create security report
```

## OWASP Top 10 Checklist

- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection
- [ ] A04: Insecure Design
- [ ] A05: Security Misconfiguration
- [ ] A06: Vulnerable Components
- [ ] A07: Authentication Failures
- [ ] A08: Software/Data Integrity
- [ ] A09: Logging/Monitoring
- [ ] A10: SSRF

## Quality Gates

- [ ] All OWASP Top 10 tested
- [ ] Vulnerabilities documented
- [ ] Proof of concepts captured
- [ ] Remediation provided
- [ ] Report generated

## Related Workflow Bundles

- `security-audit` - Security auditing
- `api-security-testing` - API security
- `wordpress-security` - WordPress security

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## wordpress
*Complete WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security hardening. Includes WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks.*

Risk: safe

# WordPress Development Workflow Bundle

## Overview

Comprehensive WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security. This bundle orchestrates skills for building production-ready WordPress sites and applications.

## WordPress 7.0 Features (Backward Compatible)

WordPress 7.0 (April 9, 2026) introduces significant features while maintaining backward compatibility:

### Real-Time Collaboration (RTC)
- Multiple users can edit simultaneously using Yjs CRDT
- HTTP polling provider (configurable via `WP_COLLABORATION_MAX_USERS`)
- Custom transport via `sync.providers` filter
- **Backward Compatibility**: Falls back to post locking when legacy meta boxes detected

### AI Connectors API
- Provider-agnostic AI interface in core (`wp_ai_client_prompt()`)
- Settings > Connectors for centralized API credential management
- Official providers: OpenAI, Anthropic Claude, Google Gemini
- **Backward Compatibility**: Works with WordPress 6.9+ via plugin

### Abilities API (Stable in 7.0)
- Standardized capability declaration system
- REST API endpoints: `/wp-json/abilities/v1/manifest`
- MCP adapter for AI agent integration
- **Backward Compatibility**: Can be used as Composer package in 6.x

### DataViews & DataForm
- Replaces WP_List_Table on Posts, Pages, Media screens
- New layouts: table, grid, list, activity
- Client-side validation (pattern, minLength, maxLength, min, max)
- **Backward Compatibility**: Plugins using old hooks still work

### PHP-Only Block Registration
- Register blocks entirely via PHP without JavaScript
- Auto-generated Inspector controls
- **Backward Compatibility**: Existing JS blocks continue to work

### Interactivity API Updates
- `watch()` replaces `effect` from @preact/signals
- State navigation changes
- **Backward Compatibility**: Old syntax deprecated but functional

### Admin Refresh
- New default color scheme
- View transitions between admin screens
- **Backward Compatibility**: CSS-level changes, no breaking changes

### Pattern Editing
- ContentOnly mode defaults for unsynced patterns
- `disableContentOnlyForUnsyncedPatterns` setting
- **Backward Compatibility**: Existing patterns work

## When to Use This Workflow

Use this workflow when:
- Building new WordPress websites
- Creating custom themes
- Developing WordPress plugins
- Setting up WooCommerce stores
- Optimizing WordPress performance
- Hardening WordPress security
- Implementing WordPress 7.0 features (RTC, AI, DataViews)

## Workflow Phases

### Phase 1: WordPress Setup

#### Skills to Invoke
- `app-builder` - Project scaffolding
- `environment-setup-guide` - Development environment

#### Actions
1. Set up local development environment (LocalWP, Docker, or Valet)
2. Install WordPress (recommend 7.0+ for new projects)
3. Configure development database
4. Set up version control
5. Configure wp-config.php for development

#### WordPress 7.0 Configuration
```php
// wp-config.php - Collaboration settings
define('WP_COLLABORATION_MAX_USERS', 5);

// AI Connector is enabled by installing a provider plugin
// (e.g., OpenAI, Anthropic Claude, or Google Gemini connector)
// No constant needed - configure via Settings > Connectors in admin
```

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new WordPress project with modern tooling
```

### Phase 2: Theme Development

#### Skills to Invoke
- `frontend-developer` - Component development
- `frontend-design` - UI implementation
- `tailwind-patterns` - Styling
- `web-performance-optimization` - Performance

#### Actions
1. Design theme architecture
2. Create theme files (style.css, functions.php, index.php)
3. Implement template hierarchy
4. Create custom page templates
5. Add custom post types and taxonomies
6. Implement theme customization options
7. Add responsive design
8. Test with WordPress 7.0 admin refresh

#### WordPress 7.0 Theme Considerations
- Block API v3 now reference model
- Pseudo-element support in theme.json
- Global Styles custom CSS honors block-defined selectors
- View transitions for admin navigation

#### Theme Structure
```
theme-name/
├── style.css
├── functions.php
├── index.php
├── header.php
├── footer.php
├── sidebar.php
├── single.php
├── page.php
├── archive.php
├── search.php
├── 404.php
├── template-parts/
├── inc/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

#### Copy-Paste Prompts
```
Use @frontend-developer to create a custom WordPress theme with React components
```

```
Use @tailwind-patterns to style WordPress theme with modern CSS
```

### Phase 3: Plugin Development

#### Skills to Invoke
- `backend-dev-guidelines` - Backend standards
- `api-design-principles` - API design
- `auth-implementation-patterns` - Authentication

#### Actions
1. Design plugin architecture
2. Create plugin boilerplate
3. Implement hooks (actions and filters)
4. Create admin interfaces
5. Add custom database tables
6. Implement REST API endpoints
7. Add settings and options pages

#### WordPress 7.0 Plugin Considerations
- **RTC Compatibility**: Register post meta with `show_in_rest => true`
- **AI Integration**: Use `wp_ai_client_prompt()` for AI features
- **DataViews**: Consider new admin UI patterns
- **Meta Boxes**: Migrate to block-based UIs for collaboration support

#### RTC-Compatible Post Meta Registration
```php
register_post_meta('post', 'custom_field', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,  // Required for RTC
    'sanitize_callback' => 'sanitize_text_field',
]);
```

#### AI Connector Example
```php
// Using WordPress 7.0 AI Connector
// Note: Requires an AI provider plugin (OpenAI, Claude, or Gemini) to be installed and configured

// Basic text generation
$response = wp_ai_client_prompt('Summarize this content.')
    ->generate_text();

// With temperature for deterministic output
$response = wp_ai_client_prompt('Summarize this content.')
    ->using_temperature(0.2)
    ->generate_text();

// With model preference (tries first available in list)
$response = wp_ai_client_prompt('Summarize this content.')
    ->using_model_preference('gpt-4', 'claude-3-opus', 'gemini-2-pro')
    ->generate_text();

// For JSON structured output
$schema = [
    'type' => 'object',
    'properties' => [
        'summary' => ['type' => 'string'],
        'keywords' => ['type' => 'array', 'items' => ['type' => 'string']]
    ],
    'required' => ['summary']
];
$response = wp_ai_client_prompt('Analyze this content and return JSON.')
    ->using_system_instruction('You are a content analyzer.')
    ->as_json_response($schema)
    ->generate_text();
```

#### Plugin Structure
```
plugin-name/
├── plugin-name.php
├── includes/
│   ├── class-plugin-activator.php
│   ├── class-plugin-deactivator.php
│   ├── class-plugin-loader.php
│   └── class-plugin.php
├── admin/
│   ├── class-plugin-admin.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-plugin-public.php
│   ├── css/
│   └── js/
└── languages/
```

#### Copy-Paste Prompts
```
Use @backend-dev-guidelines to create a WordPress plugin with proper architecture
```

### Phase 4: WooCommerce Integration

#### Skills to Invoke
- `payment-integration` - Payment processing
- `stripe-integration` - Stripe payments
- `billing-automation` - Billing workflows

#### Actions
1. Install and configure WooCommerce
2. Create custom product types
3. Customize checkout flow
4. Integrate payment gateways
5. Set up shipping methods
6. Create custom order statuses
7. Implement subscription products
8. Add custom email templates

#### WordPress 7.0 + WooCommerce Considerations
- Test checkout with new admin interfaces
- AI connectors for product descriptions
- DataViews for order management screens
- RTC for collaborative order editing

#### Copy-Paste Prompts
```
Use @payment-integration to set up WooCommerce with Stripe
```

```
Use @billing-automation to create subscription products in WooCommerce
```

### Phase 5: Performance Optimization

#### Skills to Invoke
- `web-performance-optimization` - Performance optimization
- `database-optimizer` - Database optimization

#### Actions
1. Implement caching (object, page, browser)
2. Optimize images (lazy loading, WebP)
3. Minify and combine assets
4. Enable CDN
5. Optimize database queries
6. Implement lazy loading
7. Configure OPcache
8. Set up Redis/Memcached

#### WordPress 7.0 Performance
- Client-side media processing
- Font Library enabled for all themes
- Responsive grid block optimizations
- View transitions reduce perceived load time

#### Performance Checklist
- [ ] Page load time < 3 seconds
- [ ] Time to First Byte < 200ms
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1
- [ ] First Input Delay < 100ms

#### Copy-Paste Prompts
```
Use @web-performance-optimization to audit and improve WordPress performance
```

### Phase 6: Security Hardening

#### Skills to Invoke
- `security-auditor` - Security audit
- `wordpress-penetration-testing` - WordPress security testing
- `sast-configuration` - Static analysis

#### Actions
1. Update WordPress core, themes, plugins
2. Implement security headers
3. Configure file permissions
4. Set up firewall rules
5. Enable two-factor authentication
6. Implement rate limiting
7. Configure security logging
8. Set up malware scanning

#### WordPress 7.0 Security Considerations
- PHP 7.4 minimum (drops 7.2/7.3 support)
- Test Abilities API permission boundaries
- Verify collaboration data isolation
- AI connector credential security

#### Security Checklist
- [ ] WordPress core updated (7.0+ recommended)
- [ ] All plugins/themes updated
- [ ] Strong passwords enforced
- [ ] Two-factor authentication enabled
- [ ] Security headers configured
- [ ] XML-RPC disabled or protected
- [ ] File editing disabled
- [ ] Database prefix changed
- [ ] Regular backups configured

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to audit WordPress security
```

```
Use @security-auditor to perform comprehensive security review
```

### Phase 7: Testing

#### Skills to Invoke
- `test-automator` - Test automation
- `playwright-skill` - E2E testing
- `webapp-testing` - Web app testing

#### Actions
1. Write unit tests for custom code
2. Create integration tests
3. Set up E2E tests
4. Test cross-browser compatibility
5. Test responsive design
6. Performance testing
7. Security testing

#### WordPress 7.0 Testing Priorities
- Test with iframed post editor
- Verify DataViews integration
- Test collaboration (RTC) workflows
- Validate AI connector functionality
- Test Interactivity API with watch()

#### Copy-Paste Prompts
```
Use @playwright-skill to create E2E tests for WordPress site
```

### Phase 8: Deployment

#### Skills to Invoke
- `deployment-engineer` - Deployment
- `cicd-automation-workflow-automate` - CI/CD
- `github-actions-templates` - GitHub Actions

#### Actions
1. Set up staging environment
2. Configure deployment pipeline
3. Set up database migrations
4. Configure environment variables
5. Enable maintenance mode during deployment
6. Deploy to production
7. Verify deployment
8. Monitor post-deployment

#### Copy-Paste Prompts
```
Use @deployment-engineer to set up WordPress deployment pipeline
```

## WordPress-Specific Workflows

### Custom Post Type Development (RTC-Compatible)
```php
register_post_type('book', [
    'labels' => [...],
    'public' => true,
    'has_archive' => true,
    'supports' => ['title', 'editor', 'thumbnail', 'excerpt'],
    'menu_icon' => 'dashicons-book',
    'show_in_rest' => true,  // Enable for RTC
]);

// Register meta with REST API for collaboration
register_post_meta('book', 'isbn', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,
    'sanitize_callback' => 'sanitize_text_field',
]);
```

### Custom REST API Endpoint
```php
add_action('rest_api_init', function() {
    register_rest_route('myplugin/v1', '/books', [
        'methods' => 'GET',
        'callback' => 'get_books',
        'permission_callback' => '__return_true',
    ]);
});
```

### WordPress 7.0 AI Connector Usage
```php
// Auto-generate post excerpt with AI
add_action('save_post', function($post_id, $post) {
    if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) {
        return;
    }
    
    // Skip if excerpt already exists
    if (!empty($post->post_excerpt)) {
        return;
    }
    
    $content = strip_tags($post->post_content);
    if (empty($content)) {
        return;
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    // Build prompt with input
    $result = wp_ai_client_prompt(
        'Create a brief 2-sentence summary of this content: ' . substr($content, 0, 1000)
    );
    
    if (is_wp_error($result)) {
        return; // Silently fail - don't block post saving
    }
    
    // Use temperature for consistent output
    $result->using_temperature(0.3);
    $summary = $result->generate_text();
    
    if ($summary && !is_wp_error($summary)) {
        wp_update_post([
            'ID' => $post_id,
            'post_excerpt' => sanitize_textarea_field($summary)
        ]);
    }
}, 10, 2);
```

### PHP-Only Block Registration (WordPress 7.0)
```php
// Register block entirely in PHP
register_block_type('my-plugin/hello-world', [
    'render_callback' => function($attributes, $content) {
        return '<p class="hello-world">Hello, World!</p>';
    },
    'attributes' => [
        'message' => ['type' => 'string', 'default' => 'Hello!']
    ],
]);
```

### Abilities API Registration
```php
// Register ability category on correct hook
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('content-creation', [
        'label' => __('Content Creation', 'my-plugin'),
        'description' => __('Abilities for generating and managing content', 'my-plugin'),
    ]);
});

// Register abilities on correct hook
add_action('wp_abilities_api_init', function() {
    wp_register_ability('my-plugin/generate-summary', [
        'label' => __('Generate Post Summary', 'my-plugin'),
        'description' => __('Creates an AI-powered summary of a post', 'my-plugin'),
        'category' => 'content-creation',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'post_id' => ['type' => 'integer', 'description' => 'The post ID to summarize']
            ],
            'required' => ['post_id']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'summary' => ['type' => 'string', 'description' => 'The generated summary']
            ]
        ],
        'execute_callback' => 'my_plugin_generate_summary_handler',
        'permission_callback' => function() {
            return current_user_can('edit_posts');
        }
    ]);
});

// Handler function for the ability
function my_plugin_generate_summary_handler($input) {
    $post_id = isset($input['post_id']) ? absint($input['post_id']) : 0;
    $post = get_post($post_id);
    
    if (!$post) {
        return new WP_Error('invalid_post', 'Post not found');
    }
    
    $content = strip_tags($post->post_content);
    if (empty($content)) {
        return ['summary' => ''];
    }
    
    if (!function_exists('wp_ai_client_prompt')) {
        return new WP_Error('ai_unavailable', 'AI client not available');
    }
    
    $result = wp_ai_client_prompt('Summarize in 2 sentences: ' . substr($content, 0, 1000))
        ->using_temperature(0.3)
        ->generate_text();
    
    if (is_wp_error($result)) {
        return $result;
    }
    
    return ['summary' => sanitize_textarea_field($result)];
}
```

### WooCommerce Custom Product Type
```php
add_action('init', function() {
    class WC_Product_Custom extends WC_Product {
        // Custom product implementation
    }
});
```

## Quality Gates

Before moving to next phase, verify:
- [ ] All custom code tested
- [ ] Security scan passed
- [ ] Performance targets met
- [ ] Cross-browser tested
- [ ] Mobile responsive verified
- [ ] Accessibility checked (WCAG 2.1)
- [ ] WordPress 7.0 compatibility verified (for new projects)

## Related Workflow Bundles

- `development` - General web development
- `security-audit` - Security testing
- `testing-qa` - Testing workflow
- `ecommerce` - E-commerce development

(End of file - total 440 lines)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## wordpress-plugin-development
*WordPress plugin development workflow covering plugin architecture, hooks, admin interfaces, REST API, security best practices, and WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks.*

Risk: safe

# WordPress Plugin Development Workflow

## Overview

Specialized workflow for creating WordPress plugins with proper architecture, hooks system, admin interfaces, REST API endpoints, and security practices. Now includes WordPress 7.0 features for modern plugin development.

## WordPress 7.0 Plugin Development

### Key Features for Plugin Developers

1. **Real-Time Collaboration (RTC) Compatibility**
   - Yjs-based CRDT for simultaneous editing
   - Custom transport via `sync.providers` filter
   - **Requirement**: Register post meta with `show_in_rest => true`

2. **AI Connector Integration**
   - Provider-agnostic AI via `wp_ai_client_prompt()`
   - Settings > Connectors admin screen
   - Works with OpenAI, Claude, Gemini, Ollama

3. **Abilities API**
   - Declare plugin capabilities for AI agents
   - REST API: `/wp-json/abilities/v1/manifest`
   - MCP adapter support

4. **DataViews & DataForm**
   - Modern admin interfaces
   - Replaces WP_List_Table patterns
   - Built-in validation

5. **PHP-Only Blocks**
   - Register blocks without JavaScript
   - Auto-generated Inspector controls

## When to Use This Workflow

Use this workflow when:
- Creating custom WordPress plugins
- Extending WordPress functionality
- Building admin interfaces
- Adding REST API endpoints
- Integrating third-party services
- Implementing WordPress 7.0 AI/Collaboration features

## Workflow Phases

### Phase 1: Plugin Setup

#### Skills to Invoke
- `app-builder` - Project scaffolding
- `backend-dev-guidelines` - Backend patterns

#### Actions
1. Create plugin directory structure
2. Set up main plugin file with header
3. Implement activation/deactivation hooks
4. Set up autoloading
5. Configure text domain

#### WordPress 7.0 Plugin Header
```php
/*
Plugin Name: My Plugin
Plugin URI: https://example.com/my-plugin
Description: A WordPress 7.0 compatible plugin with AI and RTC support
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 7.4
Author: Developer Name
License: GPL2+
*/
```

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new WordPress plugin
```

### Phase 2: Plugin Architecture

#### Skills to Invoke
- `backend-dev-guidelines` - Architecture patterns

#### Actions
1. Design plugin class structure
2. Implement singleton pattern
3. Create loader class
4. Set up dependency injection
5. Configure plugin lifecycle

#### WordPress 7.0 Architecture Considerations
- Prepare for iframed editor compatibility
- Design for collaboration-aware data flows
- Consider Abilities API for AI integration

#### Copy-Paste Prompts
```
Use @backend-dev-guidelines to design plugin architecture
```

### Phase 3: Hooks Implementation

#### Skills to Invoke
- `wordpress-penetration-testing` - WordPress patterns

#### Actions
1. Register action hooks
2. Create filter hooks
3. Implement callback functions
4. Set up hook priorities
5. Add conditional hooks

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to understand WordPress hooks
```

### Phase 4: Admin Interface

#### Skills to Invoke
- `frontend-developer` - Admin UI

#### Actions
1. Create admin menu
2. Build settings pages
3. Implement options registration
4. Add settings sections/fields
5. Create admin notices

#### WordPress 7.0 Admin Considerations
- Test with new admin color scheme
- Consider DataViews for data displays
- Implement view transitions
- Use new validation patterns

#### DataViews Example
```javascript
import { DataViews } from '@wordpress/dataviews';

const MyPluginDataView = () => {
    const data = [/* records */];
    const fields = [
        { id: 'title', label: 'Title', sortable: true },
        { id: 'status', label: 'Status', filterBy: true }
    ];
    const view = {
        type: 'table',
        perPage: 10,
        sort: { field: 'title', direction: 'asc' }
    };

    return (
        <DataViews
            data={data}
            fields={fields}
            view={view}
            onChangeView={handleViewChange}
        />
    );
};
```

#### Copy-Paste Prompts
```
Use @frontend-developer to create WordPress admin interface
```

### Phase 5: Database Operations

#### Skills to Invoke
- `database-design` - Database design
- `postgresql` - Database patterns

#### Actions
1. Create custom tables
2. Implement CRUD operations
3. Add data validation
4. Set up data sanitization
5. Create data upgrade routines

#### RTC-Compatible Post Meta
```php
// Register meta for Real-Time Collaboration
register_post_meta('post', 'my_custom_field', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,  // Required for RTC
    'sanitize_callback' => 'sanitize_text_field',
]);

// For WP 7.0, also consider:
register_term_meta('category', 'my_term_field', [
    'type' => 'string',
    'show_in_rest' => true,
]);
```

#### Copy-Paste Prompts
```
Use @database-design to design plugin database schema
```

### Phase 6: REST API

#### Skills to Invoke
- `api-design-principles` - API design
- `api-patterns` - API patterns

#### Actions
1. Register REST routes
2. Create endpoint callbacks
3. Implement permission callbacks
4. Add request validation
5. Document API endpoints

#### WordPress 7.0 REST API Enhancements
- Abilities API integration
- AI Connector endpoints
- Enhanced validation

#### Copy-Paste Prompts
```
Use @api-design-principles to create WordPress REST API endpoints
```

### Phase 7: Security

#### Skills to Invoke
- `wordpress-penetration-testing` - WordPress security
- `security-scanning-security-sast` - Security scanning

#### Actions
1. Implement nonce verification
2. Add capability checks
3. Sanitize all inputs
4. Escape all outputs
5. Secure database queries

#### WordPress 7.0 Security Considerations
- Test Abilities API permission boundaries
- Validate AI connector credential handling
- Review collaboration data isolation
- PHP 7.4+ requirement compliance

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to audit plugin security
```

### Phase 8: WordPress 7.0 Features

#### Skills to Invoke
- `api-design-principles` - AI integration
- `backend-dev-guidelines` - Block development

#### AI Connector Implementation
```php
// Using WordPress 7.0 AI Connector
add_action('save_post', 'my_plugin_generate_ai_summary', 10, 2);

function my_plugin_generate_ai_summary($post_id, $post) {
    if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) {
        return;
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    $content = strip_tags($post->post_content);
    if (empty($content)) {
        return;
    }
    
    // Build prompt - direct string concatenation for input
    $result = wp_ai_client_prompt(
        'Create a compelling 2-sentence summary for social media: ' . substr($content, 0, 1000)
    );
    
    if (is_wp_error($result)) {
        return;
    }
    
    // Set temperature for consistent output
    $result->using_temperature(0.3);
    $summary = $result->generate_text();
    
    if ($summary && !is_wp_error($summary)) {
        update_post_meta($post_id, '_ai_summary', sanitize_textarea_field($summary));
    }
}
```

#### Abilities API Registration
```php
// Register ability categories on their own hook
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('content-creation', [
        'label' => __('Content Creation', 'my-plugin'),
        'description' => __('Abilities for generating and managing content', 'my-plugin'),
    ]);
});

// Register abilities on their own hook
add_action('wp_abilities_api_init', function() {
    wp_register_ability('my-plugin/generate-summary', [
        'label' => __('Generate Summary', 'my-plugin'),
        'description' => __('Creates an AI-powered summary of content', 'my-plugin'),
        'category' => 'content-creation',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'content' => ['type' => 'string'],
                'length' => ['type' => 'integer', 'default' => 2]
            ],
            'required' => ['content']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'summary' => ['type' => 'string']
            ]
        ],
        'execute_callback' => 'my_plugin_generate_summary_cb',
        'permission_callback' => function() {
            return current_user_can('edit_posts');
        }
    ]);
});

// Handler callback
function my_plugin_generate_summary_cb($input) {
    $content = isset($input['content']) ? $input['content'] : '';
    $length = isset($input['length']) ? absint($input['length']) : 2;
    
    if (empty($content)) {
        return new WP_Error('empty_content', 'No content provided');
    }
    
    if (!function_exists('wp_ai_client_prompt')) {
        return new WP_Error('ai_unavailable', 'AI not available');
    }
    
    $prompt = sprintf('Create a %d-sentence summary of: %s', $length, substr($content, 0, 2000));
    
    $result = wp_ai_client_prompt($prompt)
        ->using_temperature(0.3)
        ->generate_text();
    
    if (is_wp_error($result)) {
        return $result;
    }
    
    return ['summary' => sanitize_textarea_field($result)];
}
```

#### PHP-Only Block Registration
```php
// Register block entirely in PHP (WordPress 7.0)
// Note: For full PHP-only blocks, use block.json with PHP render_callback

// First, create a block.json file in build/ or includes/blocks/
// Then register in PHP:

// Simple PHP-only block registration (WordPress 7.0+)
if (function_exists('register_block_type')) {
    register_block_type('my-plugin/featured-post', [
        'render_callback' => function($attributes, $content, $block) {
            $post_id = isset($attributes['postId']) ? absint($attributes['postId']) : 0;
            
            if (!$post_id) {
                $post_id = get_the_ID();
            }
            
            $post = get_post($post_id);
            
            if (!$post) {
                return '';
            }
            
            $title = esc_html($post->post_title);
            $excerpt = esc_html(get_the_excerpt($post));
            
            return sprintf(
                '<div class="featured-post"><h2>%s</h2><p>%s</p></div>',
                $title,
                $excerpt
            );
        },
        'attributes' => [
            'postId' => ['type' => 'integer', 'default' => 0],
            'showExcerpt' => ['type' => 'boolean', 'default' => true]
        ],
    ]);
}
```

#### Disable Collaboration (if needed)
```javascript
// Disable RTC for specific post types
import { addFilter } from '@wordpress/hooks';

addFilter(
    'sync.providers',
    'my-plugin/disable-collab',
    () => []
);
```

### Phase 9: Testing

#### Skills to Invoke
- `test-automator` - Test automation
- `php-pro` - PHP testing

#### Actions
1. Set up PHPUnit
2. Create unit tests
3. Write integration tests
4. Test with WordPress test suite
5. Configure CI

#### WordPress 7.0 Testing Priorities
- Test RTC compatibility
- Verify AI connector functionality
- Validate DataViews integration
- Test Interactivity API with watch()

#### Copy-Paste Prompts
```
Use @test-automator to set up plugin testing
```

## Plugin Structure

```
plugin-name/
├── plugin-name.php
├── includes/
│   ├── class-plugin.php
│   ├── class-loader.php
│   ├── class-activator.php
│   └── class-deactivator.php
├── admin/
│   ├── class-plugin-admin.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-plugin-public.php
│   ├── css/
│   └── js/
├── blocks/           # PHP-only blocks (WP 7.0)
├── abilities/        # Abilities API
├── ai/               # AI Connector integration
├── languages/
└── vendor/
```

## WordPress 7.0 Compatibility Checklist

- [ ] PHP 7.4+ requirement documented
- [ ] Post meta registered with `show_in_rest => true` for RTC
- [ ] Meta boxes migrated to block-based UIs
- [ ] AI Connector integration tested
- [ ] Abilities API registered (if applicable)
- [ ] DataViews integration tested (if applicable)
- [ ] Interactivity API uses `watch()` not `effect`
- [ ] Tested with iframed editor
- [ ] Collaboration fallback works (post locking)

## Quality Gates

- [ ] Plugin activates without errors
- [ ] All hooks working
- [ ] Admin interface functional
- [ ] Security measures implemented
- [ ] Tests passing
- [ ] Documentation complete
- [ ] WordPress 7.0 compatibility verified

## Related Workflow Bundles

- `wordpress` - WordPress development
- `wordpress-theme-development` - Theme development
- `wordpress-woocommerce` - WooCommerce

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## wordpress-theme-development
*WordPress theme development workflow covering theme architecture, template hierarchy, custom post types, block editor support, responsive design, and WordPress 7.0 features: DataViews, Pattern Editing, Navigation Overlays, and admin refresh.*

Risk: safe

# WordPress Theme Development Workflow

## Overview

Specialized workflow for creating custom WordPress themes from scratch, including modern block editor (Gutenberg) support, template hierarchy, responsive design, and WordPress 7.0 enhancements.

## WordPress 7.0 Theme Features

1. **Admin Refresh**
   - New default color scheme
   - View transitions between admin screens
   - Modern typography and spacing

2. **Pattern Editing**
   - ContentOnly mode defaults for unsynced patterns
   - `disableContentOnlyForUnsyncedPatterns` setting
   - Per-block instance custom CSS

3. **Navigation Overlays**
   - Customizable navigation overlays
   - Improved mobile navigation

4. **New Blocks**
   - Icon block
   - Breadcrumbs block with filters
   - Responsive grid block

5. **Theme.json Enhancements**
   - Pseudo-element support
   - Block-defined feature selectors honored
   - Enhanced custom CSS

6. **Iframed Editor**
   - Block API v3+ enables iframed post editor
   - Full enforcement in 7.1, opt-in in 7.0

## When to Use This Workflow

Use this workflow when:
- Creating custom WordPress themes
- Converting designs to WordPress themes
- Adding block editor support
- Implementing custom post types
- Building child themes
- Implementing WordPress 7.0 design features

## Workflow Phases

### Phase 1: Theme Setup

#### Skills to Invoke
- `app-builder` - Project scaffolding
- `frontend-developer` - Frontend development

#### Actions
1. Create theme directory structure
2. Set up style.css with theme header
3. Create functions.php
4. Configure theme support
5. Set up enqueue scripts/styles

#### WordPress 7.0 Theme Header
```css
/*
Theme Name: My Custom Theme
Theme URI: https://example.com
Author: Developer Name
Author URI: https://example.com
Description: A WordPress 7.0 compatible theme with modern design
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 7.4
License: GNU General Public License v2
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: my-custom-theme
Tags: block-patterns, block-styles, editor-style, wide-blocks
*/
```

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new WordPress theme project
```

### Phase 2: Template Hierarchy

#### Skills to Invoke
- `frontend-developer` - Template development

#### Actions
1. Create index.php (fallback template)
2. Implement header.php and footer.php
3. Create single.php for posts
4. Create page.php for pages
5. Add archive.php for archives
6. Implement search.php and 404.php

#### WordPress 7.0 Template Considerations
- Test with iframed editor
- Verify view transitions work
- Check new admin color scheme compatibility

#### Copy-Paste Prompts
```
Use @frontend-developer to create WordPress template files
```

### Phase 3: Theme Functions

#### Skills to Invoke
- `backend-dev-guidelines` - Backend patterns

#### Actions
1. Register navigation menus
2. Add theme support (thumbnails, RSS, etc.)
3. Register widget areas
4. Create custom template tags
5. Implement helper functions

#### WordPress 7.0 theme.json Configuration
```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "layout": {
      "contentSize": "1200px",
      "wideSize": "1400px"
    },
    "background": {
      "backgroundImage": true
    },
    "typography": {
      "fontFamilies": true,
      "fontSizes": true
    },
    "spacing": {
      "margin": true,
      "padding": true
    },
    "blocks": {
      "core/heading": {
        "typography": {
          "fontSizes": ["24px", "32px", "48px"]
        }
      }
    }
  },
  "styles": {
    "color": {
      "background": "#ffffff",
      "text": "#1a1a1a"
    },
    "elements": {
      "link": {
        "color": {
          "text": "#0066cc"
        }
      }
    }
  },
  "customTemplates": [
    {
      "name": "page-home",
      "title": "Homepage",
      "postTypes": ["page"]
    }
  ],
  "templateParts": [
    {
      "name": "header",
      "title": "Header",
      "area": "header"
    }
  ]
}
```

#### Copy-Paste Prompts
```
Use @backend-dev-guidelines to create theme functions
```

### Phase 4: Custom Post Types

#### Skills to Invoke
- `wordpress-penetration-testing` - WordPress patterns

#### Actions
1. Register custom post types
2. Create custom taxonomies
3. Add custom meta boxes
4. Implement custom fields
5. Create archive templates

#### RTC-Compatible CPT Registration
```php
register_post_type('portfolio', [
    'labels' => [
        'name' => __('Portfolio', 'my-theme'),
        'singular_name' => __('Portfolio Item', 'my-theme')
    ],
    'public' => true,
    'has_archive' => true,
    'show_in_rest' => true,  // Enable for RTC
    'supports' => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'],
    'menu_icon' => 'dashicons-portfolio',
]);

// Register meta for collaboration
register_post_meta('portfolio', 'client_name', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,
    'sanitize_callback' => 'sanitize_text_field',
]);
```

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to understand WordPress CPT patterns
```

### Phase 5: Block Editor Support

#### Skills to Invoke
- `frontend-developer` - Block development

#### Actions
1. Enable block editor support
2. Register custom blocks
3. Create block styles
4. Add block patterns
5. Configure block templates

#### WordPress 7.0 Block Features
- Block API v3 is reference model
- PHP-only block registration
- Per-instance custom CSS
- Block visibility controls (viewport-based)

#### Block Pattern with ContentOnly (WP 7.0)
```json
{
    "name": "my-theme/hero-section",
    "title": "Hero Section",
    "contentOnly": true,
    "content": [
        {
            "name": "core/cover",
            "attributes": {
                "url": "{{hero_image}}",
                "overlay": "black",
                "dimRatio": 50
            },
            "innerBlocks": [
                {
                    "name": "core/heading",
                    "attributes": {
                        "level": 1,
                        "textAlign": "center",
                        "content": "{{hero_title}}"
                    }
                },
                {
                    "name": "core/paragraph",
                    "attributes": {
                        "align": "center",
                        "content": "{{hero_description}}"
                    }
                }
            ]
        }
    ]
}
```

#### Navigation Overlay Template Part
```php
// template-parts/header-overlay.php
?>
<nav class="header-navigation-overlay" aria-label="<?php esc_attr_e('Overlay Menu', 'my-theme'); ?>">
    <button class="overlay-close" aria-label="<?php esc_attr_e('Close menu', 'my-theme'); ?>">
        <span class="close-icon" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </span>
    </button>
    <?php
    wp_nav_menu([
        'theme_location' => 'primary',
        'container' => false,
        'menu_class' => 'overlay-menu',
        'fallback_cb' => false,
    ]);
    ?>
</nav>
```

#### Copy-Paste Prompts
```
Use @frontend-developer to create custom Gutenberg blocks
```

### Phase 6: Styling and Design

#### Skills to Invoke
- `frontend-design` - UI design
- `tailwind-patterns` - Tailwind CSS

#### Actions
1. Implement responsive design
2. Add CSS framework or custom styles
3. Create design system
4. Implement theme customizer
5. Add accessibility features

#### WordPress 7.0 Admin Refresh Considerations
```css
/* Support new admin color scheme */
@media (prefers-color-scheme: dark) {
    :root {
        --admin-color: modern;
    }
}

/* View transitions */
.wp-admin {
    view-transition-name: none;
}

body {
    view-transition-name: page;
}
```

#### CSS Custom Properties (WP 7.0)
```css
:root {
    /* New DataViews colors */
    --wp-dataviews-color-background: #ffffff;
    --wp-dataviews-color-border: #e0e0e0;
    
    /* Navigation overlay */
    --wp-overlay-menu-background: #1a1a1a;
    --wp-overlay-menu-text: #ffffff;
}
```

#### Copy-Paste Prompts
```
Use @frontend-design to create responsive theme design
```

### Phase 7: WordPress 7.0 Features Integration

#### Breadcrumbs Block Support
```php
// Add breadcrumb filters for custom post types
add_filter('wp_breadcrumb_args', function($args) {
    $args['separator'] = '<span class="breadcrumb-separator"> / </span>';
    $args['before'] = '<nav class="breadcrumb" aria-label="Breadcrumb">';
    $args['after'] = '</nav>';
    return $args;
});

// Add custom breadcrumb trail for CPT
add_action('breadcrumb_items', function($trail, $crumbs) {
    if (is_singular('portfolio')) {
        $portfolio_page = get_page_by_path('portfolio');
        if ($portfolio_page) {
            array_splice($trail->crumbs, 1, 0, [
                [
                    'title' => get_the_title($portfolio_page),
                    'url' => get_permalink($portfolio_page)
                ]
            ]);
        }
    }
}, 10, 2);
```

#### Icon Block Support
```php
// Add custom icons for Icon block via pattern category
add_action('init', function() {
    register_block_pattern_category('my-theme/icons', [
        'label' => __('Theme Icons', 'my-theme'),
        'description' => __('Custom icons for use in the Icon block', 'my-theme'),
    ]);
});

// For actual SVG icons in the Icon block, use block.json or PHP registration
add_action('init', function() {
    register_block_pattern('my-theme/custom-icons', [
        'title' => __('Custom Icon Set', 'my-theme'),
        'categories' => ['my-theme/icons'],
        'content' => '<!-- Pattern content with Icon blocks -->'
    ]);
});
```

### Phase 8: Testing

#### Skills to Invoke
- `playwright-skill` - Browser testing
- `webapp-testing` - Web app testing

#### Actions
1. Test across browsers
2. Verify responsive breakpoints
3. Test block editor
4. Check accessibility
5. Performance testing

#### WordPress 7.0 Testing Checklist
- [ ] Test with iframed editor
- [ ] Verify view transitions
- [ ] Check admin color scheme
- [ ] Test navigation overlays
- [ ] Verify contentOnly patterns
- [ ] Test breadcrumbs on CPT archives

#### Copy-Paste Prompts
```
Use @playwright-skill to test WordPress theme
```

## Theme Structure

```
theme-name/
├── style.css
├── functions.php
├── index.php
├── header.php
├── footer.php
├── sidebar.php
├── single.php
├── page.php
├── archive.php
├── search.php
├── 404.php
├── comments.php
├── template-parts/
│   ├── header/
│   ├── footer/
│   ├── navigation/
│   └── content/
├── patterns/           # Block patterns (WP 7.0)
├── templates/          # Site editor templates
├── inc/
│   ├── class-theme.php
│   └── supports.php
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

## WordPress 7.0 Theme Checklist

- [ ] PHP 7.4+ requirement documented
- [ ] theme.json v3 schema used
- [ ] Block patterns tested
- [ ] ContentOnly editing supported
- [ ] Navigation overlays implemented
- [ ] Breadcrumb filters added for CPT
- [ ] View transitions working
- [ ] Admin refresh compatible
- [ ] CPT meta shows_in_rest
- [ ] Iframe editor tested

## Quality Gates

- [ ] All templates working
- [ ] Block editor supported
- [ ] Responsive design verified
- [ ] Accessibility checked
- [ ] Performance optimized
- [ ] Cross-browser tested
- [ ] WordPress 7.0 compatibility verified

## Related Workflow Bundles

- `wordpress` - WordPress development
- `wordpress-plugin-development` - Plugin development
- `wordpress-woocommerce` - WooCommerce

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

## wordpress-woocommerce-development
*WooCommerce store development workflow covering store setup, payment integration, shipping configuration, customization, and WordPress 7.0 features: AI connectors, DataViews, and collaboration tools.*

Risk: safe

# WordPress WooCommerce Development Workflow

## Overview

Specialized workflow for building WooCommerce stores including setup, payment gateway integration, shipping configuration, custom product types, store optimization, and WordPress 7.0 enhancements.

## WordPress 7.0 + WooCommerce Features

1. **AI Integration**
   - Auto-generate product descriptions
   - AI-powered customer service responses
   - Product summary generation
   - Marketing copy assistance

2. **DataViews for Orders**
   - Modern order management interfaces
   - Enhanced filtering and sorting
   - Activity layout for order history

3. **Real-Time Collaboration**
   - Collaborative order editing
   - Team notes and communication
   - Live inventory updates

4. **Admin Refresh**
   - Consistent WooCommerce admin styling
   - View transitions between screens

5. **Abilities API**
   - AI-powered order processing
   - Automated inventory management
   - Smart shipping recommendations

## When to Use This Workflow

Use this workflow when:
- Setting up WooCommerce stores
- Integrating payment gateways
- Configuring shipping methods
- Creating custom product types
- Building subscription products
- Implementing AI-powered features (WP 7.0)

## Workflow Phases

### Phase 1: Store Setup

#### Skills to Invoke
- `app-builder` - Project scaffolding
- `wordpress-penetration-testing` - WordPress patterns

#### Actions
1. Install WooCommerce
2. Run setup wizard
3. Configure store settings
4. Set up tax rules
5. Configure currency
6. Test with WordPress 7.0 admin

#### WordPress 7.0 + WooCommerce Setup
```php
// Minimum requirements for WP 7.0 + WooCommerce
// Add to wp-config.php for collaboration settings
define('WP_COLLABORATION_MAX_USERS', 10);

// AI features are enabled by installing a provider plugin
// Install OpenAI, Anthropic, or Gemini connector from WordPress.org
// Then configure via Settings > Connectors in admin panel
```

#### Copy-Paste Prompts
```
Use @app-builder to set up WooCommerce store
```

### Phase 2: Product Configuration

#### Skills to Invoke
- `wordpress-penetration-testing` - WooCommerce patterns

#### Actions
1. Create product categories
2. Add product attributes
3. Configure product types
4. Set up variable products
5. Add product images

#### AI-Powered Product Descriptions (WP 7.0)
```php
// Auto-generate product descriptions with AI
add_action('woocommerce_new_product', 'generate_ai_description', 10, 2);

function generate_ai_product_description($product_id, $product) {
    if ($product->get_description()) {
        return; // Skip if description exists
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    $title = $product->get_name();
    $short_description = $product->get_short_description();
    
    $prompt = sprintf(
        'Write a compelling WooCommerce product description for "%s" that highlights key features and benefits. Make it SEO-friendly and persuasive.',
        $title
    );
    
    if ($short_description) {
        $prompt .= "\n\nShort description: " . $short_description;
    }
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        return;
    }
    
    // Use temperature for consistent output
    $result->using_temperature(0.3);
    $description = $result->generate_text();
    
    if ($description && !is_wp_error($description)) {
        $product->set_description($description);
        $product->save();
    }
}
```

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to configure WooCommerce products
```

### Phase 3: Payment Integration

#### Skills to Invoke
- `payment-integration` - Payment processing
- `stripe-integration` - Stripe
- `paypal-integration` - PayPal

#### Actions
1. Choose payment gateways
2. Configure Stripe
3. Set up PayPal
4. Add offline payments
5. Test payment flows

#### WordPress 7.0 AI for Payments
```php
// AI-powered fraud detection
// Note: This is a demonstration - implement proper fraud detection with multiple signals

// Use AI to analyze order for fraud indicators
function ai_check_order_fraud($order_id) {
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return false; // Default to no suspicion if AI unavailable
    }
    
    $order = wc_get_order($order_id);
    if (!$order) {
        return false;
    }
    
    $prompt = sprintf(
        'Analyze this order for potential fraud. Order total: $%s. Shipping address: %s, %s. Billing: %s. Is this suspicious? Return only "suspicious" or "clean" without explanation.',
        $order->get_total(),
        $order->get_shipping_address_1(),
        $order->get_shipping_city(),
        $order->get_billing_email()
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        return false;
    }
    
    $result->using_temperature(0.1); // Low temp for consistent classification
    $analysis = $result->generate_text();
    
    return (strpos($analysis, 'suspicious') !== false);
}
```

#### Copy-Paste Prompts
```
Use @stripe-integration to integrate Stripe payments
```

```
Use @paypal-integration to integrate PayPal
```

### Phase 4: Shipping Configuration

#### Skills to Invoke
- `wordpress-penetration-testing` - WooCommerce shipping

#### Actions
1. Set up shipping zones
2. Configure shipping methods
3. Add flat rate shipping
4. Set up free shipping
5. Integrate carriers

#### AI Shipping Recommendations (WP 7.0)
```php
// AI-powered shipping recommendations
add_action('woocommerce_after_checkout_form', 'ai_shipping_recommendations');

function ai_shipping_recommendations($checkout) {
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    $cart = WC()->cart;
    if ($cart->is_empty() || !$cart->get_cart_contents_weight()) {
        return;
    }
    
    $prompt = sprintf(
        'Based on this cart (total weight: %d kg, destination: %s), recommend the best shipping method from: free shipping (orders over $100), flat rate ($9.99), or express ($24.99). Consider delivery time and cost efficiency. Respond with just the recommended method name.',
        $cart->get_cart_contents_weight(),
        WC()->customer->get_shipping_country()
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        return;
    }
    
    $result->using_temperature(0.1); // Low temp for consistent recommendation
    $recommendation = $result->generate_text();
    
    if (strpos($recommendation, 'express') !== false) {
        wc_add_notice(esc_html__('AI Recommendation: Consider Express shipping for faster delivery!', 'woocommerce'), 'info');
    }
}
```

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to configure shipping
```

### Phase 5: Store Customization

#### Skills to Invoke
- `frontend-developer` - Store customization
- `frontend-design` - Store design

#### Actions
1. Customize product pages
2. Modify cart page
3. Style checkout flow
4. Create custom templates
5. Add custom fields

#### WordPress 7.0 Template Customization
```php
// Custom product template with WP 7.0 blocks
add_action('woocommerce_after_main_content', 'add_product_ai_chat');

function add_product_ai_chat() {
    if (!is_product()) return;
    
    global $product;
    ?>
    <div class="product-ai-assistant">
        <h3>AI Shopping Assistant</h3>
        <button id="ai-chat-toggle" type="button">Ask about this product</button>
        <div id="ai-chat-panel" style="display:none;">
            <div id="ai-chat-messages"></div>
            <input type="text" id="ai-chat-input" placeholder="Ask about sizing, materials, etc.">
        </div>
    </div>
    <script>
    document.getElementById('ai-chat-toggle').addEventListener('click', function() {
        const panel = document.getElementById('ai-chat-panel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    </script>
    <?php
}

// AI-powered product Q&A
add_action('wp_ajax_ai_product_question', 'handle_ai_product_question');
add_action('wp_ajax_nopriv_ai_product_question', 'handle_ai_product_question');

function handle_ai_product_question() {
    // Verify nonce for security
    if (!check_ajax_referer('ai_product_question_nonce', 'nonce', false)) {
        wp_send_json_error(['message' => 'Security check failed']);
    }
    
    $question = isset($_POST['question']) ? sanitize_text_field($_POST['question']) : '';
    $product_id = isset($_POST['product_id']) ? intval($_POST['product_id']) : 0;
    
    if (empty($question) || empty($product_id)) {
        wp_send_json_error(['message' => 'Missing required fields']);
    }
    
    $product = wc_get_product($product_id);
    if (!$product) {
        wp_send_json_error(['message' => 'Product not found']);
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        wp_send_json_error(['message' => 'AI service unavailable']);
    }
    
    $prompt = sprintf(
        'Customer question about "%s": %s\n\nProduct details:
- Price: $%s
- SKU: %s
- Stock: %s

Answer helpfully, accurately, and concisely:',
        $product->get_name(),
        $question,
        $product->get_price(),
        $product->get_sku(),
        $product->get_stock_status()
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        wp_send_json_error(['message' => $result->get_error_message()]);
    }
    
    $result->using_temperature(0.4); // Slightly higher for more varied responses
    $answer = $result->generate_text();
    
    if (is_wp_error($answer)) {
        wp_send_json_error(['message' => 'Failed to generate response']);
    }
    
    wp_send_json_success(['answer' => $answer]);
}
```

#### Copy-Paste Prompts
```
Use @frontend-developer to customize WooCommerce templates
```

### Phase 6: Extensions

#### Skills to Invoke
- `wordpress-penetration-testing` - WooCommerce extensions

#### Actions
1. Install required extensions
2. Configure subscriptions
3. Set up bookings
4. Add memberships
5. Integrate marketplace

#### Abilities API for WooCommerce (WP 7.0)
```php
// Register ability categories first
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('ecommerce', [
        'label' => __('E-Commerce', 'woocommerce'),
        'description' => __('WooCommerce store management and operations', 'woocommerce'),
    ]);
});

// Register abilities
add_action('wp_abilities_api_init', function() {
    // Register ability to update inventory
    wp_register_ability('woocommerce/update-inventory', [
        'label' => __('Update Inventory', 'woocommerce'),
        'description' => __('Update product stock quantity', 'woocommerce'),
        'category' => 'ecommerce',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'product_id' => ['type' => 'integer', 'description' => 'Product ID to update'],
                'quantity' => ['type' => 'integer', 'description' => 'New stock quantity']
            ],
            'required' => ['product_id', 'quantity']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'success' => ['type' => 'boolean'],
                'new_quantity' => ['type' => 'integer']
            ]
        ],
        'execute_callback' => 'woocommerce_update_inventory_handler',
        'permission_callback' => function() {
            return current_user_can('manage_woocommerce');
        }
    ]);
    
    // Register ability to process orders
    wp_register_ability('woocommerce/process-order', [
        'label' => __('Process Order', 'woocommerce'),
        'description' => __('Mark order as processing and trigger fulfillment', 'woocommerce'),
        'category' => 'ecommerce',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'order_id' => ['type' => 'integer', 'description' => 'Order ID to process']
            ],
            'required' => ['order_id']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'success' => ['type' => 'boolean'],
                'status' => ['type' => 'string']
            ]
        ],
        'execute_callback' => 'woocommerce_process_order_handler',
        'permission_callback' => function() {
            return current_user_can('manage_woocommerce');
        }
    ]);
});

// Handler for inventory update
function woocommerce_update_inventory_handler($input) {
    $product_id = isset($input['product_id']) ? absint($input['product_id']) : 0;
    $quantity = isset($input['quantity']) ? absint($input['quantity']) : 0;
    
    $product = wc_get_product($product_id);
    if (!$product) {
        return new WP_Error('invalid_product', 'Product not found');
    }
    
    // Update stock
    wc_update_product_stock($product, $quantity);
    
    return [
        'success' => true,
        'new_quantity' => $product->get_stock_quantity()
    ];
}

// Handler for order processing
function woocommerce_process_order_handler($input) {
    $order_id = isset($input['order_id']) ? absint($input['order_id']) : 0;
    
    $order = wc_get_order($order_id);
    if (!$order) {
        return new WP_Error('invalid_order', 'Order not found');
    }
    
    $order->update_status('processing');
    
    return [
        'success' => true,
        'status' => 'processing'
    ];
}
```

#### Copy-Paste Prompts
```
Use @wordpress-penetration-testing to configure WooCommerce extensions
```

### Phase 7: Optimization

#### Skills to Invoke
- `web-performance-optimization` - Performance
- `database-optimizer` - Database optimization

#### Actions
1. Optimize product images
2. Enable caching
3. Optimize database
4. Configure CDN
5. Set up lazy loading

#### WordPress 7.0 Performance
- Client-side media processing
- Font Library enabled
- Responsive grid block
- View transitions for perceived performance

#### Copy-Paste Prompts
```
Use @web-performance-optimization to optimize WooCommerce store
```

### Phase 8: Testing

#### Skills to Invoke
- `playwright-skill` - E2E testing
- `test-automator` - Test automation

#### Actions
1. Test checkout flow
2. Verify payment processing
3. Test email notifications
4. Check mobile experience
5. Performance testing

#### WordPress 7.0 Testing
- Test with new admin interface
- Verify AI features work
- Test DataViews for orders
- Verify collaboration features

#### AI-Powered Store Testing
```php
// Automated AI testing for fraud detection during checkout
add_action('woocommerce_after_checkout_validation', 'ai_validate_order', 20);

function ai_validate_order($fields, $errors) {
    // Skip if AI is not available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    // Skip for logged-in users (assumed trusted)
    if (is_user_logged_in()) {
        return;
    }
    
    $order_data = [
        'email' => isset($fields['billing_email']) ? $fields['billing_email'] : '',
        'phone' => isset($fields['billing_phone']) ? $fields['billing_phone'] : '',
        'address' => isset($fields['billing_address_1']) ? $fields['billing_address_1'] : '',
    ];
    
    // Skip if insufficient data
    if (empty($order_data['email'])) {
        return;
    }
    
    $prompt = sprintf(
        'This is a checkout validation. Check if these details seem legitimate: email=%s, phone=%s, address=%s. Return only "valid" or "suspicious" without additional text.',
        sanitize_email($order_data['email']),
        sanitize_text_field($order_data['phone']),
        sanitize_text_field($order_data['address'])
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        // Don't block checkout on AI errors
        return;
    }
    
    $result->using_temperature(0.1); // Low temp for consistent classification
    $response = $result->generate_text();
    
    if (is_wp_error($response)) {
        return;
    }
    
    if (strpos($response, 'suspicious') !== false) {
        $errors->add('validation', __('Additional verification may be needed for this order. We will contact you if needed.', 'woocommerce'));
    }
}
```

#### Copy-Paste Prompts
```
Use @playwright-skill to test WooCommerce checkout flow
```

## WooCommerce + WordPress 7.0 AI Use Cases

1. **Product Descriptions**
   - Auto-generate from product attributes
   - Translate descriptions
   - SEO optimization

2. **Customer Service**
   - AI chatbot for common questions
   - Order status lookup
   - Return processing

3. **Inventory Management**
   - Demand forecasting
   - Low stock alerts
   - Reorder recommendations

4. **Marketing**
   - Personalized emails
   - Product recommendations
   - Abandoned cart recovery

5. **Order Processing**
   - Fraud detection
   - Shipping optimization
   - Invoice generation

## Quality Gates

- [ ] Products displaying correctly
- [ ] Checkout flow working
- [ ] Payments processing
- [ ] Shipping calculating
- [ ] Emails sending
- [ ] Mobile responsive
- [ ] AI features tested (WP 7.0)
- [ ] DataViews working (WP 7.0)

## Related Workflow Bundles

- `wordpress` - WordPress development
- `wordpress-theme-development` - Theme development
- `wordpress-plugin-development` - Plugin development
- `payment-integration` - Payment processing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---
