# application loadbalancer.tf

resource "aws_alb" "main" {
  name            = "${var.app_name}-${var.environment}-lb"
  subnets         = aws_subnet.public_subnet.*.id
  security_groups = [aws_security_group.lb-sg.id]
}

# Application load balancer target group for page
resource "aws_alb_target_group" "page" {
  port = var.app_port
  protocol = "HTTP"
  vpc_id = aws_vpc.main.id
  

  health_check {
    healthy_threshold   = "3"
    interval            = "5"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }

  tags = {
    "Name" = "Page-${var.environment}-${var.app_name}"
  }
}

# Application load balancer target group for weatherbot
resource "aws_alb_target_group" "weatherbot" {
  port = var.app_port
  protocol = "HTTP"
  vpc_id = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "5"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }

  tags = {
    "Name" = "weatherbot-${var.environment}-${var.app_name}"
  }
}


# Traffic from the ALB to the target group
resource "aws_alb_listener" "http-listener" {
  load_balancer_arn = aws_alb.main.arn
  port              = var.app_port
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.page.arn
    type             = "forward"
  }
}


resource "aws_alb_listener" "https-listener" {
  load_balancer_arn = aws_alb.main.arn
  port = 443
  protocol = "HTTPS"

  default_action {
    target_group_arn = aws_alb_target_group.weatherbot.arn
    type = "forward"
  }
}
