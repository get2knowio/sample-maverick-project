"""Multilingual proverbs and sayings for the fortune feature."""

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Proverb:
    """Represents a multilingual proverb or saying.

    Attributes:
        text: The proverb text in its original language
        language: Language name (matches Language.name)
        translation: Optional English translation (None if already in English)
    """

    text: str
    language: str
    translation: str | None = None


PROVERBS: list[Proverb] = [
    Proverb(
        text="A journey of a thousand miles begins with a single step.",
        language="English",
        translation=None,
    ),
    Proverb(
        text="Where there's a will, there's a way.",
        language="English",
        translation=None,
    ),
    Proverb(
        text="Petit à petit, l'oiseau fait son nid.",
        language="French",
        translation="Little by little, the bird builds its nest.",
    ),
    Proverb(
        text="L'habit ne fait pas le moine.",
        language="French",
        translation="The habit does not make the monk.",
    ),
    Proverb(
        text="No hay mal que por bien no venga.",
        language="Spanish",
        translation="There is no bad from which good doesn't come.",
    ),
    Proverb(
        text="A quien madruga, Dios le ayuda.",
        language="Spanish",
        translation="God helps those who wake up early.",
    ),
    Proverb(
        text="Aller Anfang ist schwer.",
        language="German",
        translation="All beginnings are difficult.",
    ),
    Proverb(
        text="Übung macht den Meister.",
        language="German",
        translation="Practice makes perfect.",
    ),
    Proverb(
        text="七転び八起き",
        language="Japanese",
        translation="Fall seven times, stand up eight.",
    ),
    Proverb(
        text="一期一会",
        language="Japanese",
        translation="One time, one meeting (treasure every encounter).",
    ),
    Proverb(
        text="千里之行，始于足下",
        language="Mandarin",
        translation="A journey of a thousand miles begins with a single step.",
    ),
    Proverb(
        text="学如逆水行舟，不进则退",
        language="Mandarin",
        translation="Learning is like rowing upstream; not to advance is to drop back.",
    ),
    Proverb(
        text="الصبر مفتاح الفرج",
        language="Arabic",
        translation="Patience is the key to relief.",
    ),
    Proverb(
        text="العلم نور",
        language="Arabic",
        translation="Knowledge is light.",
    ),
    Proverb(
        text="जहाँ चाह वहाँ राह",
        language="Hindi",
        translation="Where there is a will, there is a way.",
    ),
    Proverb(
        text="बूँद बूँद से सागर भरता है",
        language="Hindi",
        translation="Drop by drop fills the ocean.",
    ),
    Proverb(
        text="Haraka haraka haina baraka.",
        language="Swahili",
        translation="Hurry hurry has no blessing.",
    ),
    Proverb(
        text="Asiyefunzwa na mamaye hufunzwa na ulimwengu.",
        language="Swahili",
        translation="He who is not taught by his mother will be taught by the world.",
    ),
    Proverb(
        text="Devagar se vai ao longe.",
        language="Portuguese",
        translation="Slowly one goes far.",
    ),
    Proverb(
        text="Água mole em pedra dura, tanto bate até que fura.",
        language="Portuguese",
        translation="Soft water on hard stone hits until it pierces.",
    ),
]


def select_random_proverb() -> Proverb:
    """Select a random proverb from the PROVERBS list.

    Returns:
        A randomly selected Proverb object
    """
    return random.choice(PROVERBS)
