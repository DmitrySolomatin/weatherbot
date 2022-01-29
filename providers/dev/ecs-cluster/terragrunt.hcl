terraform {
  source = "../../../modules//ecs-cluster"
}

include {
  path = find_in_parent_folders()
}

dependency "ecr" {
    config_path = "../ecr"
    mock_outputs = {
      ecr_repository_url = "000000000000.dkr.ecr.eu-north-1.amazonaws.com/weatherbot"
  }
}

inputs = {
    ecr_repository_url = dependency.ecr.outputs.ecr_repository_url
  }
