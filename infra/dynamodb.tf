resource "aws_dynamodb_table" "posts" {
  count = var.deploy_enabled == "true" ? 1 : 0

  name           = "DevOps1_Posts"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}