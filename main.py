#!/usr/bin/env python3

import csv
from dataclasses import dataclass
from enum import Enum
import sys


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


def main():
    graph = {
        id_: (Person(first_name, last_name, Gender[gender]), mother_id, father_id)
        for (id_, first_name, last_name, gender, mother_id, father_id) in csv.reader(
            sys.stdin
        )
    }
    for person, mother_id, father_id in graph.values():
        person.mother = graph[mother_id][0] if mother_id != "" else None
        person.father = graph[father_id][0] if father_id != "" else None
    people = {id: person for id, (person, _, _) in graph.items()}

    for person in people.values():
        print(person)


if __name__ == "__main__":
    main()
