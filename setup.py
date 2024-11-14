from setuptools import find_packages, setup

setup(
    name="munaray_fastapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "init_fastapi_project=fastapi_setup.init_project:create_fastapi_project",
        ],
    },
)
