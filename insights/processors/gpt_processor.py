import os

import openai
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response
from bs4 import BeautifulSoup
import tiktoken

from insights.processors.base_processors import BaseProcessor

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class GptProcessor(BaseProcessor):
    def __init__(self, model: str = "gpt-3.5-turbo", system_prompt: str = "You are a helpful assistant.", max_tokens: int = 4000):
        """
        Initialize the GptProcessor with the specified model.
        :param model: The model to use for processing.
        :param system_prompt: The system prompt to use.
        :param max_tokens: Maximum number of tokens to process.
        """
        self.client = OpenAI()
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model(model)

    def _preprocess_html(self, html: str) -> str:
        """
        HTML을 전처리하여 텍스트만 추출하고 토큰 수를 제한합니다.
        :param html: HTML 문자열
        :return: 전처리된 텍스트
        """
        # HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')
        
        # 불필요한 태그 제거
        for tag in soup(['script', 'style', 'meta', 'link', 'header', 'footer', 'nav']):
            tag.decompose()
            
        # 텍스트 추출 및 정리
        text = ' '.join(soup.stripped_strings)
        text = ' '.join(text.split())
        
        # 토큰 수 제한
        tokens = self.encoding.encode(text)
        if len(tokens) > self.max_tokens:
            text = self.encoding.decode(tokens[:self.max_tokens])
            
        return text

    def process(self, data: str):
        """
        데이터를 처리하고 결과를 반환합니다.
        :param data: 처리할 데이터
        :return:
        """
        processed_text = self._preprocess_html(data)
        openai_response = self._call_openai_api(processed_text)
        if openai_response and openai_response.output_text:
            return openai_response.output_text
        else:
            raise ValueError("No response from OpenAI API or invalid response format.")

    def _call_openai_api(self, user_prompt: str) -> Response:
        """
        OpenAI API를 호출하여 응답을 가져옵니다.
        :param user_prompt: 사용자 프롬프트
        :return:
        """
        openai.api_key = OPENAI_API_KEY
        response = self.client.responses.create(
            model=self.model,
            input=f"""
                system: {self.system_prompt}
                ===========================
                user: {user_prompt}
                ===========================
                assistant:
            """
        )
        return response
