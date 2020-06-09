provider "aws" {
  region = var.region
}

terraform {
  backend "s3" {
    bucket = "wsbbot-api-terraform"
    region = "us-east-1"
    key    = "state"
  }
}