resource "aws_db_event_subscription" "db_cluster" {
  count = var.create && length(var.db_cluster_ids) > 0 ? 1 : 0

  name             = "${var.name}-cluster"
  source_type      = "db-cluster"
  source_ids       = var.db_cluster_ids
  event_categories = var.db_cluster_event_categories
  sns_topic        = aws_sns_topic.this[0].arn

  tags = merge(
    { "Name" : var.name },
    var.tags
  )
}

resource "aws_db_event_subscription" "instances" {
  count = var.create && length(var.db_instance_ids) > 0 ? 1 : 0

  name             = "${var.name}-instances"
  source_type      = "db-instance"
  source_ids       = var.db_instance_ids
  event_categories = var.db_instance_event_categories
  sns_topic        = aws_sns_topic.this[0].arn

  tags = merge(
    { "Name" : var.name },
    var.tags
  )
}

resource "aws_sns_topic" "this" {
  count = var.create ? 1 : 0

  name = var.name

  tags = merge(
    { "Name" : var.name },
    var.tags
  )
}

#####################
## Lambda function ##
#####################
resource "aws_sns_topic_subscription" "slack_notifier_function" {
  count = var.create ? 1 : 0

  topic_arn = aws_sns_topic.this[0].arn
  protocol  = "lambda"
  endpoint  = module.slack_notifier_function[0].lambda_function_arn
}

module "slack_notifier_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.7.1"

  count = var.create ? 1 : 0

  function_name = "${var.name}-slack-notifier"
  description   = "Slack notifier function for RDS event"

  source_path   = "${path.module}/assets/lambda-functions/slack-notifier"
  handler       = "index.lambda_handler"
  runtime       = "python3.12"
  architectures = ["arm64"]
  timeout       = 15

  environment_variables = {
    SLACK_WEBHOOK = base64encode(var.slack_webhook)
  }

  allowed_triggers = {
    sns = {
      principal  = "sns.amazonaws.com"
      source_arn = aws_sns_topic.this[0].arn
    }
  }
  create_current_version_allowed_triggers = false

  cloudwatch_logs_retention_in_days = 30

  tags = merge({
    Name = "${var.name}-slack-notifier"
  }, var.tags)
}
