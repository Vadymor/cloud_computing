# 6. Haunting CVEs

1. Pull docker image of `ghcr.io/mlflow/mlflow:v2.3.0`.
2. Install grype with command: 
````
sudo curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
````
3. Scan with grype command
````
grype docker:ghcr.io/mlflow/mlflow:v2.3.0 --only-fixed
````
However, it doesn't filter output: 
![](./img/grype_doesnt_work.png)

So, I created python [script]() that parse command output and show filtered scan results:







![](./img/schema.png)

 jyt [http_triggered_function](https://github.com/Vadymor/cloud_computing/blob/6f9705db4e442379fe97f6bd5c5f67078421d84f/Task2/http_triggered_function).
    




docker pull ghcr.io/mlflow/mlflow:v2.3.0

docker pull aquasec/trivy:0.41.0


docker run --rm -v ~/.trivy:/root/.cache/ aquasec/trivy:0.41.0 image --severity HIGH,CRITICAL --ignore-unfixed ghcr.io/mlflow/mlflow:v2.3.0






Doesn't work
grype docker:ghcr.io/mlflow/mlflow:v2.3.0 --only-fixed

Custom script
