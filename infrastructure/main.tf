terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.57.0"
    }
  }
}

provider "aws" {
  region = var.aws_region_name
}

resource "aws_iam_policy" "s3_policy_snowflake" {
    name = "snowflake_s3_policy"
    description = "Iam Policy to access s3 bucket"
    policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
        {
        "Effect": "Allow",
        "Action": [
          #"s3:PutObject",
          "s3:GetObject",
          "s3:GetObjectVersion"
         # "s3:DeleteObject",
          #"s3:DeleteObjectVersion"
        ],
        "Resource": "arn:aws:s3:::snowflake-integration-bucket-data/*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ],
        "Resource": "arn:aws:s3:::snowflake-integration-bucket-data",
        "Condition": {
          "StringLike": {
            "s3:prefix": [
              "*"
            ]
          }
        }
      }
    ]
    })
}


resource "aws_iam_role" "s3_role" {
  name = "SnowflakeIntegrationS3Role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": ""
        },
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "sts:ExternalId": ""
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_role_policy_attachment" {
  role       = aws_iam_role.s3_role.name
  policy_arn = aws_iam_policy.s3_policy_snowflake.arn
}
