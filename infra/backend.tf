terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend-konfiguration för tillståndshantering
  backend "s3" {
    # bucket sätts av tofu init-kommandot eftersom den innehåller en variabel (denna tf-fil tillåter inte variabler i värden)
    key            = "app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "devops1-tfstate-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}
