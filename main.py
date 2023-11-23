#!/usr/bin/env python3

import sys
from family import Family, Relationship

family = Family.from_csv(sys.stdin)
relationships = (
    Relationship.of(person1, person2)
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
