import os
import time
from prometheus_client import Gauge, start_http_server

# Создаём метрику типа Gauge (текущее значение, может расти и падать)
f1_gauge = Gauge(
    "model_f1_score",
    "F1 score of the diabetes model",
    ["dataset", "gender"],
)


def get_f1_values():
    # По умолчанию берём значения из запуска
    f1_ref = float(os.getenv("F1_REFERENCE", "0.615"))
    f1_curr = float(os.getenv("F1_CURRENT", "0.45"))  # < 0.55, чтобы алерт сработал
    # f1_curr = float(os.getenv("F1_CURRENT", "0.56"))
    return f1_ref, f1_curr


if __name__ == "__main__":
    start_http_server(8000)
    print("Экспортер запущен: http://localhost:8000/metrics")
    while True:
        f1_ref, f1_curr = get_f1_values()
        f1_gauge.labels(dataset="reference", gender="all").set(f1_ref)
        f1_gauge.labels(dataset="current", gender="all").set(f1_curr)
        time.sleep(5)
