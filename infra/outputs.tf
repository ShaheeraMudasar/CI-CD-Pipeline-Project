output "apprunner_service_url" {
  description = "The URL of the AppRunner service"
  value       = var.deploy_enabled == "true" ? aws_apprunner_service.app[0].service_url : null
}

output "ecr_repository_uri" {
  description = "The URI of the ECR repository"
  value       = data.aws_ecr_repository.app.repository_url
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table"
  value       = var.deploy_enabled == "true" ? aws_dynamodb_table.posts[0].name : null
}

output "apprunner_service_arn" {
  description = "The ARN of the AppRunner service"
  value       = var.deploy_enabled == "true" ? aws_apprunner_service.app[0].arn : null
}