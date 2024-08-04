output "policy_name" {
  value = "Policy Name : ${aws_iam_policy.s3_policy_snowflake.name}, Role : ${aws_iam_role.s3_role.name}" 
}