import json
from typing import Any, Dict, List

from openai import OpenAI

from insights.models import Insight


class InfoProcessor:
    def __init__(self, model: str = "gpt-4o-2024-08-06"):
        self.client = OpenAI()
        self.model = model

    def process_visa_info(self, insights: list[Insight]) -> List[Dict[str, Any]]:
        """비자 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights(insights)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Convert visa-related information into structured JSON. Please return various types of visa information in array format.",
                },
                {"role": "user", "content": combined_content},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "VisaInfoList",
                    "schema": {
                        "type": "object",
                        "description": "Visa information list",
                        "properties": {
                            "visa_list": {
                                "type": "array",
                                "description": "List of various visa information",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "visa_type": {
                                            "type": "string",
                                            "description": "Type of Visa(name of visa only, e.g., E-2, F-4, etc.)",
                                        },
                                        "requirements": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "requirements for visa application",
                                        },
                                        "process": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "process of visa application",
                                        },
                                        "duration": {
                                            "type": "string",
                                            "description": "duration of visa application",
                                        },
                                    },
                                    "required": [
                                        "visa_type",
                                        "requirements",
                                        "process",
                                        "duration",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["visa_list"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            },
        )

        try:
            result = json.loads(response.output_text)
            return result.get("visa_list", [])
        except json.JSONDecodeError:
            return []

    def process_culture_info(self, insights: list[Insight]) -> List[Dict[str, Any]]:
        """문화 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights(insights)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Convert culture-related information into structured JSON. Please return various types of culture information in array format.",
                },
                {"role": "user", "content": combined_content},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "CultureInfoList",
                    "schema": {
                        "type": "object",
                        "description": "Culture information list",
                        "properties": {
                            "culture_list": {
                                "type": "array",
                                "description": "List of various culture information",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "culture_type": {
                                            "type": "string",
                                            "description": "Type of Culture(Select in {business, daily, social, food, housing, transportation, entertainment})",
                                        },
                                        "title": {
                                            "type": "string",
                                            "description": "title",
                                        },
                                        "content": {
                                            "type": "string",
                                            "description": "content",
                                        },
                                        "tags": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "tags",
                                        },
                                        "source_urls": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "source urls",
                                        },
                                    },
                                    "required": [
                                        "culture_type",
                                        "title",
                                        "content",
                                        "tags",
                                        "source_urls",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["culture_list"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            },
        )

        try:
            result = json.loads(response.output_text)
            return result.get("culture_list", [])
        except json.JSONDecodeError:
            return []

    def process_industry_info(self, insights: list[Insight]) -> List[Dict[str, Any]]:
        """산업 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights(insights)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Convert industry-related information into structured JSON. Please return various types of industry information in array format.",
                },
                {"role": "user", "content": combined_content},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "IndustryInfoList",
                    "schema": {
                        "type": "object",
                        "description": "Industry information list",
                        "properties": {
                            "industry_list": {
                                "type": "array",
                                "description": "List of various industry information",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "industry_type": {
                                            "type": "string",
                                            "description": "Industry type (e.g., technology, healthcare, finance)",
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "Description of the industry",
                                        },
                                        "trends": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "trend of industry",
                                        },
                                        "opportunities": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "opportunities in industry",
                                        },
                                    },
                                    "required": [
                                        "industry_type",
                                        "description",
                                        "trends",
                                        "opportunities",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["industry_list"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            },
        )

        try:
            result = json.loads(response.output_text)
            return result.get("industry_list", [])
        except json.JSONDecodeError:
            return []

    def _combine_insights(self, insights: list[Insight]) -> str:
        """여러 인사이트를 하나의 텍스트로 결합"""
        return "\n\n".join([insight.content for insight in insights])
