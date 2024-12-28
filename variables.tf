variable "create" {
  type        = bool
  default     = true
  description = "wheter or not to create resources"
}

variable "name" {
  description = "Name to apply for created resources"
  type        = string
}

variable "db_cluster_ids" {
  description = "List of RDS cluster instances to monitor"
  type        = list(string)
  default     = []
}

variable "db_cluster_event_categories" {
  description = "List of event categories for RDS cluster instances"
  type        = list(string)
  default     = ["configuration change", "failover", "failure", "maintenance"]
}

variable "db_instance_ids" {
  description = "List of RDS instances to monitor"
  type        = list(string)
  default     = []
}

variable "db_instance_event_categories" {
  description = "List of event categories for RDS instances"
  type        = list(string)
  default     = ["availability", "configuration change", "failover", "failure", "low storage", "maintenance"]
}

variable "slack_webhook" {
  type        = string
  description = "Slack webhook URL"
}

variable "tags" {
  type    = map(string)
  default = {}
}
