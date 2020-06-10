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

github_url    = "https://github.com/deweyjose/wsbbot.git"
github_branch = "master"
github_owner  = "deweyjose"
github_repo   = "wsbbot"