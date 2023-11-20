#!/usr/bin/env python3

from itertools import product
import sys

from family import Family, Relationship

family = Family.from_csv(sys.stdin)

if family.is_valid():
    table = [
        (
            f"{person1.first_name} {person1.last_name}",
            f"{person2.first_name} {person2.last_name}",
            Relationship.of(person1, person2).get_description(),
        )
        for person1, person2 in product(family.members.values(), repeat=2)
    ]

    for row in table:
        print("\t".join(row))
