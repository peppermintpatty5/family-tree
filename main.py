#!/usr/bin/env python3

import csv
from dataclasses import dataclass
from enum import Enum
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
        for person in family.members.values():
            print(person)


if __name__ == "__main__":
    main()
