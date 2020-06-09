data "aws_ssm_parameter" "DATABASE_USERNAME" {
  name = "DATABASE_USERNAME"
}

data "aws_ssm_parameter" "DATABASE_PASSWORD" {
  name = "DATABASE_PASSWORD"
}

resource "aws_security_group" "db" {
  vpc_id = aws_vpc.vpc.id
  tags   = { application = var.application }

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = list(aws_security_group.ecs.id, aws_security_group.sg.id)
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "db" {
  allocated_storage               = 20
  engine                          = "postgres"
  engine_version                  = "12.2"
  instance_class                  = "db.t2.micro"
  name                            = "${replace(var.application, "-", "_")}_db"
  storage_type                    = "gp2"
  username                        = data.aws_ssm_parameter.DATABASE_USERNAME.value
  password                        = data.aws_ssm_parameter.DATABASE_PASSWORD.value
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  vpc_security_group_ids          = list(aws_security_group.db.id)
  db_subnet_group_name            = aws_db_subnet_group.a.name
  skip_final_snapshot             = true
  tags                            = { application = var.application }
}

resource "aws_db_subnet_group" "a" {
  subnet_ids = list(aws_subnet.a_priv.id, aws_subnet.b_priv.id)
  tags       = { application = var.application }
}