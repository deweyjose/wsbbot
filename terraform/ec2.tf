## might make more sense to do this all in one ecs module/file
data "template_file" "user_data" {
  template = "${file("${path.module}/templates/user_data.sh")}"

  vars = {
    application = "${replace(var.application, "-", "_")}_ecs_cluster"
  }
}

data "aws_ami" "ecs" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }

  filter {
    name = "virtualization-type"
    values = [
    "hvm"]
  }

  owners = ["amazon"]
}

resource "aws_iam_instance_profile" "instance" {
  name = "${var.application}-instance-profile"
  role = aws_iam_role.instance.name
}

resource "aws_security_group" "ecs" {
  name   = "${var.application}-ecs-sg"
  vpc_id = aws_vpc.vpc.id
  tags   = { application = var.application }

  ingress {
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = ["${aws_security_group.lb.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_launch_configuration" "lc" {
  name_prefix   = "${var.application}-lc"
  image_id      = data.aws_ami.ecs.image_id
  instance_type = "t3a.small"
  spot_price    = "0.01"

  user_data            = data.template_file.user_data.rendered
  security_groups      = list(aws_security_group.ecs.id)
  iam_instance_profile = aws_iam_instance_profile.instance.name

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "grp" {
  name_prefix          = "${var.application}-auto-scale-group"
  launch_configuration = aws_launch_configuration.lc.name
  min_size             = 0
  max_size             = 2
  vpc_zone_identifier  = list(aws_subnet.a_priv.id, aws_subnet.b_priv.id)

  lifecycle {
    create_before_destroy = true
  }
}

