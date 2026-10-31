# Configurable CLI Password Generator

> **Level 1 Internship Task 31**  
> A beginner-friendly, secure, and modular Command-Line Password Generator built in pure Python using only standard library modules.

---

## 📌 Project Overview

This project provides an interactive command-line interface (CLI) to generate strong, cryptographically secure passwords. Users can configure the desired password length, toggle specific character sets (lowercase, uppercase, numbers, and symbols), and generate single or bulk batches of passwords on demand.

The generator guarantees that every selected character type is represented at least once in the generated output, eliminates positional bias with cryptographic shuffling, and never stores passwords to disk.

---

## ✨ Features

- **Standard Library Only**: Built entirely using Python's built-in `secrets` and `string` modules—no external dependencies or packages needed.
- **Configurable Length**: User-selectable password length validated between **8** and **128** characters.
- **Toggleable Character Sets**:
  - Lowercase letters (`a-z`)
  - Uppercase letters (`A-Z`)
  - Numeric digits (`0-9`)
  - Special punctuation/symbols (`!@#$%^&*...`)
- **Guaranteed Variety**: Enforces at least one character from every active category, then fills remaining slots from the combined pool.
- **Unpredictable Shuffling**: Uses `secrets.SystemRandom().shuffle()` to eliminate predictable placement (e.g., guaranteed characters won't cluster at the beginning).
- **Strict Input Validation**: Rejects non-numeric characters, numbers outside bounds, and empty character selections, re-prompting cleanly without crashing.
- **Batch Generation**: Allows generating 1 to 100 passwords in a single run.
- **Password Strength Evaluation**: Evaluates and displays a real-time rating (**Weak**, **Medium**, or **Strong**) based on length and character diversity.
- **Zero-Storage Privacy**: Passwords exist exclusively in volatile memory (`stdout`) and are never written to any log or file.

---

## 📂 Project Structure

```text
password-generator/
│
├── password_generator.py   # Main CLI application source code
├── sample_output.txt       # Sample terminal runs with test outputs
├── .gitignore              # Standard Python gitignore file
└── README.md               # Project documentation and interview Q&A
```

---

## 🚀 How to Run

### 1. Prerequisites
- Python 3.8 or higher installed on your system.
- Check your installation:
  ```bash
  python --version
  ```

### 2. Run the Application
Open your terminal or command prompt, navigate to the project directory, and execute:

```bash
python password_generator.py
```

On Linux or macOS systems with multiple Python versions:
```bash
python3 password_generator.py
```

---

## 💻 Example Usage

```text
============================================================
             CONFIGURABLE CLI PASSWORD GENERATOR
             Level 1 Internship Project (Task 31)
============================================================

Enter password length (8-128): 16

Select character types to include:
  Include lowercase letters (a-z)? [Y/n]: y
  Include uppercase letters (A-Z)? [Y/n]: y
  Include digits (0-9)? [Y/n]: y
  Include special symbols (!@#$%...)? [Y/n]: y

How many passwords to generate (1-100) [Default: 1]: 2

============================================================
                    CONFIGURATION SUMMARY
============================================================
  Length:            16 characters
  Character Types:   Lowercase, Uppercase, Digits, Symbols (4/4)
  Strength Rating:   [STRONG] - Excellent length and diverse character variety.
============================================================
                    GENERATED PASSWORD(S)
============================================================
  [01]  k9#M$xR8!vP2*wTq
  [02]  B5@zL#1pY&9dF!mQ
============================================================
  [Security Notice] Generated passwords are held strictly in memory
  and are NOT stored or written to any file automatically.
============================================================

Would you like to generate another batch? [y/N]: n

Thank you for using the CLI Password Generator. Stay secure!
```

See [sample_output.txt](sample_output.txt) for more sample runs covering different character combinations, lengths, and edge cases.

---

## 🧠 Technical Q&A

### 1. Why is `secrets` preferred over `random` for passwords?

| Feature | `random` Module | `secrets` Module |
| :--- | :--- | :--- |
| **Generator Type** | Pseudo-Random Number Generator (PRNG) using the **Mersenne Twister** algorithm (MT19937). | Cryptographically Secure Pseudo-Random Number Generator (**CSPRNG**). |
| **Entropy Source** | Purely mathematical algorithm initialized by an internal seed (usually system time). | OS-level entropy pool (e.g., `/dev/urandom` on Unix/macOS, `CryptGenRandom` / `BCryptGenRandom` on Windows). |
| **Predictability** | **Deterministic & Predictable**. If an attacker observes approximately 624 consecutive 32-bit outputs, the internal state can be fully reconstructed, allowing future and past values to be predicted. | **Unpredictable**. Even with access to previous outputs, an attacker cannot compute subsequent outputs in polynomial time. |
| **Intended Use** | Simulations, statistical modeling, gaming, Monte Carlo algorithms. | Security-sensitive applications: passwords, authentication tokens, session IDs, cryptographic salts. |

**Summary**: Standard Python `random` is designed for speed and statistical uniformity, *not* security. `secrets` was introduced in Python 3.6 specifically to provide access to hardware/OS-level entropy, making it resistant to reverse engineering and state reconstruction.

---

### 2. What makes a password strong?

A password's security is measured mathematically by **information entropy** ($E = L \times \log_2(R)$), where $L$ is password length and $R$ is the size of the character pool:

1. **Length (Primary Factor)**:
   - Increasing password length exponentially increases the total possible permutations.
   - An 8-character password using 94 printable ASCII characters has $94^8 \approx 6.09 \times 10^{15}$ combinations (crackable in seconds to hours with modern GPUs).
   - A 16-character password has $94^{16} \approx 3.7 \times 10^{31}$ combinations, taking trillions of centuries to exhaustively brute-force.
2. **Character Diversity**:
   - Mixing uppercase, lowercase, numbers, and symbols maximizes the pool size ($R$), raising the base of the exponent.
3. **Absence of Predictable Patterns**:
   - Avoiding dictionary words, sequential characters (`abc`, `123`), keyboard walks (`qwerty`), and personal information (birthdays, names).
4. **Independent Randomness**:
   - Each position in the password must be chosen independently from a cryptographically secure random source, ensuring equal probability for all potential keys.

---

## 🛠️ Code Structure & Architecture

The script follows functional programming best practices with clear separation of concerns:

- `get_length(min_len, max_len)`: Handles user input for password length with range validation and type safety.
- `get_character_options()`: Prompts for character sets and verifies that at least one set is selected.
- `get_password_count(min_count, max_count)`: Validates how many passwords the user wants to produce.
- `build_character_pool(options)`: Concatenates active character sets into a unified pool and returns individual sets for guaranteed distribution.
- `generate_password(length, pool, guaranteed_sets)`: Guarantees at least one character per selected category, fills remaining length from the pool, and applies `secrets.SystemRandom().shuffle()`.
- `evaluate_strength(length, variety_count)`: Evaluates strength rating (`Weak`, `Medium`, `Strong`) using scoring heuristics based on length and variety.
- `display_results(...)`: Neatly formats outputs, summaries, and security disclaimers.
- `main()`: Orchestrates the overall program flow and supports repeated batch generation.

---

## 📄 License

This project is created for educational and internship demonstration purposes. Feel free to use and modify for learning!
