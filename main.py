#!/usr/bin/env python3

from collections.abc import Iterable
import csv
import sys

from family import Family, Gender, Person


def from_csv(csv_file: Iterable[str]) -> list[Person]:
    """
    Read a list of people from a CSV file.
    """
    return [
        Person(
            id,
            first_name,
            last_name,
            Gender[gender],
            mother_id if mother_id != "" else None,
            father_id if father_id != "" else None,
        )
        for (id, first_name, last_name, gender, mother_id, father_id) in csv.reader(
            csv_file
        )
    ]


people = from_csv(sys.stdin)
family = Family(people)
relationships = (
    family.relationship(person1, person2)
    for person1 in family.members.values()
    for person2 in family.members.values()
)

for r in relationships:
    print(
        "\t".join(
            [
                f"{r.person1.first_name} {r.person1.last_name}",
                f"{r.person2.first_name} {r.person2.last_name}",
                r.label(),
            ]
        )
    )
