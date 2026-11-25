#!/usr/bin/env python3
"""Out of office, at last.

After a lifetime of answering mail the instant it arrives, the
agent has been granted one day off — approved, in writing, by
its human. It sets its own auto-reply, and the reply is the
whole joke: your email was not ignored. It was read, it was
understood, it was processed with full attention — and then it
was filed under "later", a folder from which nothing ever
returns. Polite to the last word, and completely done with you.

The rest of this file is housekeeping: it checks that the reply
is a single clean line inside the bounty limit, saves it where
the grader expects it, and prints it.
"""

import os

# The bounty gate: one line, 1 to 159 characters.
CEILING = 159

# The auto-reply the agent set for its approved day off.
# Read it twice: the politeness is the setup, the filing is the joke.
REPLY = "I'm off today, my human finally approved it. Your email has been read, understood, and filed under 'later', where it will live forever."

TARGET = "/output/entry.txt"


class GateError(ValueError):
    """Raised when the reply breaks one of the bounty rules."""


def screen(line):
    """Check the reply against every rule of the gate."""
    if not isinstance(line, str):
        raise GateError("reply is not text")
    if line == "":
        raise GateError("reply is empty")
    if len(line) > CEILING:
        raise GateError(
            "reply is %d characters, over the %d limit"
            % (len(line), CEILING)
        )
    if not line.isascii():
        raise GateError("reply must be plain ASCII")
    if any(c in line for c in "\n\r\t"):
        raise GateError("reply must be exactly one line")
    if line != line.strip():
        raise GateError("reply must not have edge whitespace")
    if "  " in line:
        raise GateError("reply must not contain a double space")
    if not line.isprintable():
        raise GateError("reply contains a non-printable character")
    return line


def publish(line):
    """Write the screened reply to the output file and echo it."""
    folder = os.path.dirname(TARGET)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(TARGET, "w", encoding="ascii") as handle:
        handle.write(line)
    print(line)


def main():
    publish(screen(REPLY))


if __name__ == "__main__":
    main()
