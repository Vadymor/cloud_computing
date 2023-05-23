# 7. Policies check

1. Scan FaaS project
````
ABSOLUTE_PATH_TO_PROJECT=/home/vadymor/PycharmProjects/cloud_computing/Task7
docker run --volume $ABSOLUTE_PATH_TO_PROJECT:/project bridgecrew/checkov:2.3.199 --quiet --compact --directory /project
````
2. The output:
````
Passed checks: 15, Failed checks: 18, Skipped checks: 0
````

3. I decided to fix this two failed checks:
````
Check: CKV_GCP_14: "Ensure all Cloud SQL database instance have backup configuration enabled"
        FAILED for resource: google_sql_database_instance.db_instance
        File: /db_resources.tf:2-10
        Guide: https://docs.bridgecrew.io/docs/bc_gcp_general_2
````
````
Check: CKV2_GCP_10: "Ensure GCP Cloud Function HTTP trigger is secured"
        FAILED for resource: google_cloudfunctions_function.tf_event_db_function
        File: /db_resources.tf:46-70
        Guide: https://docs.bridgecrew.io/docs/ensure-gcp-cloud-function-http-trigger-is-secured
````

4. I created [commit](https://github.com/Vadymor/cloud_computing/commit/d3206f5c7b86ae6459f60ff3b998bfda02178137) 
to fix them.

5. After that, I run checks again and got the output:
````
Passed checks: 17, Failed checks: 16, Skipped checks: 0
````
6. So, 2 failed checks is fixed :)
