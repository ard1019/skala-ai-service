from typing import List, Dict, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from utils.logger import logger
from utils.exceptions import ValidationError

class TextAnalyzer:
    def __init__(self) -> None:
        self._initialize_nltk()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def _initialize_nltk(self) -> None:
        """NLTK 데이터 초기화"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')

    def extract_keywords(self, texts: List[str], top_n: int = 10) -> List[Dict[str, Any]]:
        """텍스트에서 주요 키워드 추출"""
        if not texts:
            raise ValidationError("Empty text list provided")

        try:
            words = []
            for text in texts:
                tokens = word_tokenize(text.lower())
                tokens = [
                    self.lemmatizer.lemmatize(token) 
                    for token in tokens 
                    if token.isalnum() and token not in self.stop_words
                ]
                words.extend(tokens)

            word_freq = Counter(words)
            top_keywords = word_freq.most_common(top_n)

            return [
                {
                    "keyword": word,
                    "frequency": freq,
                    "score": freq / len(words)
                }
                for word, freq in top_keywords
            ]

        except Exception as e:
            logger.error(f"Error in keyword extraction: {e}")
            raise

    def analyze_topic_trends(self, texts: List[str], time_periods: List[str]) -> Dict[str, Any]:
        """시간별 토픽 트렌드 분석"""
        if len(texts) != len(time_periods):
            raise ValidationError("Number of texts and time periods must match")

        try:
            trends = {}
            for period, text_group in zip(time_periods, texts):
                keywords = self.extract_keywords(text_group, top_n=5)
                trends[period] = keywords

            return {
                "trend_analysis": trends,
                "trend_summary": self._generate_trend_summary(trends)
            }

        except Exception as e:
            logger.error(f"Error in topic trend analysis: {e}")
            raise