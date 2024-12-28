output "sns_topic_arn" {
  value = try(aws_sns_topic.this[0].arn, null)
}
