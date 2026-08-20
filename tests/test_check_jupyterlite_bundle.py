import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class JupyterLiteBundleTests(unittest.TestCase):
    def test_requires_xeus_kernel_and_declared_scientific_packages(self):
        from scripts.check_jupyterlite_bundle import required_bundle_files, validate_bundle

        with TemporaryDirectory() as temporary:
            bundle = Path(temporary)
            (bundle / "jupyter-lite.json").write_text('{"jupyter-lite-schema-version": 0}')
            self.assertEqual(validate_bundle(bundle), required_bundle_files(bundle))


if __name__ == "__main__":
    unittest.main()
