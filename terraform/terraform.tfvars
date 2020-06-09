region           = "us-east-1"
ecr_region       = "us-east-1"
environment      = "production"
account_id       = 355804542548
application      = "wsbbot-api"
hosted_zone_name = "wsbbot.net"
environment_domain_map = {
  "staging" : "staging.api.wsbbot.net",
  "production" : "api.wsbbot.net"
}

cb_igw_id          = "igw-783cda03"
cb_vpc_id          = "vpc-b42b98ce"
cb_pub_cidr_block  = "172.31.96.0/20"
cb_priv_cidr_block = "172.31.112.0/20"
github_url         = "https://github.com/deweyjose/wsbbot.git"
github_branch      = "master"
github_owner       = "deweyjose"
github_repo        = "wsbbot"