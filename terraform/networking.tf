resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name        = "${var.application}-vpc"
    application = var.application
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = "${var.application}-igw"
    application = var.application
  }
}

resource "aws_subnet" "a_priv" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.0.0/20"
  availability_zone = "${var.region}a"
  tags = {
    Name        = "${var.application}-priv-sn-a"
    application = var.application
  }
}

resource "aws_subnet" "b_priv" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.16.0/20"
  availability_zone = "${var.region}b"
  tags = {
    Name        = "${var.application}-priv-sn-b"
    application = var.application
  }
}

resource "aws_subnet" "a_pub" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.32.0/20"
  availability_zone = "${var.region}a"
  tags = {
    Name        = "${var.application}-pub-sn-a"
    application = var.application
  }
}

resource "aws_subnet" "b_pub" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.64.0/20"
  availability_zone = "${var.region}b"
  tags = {
    Name        = "${var.application}-pub-sn-b"
    application = var.application
  }
}

resource "aws_eip" "a" {
  vpc = true
  tags = {
    Name        = "${var.application}-ip-ngw-a"
    application = var.application
  }
}

resource "aws_nat_gateway" "a" {
  allocation_id = aws_eip.a.id
  subnet_id     = aws_subnet.a_pub.id
  depends_on    = [aws_internet_gateway.igw]
  tags = {
    Name        = "${var.application}-nat-gw-a"
    application = var.application
  }
}

resource "aws_eip" "b" {
  vpc = true
  tags = {
    Name        = "${var.application}-ip-ngw-b"
    application = var.application
  }
}

resource "aws_nat_gateway" "b" {
  allocation_id = aws_eip.b.id
  subnet_id     = aws_subnet.b_pub.id
  depends_on    = [aws_internet_gateway.igw]
  tags = {
    Name        = "${var.application}-nat-gw-b"
    application = var.application
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name        = "${var.application}-route-pub"
    application = var.application
  }
}

resource "aws_route_table_association" "apub" {
  subnet_id      = aws_subnet.a_pub.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "bpub" {
  subnet_id      = aws_subnet.b_pub.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "a_priv" {
  vpc_id = aws_vpc.vpc.id

  route {
    nat_gateway_id = aws_nat_gateway.a.id
    cidr_block     = "0.0.0.0/0"
  }

  tags = {
    Name        = "${var.application}-route-priv-a"
    application = var.application
  }
}

resource "aws_route_table" "b_priv" {
  vpc_id = aws_vpc.vpc.id

  route {
    nat_gateway_id = aws_nat_gateway.b.id
    cidr_block     = "0.0.0.0/0"
  }

  tags = {
    Name        = "${var.application}-route-priv-b"
    application = var.application
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.a_priv.id
  route_table_id = aws_route_table.a_priv.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.b_priv.id
  route_table_id = aws_route_table.b_priv.id
}

resource "aws_security_group" "lb" {
  name = "${var.application}-sg-lb"

  vpc_id = aws_vpc.vpc.id
  tags   = { application = var.application }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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

resource "aws_acm_certificate" "cert" {
  domain_name       = lookup(var.environment_domain_map, var.environment)
  validation_method = "DNS"

  tags = {
    Name        = "${var.application}-cert"
    application = var.application
  }

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_route53_zone" "zone" {
  name         = var.hosted_zone_name
  private_zone = false
}

resource "aws_route53_record" "cert_validation" {
  name    = aws_acm_certificate.cert.domain_validation_options.0.resource_record_name
  type    = aws_acm_certificate.cert.domain_validation_options.0.resource_record_type
  zone_id = data.aws_route53_zone.zone.zone_id
  records = [aws_acm_certificate.cert.domain_validation_options.0.resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [aws_route53_record.cert_validation.fqdn]
}

resource "aws_lb" "lb" {
  name               = "${var.application}-lb"
  security_groups    = list(aws_security_group.lb.id)
  subnets            = list(aws_subnet.a_pub.id, aws_subnet.b_pub.id)
  internal           = false
  load_balancer_type = "application"
  tags               = { application = var.application }
}

resource "aws_lb_listener" "lb_listen" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate_validation.cert.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.blue.arn
  }
}

resource "aws_lb_target_group" "blue" {
  name       = "${var.application}-lb-tg-blue"
  port       = 5000
  protocol   = "HTTP"
  vpc_id     = aws_vpc.vpc.id
  depends_on = [aws_lb.lb]
  tags       = { application = var.application }

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    port                = "5000"
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_lb_target_group" "green" {
  name       = "${var.application}-lb-tg-green"
  port       = 5000
  protocol   = "HTTP"
  vpc_id     = aws_vpc.vpc.id
  depends_on = [aws_lb.lb]
  tags       = { application = var.application }
  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    port                = "5000"
    matcher             = "200"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.zone.id
  name    = aws_acm_certificate.cert.domain_name
  type    = "CNAME"
  ttl     = "300"
  records = [aws_lb.lb.dns_name]
}

#################################################

data "aws_internet_gateway" "cb_igw" {
  internet_gateway_id = var.cb_igw_id
}

data "aws_vpc" "vpc" {
  id = var.cb_vpc_id
}

resource "aws_subnet" "cb_public" {
  vpc_id            = data.aws_vpc.vpc.id
  cidr_block        = var.cb_pub_cidr_block
  availability_zone = "${var.region}a"
  tags = {
    Name        = "${var.application}-build-public"
    application = var.application
  }
}

resource "aws_subnet" "cb_private" {
  vpc_id            = data.aws_vpc.vpc.id
  cidr_block        = var.cb_priv_cidr_block
  availability_zone = "${var.region}a"
  tags = {
    Name        = "${var.application}-build-private"
    application = var.application
  }
}

resource "aws_eip" "cb_ip" {
  vpc = true
  tags = {
    Name        = "${var.application}-ngw-ip"
    application = var.application
  }
}

resource "aws_nat_gateway" "cb_ngw" {
  allocation_id = aws_eip.cb_ip.id
  subnet_id     = aws_subnet.cb_public.id
  tags = {
    Name        = "${var.application}-code-build-ngw"
    application = var.application
  }
}

resource "aws_route_table" "cb_public" {
  vpc_id = data.aws_vpc.vpc.id
  tags = {
    Name        = "${var.application}-ngw-public-rt"
    application = var.application
  }
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = data.aws_internet_gateway.cb_igw.id
  }
}

resource "aws_route_table_association" "cb_pub" {
  subnet_id      = aws_subnet.cb_public.id
  route_table_id = aws_route_table.cb_public.id
}

resource "aws_route_table" "cb_private" {
  vpc_id = data.aws_vpc.vpc.id
  tags = {
    Name        = "${var.application}-ngw-private-rt"
    application = var.application
  }
  route {
    nat_gateway_id = aws_nat_gateway.cb_ngw.id
    cidr_block     = "0.0.0.0/0"
  }
}

resource "aws_route_table_association" "cb_private" {
  subnet_id      = aws_subnet.cb_private.id
  route_table_id = aws_route_table.cb_private.id
}