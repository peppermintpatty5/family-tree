from collections import deque
import csv
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Self


class Gender(Enum):
    """
    The two possible genders of a person.
    """

    MALE = 0
    FEMALE = 1


@dataclass
class Person:
    """
    Represents the basic genealogical information of a person.
    """

    id: int
    first_name: str
    last_name: str
    gender: Gender
    mother: "Person | None" = None
    father: "Person | None" = None


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
            else female or neutral
            if gender is Gender.FEMALE
            else neutral or f"{female} or {male}"
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
    gender: Gender | None

    @classmethod
    def of(cls, person1: Person, person2: Person) -> Self:
        queue1: deque[tuple[Person, int]] = deque([(person1, 0)])
        queue2: deque[tuple[Person, int]] = deque([(person2, 0)])
        visited: dict[int, int] = {}

        while queue1 or queue2:
            if queue1:
                person, depth = queue1.popleft()
                if person.id in visited:
                    return cls(depth, visited[person.id], person2.gender)

                visited[person.id] = depth
                if person.mother is not None:
                    queue1.append((person.mother, depth + 1))
                if person.father is not None:
                    queue1.append((person.father, depth + 1))
            if queue2:
                person, depth = queue2.popleft()
                if person.id in visited:
                    return cls(visited[person.id], depth, person2.gender)

                visited[person.id] = depth
                if person.mother is not None:
                    queue2.append((person.mother, depth + 1))
                if person.father is not None:
                    queue2.append((person.father, depth + 1))

        return cls(-1, -1, person2.gender)

    def label(self) -> str:
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
                else "great"
                if n == 1
                else "great great"
                if n == 2
                else f"{(_ordinal(n))} great"
            )

        def removed(n: int) -> str:
            if n > 0:
                times = ["once", "twice", "thrice"][n - 1] if n <= 3 else f"{n} times"
                return f"{times} removed"
            return ""

        g = self.gender
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
                label = (
                    f"{great(max(1, up - 3))}{" grand" * (up > 3)} {R.AUNT_OR_UNCLE.label(g)}"
                )
            case (up, down):
                label = (
                    f"{_ordinal(min(up, down) - 1)} {R.COUSIN.label(g)} {removed(abs(up - down))}"
                )

        return label.strip()


@dataclass
class Family:
    members: dict[int, Person]

    @classmethod
    def from_csv(cls, csv_file: Iterable[str]) -> Self:
        graph = {
            int(id, base=16): (
                Person(int(id, base=16), first_name, last_name, Gender[gender]),
                int(mother_id, base=16) if mother_id != "" else None,
                int(father_id, base=16) if father_id != "" else None,
            )
            for (
                id,
                first_name,
                last_name,
                gender,
                mother_id,
                father_id,
            ) in csv.reader(csv_file)
        }
        for person, mother_id, father_id in graph.values():
            person.mother = graph[mother_id][0] if mother_id is not None else None
            person.father = graph[father_id][0] if father_id is not None else None

        return cls({person.id: person for person, _, _ in graph.values()})

    def is_valid(self) -> bool:
        """
        A family graph is valid if the following conditions are met:
        - All fathers are male
        - All mothers are female
        """
        return all(
            person.father.gender is Gender.MALE
            for person in self.members.values()
            if person.father is not None
        ) and all(
            person.mother.gender is Gender.FEMALE
            for person in self.members.values()
            if person.mother is not None
        )


def _ordinal(n: int) -> str:
    """
    Returns the corresponding ordinal for a given non-negative integer.
    """
    suffix = (
        "th" if 11 <= n % 100 <= 13 else ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    )
    return str(n) + suffix
