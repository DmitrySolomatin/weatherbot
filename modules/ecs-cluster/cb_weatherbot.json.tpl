[
  {
    "name": "${app_name}",
    "image": "${app_image}",
    "cpu": ${fargate_cpu}, 
    "memory": ${fargate_memory}, 
    "networkMode": "awsvpc", 
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cb-weatherbot",
          "awslogs-region": "${aws_region}",
          "awslogs-stream-prefix": "ecs"
        }
    },
    "portMappings": [
      {
        "containerPort": ${app_port},
        "hostPort": ${app_port}
      }
    ],
    "environment": [
      {
        "name": "VERSION",
        "value": "${image_tag}"
      }
    ],
    "secrets": [
      {
        "name": "API_TOKEN",
        "valueFrom": "${aws_ssm_parameter.api_token.arn}"
      }
    ]
  }
]
