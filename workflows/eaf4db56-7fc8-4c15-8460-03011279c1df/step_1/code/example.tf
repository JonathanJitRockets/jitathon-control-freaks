resource "aws_s3_bucket" "foo-bucket" {
  region        = "us-east-1"
  bucket        = "example-bucket"
  force_destroy = true
  acl           = "public-read"
  #checkov:skip=CKV_AWS_20:The bucket is a public static content host
}