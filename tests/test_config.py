from app.config import settings


def test_app_name():
    assert settings.app_name == "DataPilot AI"


def test_default_environment():
    assert settings.app_env in {"development", "test"}


def test_max_file_size():
    assert settings.max_file_size_mb > 0


def test_max_file_size_bytes():
    expected = settings.max_file_size_mb * 1024 * 1024

    assert settings.max_file_size_bytes == expected