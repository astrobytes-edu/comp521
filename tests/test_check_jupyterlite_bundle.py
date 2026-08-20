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

    def test_requires_bundle_in_published_html_tree(self):
        from scripts.check_jupyterlite_bundle import validate_published_site

        with TemporaryDirectory() as temporary:
            site = Path(temporary)
            self.assertEqual(
                validate_published_site(site),
                [f"{site}: missing published jupyterlite/jupyter-lite.json"],
            )


if __name__ == "__main__":
    unittest.main()
