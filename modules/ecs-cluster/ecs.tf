# ecs.tf

resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-${var.environment}-cluster"
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

resource "aws_ecs_task_definition" "weatherbot-prod" {
  family                   = "${var.app_name}-${var.environment}-task"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"] 
  #network_mode             = "awsvpc"
  #requires_compatibilities = ["EC2"]
  cpu                      = var.fargate_cpu 
  memory                   = var.fargate_memory 
  container_definitions    = data.template_file.cb_weatherbot.rendered
}

resource "aws_ecs_service" "main" {
  name            = "${var.app_name}-${var.environment}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.weatherbot-prod.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"
  #launch_type     = "EC2"
  #instance_type = t3.nano

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.private_subnet.*.id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.weatherbot-prod.id
    container_name   = "${var.app_name}"
    container_port   = var.app_port
  }

  depends_on = [aws_alb_listener.listener, aws_iam_role_policy.ecs_task_execution_role]
}

