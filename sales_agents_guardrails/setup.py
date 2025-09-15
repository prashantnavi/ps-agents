"""
Setup script for the Sales Agents with Guardrails application.

This script provides easy installation and setup for the application.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read the README file for the long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Sales Agents with Guardrails - AI-powered sales email automation with compliance guardrails"

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt file."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="sales-agents-guardrails",
    version="1.0.0",
    author="Sales Agents Team",
    author_email="team@salesagents.com",
    description="AI-powered sales email automation with comprehensive guardrails",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/sales-agents-guardrails",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Business",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Email",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sales-agents=src.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="ai, sales, email, automation, guardrails, compliance, openai, sendgrid",
    project_urls={
        "Bug Reports": "https://github.com/your-org/sales-agents-guardrails/issues",
        "Source": "https://github.com/your-org/sales-agents-guardrails",
        "Documentation": "https://sales-agents-guardrails.readthedocs.io/",
    },
)
