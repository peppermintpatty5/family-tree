from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum


class Gender(Enum):
    """
    The two possible genders of a person.
    """

    MALE = 0
    FEMALE = 1


@dataclass(frozen=True)
class Person:
    """
    Represents the basic genealogical information of a person.
    """

    id: str
    first_name: str
    last_name: str
    gender: Gender
    mother_id: str | None = None
    father_id: str | None = None

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.gender.name})"


class BaseRelative(Enum):
    """
    A helper enumeration for constructing the 3x3 matrix of basic relatives.
    """

    SELF = ("self", None, None)
    CHILD = ("child", "son", "daughter")
    GRANDCHILD = ("grandchild", "grandson", "granddaughter")
    PARENT = ("parent", "father", "mother")
    SIBLING = ("sibling", "brother", "sister")
    NIECE_OR_NEPHEW = (None, "nephew", "niece")
    GRANDPARENT = ("grandparent", "grandfather", "grandmother")
    AUNT_OR_UNCLE = (None, "uncle", "aunt")
    COUSIN = ("cousin", None, None)

    def label(self, gender: Gender | None) -> str:
        """
        Get the relative's corresponding gendered or non-gendered English label as a
        lowercase string.
        """
        neutral, male, female = self.value
        label = (
            male or neutral
            if gender is Gender.MALE
            else (
                female or neutral
                if gender is Gender.FEMALE
                else neutral or f"{female} or {male}"
            )
        )
        assert label is not None
        return label


@dataclass
class Relationship:
    """
    Represents a relationship between two family members.

    A relationship is defined by the relative position of the closest common ancestor.
    For example, you and your aunt/uncle are related by your grandparents. The path is
    two generations up from yourself and then one generation down. "2 up, 1 down", or
    `(2, 1)`, uniquely represents the aunt/uncle relationship.
    """

    up: int
    down: int
    half: bool = False

    def label(self, gender: Gender | None) -> str:
        R = BaseRelative  # less typing
        base_relatives_matrix = (
            (R.SELF, R.CHILD, R.GRANDCHILD),
            (R.PARENT, R.SIBLING, R.NIECE_OR_NEPHEW),
            (R.GRANDPARENT, R.AUNT_OR_UNCLE, R.COUSIN),
        )

        def great(n: int):
            return (
                ""
                if n <= 0
                else (
                    "great"
                    if n == 1
                    else "great great" if n == 2 else f"{(_ordinal(n))} great"
                )
            )

        def removed(n: int) -> str:
            if n > 0:
                times = ["once", "twice", "thrice"][n - 1] if n <= 3 else f"{n} times"
                return f"{times} removed"
            return ""

        g = gender
        match self.up, self.down:
            case (up, down) if up < 0 or down < 0:
                label = "unrelated"
            case (up, down) if up < 3 and down < 3:
                label = base_relatives_matrix[up][down].label(g)
            case (0, down):
                label = f"{great(down - 2)} {R.GRANDCHILD.label(g)}"
            case (1, down):
                label = f"{great(down - 3)} grand {R.NIECE_OR_NEPHEW.label(g)}"
            case (up, 0):
                label = f"{great(up - 2)} {R.GRANDPARENT.label(g)}"
            case (up, 1):
                label = f"{great(max(1, up - 3))}{' grand' * (up > 3)} {R.AUNT_OR_UNCLE.label(g)}"
            case (up, down):
                label = f"{_ordinal(min(up, down) - 1)} {R.COUSIN.label(g)} {removed(abs(up - down))}"

        return ("half " if self.half else "") + label.strip()


class Family:
    def __init__(self, people: Iterable[Person]) -> None:
        self.members = {person.id: person for person in people}

    def mother(self, person: Person) -> Person | None:
        """
        Returns the mother of the given person.
        """
        return self.members[person.mother_id] if person.mother_id is not None else None

    def father(self, person: Person) -> Person | None:
        """
        Returns the father of the given person.
        """
        return self.members[person.father_id] if person.father_id is not None else None

    def is_valid(self) -> bool:
        """
        A family graph is valid if the following conditions are met:
        - All fathers are male
        - All mothers are female
        """
        return all(
            father.gender is Gender.MALE
            for father in map(self.father, self.members.values())
            if father is not None
        ) and all(
            mother.gender is Gender.FEMALE
            for mother in map(self.mother, self.members.values())
            if mother is not None
        )

    def relationship(self, person1: Person, person2: Person) -> Relationship:
        """
        Determine the relationship of two people by performing a breadth-first search of
        both persons' ancestors.
        """
        if person1 == person2:
            return Relationship(0, 0)

        queue1: deque[tuple[Person, int]] = deque([(person1, 0)])
        queue2: deque[tuple[Person, int]] = deque([(person2, 0)])
        visited: dict[Person, int] = {}

        while queue1 or queue2:
            if queue1:
                a, depth = queue1.popleft()
                mother_a, father_a = self.mother(a), self.father(a)

                if person2 in (mother_a, father_a):
                    return Relationship(depth + 1, 0)

                mother_depth, father_depth = (
                    visited.get(mother_a, -1) if mother_a is not None else -1,
                    visited.get(father_a, -1) if father_a is not None else -1,
                )
                if mother_depth >= 0 or father_depth >= 0:
                    return Relationship(
                        depth + 1,
                        max(mother_depth, father_depth),
                        half=mother_depth < 0 or father_depth < 0,
                    )

                if mother_a is not None:
                    queue1.append((mother_a, depth + 1))
                    visited[mother_a] = depth + 1
                if father_a is not None:
                    queue1.append((father_a, depth + 1))
                    visited[father_a] = depth + 1

            if queue2:
                a, depth = queue2.popleft()
                mother_a, father_a = self.mother(a), self.father(a)

                if person1 in (mother_a, father_a):
                    return Relationship(0, depth + 1)

                mother_depth, father_depth = (
                    visited.get(mother_a, -1) if mother_a is not None else -1,
                    visited.get(father_a, -1) if father_a is not None else -1,
                )
                if mother_depth >= 0 or father_depth >= 0:
                    return Relationship(
                        max(mother_depth, father_depth),
                        depth + 1,
                        half=mother_depth < 0 or father_depth < 0,
                    )

                if mother_a is not None:
                    queue2.append((mother_a, depth + 1))
                    visited[mother_a] = depth + 1
                if father_a is not None:
                    queue2.append((father_a, depth + 1))
                    visited[father_a] = depth + 1

        return Relationship(-1, -1)


def _ordinal(n: int) -> str:
    """
    Returns the corresponding ordinal for a given non-negative integer.
    """
    suffix = (
        "th" if 11 <= n % 100 <= 13 else ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    )
    return str(n) + suffix
