from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="voice-agent-reinforcement-learning",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered voice agent system with reinforcement learning for agricultural outreach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/voice-agent-project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "voice-agent=src.main_system:main",
            "voice-agent-demo=src.demo_system:main",
        ],
    },
)