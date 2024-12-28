module "rds_event_noti" {
  source = "../../"

  name           = "${local.realm.name}-event"
  db_cluster_ids = [module.rds.cluster_id]
  db_instance_ids = [
    for instance in module.rds.cluster_instances : instance.id
  ]
  slack_webhook = "<slack_webhook_url>"
}

#####################################################
# Supporting resources
#####################################################
module "rds" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "9.8.0"

  name = "example-cluster"

  engine         = "aurora-postgresql"
  engine_version = "16.3"

  instances = {
    provisioned = {
      instance_class = "db.t4g.large"
    }
    serverless = {
      instance_class = "db.serverless"
      promotion_tier = 5
    }
  }
  serverlessv2_scaling_configuration = {
    min_capacity = 0.5
    max_capacity = 1
  }

  master_username = "postgres"
  port            = 5432

  # omitting other parameters...
}
