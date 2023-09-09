from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="rushguard_")

    prometheus_url: str
    kube_context: str
    kube_namespace: str
    kube_deployment: str
    max_replicas: int
    ingress_name: str
    interval_unit: str
    response_time_threshold: float


settings = Settings()
