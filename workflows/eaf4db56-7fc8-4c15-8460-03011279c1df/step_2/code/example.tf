resource "aws_s3_bucket" "example_bucket" {
  region        = "us-west-1"
  bucket        = "my-example-bucket"
  acl           = "public-read"
  force_destroy = true
}