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
    id: int
    first_name: str
    last_name: str
    gender: Gender
    mother: "Person | None" = None
    father: "Person | None" = None


@dataclass
class Relationship:
    up: int
    down: int

    @classmethod
    def of(cls, person1: Person, person2: Person) -> Self:
        queue1: deque[tuple[Person, int]] = deque([(person1, 0)])
        queue2: deque[tuple[Person, int]] = deque([(person2, 0)])
        visited: dict[int, int] = {}

        while queue1 or queue2:
            if queue1:
                person, depth = queue1.popleft()
                if person.id in visited:
                    return cls(depth, visited[person.id])

                visited[person.id] = depth
                if person.mother is not None:
                    queue1.append((person.mother, depth + 1))
                if person.father is not None:
                    queue1.append((person.father, depth + 1))
            if queue2:
                person, depth = queue2.popleft()
                if person.id in visited:
                    return cls(visited[person.id], depth)

                visited[person.id] = depth
                if person.mother is not None:
                    queue2.append((person.mother, depth + 1))
                if person.father is not None:
                    queue2.append((person.father, depth + 1))

        return cls(-1, -1)

    def get_description(self) -> str:
        match (self.up, self.down):
            case (x, y) if x < 0 and y < 0:
                return "unrelated"
            case (0, 0):
                return "self"
            case (0, 1):
                return "child"
            case (0, 2):
                return "grandchild"
            case (0, 3):
                return "great grandchild"
            case (1, 0):
                return "parent"
            case (1, 1):
                return "sibling"
            case (1, 2):
                return "niece/nephew"
            case (2, 0):
                return "grandparent"
            case (2, 1):
                return "aunt/uncle"
            case (2, 2):
                return "cousin"
            case (3, 0):
                return "great grandparent"
            case _:
                return ""


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
