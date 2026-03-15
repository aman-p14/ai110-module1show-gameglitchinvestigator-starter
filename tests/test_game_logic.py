from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    # FIX: Unpacked tuple return value — Claude Code pointed out check_guess returns
    # (outcome, message), so `result == "Win"` always failed. Changed to `outcome, _ = ...`
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    # FIX: Same tuple-unpacking fix applied here as in test_winning_guess.
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    # FIX: Same tuple-unpacking fix applied here as in test_winning_guess.
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# --- Bug fix verification: high/low message swap in string-comparison fallback ---
# FIX: I asked Claude Code to write tests targeting the FIXME in logic_utils.py.
# Claude identified that passing a str guess with an int secret triggers the buggy
# TypeError branch, and generated these two tests to confirm the swap is corrected.

def test_string_guess_too_high_message_is_go_lower():
    # "60" (str) vs 50 (int) raises TypeError internally, falls to string comparison.
    # Bug: "Too High" incorrectly returned "📈 Go HIGHER!" instead of "📉 Go LOWER!".
    outcome, message = check_guess("60", 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!", f"Expected 'Go LOWER!' for Too High, got: {message!r}"

def test_string_guess_too_low_message_is_go_higher():
    # "40" (str) vs 50 (int) raises TypeError internally, falls to string comparison.
    # Bug: "Too Low" incorrectly returned "📉 Go LOWER!" instead of "📈 Go HIGHER!".
    outcome, message = check_guess("40", 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!", f"Expected 'Go HIGHER!' for Too Low, got: {message!r}"
