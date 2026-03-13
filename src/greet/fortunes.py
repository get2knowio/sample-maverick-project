from dataclasses import dataclass


@dataclass(frozen=True)
class Proverb:
    text: str
    source: str


PROVERBS: list[Proverb] = [
    Proverb(
        text="The journey of a thousand miles begins with one step.",
        source="Lao Tzu",
    ),
    Proverb(
        text="In the middle of difficulty lies opportunity.",
        source="Albert Einstein",
    ),
    Proverb(
        text="It does not matter how slowly you go as long as you do not stop.",
        source="Confucius",
    ),
    Proverb(
        text="Fall seven times, stand up eight.",
        source="Japanese proverb",
    ),
    Proverb(
        text=(
            "When the winds of change blow,"
            " some build walls and others build windmills."
        ),
        source="Chinese proverb",
    ),
    Proverb(
        text="A smooth sea never made a skilled sailor.",
        source="English proverb",
    ),
    Proverb(
        text="The pen is mightier than the sword.",
        source="Edward Bulwer-Lytton",
    ),
    Proverb(
        text="To know the road ahead, ask those coming back.",
        source="Chinese proverb",
    ),
    Proverb(
        text="Ubuntu: I am because we are.",
        source="African proverb",
    ),
    Proverb(
        text="Even the longest night will end and the sun will rise.",
        source="Victor Hugo",
    ),
    Proverb(
        text="Knowledge is a treasure, but practice is the key to it.",
        source="Thomas Fuller",
    ),
    Proverb(
        text=(
            "He who asks a question is a fool for five minutes;"
            " he who does not ask remains a fool forever."
        ),
        source="Chinese proverb",
    ),
    Proverb(
        text=(
            "The forest would be silent if no bird sang except the one that sang best."
        ),
        source="Henry van Dyke",
    ),
    Proverb(
        text="Little by little, a little becomes a lot.",
        source="Tanzanian proverb",
    ),
    Proverb(
        text="Do not wait to strike till the iron is hot; make it hot by striking.",
        source="W.B. Yeats",
    ),
    Proverb(
        text=(
            "The best time to plant a tree was twenty years ago."
            " The second best time is now."
        ),
        source="Chinese proverb",
    ),
    Proverb(
        text="Courage is not the absence of fear, but the triumph over it.",
        source="Nelson Mandela",
    ),
    Proverb(
        text="What you do today can improve all your tomorrows.",
        source="Ralph Marston",
    ),
    Proverb(
        text="An unexamined life is not worth living.",
        source="Socrates",
    ),
    Proverb(
        text=(
            "We are what we repeatedly do."
            " Excellence, then, is not an act, but a habit."
        ),
        source="Aristotle",
    ),
]
