# logs.tf

# Set up CloudWatch group and log stream and retain logs for 30 days
resource "aws_cloudwatch_log_group" "cb_log_group-dev" {
  name              = "/ecs/cb-weatherbot-dev"
  retention_in_days = 30

  tags = {
    Name = "cb-log-group-dev"
  }
}

resource "aws_cloudwatch_log_stream" "cb_log_stream-dev" {
  name           = "${var.app_name}-${var.environment}-log-stream"
  log_group_name = aws_cloudwatch_log_group.cb_log_group-dev.name
}
