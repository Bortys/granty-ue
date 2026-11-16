import datetime as dt
import json
import unittest

from scripts import nabory_ue


UTC = dt.timezone.utc


def grant_result(reference, deadlines, *, call_title="Example call", url="https://example.test/project"):
    return {
        "reference": reference,
        "url": url,
        "weight": 1,
        "metadata": {
            "type": "8",
            "identifier": "CASCADE-PROJECT",
            "callTitle": call_title,
            "projectAcronym": "EXAMPLE",
            "status": "31094502",
            "deadlineDate": deadlines,
            "frameworkProgramme": [],
        },
    }


class DeadlineHandlingTests(unittest.TestCase):
    def test_record_selects_nearest_future_deadline_and_ignores_past_dates(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        result = {
            "url": "https://example.test/call",
            "weight": 1,
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-TEST-01",
                "title": "Test call",
                "status": "31094502",
                "deadlineDate": [
                    "2026-11-15T10:00:00+0000",
                    "2026-11-20T17:00:00+0000",
                    "2026-11-18T09:00:00+0000",
                ],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertEqual(record["nastepny_termin"], "2026-11-18 09:00")
        self.assertEqual(
            record["wszystkie_terminy"],
            ["2026-11-15 10:00", "2026-11-18 09:00", "2026-11-20 17:00"],
        )
        self.assertEqual(record["_termin_sort"], dt.datetime(2026, 11, 18, 9, 0, tzinfo=UTC))

    def test_record_with_only_past_deadlines_has_no_active_deadline(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        result = {
            "url": "https://example.test/old-call",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-OLD-01",
                "title": "Old call",
                "status": "31094502",
                "deadlineDate": ["2026-11-15T17:00:00+0000"],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertIsNone(record["nastepny_termin"])
        self.assertIsNone(record["_termin_sort"])

    def test_date_only_deadline_remains_current_for_the_whole_day(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        result = {
            "url": "https://example.test/date-only-call",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-DATE-ONLY-01",
                "title": "Date-only call",
                "status": "31094502",
                "deadlineDate": ["2026-11-16"],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertEqual(record["nastepny_termin"], "2026-11-16")
        self.assertIsNotNone(record["_termin_sort"])

    def test_full_timestamp_at_utc_midnight_expires_at_that_instant(self):
        now = dt.datetime(2026, 11, 17, 23, 50, tzinfo=UTC)
        result = {
            "url": "https://example.test/midnight-timestamp",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-MIDNIGHT-UTC-01",
                "title": "Midnight timestamp",
                "status": "31094502",
                "deadlineDate": ["2026-11-17T00:00:00+0000"],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertIsNone(record["nastepny_termin"])
        self.assertIsNone(record["_termin_sort"])

    def test_full_timestamp_at_midnight_with_offset_uses_its_instant(self):
        now = dt.datetime(2026, 11, 16, 22, 30, tzinfo=UTC)
        result = {
            "url": "https://example.test/midnight-offset-timestamp",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-MIDNIGHT-OFFSET-01",
                "title": "Midnight timestamp with offset",
                "status": "31094502",
                "deadlineDate": ["2026-11-17T00:00:00+0200"],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertIsNone(record["nastepny_termin"])
        self.assertIsNone(record["_termin_sort"])

    def test_date_only_deadline_compares_calendar_day_in_utc(self):
        now = dt.datetime(2026, 11, 17, 0, 30, tzinfo=dt.timezone(dt.timedelta(hours=2)))
        result = {
            "url": "https://example.test/date-only-timezone",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-DATE-ONLY-TZ-01",
                "title": "Date-only timezone",
                "status": "31094502",
                "deadlineDate": ["2026-11-16"],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertEqual(record["nastepny_termin"], "2026-11-16")
        self.assertIsNotNone(record["_termin_sort"])

    def test_date_only_deadline_from_previous_day_is_expired(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        result = {
            "url": "https://example.test/expired-date-only-call",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-EXPIRED-DATE-ONLY-01",
                "title": "Expired date-only call",
                "status": "31094502",
                "deadlineDate": ["2026-11-15"],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertIsNone(record["nastepny_termin"])
        self.assertIsNone(record["_termin_sort"])

    def test_deadlines_with_offsets_are_compared_as_instants(self):
        now = dt.datetime(2026, 11, 16, 23, 45, tzinfo=UTC)
        result = {
            "url": "https://example.test/timezone-call",
            "metadata": {
                "type": "1",
                "identifier": "HORIZON-TZ-01",
                "title": "Timezone call",
                "status": "31094502",
                "deadlineDate": [
                    "2026-11-17T00:30:00+0100",
                    "2026-11-17T01:30:00+0100",
                ],
                "frameworkProgramme": [],
            },
        }

        record = nabory_ue.rekord(result, now, {})

        self.assertEqual(record["nastepny_termin"], "2026-11-17 01:30")
        self.assertEqual(
            record["_termin_sort"],
            dt.datetime(2026, 11, 17, 1, 30, tzinfo=dt.timezone(dt.timedelta(hours=1))),
        )


class CascadeDeduplicationTests(unittest.TestCase):
    def test_different_calls_sharing_project_url_are_preserved(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        shared_url = "https://example.test/project"
        results = [
            grant_result("call-reference-1", ["2026-11-20T17:00:00+0000"], call_title="Call one", url=shared_url),
            grant_result("call-reference-2", ["2026-11-22T17:00:00+0000"], call_title="Call two", url=shared_url),
        ]

        records = nabory_ue._unikalne_rekordy(results, now, {})

        self.assertEqual(len(records), 2)
        self.assertEqual([record["tytul"] for record in records], ["Call one", "Call two"])

    def test_duplicate_api_reference_is_removed(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        result = grant_result("same-reference", ["2026-11-20T17:00:00+0000"])

        records = nabory_ue._unikalne_rekordy([result, dict(result)], now, {})

        self.assertEqual(len(records), 1)

    def test_seen_references_are_shared_across_pages(self):
        now = dt.datetime(2026, 11, 16, 12, 0, tzinfo=UTC)
        seen = set()
        first_page = grant_result("same-reference", ["2026-11-20T17:00:00+0000"])
        second_page = dict(first_page)

        first_records = nabory_ue._unikalne_rekordy([first_page], now, {}, seen)
        second_records = nabory_ue._unikalne_rekordy([second_page], now, {}, seen)

        self.assertEqual(len(first_records), 1)
        self.assertEqual(second_records, [])


class BudgetParsingTests(unittest.TestCase):
    def test_budget_contributions_expressed_in_millions_are_converted(self):
        metadata = {
            "budgetOverview": json.dumps({
                "budgetTopicActionMap": {
                    "2027": [
                        {
                            "action": "HORIZON-TEST-01 - Research action",
                            "minContribution": 10,
                            "maxContribution": 15,
                            "expectedGrants": 3,
                            "budgetYearMap": {"2027": 45_000_000},
                        },
                        {
                            "action": "HORIZON-OTHER-01 - Unrelated action",
                            "minContribution": 1,
                            "maxContribution": 2,
                        },
                    ]
                }
            })
        }

        budget = nabory_ue._budzet_tematu(metadata, "HORIZON-TEST-01")

        self.assertEqual(len(budget), 1)
        self.assertEqual(budget[0]["dotacja_min"], 10_000_000)
        self.assertEqual(budget[0]["dotacja_max"], 15_000_000)
        self.assertEqual(budget[0]["budzet_lacznie"], 45_000_000)
        self.assertEqual(nabory_ue._na_projekt(budget), "10 mln–15 mln EUR")

    def test_large_budget_values_are_not_scaled_twice(self):
        metadata = {
            "budgetOverview": json.dumps({
                "budgetTopicActionMap": {
                    "2027": [{
                        "action": "HORIZON-TEST-02 - Research action",
                        "minContribution": 2_000_000,
                        "maxContribution": 5_000_000,
                    }]
                }
            })
        }

        budget = nabory_ue._budzet_tematu(metadata, "HORIZON-TEST-02")

        self.assertEqual(budget[0]["dotacja_min"], 2_000_000)
        self.assertEqual(budget[0]["dotacja_max"], 5_000_000)

    def test_missing_or_malformed_budget_data_returns_no_budget(self):
        self.assertEqual(nabory_ue._budzet_tematu({}, "HORIZON-TEST-03"), [])
        self.assertEqual(
            nabory_ue._budzet_tematu({"budgetOverview": "not-json"}, "HORIZON-TEST-03"),
            [],
        )
        self.assertIsNone(nabory_ue._na_projekt([]))


if __name__ == "__main__":
    unittest.main()
