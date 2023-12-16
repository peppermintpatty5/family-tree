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
    (family.relationship(person1, person2), person1, person2)
    for person1 in family.members.values()
    for person2 in family.members.values()
)

for r, person1, person2 in relationships:
    print(
        "\t".join(
            [
                f"{person1.first_name} {person1.last_name}",
                f"{person2.first_name} {person2.last_name}",
                r.label(person2.gender),
            ]
        )
    )
