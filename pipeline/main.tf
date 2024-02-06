
# Configure the AWS Provider
provider "aws" {
  region = "eu-west-2"
}

# Create a VPC
resource "aws_vpc" "c9-vpc" {
  id = "vpc-04423dbb18410aece"
}

data "aws_ecs_cluster" "c9-ecs-cluster" {
    cluster_name = "c9-ecs-cluster"
}

