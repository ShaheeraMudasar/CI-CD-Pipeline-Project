# ECR Repository (skapad av bootstrap workflow)
data "aws_ecr_repository" "app" {
  name = "devops1-blog-app"
}

# Auto Scaling-konfiguration för kostnadskontroll och DOS-skydd
resource "aws_apprunner_auto_scaling_configuration_version" "app" {
  count = var.deploy_enabled == "true" ? 1 : 0

  auto_scaling_configuration_name = "devops1-blog-app-scaling"

  max_concurrency = 100 # Samtidiga förfrågningar per instans innan skalning
  max_size        = 2   # Maximalt 2 instanser för driftsättning utan nertid
  min_size        = 1   # Håll alltid 1 instans igång
}

# AppRunner-tjänst
resource "aws_apprunner_service" "app" {
  count        = var.deploy_enabled == "true" ? 1 : 0
  service_name = "devops1-blog-app"

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.app[0].arn

  source_configuration {
    authentication_configuration {
      access_role_arn = "arn:aws:iam::${var.aws_account_id}:role/Student-AppRunnerECRAccess"
    }
    image_repository {
      image_configuration {
        port = "8000"

        runtime_environment_variables = {
          FEATURE_DDB    = var.feature_ddb
          FEATURE_ADMIN  = var.feature_admin
          ADMIN_PASSWORD = var.admin_password
          AWS_REGION     = var.aws_region
        }
      }

      image_identifier      = "${data.aws_ecr_repository.app.repository_url}:${var.image_tag}"
      image_repository_type = "ECR"
    }

    # Inaktivera auto-driftsättningar då vi sätter en specifik image att driftsätta (image_identifier)
    auto_deployments_enabled = false
  }

  instance_configuration {
    cpu               = "256" # 0.25 vCPU i CPU-enheter
    memory            = "512" # 0.5 GB i MB
    instance_role_arn = "arn:aws:iam::${var.aws_account_id}:role/Student-AppRunnerLimitedExecution"
  }

  health_check_configuration {
    healthy_threshold   = 1
    interval            = 10
    path                = "/api/v1/health"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 5
  }
}
