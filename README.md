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

2. Install packages

```
poetry install
```

3. Install pre-commit

```
pre-commit install
```

4. Test

```
poetry run pytest
```

### CI/CD setup

1. docker-registry 접속 계정을 SECRETS로 등록 (docker-registry.com)

2. [WIP] ArgoCD 설정
