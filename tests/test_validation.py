from __future__ import annotations

import unittest

from src.cv_builder.validation import date_format_error, email_format_error, links_format_error, phone_format_error


class FieldValidationTests(unittest.TestCase):
    def test_phone_accepts_blank_and_international_format(self) -> None:
        self.assertIsNone(phone_format_error(""))
        self.assertIsNone(phone_format_error("+49 (30) 1234-5678"))

    def test_phone_rejects_unquoted_or_malformed_values(self) -> None:
        self.assertIsNotNone(phone_format_error("9620531036"))
        self.assertIsNotNone(phone_format_error("+49 phone number"))

    def test_email_validation(self) -> None:
        self.assertIsNone(email_format_error("person@example.com"))
        self.assertIsNone(email_format_error(""))
        self.assertIsNotNone(email_format_error("person@example"))

    def test_dates_validate_format_and_end_order_is_checked_by_form(self) -> None:
        self.assertIsNone(date_format_error("2024-03"))
        self.assertIsNone(date_format_error("present", end_date=True))
        self.assertIsNotNone(date_format_error("2024-13"))

    def test_links_validate_networks_and_urls(self) -> None:
        self.assertIsNone(links_format_error("LinkedIn: jane-doe\nWebsite: https://example.com"))
        self.assertIsNotNone(links_format_error("Website:"))
        self.assertIsNotNone(links_format_error("MySpace: jane"))


if __name__ == "__main__":
    unittest.main()
