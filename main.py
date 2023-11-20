#!/usr/bin/env python3

from collections import deque
import csv
from dataclasses import dataclass
from enum import Enum
from itertools import product
import sys
from typing import Iterable, Self


class Gender(Enum):
    MALE = 0
    FEMALE = 1


@dataclass
class Person:
    first_name: str
    last_name: str
    gender: Gender
    mother: "Person | None" = None
    father: "Person | None" = None

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name} ({self.gender.name})"

    def get_distance(self, other: "Person") -> tuple[int, int] | None:
        queue1: deque[tuple[Person, int]] = deque([(self, 0)])
        queue2: deque[tuple[Person, int]] = deque([(other, 0)])
        visited: dict[int, int] = {}

        while queue1 or queue2:
            if queue1:
                person, depth = queue1.popleft()
                if id(person) in visited:
                    return (depth, visited[id(person)])

                visited[id(person)] = depth
                if person.mother is not None:
                    queue1.append((person.mother, depth + 1))
                if person.father is not None:
                    queue1.append((person.father, depth + 1))
            if queue2:
                person, depth = queue2.popleft()
                if id(person) in visited:
                    return (visited[id(person)], depth)

                visited[id(person)] = depth
                if person.mother is not None:
                    queue2.append((person.mother, depth + 1))
                if person.father is not None:
                    queue2.append((person.father, depth + 1))

        return None


class Relationship:
    @staticmethod
    def get_description(pair: tuple[int, int] | None) -> str:
        match pair:
            case None:
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
    members: dict[str, Person]

    @classmethod
    def from_csv(cls, csv_file: Iterable[str]) -> Self:
        graph = {
            id_: (Person(first_name, last_name, Gender[gender]), mother_id, father_id)
            for (
                id_,
                first_name,
                last_name,
                gender,
                mother_id,
                father_id,
            ) in csv.reader(csv_file)
        }
        for person, mother_id, father_id in graph.values():
            person.mother = graph[mother_id][0] if mother_id != "" else None
            person.father = graph[father_id][0] if father_id != "" else None

        return cls({id_: person for id_, (person, _, _) in graph.items()})

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


def main():
    family = Family.from_csv(sys.stdin)

    if family.is_valid():
        table = [
            (
                f"{person1.first_name} {person1.last_name}",
                f"{person2.first_name} {person2.last_name}",
                Relationship.get_description(person1.get_distance(person2)),
            )
            for person1, person2 in product(family.members.values(), repeat=2)
        ]

        for row in table:
            print("\t".join(row))


if __name__ == "__main__":
    main()
