resource "aws_ssm_parameter" "api_token" {
  name        = "API TOKEN"
  description = "The parameter description"
  type        = "SecureString"
  value       = var.api_token
}
