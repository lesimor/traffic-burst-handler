from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="rushguard_"
    )  # .env 파일을 사용하여 설정을 로드하고, 환경 변수의 접두사를 "rushguard_"로 지정하는 설정 딕셔너리

    prometheus_url: str  # 프로메테우스 URL
    kube_context: str  # 쿠버네티스 컨텍스트
    kube_namespace: str  # 쿠버네티스 네임스페이스
    kube_deployment: str  # 쿠버네티스 디플로이먼트
    max_replicas: int  # 최대 레플리카 수
    ingress_name: str  # 인그레스 이름
    interval_unit: str  # 간격 단위
    response_time_threshold: float  # 응답 시간 임계값
    response_time_threshold_bandwidth_below: float  # 응답 시간 임계값 아래 대역폭
    default_pod_buffer: int = 1  # 기본 Pod 버퍼
    max_pod_buffer: int = 10  # 최대 Pod 버퍼
    capacity_per_pod: int = 5  # Pod 당 처리량
    max_pod_number_by_elapsed_time: int = 10  # 트래픽 급증 시점으로부터의 경과 시간으로 결정되는 최대 Pod 수
    buffer_exponential_decay_rate: float = 0.001  # 버퍼의 지수 감쇠율
