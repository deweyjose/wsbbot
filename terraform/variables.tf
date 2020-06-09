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

variable "hosted_zone_name" {
  description = "Route53 hosted zone name"
}

# CODEBUILD...

variable "cb_igw_id" {
  default = "CODEBUILD. ID of the Internet gateway to use for public subnet."
}

variable "cb_vpc_id" {
  description = "CODEBUILD. ID of the VPC for subnets"
}

variable "cb_pub_cidr_block" {
  description = "CODEBUILD. CIDR block for public subnet"
}

variable "cb_priv_cidr_block" {
  description = "CODEBUILD. CIDR block for private subnet"
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

