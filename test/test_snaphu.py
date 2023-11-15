import os
import tempfile
from pathlib import Path

import pytest

from snaphu._snaphu import get_snaphu_executable, run_snaphu


def test_get_snaphu_executable():
    # Check that the file exists and is executable.
    with get_snaphu_executable() as snaphu_exe:
        assert Path(snaphu_exe).is_file()
        assert os.access(snaphu_exe, os.X_OK)


class TestRunSnaphu:
    def test_empty_config(self):
        # Test running SNAPHU with an empty config file.
        with tempfile.NamedTemporaryFile() as config_file:
            pattern = r"^not enough input arguments\.\s+type snaphu -h for help$"
            with pytest.raises(RuntimeError, match=pattern):
                run_snaphu(config_file.name)

    def test_missing_config(self):
        config_file = "/this/file/does/not/exist"
        assert not Path(config_file).is_file()

        # Should raise a `FileNotFoundError` if the config file did not exist.
        pattern = r"^config file not found"
        with pytest.raises(FileNotFoundError, match=pattern):
            run_snaphu(config_file)
