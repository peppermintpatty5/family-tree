#!/usr/bin/env python3

from family import Relationship

table = [
    [Relationship(up, down, None).get_label() for up in range(6)] for down in range(6)
]
for row in table:
    print("\t".join(row))
