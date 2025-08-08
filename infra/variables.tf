variable "deploy_enabled" {
  description = "Enable terraform deployment of infrastructure resources"
  type        = string
  default     = "false"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "feature_ddb" {
  description = "Enable DynamoDB feature (false means mocked)"
  type        = string
  default     = "false"
}

variable "feature_admin" {
  description = "Enable admin feature"
  type        = string
  default     = "false"
}

variable "admin_password" {
  description = "Admin password for the application"
  type        = string
  sensitive   = true
}

variable "image_tag" {
  # DENNA VARIABEL SÄTTS av "Set image metadata" i .github/workflows/deploy-to-dev.yml
  description = "Docker image tag (commit SHA)"
  type        = string
}
