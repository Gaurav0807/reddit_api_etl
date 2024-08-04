terraform {
  backend "s3" {
    bucket = "snowflake-integration-bucket-data"
    key = "terraform_state_backup/backend.tfstate"
    region = "us-east-1"
  }
}