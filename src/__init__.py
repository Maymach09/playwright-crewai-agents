"""
Playwright CrewAI Agents Package

This package provides AI-powered test automation for Playwright using CrewAI multi-agent framework.
"""

__version__ = "1.0.0"
__author__ = "Playwright CrewAI Agents"
__license__ = "MIT"

from src.test_ai_assistant.crew import PlaywrightAutomationCrew
from src.test_ai_assistant.main import (
    run_planner,
    run_generator,
    run_healer,
    run_planner_then_generator,
    run_full_pipeline,
)

__all__ = [
    "PlaywrightAutomationCrew",
    "run_planner",
    "run_generator",
    "run_healer",
    "run_planner_then_generator",
    "run_full_pipeline",
]
