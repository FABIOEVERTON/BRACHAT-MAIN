# EZRA — infra AWS staging (PRD §6.2 reduzido para FASE 0, E0-S10)
# F0-43: services web + shared com healthcheck. Região sa-east-1 (F0-40).
# Segredos via variáveis (plan → apply), nunca hardcoded (F0-44).

variable "env" {
  type    = string
  default = "staging"
}

variable "image_web" {
  type = string
}

variable "image_shared" {
  type = string
}

variable "jwt_secret" {
  type      = string
  sensitive = true
}

provider "aws" {
  region = "sa-east-1"
}

# --- VPC isolada (PRD §6.2) ---
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "ezra-${var.env}-vpc", Platform = "ezra" }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = "sa-east-1${count.index == 0 ? "a" : "b"}"
  tags              = { Name = "ezra-${var.env}-private-${count.index}" }
}

# --- ECR (imagens) ---
resource "aws_ecr_repository" "web" {
  name = "ezra-${var.env}/web"
  tags = { Platform = "ezra" }
}

resource "aws_ecr_repository" "shared" {
  name = "ezra-${var.env}/shared"
  tags = { Platform = "ezra" }
}

# --- ECS Fargate (PRD §6.2: serviço por app) ---
resource "aws_ecs_cluster" "main" {
  name = "ezra-${var.env}-cluster"
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name       = aws_ecs_cluster.main.name
  capacity_providers = ["FARGATE"]
}

resource "aws_ecs_service" "web" {
  name            = "web"
  cluster         = aws_ecs_cluster.main.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.web.arn
  desired_count   = 1
}

resource "aws_ecs_task_definition" "web" {
  family                   = "ezra-${var.env}-web"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  container_definitions = jsonencode([
    {
      name      = "web"
      image     = var.image_web
      essential = true
      portMappings = [{ containerPort = 3000, hostPort = 3000 }]
      environment = [
        { name = "JWT_SECRET", value = var.jwt_secret }
      ]
      healthCheck = {
        command     = ["CMD", "node", "-e", "fetch('http://127.0.0.1:3000/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 30
      }
    }
  ])
}

# --- S3 WORM (PRD §3.5) — Object Lock COMPLIANCE, retenção 10 anos ---
resource "aws_s3_bucket" "worm" {
  bucket        = "ezra-worm-vault-${var.env}"
  force_destroy = false # NUNCA destruir cofre WORM (regra legal)
  tags          = { Platform = "ezra", Immutable = "true" }
}

resource "aws_s3_bucket_versioning" "worm" {
  bucket = aws_s3_bucket.worm.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_object_lock_configuration" "worm" {
  bucket = aws_s3_bucket.worm.id
  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = 3650
    }
  }
}

# --- SQS (motor de jobs, PRD §9.2) ---
resource "aws_sqs_queue" "jobs" {
  name                      = "ezra-${var.env}-jobs"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  tags = { Platform = "ezra" }
}

output "healthcheck_url" {
  value = "https://${var.env}.ezra.com.br/api/health"
}