"""
Module for validating the length of a review.
"""
class ValidationReviews:

    def validation_long_reviews(self, text: str,
                                min_len: int) -> bool:
        """
        Validation of the length of the incoming review
        in the feedback book .

        :param text: str
        :param min_len: int
        :return: bool
        """
        return len(text) >= min_len
