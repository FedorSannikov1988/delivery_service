"""
Validation of input parameters
(date of receipt, time of receipt,
recipient's name) for delivery.
"""
class ValidationReviews:

    def validation_long_reviews(self, text: str,
                                min_len: int) -> bool:
        return len(text) >= min_len
