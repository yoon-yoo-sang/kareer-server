import json
from typing import Any, Dict, List, Type

from langchain_community.document_loaders import SQLDatabaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from openai import OpenAI
from sqlalchemy import create_engine

from common.models import BaseModel
from config.settings import DATABASE_URL
from insights.models import IndustryInfo, CultureInfo, VisaInfo


class InfoProcessor:
    def __init__(self, model: str = "gpt-4o-2024-08-06"):
        self.client = OpenAI()
        self.model = model

    def process_visa_info(self) -> List[Dict[str, Any]]:
        """비자 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights('visa')

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
            return self._deduplicate_by_vector_store(result.get("visa_list", []), VisaInfo)
        except json.JSONDecodeError:
            return []

    def process_culture_info(self) -> List[Dict[str, Any]]:
        """문화 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights('culture')

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
            return self._deduplicate_by_vector_store(result.get("culture_list", []), CultureInfo)
        except json.JSONDecodeError:
            return []

    def process_industry_info(self) -> List[Dict[str, Any]]:
        """산업 관련 인사이트를 구조화된 정보로 변환"""
        combined_content = self._combine_insights('industry')

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
            return self._deduplicate_by_vector_store(result.get("industry_list", []), IndustryInfo)
        except json.JSONDecodeError:
            return []

    def _combine_insights(self, query: str) -> str:
        engine = create_engine(DATABASE_URL)
        loader = SQLDatabaseLoader(
            db=SQLDatabase(
                engine=engine,
            ),
            query="SELECT * FROM insights",
        )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(texts, embeddings)
        docs = vectorstore.similarity_search(query, k=10)
        context = "\n".join([doc.page_content for doc in docs])
        return context

    def _deduplicate_by_vector_store(
        self, info_list: List[Dict[str, Any]], model: Type[BaseModel]
    ) -> List[Dict[str, Any]]:
        """
        중복된 정보를 벡터 스토어를 사용하여 제거합니다. 벡터유사도가 높은 정보가 있으면 제거합니다.
        :param info_list:
        :return:
        """
        engine = create_engine(DATABASE_URL)
        sql_query = f"SELECT * FROM {model._meta.db_table}"
        loader = SQLDatabaseLoader(
            db=SQLDatabase(
                engine=engine,
            ),
            query=sql_query,
        )

        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()

        try:
            vectorstore = Chroma.from_documents(texts, embeddings)
        except ValueError:
            # If the vectorstore is empty, return the original list
            return info_list

        results = []
        for info in info_list:
            text = json.dumps(info)
            doc, score = vectorstore.similarity_search_with_score(text, k=1)[0]
            if score < 0.8:
                results.append(info)

        return results
