"""
CLI Password Generator (Level 1 Internship - Task 31)
=====================================================
A beginner-friendly, secure, and configurable command-line password generator
written in pure Python using only standard library modules (`secrets` and `string`).

Features:
- Validated password length (8 to 128 characters).
- Toggleable character sets: lowercase, uppercase, digits, and special symbols.
- Guaranteed inclusion of at least one character from each selected set.
- Cryptographically secure randomness powered by the OS via `secrets`.
- Unpredictable character order via `secrets.SystemRandom().shuffle()`.
- Password strength indicator (Weak / Medium / Strong).
- Pure in-memory display: never writes generated passwords to disk.
"""

import secrets
import string


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """
    Prompt the user for a yes/no response with a default value.
    Re-prompts until valid input ('y', 'yes', 'n', 'no', or empty) is provided.

    Args:
        prompt: The question to display to the user.
        default: The boolean value to return if the user presses Enter without typing.

    Returns:
        bool: True for yes, False for no.
    """
    hint = " [Y/n]: " if default else " [y/N]: "
    while True:
        choice = input(prompt + hint).strip().lower()
        if choice == "":
            return default
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("  [!] Please enter 'y' for yes or 'n' for no.")


def get_length(min_len: int = 8, max_len: int = 128) -> int:
    """
    Prompt the user for the desired password length and validate input.

    Re-prompts until a valid integer within the allowed range [min_len, max_len]
    is entered.

    Args:
        min_len: Minimum allowed length (default: 8).
        max_len: Maximum allowed length (default: 128).

    Returns:
        int: Validated password length.
    """
    while True:
        user_input = input(f"\nEnter password length ({min_len}-{max_len}): ").strip()
        try:
            length = int(user_input)
            if min_len <= length <= max_len:
                return length
            print(f"  [!] Invalid range: Length must be between {min_len} and {max_len}.")
        except ValueError:
            print("  [!] Invalid input: Please enter a whole numeric value.")


def get_character_options() -> dict[str, bool]:
    """
    Prompt the user to toggle each character type on or off.

    Ensures that at least one character type is selected before proceeding.
    If the user rejects all options, an error is displayed and the options
    are re-prompted.

    Returns:
        dict: Mapping of category names ('lowercase', 'uppercase', 'digits',
              'symbols') to their selected boolean status.
    """
    print("\nSelect character types to include:")
    while True:
        include_lower = ask_yes_no("  Include lowercase letters (a-z)?", default=True)
        include_upper = ask_yes_no("  Include uppercase letters (A-Z)?", default=True)
        include_digits = ask_yes_no("  Include digits (0-9)?", default=True)
        include_symbols = ask_yes_no("  Include special symbols (!@#$%...)?", default=True)

        # Reject the case where no character type is selected
        if include_lower or include_upper or include_digits or include_symbols:
            return {
                "lowercase": include_lower,
                "uppercase": include_upper,
                "digits": include_digits,
                "symbols": include_symbols,
            }

        print("\n  [!] Error: You must select at least one character type! Please try again.\n")


def get_password_count(min_count: int = 1, max_count: int = 100) -> int:
    """
    Prompt the user for the number of passwords to generate.

    Args:
        min_count: Minimum number of passwords (default: 1).
        max_count: Maximum number of passwords (default: 100).

    Returns:
        int: Validated number of passwords to generate.
    """
    while True:
        user_input = input(f"\nHow many passwords to generate ({min_count}-{max_count}) [Default: 1]: ").strip()
        if user_input == "":
            return 1
        try:
            count = int(user_input)
            if min_count <= count <= max_count:
                return count
            print(f"  [!] Count must be between {min_count} and {max_count}.")
        except ValueError:
            print("  [!] Invalid input: Please enter a whole numeric value.")


def build_character_pool(options: dict[str, bool]) -> tuple[str, list[str]]:
    """
    Build the full character pool and separate sets for guaranteed characters.

    Args:
        options: Dictionary indicating enabled character sets.

    Returns:
        tuple[str, list[str]]:
            - combined_pool: A string containing all selectable characters.
            - guaranteed_sets: A list of character set strings, one for each
              enabled category, used to ensure at least one character from
              every chosen category appears in the final password.
    """
    category_map = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "digits": string.digits,
        "symbols": string.punctuation,
    }

    guaranteed_sets = []
    combined_pool = ""

    for category, is_enabled in options.items():
        if is_enabled:
            charset = category_map[category]
            guaranteed_sets.append(charset)
            combined_pool += charset

    return combined_pool, guaranteed_sets


def generate_password(length: int, pool: str, guaranteed_sets: list[str]) -> str:
    """
    Generate a single cryptographically secure password.

    Steps:
    1. Guarantees at least one character from every selected category by picking
       one character from each set using `secrets.choice()`.
    2. Fills the remaining positions up to `length` from the full combined pool.
    3. Shuffles the character list in place using `secrets.SystemRandom().shuffle()`
       so the guaranteed characters do not appear in predictable initial positions.
    4. Converts the list back into a string and returns it.

    Args:
        length: Desired length of the password.
        pool: Combined string of all allowable characters.
        guaranteed_sets: List of strings representing each active category.

    Returns:
        str: Generated password string.
    """
    # Step 1: Guarantee at least one character from each selected category
    password_chars = [secrets.choice(charset) for charset in guaranteed_sets]

    # Step 2: Fill remaining characters randomly from the entire pool
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(pool))

    # Step 3: Cryptographically shuffle to prevent predictable placement
    secrets.SystemRandom().shuffle(password_chars)

    # Step 4: Join into a string
    return "".join(password_chars)


def evaluate_strength(length: int, variety_count: int) -> tuple[str, str]:
    """
    Calculate a simple password strength indicator based on length and character variety.

    Scoring logic:
    - Length score:
        >= 16 chars: 3 points
        12-15 chars: 2 points
        8-11 chars:  1 point
    - Variety score (number of character types selected):
        4 types:     3 points
        3 types:     2 points
        1-2 types:   1 point

    Strength Rating:
    - Strong (Score >= 5): Length >= 16 with 3+ types, or 12+ chars with all 4 types.
    - Medium (Score 3-4): Balanced combination, e.g., 12 chars with 2 types or 8-11 with 4 types.
    - Weak (Score < 3): Short length (8-11 chars) with only 1 or 2 character types.

    Args:
        length: Selected password length.
        variety_count: Number of selected character categories (1 to 4).

    Returns:
        tuple[str, str]: (Rating name, explanatory reason)
    """
    if length >= 16:
        length_score = 3
    elif length >= 12:
        length_score = 2
    else:
        length_score = 1

    if variety_count == 4:
        variety_score = 3
    elif variety_count == 3:
        variety_score = 2
    else:
        variety_score = 1

    total_score = length_score + variety_score

    if total_score >= 5:
        return "Strong", "Excellent length and diverse character variety."
    elif total_score >= 3:
        return "Medium", "Moderate strength. Consider 14+ characters and all 4 types for maximum security."
    else:
        return "Weak", "Short length or limited character types. Easily vulnerable to brute force."


def display_results(passwords: list[str], length: int, options: dict[str, bool]) -> None:
    """
    Format and display the generated password(s) and strength evaluation.

    Args:
        passwords: List of generated password strings.
        length: Selected password length.
        options: Dictionary of selected character categories.
    """
    active_types = [name.capitalize() for name, enabled in options.items() if enabled]
    strength_rating, strength_desc = evaluate_strength(length, len(active_types))

    print("\n" + "=" * 60)
    print("                    CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"  Length:            {length} characters")
    print(f"  Character Types:   {', '.join(active_types)} ({len(active_types)}/4)")
    print(f"  Strength Rating:   [{strength_rating.upper()}] - {strength_desc}")
    print("=" * 60)
    print("                    GENERATED PASSWORD(S)")
    print("=" * 60)

    for idx, pwd in enumerate(passwords, start=1):
        if len(passwords) == 1:
            print(f"\n  Password:  {pwd}\n")
        else:
            print(f"  [{idx:02d}]  {pwd}")

    print("=" * 60)
    print("  [Security Notice] Generated passwords are held strictly in memory")
    print("  and are NOT stored or written to any file automatically.")
    print("=" * 60)


def main() -> None:
    """
    Main driver function to run the CLI Password Generator.
    Controls workflow, collects input, generates passwords, and handles looping.
    """
    print("=" * 60)
    print("             CONFIGURABLE CLI PASSWORD GENERATOR")
    print("             Level 1 Internship Project (Task 31)")
    print("=" * 60)

    while True:
        # 1. Get validated password length
        length = get_length()

        # 2. Get validated character options
        options = get_character_options()

        # 3. Get number of passwords to generate
        count = get_password_count()

        # 4. Build character pool and guaranteed sets
        pool, guaranteed_sets = build_character_pool(options)

        # 5. Generate password(s)
        passwords = [
            generate_password(length, pool, guaranteed_sets)
            for _ in range(count)
        ]

        # 6. Display results
        display_results(passwords, length, options)

        # 7. Ask if the user wants to generate another batch
        print()
        if not ask_yes_no("Would you like to generate another batch?", default=False):
            print("\nThank you for using the CLI Password Generator. Stay secure!\n")
            break


if __name__ == "__main__":
    main()
