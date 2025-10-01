from core.gunicorn_.g_logger import GunicornLogger


def get_app_options(
    host: str, port: int, timeout: int, workers: int, log_level: str
) -> dict:
    return {
        "log_level": log_level,
        "accesslog": "-",
        "logger_class": GunicornLogger,
        "errorlog": "-",
        "bind": f"{host}:{port}",
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "timeout": timeout,
    }
