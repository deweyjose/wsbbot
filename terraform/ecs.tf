resource "aws_ecs_capacity_provider" "cp" {
  name = aws_autoscaling_group.grp.name

  depends_on = [aws_autoscaling_group.grp]

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.grp.arn
    managed_termination_protection = "DISABLED"

    managed_scaling {
      maximum_scaling_step_size = 1000
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 10
    }
  }
}

resource "aws_ecs_cluster" "cluster" {
  name               = "${replace(var.application, "-", "_")}_ecs_cluster"
  capacity_providers = list(aws_ecs_capacity_provider.cp.name)
  tags               = { application = var.application }
}

data "template_file" "container_definition" {
  template = "${file("${path.module}/templates/service.tf.json")}"

  vars = {
    log_group       = "/ecs/${var.application}"
    region          = "${var.region}"
    image           = "${var.account_id}.dkr.ecr.${var.ecr_region}.amazonaws.com/${var.application}:latest"
    name            = "${var.application}-task-container"
    DATABASE_NAME   = aws_db_instance.db.name
    DATABASE_SERVER = aws_db_instance.db.endpoint
    DATABASE_PORT   = aws_db_instance.db.port
  }
}

resource "aws_ecs_task_definition" "task" {
  family                = var.application
  tags                  = { application = var.application }
  cpu                   = "512"
  memory                = "256"
  container_definitions = data.template_file.container_definition.rendered
  execution_role_arn    = aws_iam_role.task.arn
}

resource "aws_ecs_service" "wsbbot" {
  name            = "${var.application}-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 1

  load_balancer {
    target_group_arn = aws_lb_target_group.blue.arn
    container_name   = "${var.application}-task-container"
    container_port   = 5000
  }

  deployment_controller {
    type = "CODE_DEPLOY"
  }
}

resource "aws_cloudwatch_log_group" "task" {
  name = "/ecs/${var.application}"
  tags = { application = var.application }
}

