terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_path)

  project = var.project_id
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_storage_bucket" "tf_events_storage"{
  name = var.bucket_name
  location = "US"
  uniform_bucket_level_access = "true"
  public_access_prevention = "enforced"
  force_destroy = true
}

resource "google_pubsub_topic" "tf_event_stream" {
  name = var.stream_topic_name
}

resource "google_pubsub_subscription" "tf_event_stream-sub" {
  name  = "tf_event_stream-sub"
  topic = google_pubsub_topic.tf_event_stream.name

  ack_deadline_seconds = 10

}

# http function
resource "random_id" "bucket_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "bucket" {
  name                        = "${random_id.bucket_prefix.hex}-gcf-source"
  location                    = "US"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "object" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.bucket.name
  source = "./archived_functions/http_triggered_function.zip"
}

resource "google_cloudfunctions_function" "tf_http_triggered_function" {
  name        = "tf_http_triggered_function"
  region      = "us-central1"

  runtime     = "python39"
  entry_point = "http_triggered_function"
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.object.name

  max_instances = 1
  available_memory_mb   = 256
  timeout    = 60
  trigger_http = true

}

# store function
resource "random_id" "bucket2_prefix" {
  byte_length = 8
}

resource "google_storage_bucket" "bucket2" {
  name                        = "${random_id.bucket2_prefix.hex}-gcf-source"
  location                    = "US"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "object2" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.bucket2.name
  source = "./archived_functions/event_store_function.zip"
}

resource "google_cloudfunctions_function" "tf_event_store_function" {
  name        = "tf_event_store_function"
  region      = "us-central1"

  runtime     = "python39"
  entry_point = "hello_pubsub"
  source_archive_bucket = google_storage_bucket.bucket2.name
  source_archive_object = google_storage_bucket_object.object2.name

  max_instances = 1
  available_memory_mb   = 256
  timeout    = 60
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/tf_event_stream"
  }

}