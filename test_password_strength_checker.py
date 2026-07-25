import sys
import unittest

sys.path.insert(0, "/mnt/user-data/outputs")
import pw_strength_tester as pw


class TestCharacterChecker(unittest.TestCase):
    def test_detects_all_four_classes(self):
        result = pw.character_checker("aA1!")
        self.assertTrue(result["lowercase bool"])
        self.assertTrue(result["uppercase bool"])
        self.assertTrue(result["num bool"])
        self.assertTrue(result["special char bool"])

    def test_lowercase_only(self):
        result = pw.character_checker("abcdef")
        self.assertTrue(result["lowercase bool"])
        self.assertFalse(result["uppercase bool"])
        self.assertFalse(result["num bool"])
        self.assertFalse(result["special char bool"])


class TestEntropy(unittest.TestCase):
    def test_empty_password_is_zero(self):
        self.assertEqual(pw.entropy(""), "0%")

    def test_never_exceeds_100_percent(self):
        pct = int(pw.entropy("x" * 50 + "!@#123ABC").rstrip("%"))
        self.assertLessEqual(pct, 100)

    def test_disguised_date_is_capped_low(self):
        # FIX regression test: before wiring leet_word_translator into
        # entropy(), this 17-char full-pool password scored ~100% because
        # the date-pattern cap never saw the translated string.
        pct = int(pw.entropy("11 $3p7Em8e2 z0z6").rstrip("%"))
        self.assertLessEqual(pct, 25, "disguised date should score Very Weak / Weak")

    def test_pure_random_string_scores_higher_than_disguised_date(self):
        random_pct = int(pw.entropy("qXmnZK65rf*&").rstrip("%"))
        date_pct = int(pw.entropy("11 $3p7Em8e2 z0z6").rstrip("%"))
        self.assertGreater(random_pct, date_pct)


class TestLeetspeakReverseCaseFix(unittest.TestCase):
    def test_lowercase_real_word_scores_zero(self):
        # Always worked, even before the fix.
        self.assertEqual(pw.leetspeak_reverse("banana"), 0)

    def test_mixed_case_real_word_scores_zero_after_fix(self):
        # FIX regression test: "Banana" (capital B) used to fail the
        # `password in eng_word_list` check because eng_word_list is
        # always lowercase. Should now correctly score 0, not 20.
        self.assertEqual(pw.leetspeak_reverse("Banana"), 0)

    def test_random_short_string_scores_twenty(self):
        self.assertEqual(pw.leetspeak_reverse("xqz7v"), 20)


class TestDiffCharFriction(unittest.TestCase):
    def test_empty_password_is_zero(self):
        # FIX regression test: previously returned "20%" for "" because
        # leetspeak_reverse("") fell into the len < 10 branch.
        self.assertEqual(pw.diff_char_friction(""), "0%")

    def test_never_exceeds_100_percent(self):
        pct = int(pw.diff_char_friction("Zz9!Zz9!Zz9!Zz9!").rstrip("%"))
        self.assertLessEqual(pct, 100)


class TestKeyboardShiftTransitions(unittest.TestCase):
    def test_no_shifted_chars(self):
        self.assertEqual(pw.keyboard_shift_transitions("abcdef123"), 0)

    def test_single_run_counts_once(self):
        # "ABC" is one contiguous shift-held run, not three presses.
        self.assertEqual(pw.keyboard_shift_transitions("abcABCdef"), 1)

    def test_separate_runs_count_separately(self):
        # "A" ... "B" separated by lowercase = two separate Shift presses.
        self.assertEqual(pw.keyboard_shift_transitions("aAbbBc"), 2)

    def test_shift_symbols_count_like_uppercase(self):
        self.assertEqual(pw.keyboard_shift_transitions("ab*&cd"), 1)
        self.assertEqual(pw.keyboard_shift_transitions("ab*cd&ef"), 2)


class TestIsDatePattern(unittest.TestCase):
    def test_plain_date_detected(self):
        self.assertTrue(pw.is_date_pattern("11 September 2026"))

    def test_leet_disguised_date_detected(self):
        self.assertTrue(pw.is_date_pattern("11 $3p7Em8e2 z0z6"))

    def test_random_string_not_a_date(self):
        self.assertFalse(pw.is_date_pattern("qXmnZK65rf*&"))

    def test_missing_component_not_a_date(self):
        # Day + month but no year -> should not count as a full date.
        self.assertFalse(pw.is_date_pattern("11 September"))


class TestMemoryHookDescription(unittest.TestCase):
    def test_passphrase_gets_hooks(self):
        desc = pw.memory_hook_description("correcthorsebatterystaple")
        self.assertIn("hooks", desc)

    def test_random_string_gets_no_hooks(self):
        desc = pw.memory_hook_description("qXmnZK65rf*&")
        self.assertIn("zero cognitive hooks", desc)


class TestDisplayPasswordReportRuns(unittest.TestCase):
    def test_runs_without_raising_for_various_inputs(self):
        for sample in ["qXmnZK65rf*&", "11 $3p7Em8e2 z0z6",
                        "correcthorsebatterystaple", "password123", ""]:
            try:
                pw.display_password_report(sample)
            except Exception as exc:
                self.fail(f"display_password_report raised on {sample!r}: {exc}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
