import re
from math import ceil


class ArticleReadTimeEngine:
    @staticmethod
    def word_count(text):
        words = re.findall(r"\w+", text)
        return len(words)

    @staticmethod
    def estimate_reading_time(
        article, words_per_minute=250, seconds_per_image=10, seconds_per_tag=2
    ):
        words_count_title = ArticleReadTimeEngine.word_count(article.title)
        words_count_body = ArticleReadTimeEngine.word_count(article.body)
        words_count_description = ArticleReadTimeEngine.word_count(article.description)

        total_words_count = (
            words_count_title + words_count_body + words_count_description
        )

        reading_time = total_words_count / words_per_minute

        if article.banner_image:
            reading_time += seconds_per_image / 60

        tags_count = article.tags.count()

        reading_time += (tags_count * seconds_per_tag) / 60

        return ceil(reading_time)
