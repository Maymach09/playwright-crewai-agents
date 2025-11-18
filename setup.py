"""
Setup script for Playwright CrewAI Agents

For modern Python packaging, prefer pyproject.toml.
This file is kept for backward compatibility.
"""

from setuptools import setup, find_packages

setup(
    name="playwright-crewai-agents",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.13",
)
