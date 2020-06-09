resource "aws_iam_policy" "db" {
  name        = "${var.application}-ssm-policy"
  path        = "/"
  description = "Provides application and database settings in SSM"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameters"
            ],
            "Resource": [
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/APP_SETTINGS",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_NAME",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_SERVER",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_PASSWORD",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_USERNAME"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_policy" "task" {
  name        = "${var.application}-task-policy"
  path        = "/"
  description = "Provides access to other AWS service resources that are required to run Amazon ECS tasks"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_policy" "instance" {
  name        = "${var.application}-instance-policy"
  description = "Policy for the Amazon EC2 Role for Amazon EC2 Container Service."
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeTags",
                "ecs:CreateCluster",
                "ecs:DeregisterContainerInstance",
                "ecs:DiscoverPollEndpoint",
                "ecs:Poll",
                "ecs:RegisterContainerInstance",
                "ecs:StartTelemetrySession",
                "ecs:UpdateContainerInstancesState",
                "ecs:Submit*",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:DescribeLogStreams"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

data template_file "assume_ec2" {
  template = file("${path.module}/templates/assume-role.tf.json")

  vars = {
    service = "ec2.amazonaws.com"
  }
}
data template_file "assume_ecs" {
  template = file("${path.module}/templates/assume-role.tf.json")

  vars = {
    service = "ecs-tasks.amazonaws.com"
  }
}

resource "aws_iam_role" "instance" {
  name               = "${var.application}-instance-role"
  assume_role_policy = data.template_file.assume_ec2.rendered
  tags               = { application = var.application }
}

resource "aws_iam_role" "task" {
  name               = "${var.application}-task-role"
  assume_role_policy = data.template_file.assume_ecs.rendered
  tags               = { application = var.application }
}

resource "aws_iam_role_policy_attachment" "instance" {
  role       = aws_iam_role.instance.name
  policy_arn = aws_iam_policy.instance.arn
}

locals {
  policies = list(
    aws_iam_policy.task.arn,
    aws_iam_policy.db.arn
  )
}

resource "aws_iam_role_policy_attachment" "task" {
  count      = length(local.policies)
  role       = aws_iam_role.task.name
  policy_arn = local.policies[count.index]
}
