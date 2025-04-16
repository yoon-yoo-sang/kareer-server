import json
from typing import Dict, Any, List

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
                {"role": "system", "content": "비자 관련 정보를 구조화된 JSON으로 변환합니다. 여러 종류의 비자 정보를 배열 형태로 반환해주세요."},
                {"role": "user", "content": combined_content},
            ],
            text={"format": {
                "type": "json_schema",
                "name": "VisaInfoList",
                "schema": {
                    "type": "object",
                    "description": "비자 정보 목록",
                    "properties": {
                        "visa_list": {
                            "type": "array",
                            "description": "여러 비자 정보 목록",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "visa_type": {
                                        "type": "string",
                                        "description": "비자 종류"
                                    },
                                    "requirements": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "비자 신청 요건"
                                    },
                                    "process": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "비자 신청 절차"
                                    },
                                    "duration": {
                                        "type": "string",
                                        "description": "비자 처리 기간"
                                    }
                                },
                                "required": ["visa_type", "requirements", "process", "duration"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["visa_list"],
                    "additionalProperties": False
                },
                "strict": True
            }}
        )

        try:
            result = json.loads(response.output_text)
            return result.get('visa_list', [])
        except json.JSONDecodeError:
            return []

    def process_culture_info(self, insights: list[Insight]) -> List[Dict[str, Any]]:
        """문화 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights(insights)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": "문화 관련 정보를 구조화된 JSON으로 변환합니다. 여러 종류의 문화 정보를 배열 형태로 반환해주세요."},
                {"role": "user", "content": combined_content},
            ],
            text={"format": {
                "type": "json_schema",
                "name": "CultureInfoList",
                "schema": {
                    "type": "object",
                    "description": "문화 정보 목록",
                    "properties": {
                        "culture_list": {
                            "type": "array",
                            "description": "여러 문화 정보 목록",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "culture_type": {
                                        "type": "string",
                                        "description": "문화 종류(business, daily, social, food, housing, transportation, entertainment 내에서 선택)"
                                    },
                                    "title": {
                                        "type": "string",
                                        "description": "제목"
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "내용"
                                    },
                                    "tags": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "태그"
                                    },
                                    "source_urls": {
                                        "type": "array",
                                        "items": {
                                            "type": ["string"]
                                        },
                                        'description': '출처 URL'
                                    }
                                },
                                'required': ['culture_type', 'title', 'content', 'tags', 'source_urls'],
                                'additionalProperties': False
                            }
                        }
                    },
                    'required': ['culture_list'],
                    'additionalProperties': False
                },
                'strict': True
            }}
        )

        try:
            result = json.loads(response.output_text)
            return result.get('culture_list', [])
        except json.JSONDecodeError:
            return []

    def process_industry_info(self, insights: list[Insight]) -> List[Dict[str, Any]]:
        """산업 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights(insights)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": "산업 관련 정보를 구조화된 JSON으로 변환합니다. 여러 종류의 산업 정보를 배열 형태로 반환해주세요."},
                {"role": "user", "content": combined_content},
            ],
            text={"format": {
                "type": "json_schema",
                "name": "IndustryInfoList",
                "schema": {
                    "type": "object",
                    "description": "산업 정보 목록",
                    "properties": {
                        "industry_list": {
                            "type": "array",
                            "description": "여러 산업 정보 목록",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "industry_type": {
                                        "type": "string",
                                        "description": "산업 종류"
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "산업 설명"
                                    },
                                    "trends": {
                                        "type": "array",
                                        'items': {'type': 'string'},
                                        'description': '산업 트렌드'
                                    },
                                    'opportunities': {
                                        'type': 'array',
                                        'items': {'type': 'string'},
                                        'description': '산업 기회'
                                    }
                                },
                                'required': ['industry_type', 'description', 'trends', 'opportunities'],
                                'additionalProperties': False
                            }
                        }
                    },
                    'required': ['industry_list'],
                    'additionalProperties': False
                },
                'strict': True
            }}
        )

        try:
            result = json.loads(response.output_text)
            return result.get('industry_list', [])
        except json.JSONDecodeError:
            return []

    def _combine_insights(self, insights: list[Insight]) -> str:
        """여러 인사이트를 하나의 텍스트로 결합"""
        return "\n\n".join([insight.content for insight in insights])
