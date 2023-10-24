### Requirements

- Python 3.9+
- poetry 1.5.1

### Development Setup

1. local poetry environment (recommended)

```
poetry config virtualenvs.create true --local
poetry config virtualenvs.in-project true --local
poetry config virtualenvs.path .venv --local
```

2. Create `.env` file

```
RUSHGUARD_PROMETHEUS_URL="http://kaist-ingress-prometheus.dchain-connect.com"
RUSHGUARD_KUBE_CONTEXT="nks_kr_kaist-cluster_fe68cb8f-65ef-42a2-a3c4-deb608eacbce"
RUSHGUARD_KUBE_NAMESPACE="webeng"
RUSHGUARD_KUBE_DEPLOYMENT="php-apache"
RUSHGUARD_MAX_REPLICAS=10
RUSHGUARD_INGRESS_NAME=php-apache-ingress
RUSHGUARD_INTERVAL_UNIT="2m"
RUSHGUARD_RESPONSE_TIME_THRESHOLD=1.0
```

3. Install packages

```
poetry install
```

4. Install pre-commit

```
pre-commit install
```

5. Test

```
poetry run pytest
```

### python package build

```
poetry config repositories.dc http://docker-registry.com/repository/dchain-connect-pypi/
poetry config http-basic.dc <USERNAME> <PASSWORD>
poetry build
poetry publish -r dc
```

### Docker build

```
docker build --platform linux/amd64 -t rushguard-scaler .
docker tag rushguard-scaler docker-registry.com/rushguard-scaler:v0.0.1
docker push docker-registry.com/rushguard-scaler:v0.0.1
```
