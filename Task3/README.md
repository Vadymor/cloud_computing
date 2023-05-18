# 3. Terraform configuration for the project

To use this project you need to change 'credentials_path' and 'project_id' in [variables.tf](https://github.com/Vadymor/cloud_computing/blob/d335c9a4033aa0d16d5d3b4c880864799bd24f32/Task3/variables.tf)
to your` values.

This Terraform configuration is ready to use.

If you want to change 'bucket_name' in  [variables.tf](https://github.com/Vadymor/cloud_computing/blob/d335c9a4033aa0d16d5d3b4c880864799bd24f32/Task3/variables.tf)
you should change BUCKET_NAME variable in [event_store_function/main.py](https://github.com/Vadymor/cloud_computing/blob/d335c9a4033aa0d16d5d3b4c880864799bd24f32/Task3/event_store_function/main.py)
and vice versa

If you want to change 'stream_topic_name' or 'project_id' in [variables.tf](https://github.com/Vadymor/cloud_computing/blob/d335c9a4033aa0d16d5d3b4c880864799bd24f32/Task3/variables.tf)
you should change TOPIC_NAME or PROJECT_ID respectively in [http_triggered_function/main.py](https://github.com/Vadymor/cloud_computing/blob/d335c9a4033aa0d16d5d3b4c880864799bd24f32/Task3/http_triggered_function/main.py)
and vice versa

If you want to change the source code of Function you should recreate zip files, for this purpose here is [function_archivator.py](https://github.com/Vadymor/cloud_computing/blob/d335c9a4033aa0d16d5d3b4c880864799bd24f32/Task3/function_archivator.py)
You should do this because these zip files is uploaded to Cloud Functions.