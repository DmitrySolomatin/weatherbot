locals {
  remote_state_bucket_prefix = "terra-weather"
  environment = "prod"
  app_name = "weatherbot"
  aws_profile = "default"
  aws_account = "978552764709"
  aws_region = "eu-north-1"
  image_tag = "latest"
  repo_url = "https://github.com/DmitrySolomatin/weatherbot.git"
  branch_pattern = "^refs/heads/main$"
  git_trigger_event = "PUSH"
  app_count = 1
}

inputs = {
  remote_state_bucket = format("%s-%s-%s-%s", local.remote_state_bucket_prefix, local.app_name, local.environment, local.aws_region)
  environment = local.environment
  app_name = local.app_name
  aws_profile = local.aws_profile
  aws_account = local.aws_account
  aws_region = local.aws_region
  image_tag = local.image_tag
  repo_url = local.repo_url
  github_personal_access_token = "GITHUB_TOKEN"
  branch_pattern = local.branch_pattern
  git_trigger_event = local.git_trigger_event
  app_count = local.app_count
}

remote_state {
  backend = "s3"

  config = {
    encrypt        = true
    bucket         = format("%s-%s-%s-%s", local.remote_state_bucket_prefix, local.app_name, local.environment, local.aws_region)
    key            = format("%s/terraform.tfstate", path_relative_to_include())
    region         = local.aws_region
    dynamodb_table = format("tflock-%s-%s-%s", local.environment, local.app_name, local.aws_region)
    profile        = local.aws_profile
  }
}

# Version Locking
## tfenv exists to help developer experience for those who use tfenv
## it will automatically download and use this terraform version
generate "tfenv" {
  path              = ".terraform-version"
  if_exists         = "overwrite"
  disable_signature = true

  contents = <<EOF
1.1.4
EOF
}

terraform_version_constraint = ">= 1.1.4"

terragrunt_version_constraint = ">= 0.36.0"

terraform {
  after_hook "remove_lock" {
    commands = [
      "apply",
      "console",
      "destroy",
      "import",
      "init",
      "plan",
      "push",
      "refresh",
    ]

    execute = [
      "rm",
      "-f",
      "${get_terragrunt_dir()}/.terraform.lock.hcl",
    ]

    run_on_error = true
  }
}
