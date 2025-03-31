from setuptools import setup, find_packages

setup(
    name="compass-case",
    version="0.1.0",
    description="Cohere Compass SDK Web Interface",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/compass-case",
    packages=find_packages(exclude=["cohere_compass*"]),
    install_requires=[
        "cohere-compass @ git+https://github.com/cohere-ai/cohere-compass-sdk.git",
        "requests>=2.32.0",
        "joblib>=1.4.0",
        "tenacity>=9.0.0",
        "fsspec>=2025.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "flask==2.3.3",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 