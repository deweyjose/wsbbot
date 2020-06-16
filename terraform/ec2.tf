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

  tags = {
    application = var.application
    Name        = "${var.application}-ecs-sg"
  }

  ingress {
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = list(aws_security_group.lb.id)
  }

  ingress {
    from_port       = 22
    protocol        = "tcp"
    to_port         = 22
    security_groups = list(aws_security_group.bastion.id)
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

data "aws_ami" "bastion" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.0.20200520.1-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}


resource "aws_security_group" "bastion" {
  name = "${var.application}-bastion-sg"

  vpc_id = aws_vpc.vpc.id
  tags = {
    application = var.application
    Name        = "${var.application}-bastion-sg"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_instance" "bastion" {
  instance_type   = "t2.micro"
  ami             = data.aws_ami.bastion.id
  subnet_id       = aws_subnet.a_pub.id
  security_groups = list(aws_security_group.bastion.id)
  key_name        = var.bastion_key_name

  tags = {
    Name        = "${var.application}-bastion"
    application = var.application
  }
}
