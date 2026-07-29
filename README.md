# Human-Centric Password Strength Tester

A password strength checker that scores passwords along two axes instead of one: how **secure** a password is against real-world cracking techniques, and how much **friction** it creates for the human who actually has to type and remember it.

Most password checkers only answer the first question. This project treats the second as equally important — a password can be mathematically strong and still a bad password if no human can reliably use it.

---

## Why two scores instead of one

A 20-character random string and a well-chosen four-word passphrase can both be "secure," but they are not equally usable. A checker that only reports entropy tells you nothing about whether a real person will actually be able to use the password you're recommending — which, in practice, is often *why* people fall back to weak, memorable passwords in the first place. This project scores both sides so the tradeoff is visible, not hidden.

## Features

- **Entropy-based security scoring** (`E = L × log2(R)`) based on password length and character pool size (lowercase, uppercase, digits, symbols).
- **Dictionary, name, and place detection** — checks whether a password (or a leetspeak-decoded version of it) is a real word, a common first/last name, or a city/country name, and penalizes accordingly.
- **Leetspeak reversal** — decodes both single-character substitutions (`3` → `e`, `$` → `s`) and multi-character substitutions (`|\/|` → `m`) to catch passwords that look random but are disguised words.
- **Date pattern detection** — recognizes day/month/year patterns even when leetspeak-obscured (e.g. `11 $3p7Em8e2 z0z6` decodes to 11 September 2026), since dates are among the first things real attackers try.
- **Human friction scoring** — scores typing/memory difficulty based on character-class diversity, ambiguous-looking characters (e.g. `l` vs `1` appearing together), and randomness.
- **Offline lookups** — dictionary, name, and place data are loaded locally at startup; no network calls are made while scoring a password.

## Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`:
  - `geonamescache`
  - `english_words`
  - `names-dataset`

## Installation

```bash
git clone https://github.com/Max11Siphe/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
```

**Note:** the first install downloads roughly 100MB of offline dictionary, name, and place data used for lookups. This requires an internet connection once, at install time — the program itself does not need internet to run afterward.

## Usage

Run the script directly:

```bash
python password_strength_checker.py
```

This runs a fixed demo set of example passwords through the full analysis and prints a report for each. Sample output:

```
===================================================
 INPUT: qXmnZK65rf*&
 [🛡️ SECURITY STRENGTH] -> 87% (Strong)
 • Math: High entropy, 94-character pool, 12 length.
 • Hacker Verdict: Will take years to decades to brute-force.
 [🧠 HUMAN FRICTION]    -> 71% (High Friction)
 • Typing: Requires 3 keyboard layout shifts.
 • Memory: Random string offers zero cognitive hooks.
 • Verdict: User may struggle to recall this reliably.
===================================================
===================================================
 INPUT: 11 $3p7Em8e2 z0z6
 [🛡️ SECURITY STRENGTH] -> 18% (Very Weak)
 • Math: Low entropy, 94-character pool, 17 length.
 • Hacker Verdict: Crackable almost instantly.
 [🧠 HUMAN FRICTION]    -> 100% (Very High Friction)
 • Typing: Requires 2 keyboard layout shifts.
 • Memory: Random string offers zero cognitive hooks.
 • Verdict: User will likely forget this or write it down.
===================================================
```

The second example is deliberately included in the demo set: it *looks* like a random string of symbols and numbers, but it decodes to a disguised date (`11 September 2026`) — a pattern real cracking tools check for before brute-forcing. It scores low on security despite its length, and high on friction, since it's genuinely painful to type and recall. That combination — weak *and* annoying — is the worst case a password can land in, and is the main thing this tool is built to surface.

To check your own passwords, edit the `DEMO_PASSWORDS` (or equivalent) list in `main()` and re-run the script.

## How it works

**Security score.** Entropy is calculated as `length × log2(character pool size)`, then expressed as a percentage of a target "effectively uncrackable" ceiling. This raw entropy is capped downward if the password (after leetspeak decoding) turns out to be a dictionary word, name, place, or a disguised date — because attackers don't brute-force character-by-character first; they run wordlists, name lists, and common patterns (dates, keyboard walks, `password123`) before anything else. A password that would take centuries to brute-force character-by-character can still fall in seconds to a wordlist attack if it's just a decorated real word.

**Friction score.** This is scored independently of security and measures how hard the password is on a human: how many character classes it mixes (each additional class adds typing effort), whether it contains visually ambiguous characters (`l`/`1`, `0`/`O`) that cause typos, how many times the typist has to reach for Shift, and whether the password contains any recognizable words/names that give the brain something to hold onto versus being pure random noise.

## Known limitations / design decisions

- **The entropy ceiling (`BITS_TARGET_CEILING`) is a calibration choice, not a fixed standard.** It determines what percentage of "excellent" corresponds to what raw bit count. There's no universally agreed number for "uncrackable" — this project uses 90 bits as a reasonable benchmark, but that value can reasonably be tuned.
- **Whole-password dictionary matching only, not multi-word passphrases.** A password like `correcthorsebatterystaple` currently scores full entropy credit per character, because the dictionary-match check only fires when the *entire* password is one word — it doesn't yet penalize passphrases built from multiple real dictionary words the way a real wordlist-combination attack would. This is a known gap, not an oversight: closing it is a matter of also feeding the password through the passphrase detector before capping entropy, but doing so changes the scoring philosophy (passphrases are a legitimate, currently-recommended password strategy) and was left as a deliberate open design question rather than silently "fixed."
- **Keyboard-shift counting assumes a US QWERTY layout.** Symbol positions (and therefore which characters require Shift) differ on UK, French (AZERTY), and German (QWERTZ) layouts; this isn't currently layout-aware.
- **All lookups are offline and English-centric.** The dictionary, name, and place data used for detection are drawn from English-language and global-but-English-indexed sources; non-English dictionary words may not be detected as such.

## Testing

Unit tests are provided in `test_password_strength_checker.py`, covering entropy calculation, dictionary/date detection (including the leetspeak-decoding path), friction scoring, and edge cases like empty input.

```bash
python -m unittest test_password_strength_checker -v
```

## Author

Siphe — built as a cybersecurity project exploring the intersection of password security and human usability.