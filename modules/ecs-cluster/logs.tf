# logs.tf

# Set up CloudWatch group and log stream and retain logs for 30 days
resource "aws_cloudwatch_log_group" "cb_log_group_prod" {
  name              = "/ecs/cb-weatherbot-prod"
  retention_in_days = 30

  tags = {
    Name = "cb-log-group-prod"
  }
}

resource "aws_cloudwatch_log_stream" "cb_log_stream_prod" {
  name           = "${var.app_name}-${var.environment}-log-stream"
  log_group_name = aws_cloudwatch_log_group.cb_log_group_prod.name
}

