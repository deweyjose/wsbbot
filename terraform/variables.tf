variable "region" {
  description = "The deploy region"
}

variable "ecr_region" {
  description = "The region hosting ECR images"
}

variable "environment" {
  description = "The deploy environment: {staging|production}"
}

variable "account_id" {
  description = "AWS account id"
}

variable "application" {
  description = "Tag for each resource to be searchable"
}

variable "environment_domain_map" {
  type = map
}

variable "bastion_key_name" {
  description = "Name of key-pair for bastion host access"
}

variable "hosted_zone_name" {
  description = "Route53 hosted zone name"
}

variable "github_url" {
  description = "CODEBUILD. URL to Github repo"
}

variable "github_owner" {
  description = "owner of the github repo"
}

variable "github_repo" {
  description = "repo to build"
}

variable "github_branch" {
  description = "CODEBUILD. Branch to build"
}

