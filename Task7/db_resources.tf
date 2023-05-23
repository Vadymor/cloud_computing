# SQL db
resource "google_sql_database_instance" "db_instance" {
  name             = "events-database"
  database_version = "MYSQL_8_0"
  settings {
    backup_configuration {
        enabled = True
    }
    tier = "db-f1-micro"
  }

  deletion_protection  = false
}

resource "google_sql_database" "database" {
  name     = "events_schema"
  instance = google_sql_database_instance.db_instance.name
}

resource "google_sql_user" "users" {
  name     = "admin"
  instance = google_sql_database_instance.db_instance.name
  password = "admin"
}

# db function
resource "random_id" "bucket3_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "bucket3" {
  name                        = "${random_id.bucket3_prefix.hex}-gcf-source"
  location                    = "US"
  uniform_bucket_level_access = true
}

data "archive_file" "tf_event_db_archive" {
  type       = "zip"
  source_dir = "${path.module}/event_db_function"
  output_path = "${path.module}/archived_functions/event_db_function.zip"
}

resource "google_storage_bucket_object" "object3" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.bucket3.name
  source = "${path.module}/archived_functions/event_db_function.zip"
}

resource "google_cloudfunctions_function" "tf_event_db_function" {
  name        = "tf_event_db_function"
  region      = var.region

  runtime     = "python39"
  entry_point = "hello_pubsub"
  source_archive_bucket = google_storage_bucket.bucket3.name
  source_archive_object = google_storage_bucket_object.object3.name

  https_trigger_security_level = "SECURE_ALWAYS"
  max_instances = 1
  available_memory_mb   = 256
  timeout    = 60
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${var.stream_topic_name}"
  }

  environment_variables = {
    INSTANCE_CONNECTION_NAME = "${var.project_id}:${var.region}:${google_sql_database_instance.db_instance.name}"
    DB_USER = google_sql_user.users.name
    DB_PASS = google_sql_user.users.password
    DB_NAME = google_sql_database.database.name
  }

}