from setuptools import setup, find_packages

setup(
    name="perceptraderai",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "MetaTrader5>=5.0.36",
        "gym>=0.26.0",
        "stable-baselines3>=2.0.0",
        "ta-lib>=0.4.24",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": ["perceptrader=perceptrader:main"]
    }
)
