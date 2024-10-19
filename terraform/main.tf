provider "aws" {
  region = "ap-southeast-2"

  default_tags {
    tags = {
      ServiceName = var.service_name
      CostCenter  = var.cost_center
    }
  }
}
