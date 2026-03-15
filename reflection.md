# 💭 Reflection: Game Glitch Investigator

---

## 1. What was broken when you started?

When I first ran the game, the score immediately went negative (reaching -35) after just a few wrong guesses, and the range displayed in the prompt was always "1 and 100" no matter which difficulty I selected. Here are all the bugs I found:

- Expected the prompt to say the correct range for the selected difficulty (e.g., "1 and 20" on Easy). Instead, it always said "Guess a number between 1 and 100."

- Expected wrong guesses to always cost points. Instead, on even-numbered attempts a "Too High" guess gave +5 points, making the score unpredictable and often very negative.

- Expected "Go LOWER!" when my guess was too high. Instead, the game showed "📈 Go HIGHER!" — the exact opposite of the correct hint.

- Expected Hard to have a wider range than Normal. Instead, Hard was 1–50 and Normal was 1–100, making Hard actually easier.

- Expected the game to always compare my guess to a number. Instead, on every even attempt the secret was converted to a string, breaking numeric comparison and giving wrong hints.

- Expected "New Game" to generate a secret within the selected difficulty's range. Instead, it always picked from 1–100 regardless of difficulty.

---

## 2. How did you use AI as a teammate?

**Which AI tools did you use on this project?**
I used ChatGPT, Perplexity, and Claude Code.

**Give one example of an AI suggestion that was correct.**
One correct suggestion from AI was identifying why the first three tests were failing. Claude Code pointed out that the `check_guess` function returns a tuple `(outcome, message)`, but the tests were comparing the entire tuple to a string such as `"Win"`. Because of this mismatch, the tests would always fail even if the game logic was correct. I verified this by running `pytest`, which showed an error like `assert ('Win', '🎉 Correct!') == 'Win'`. After updating the tests to unpack the tuple using `outcome, _ = check_guess(...)`, those failures were resolved and the tests passed.

**Give one example of an AI suggestion that was incorrect or misleading.**
One misleading AI suggestion occurred when writing the two new bug-fix tests. Claude assumed that passing a string guess (like `"60"`) against an integer secret (`50`) would trigger the `except TypeError` branch and still return a result that the tests could check. However, this was incorrect because the `except` block itself compared `g > secret`, which is still a string-to-integer comparison. This caused another `TypeError`, so the function crashed instead of returning a value. I verified this by running `pytest`, which showed a failure trace pointing to line 55 in `logic_utils.py`. After seeing this error in the test output, the comparison was corrected so that both values were comparable, allowing the tests to pass.

---

## 3. Debugging and testing your fixes

**How did you decide whether a bug was really fixed?**
By running `pytest` and checking in the game itself after every bug fix.

**Describe at least one test you ran and what it showed you about your code.**
Running `pytest` showed that five tests were still failing even after fixing the original bug. The output revealed two issues: the first three tests compared a tuple to a string, causing a mismatch, and the two new tests crashed with a second `TypeError` in the `except` block due to a `str` vs `int` comparison. The test output pinpointed the exact lines and reasons for the failures, which made it possible to fix the problems accurately instead of guessing.

**Did AI help you design or understand any tests? How?**
Claude recognized that `check_guess` returns a tuple, so asserting `result == "Win"` would always fail regardless of whether the logic was correct. That distinction — the difference between a structural test failure and a logic test failure — helped clarify what needed to be fixed in the tests vs. what needed to be fixed in the code.

---

## 4. What did you learn about Streamlit and state?

**In your own words, explain why the secret number kept changing in the original app.**
The secret number appeared to keep changing because Streamlit reruns the entire script whenever a widget changes, such as the difficulty selector. When the app reran, the input field reset due to its key being tied to the difficulty setting, which made it seem like the secret number had changed. In reality, the rerun and state reset created the illusion that the target number was moving.

**How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?**
Streamlit reruns mean the whole script runs again from top to bottom every time a user changes something in the app. Session state works like memory that stores values so they do not reset during these reruns. This allows the app to remember important things like the secret number.

**What change did you make that finally gave the game a stable secret number?**
The fix was to store the secret number in `st.session_state` and only generate it if it does not already exist. Since Streamlit reruns the whole script every time a user interacts with the app, a normal `random.randint` call would create a new secret each time. By checking `if "secret" not in st.session_state` first, the number is created once and then kept the same across reruns, so the target stays stable during the game.

---

## 5. Looking ahead: your developer habits

**What is one habit or strategy from this project that you want to reuse in future labs or projects?**
One habit I want to reuse in future projects is writing and running tests with `pytest` after fixing a bug. Tests help confirm that the code works as expected and make it easier to catch mistakes quickly. This also ensures that if a similar bug appears again, the tests will immediately reveal the problem.

**What is one thing you would do differently next time you work with AI on a coding task?**
One thing I would do differently next time is give more specific prompts when asking AI for help. Clear instructions about the file, the bug, and the expected behavior can help the AI provide more accurate suggestions and avoid misleading fixes.

**In one or two sentences, describe how this project changed the way you think about AI generated code.**
This project showed me that AI-generated code is helpful but should not be trusted without verification. It is important to test and review AI suggestions carefully to make sure the code actually works as expected.
