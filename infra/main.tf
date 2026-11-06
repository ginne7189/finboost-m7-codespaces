# 검토용 예시. apply를 실행하지 않습니다. 계정/리전/비용 승인 미확정.
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}
provider "aws" { region = var.region }
variable "region" { type = string }
resource "aws_sqs_queue" "events" {
  name                      = "finboost-training-events"
  message_retention_seconds = 86400
  sqs_managed_sse_enabled    = true
  tags = { Purpose = "training-only" }
}
