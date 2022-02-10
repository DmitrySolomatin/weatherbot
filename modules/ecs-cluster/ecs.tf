# Main cluster
resource "aws_ecs_cluster" "main" {
  depends_on = [aws_autoscaling_group.autoscale]
  name = "Cluster-${var.environment}-${var.app_name}"
  capacity_providers = [aws_ecs_capacity_provider.capacity_provider.name]
}

data "template_file" "cb_weatherbot" {
  template = file(var.taskdef_template)

  vars = {
    app_image      = local.app_image
    app_port       = var.app_port
    fargate_cpu    = var.fargate_cpu 
    fargate_memory = var.fargate_memory 
    aws_region     = var.aws_region
    app_name       = var.app_name
    image_tag      = var.image_tag
  }
}

# Task definition for web page
resource "aws_ecs_task_definition" "task_def_page" {
  family = "task-page-${var.app_name}-${var.environment}"
  container_definitions    = data.template_file.cb_weatherbot.rendered
}

# Task definition for weatherbot 
resource "aws_ecs_task_definition" "task_def_weatherbot" {
  family = "task-bot-${var.app_name}-${var.environment}"
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn = aws_iam_role.ecs_task_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = var.fargate_cpu
  memory = var.fargate_memory
  container_definitions    = data.template_file.cb_weatherbot.rendered
}

# Service for web-page
resource "aws_ecs_service" "service_page" {
  capacity_provider_strategy {
  capacity_provider = aws_ecs_capacity_provider.capacity_provider.name
  weight = 1
  base = 0
}
  name = "Service-Page-${var.app_name}-${var.environment}"
  cluster = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.task_def_page.arn
  desired_count = 2
  deployment_minimum_healthy_percent = "90"
  
  load_balancer {
    target_group_arn = aws_alb_target_group.page.arn
    container_name = "page-${var.app_name}-${var.environment}"
    container_port = var.app_port
  }
}


# Service for weatherbot
resource "aws_ecs_service" "service_weatherbot" {
  name = "${var.app_name}-${var.environment}-bot"
  cluster = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.task_def_weatherbot.arn
  desired_count = 1
  launch_type = "FARGATE"
  
  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.private_subnet.*.id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.weatherbot.arn
    container_name = "weatherbot-${var.app_name}-${var.environment}"
    container_port = var.app_port
  }
}


# Capacity provider for web-page
resource "aws_ecs_capacity_provider" "capacity_provider" {
  name = "CP-${var.environment}-${var.app_name}"
  
  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.autoscale.arn
    managed_termination_protection = "DISABLED"

    managed_scaling {
      maximum_scaling_step_size = var.counter_for_az*2
      minimum_scaling_step_size = 2
      status                    = "ENABLED"
      target_capacity           = 100
      
    }
  }
}
