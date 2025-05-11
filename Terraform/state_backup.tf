terraform {
  backend "s3" {
    bucket = "terraform-backend-unirank"
    key    = "backend/terraform/state"
    region = "us-east-1"
    encrypt = true
    use_lockfile = true
  }
}
