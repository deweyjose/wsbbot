
resource "aws_security_group" "sg" {
  name   = "${var.application}-code-build-sg"
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = "${var.application}-code-build-sg"
    application = var.application
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = [
    "0.0.0.0/0"]
  }
}

resource "aws_iam_role" "role" {
  name = "${var.application}-code-build-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "cb_policy" {
  role = aws_iam_role.role.name

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetRepositoryPolicy",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
                "ecr:BatchGetImage",
                "ecr:GetLifecyclePolicy",
                "ecr:GetLifecyclePolicyPreview",
                "ecr:ListTagsForResource",
                "ecr:DescribeImageScanFindings",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Resource": [
                "arn:aws:logs:${var.region}:${var.account_id}:log-group:*"
            ],
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
        },
        {
            "Effect": "Allow",
            "Resource": [
                "${aws_s3_bucket.cp_bucket.arn}/*"
            ],
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "codebuild:CreateReportGroup",
                "codebuild:CreateReport",
                "codebuild:UpdateReport",
                "codebuild:BatchPutTestCases"
            ],
            "Resource": [
                "arn:aws:codebuild:${var.region}:${var.account_id}:report-group/wsbbot-api-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
              "ecs:DescribeTaskDefinition"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
              "ec2:CreateNetworkInterface",
              "ec2:DescribeDhcpOptions",
              "ec2:DescribeNetworkInterfaces",
              "ec2:DeleteNetworkInterface",
              "ec2:DescribeSubnets",
              "ec2:DescribeSecurityGroups",
              "ec2:DescribeVpcs"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
              "ec2:CreateNetworkInterfacePermission"
            ],
            "Resource": [
              "arn:aws:ec2:${var.region}:${var.account_id}:network-interface/*"
            ],
            "Condition": {
              "StringEquals": {
                "ec2:Subnet": ["${aws_subnet.a_priv.arn}"],
                "ec2:AuthorizedService": "codebuild.amazonaws.com"
              }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
              "rds:DescribeDBInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameter"
            ],
            "Resource": [
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_NAME",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_SERVER",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_PASSWORD",
                "arn:aws:ssm:${var.region}:${var.account_id}:parameter/DATABASE_USERNAME"
            ]
        }
    ]
}
POLICY
}

resource "aws_codebuild_project" "project" {
  name          = "${var.application}-project"
  build_timeout = "5"
  service_role  = aws_iam_role.role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:4.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true

    environment_variable {
      name  = "TASK_DEFINITION"
      value = "arn:aws:ecs:${var.region}:${var.account_id}:task-definition/${aws_ecs_task_definition.task.family}"
    }

    environment_variable {
      name  = "CONTAINER_NAME"
      value = "${var.application}-task-container"
    }

    environment_variable {
      name = "ACCOUNT_ID"
      value = var.account_id
    }

    environment_variable {
      name = "ECR_REGION"
      value = var.ecr_region
    }

    environment_variable {
      name = "APPLICATION"
      value = var.application
    }

    environment_variable {
      name = "DATABASE_NAME"
      value = replace(var.application, "-", "_")
    }
  }

  source {
    type            = "GITHUB"
    location        = var.github_url
    git_clone_depth = 1

    git_submodules_config {
      fetch_submodules = false
    }

    buildspec = "buildspec.yml"
  }

  source_version = var.github_branch

  vpc_config {
    vpc_id = aws_vpc.vpc.id

    subnets = [
    aws_subnet.a_priv.id]

    security_group_ids = [
    aws_security_group.sg.id]
  }

  logs_config {
    cloudwatch_logs {
      group_name = "${var.application}-code-build"
    }
  }

}

resource "aws_ecr_repository" "ecr" {
  name                 = var.application
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}