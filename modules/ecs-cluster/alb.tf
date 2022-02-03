#application loadbalancer.tf

resource "aws_alb" "main" {
  name            = "${var.app_name}-${var.environment}-lb"
  subnets         = aws_subnet.public_subnet.*.id
  security_groups = [aws_security_group.lb-sg.id]
}

resource "aws_alb_target_group" "weatherbot-dev" {
  name        = "${var.app_name}-${var.environment}-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "2"
    path                = var.health_check_path
    unhealthy_threshold = "2"
  }
}

# Traffic from the ALB to the target group
resource "aws_alb_listener" "listener" {
  load_balancer_arn = aws_alb.main.id
  port              = var.app_port
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.weatherbot-dev.id
    type             = "forward"
  }
}

