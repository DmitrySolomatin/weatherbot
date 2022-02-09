# Repository for telegram bot
resource "aws_ecr_repository" "ecr_repository" {
  name = local.repository_name
}

# Repository for web-page
resource "aws_ecr_repository" "ecr_repository_page" {
  name = "${var.app_name}-${var.environment}-page"
}
