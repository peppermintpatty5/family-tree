# family-tree

## How it works

Biologically speaking, every person has a mother and father. Therefore a family tree can be represented as a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) with edges from each person to their parents. Here is an example of a family tree with characters from *The Simpsons*.

| ID     | First name  | Last name | Gender        | Mother | Father |
| :----- | :---------- | :-------- | :------------ | :----- | :----- |
| `8114` | Abraham     | Simpson   | :male_sign:   |        |        |
| `4a0c` | Bartholomew | Simpson   | :male_sign:   | `5212` | `57b9` |
| `b72b` | Clancy      | Bouvier   | :male_sign:   |        |        |
| `167b` | Gaby        |           | :female_sign: |        |        |
| `9ca0` | Herbert     | Powell    | :male_sign:   | `167b` | `8114` |
| `57b9` | Homer       | Simpson   | :male_sign:   | `0b36` | `8114` |
| `c069` | Jacqueline  | Gurney    | :female_sign: |        |        |
| `8c5d` | Lisa        | Simpson   | :female_sign: | `5212` | `57b9` |
| `55d3` | Margaret    | Simpson   | :female_sign: | `5212` | `57b9` |
| `5212` | Marjorie    | Bouvier   | :female_sign: | `c069` | `b72b` |
| `7d2e` | Patty       | Bouvier   | :female_sign: | `c069` | `b72b` |
| `0b36` | Penelope    | Olsen     | :female_sign: |        |        |
| `e049` | Selma       | Bouvier   | :female_sign: | `c069` | `b72b` |

> [!NOTE]
> I have opted to use "random" hex IDs instead of row indices. This eliminates the dilemma of which person to list first as row ordering becomes inconsequential.

## Relationship diagram

### Tree form

```txt
                                                ┌────┴────┐
                                                │ Great x3│
                                                │ G-parent│
                                                └────┬────┘
                                         ┌───────────┴───────────┐
                                    ┌────┴────┐             ┌────┴────┐
                                    │ Great x2│             │ Great x2│
                                    │ G-parent│             │ Grnd A/U│
                                    └────┬────┘             └────┬────┘
                              ┌──────────┴───────────┐           │
                         ┌────┴────┐            ┌────┴────┐ ┌────┴────┐
                         │ Great   │            │ Great   │ │ 1st Csn │
                         │ G-parent│            │ Grnd A/U│ │ rm x3   │
                         └────┬────┘            └────┬────┘ └────┬────┘
                    ┌─────────┴──────────┐           │           │
               ┌────┴────┐          ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
               │ Grand-  │          │ Great   │ │ 1st Csn │ │ 2nd Csn │
               │ parent  │          │ A/U     │ │ rm x2   │ │ rm x2   │
               └────┬────┘          └────┬────┘ └────┬────┘ └────┬────┘
           ┌────────┴────────┐           │           │           │
      ┌────┴────┐       ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
      │ Parent  │       │ Aunt /  │ │ 1st Csn │ │ 2nd Csn │ │ 3rd Csn │
      │         │       │ Uncle   │ │ rm x1   │ │ rm x1   │ │ rm x1   │
      └────┬────┘       └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     ┌─────┴─────┐           │           │           │           │
┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
│ Self    │ │ Sibling │ │ 1st     │ │ 2nd     │ │ 3rd     │ │ 4th     │
│         │ │         │ │ Cousin  │ │ Cousin  │ │ Cousin  │ │ Cousin  │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │           │
┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
│ Child   │ │ Niece / │ │ 1st Csn │ │ 2nd Csn │ │ 3rd Csn │
│         │ │ Nephew  │ │ rm x1   │ │ rm x1   │ │ rm x1   │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │
┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
│ Grand-  │ │ Grand   │ │ 1st Csn │ │ 2nd Csn │
│ child   │ │ Niece   │ │ rm x2   │ │ rm x2   │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
┌────┴────┐ ┌────┴────┐ ┌────┴────┐
│ Great   │ │ Great G │ │ 1st Csn │
│ G-child │ │ Nephew  │ │ rm x3   │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │
┌────┴────┐ ┌────┴────┐
│ Great x2│ │ Great x2│
│ G-child │ │ G Niece │
└────┬────┘ └────┬────┘
     │
┌────┴────┐
│ Great x3│
│ G-child │
└────┬────┘
```

### Matrix form

In the tree above the rows are aligned by generation. If you tilt your head to the left, you can see that each row forms the diagonal of a matrix.

|              | **`up=0`**             | **`up=1`**              | **`up=2`**                | **`up=3`**               | **`up=4`**               | **`up=5`**                |
| -----------: | :--------------------- | :---------------------- | :------------------------ | :----------------------- | :----------------------- | :------------------------ |
| **`down=0`** | Self                   | Parent                  | Grandparent               | Great Grandparent        | Great Great Grandparent  | 3rd Great Grandparent     |
| **`down=1`** | Child                  | Sibling                 | Aunt or Uncle             | Great Aunt or Uncle      | Great Grand Uncle        | Great Great Grand Aunt    |
| **`down=2`** | Grandchild             | Niece or Nephew         | 1st Cousin                | 1st Cousin once removed  | 1st Cousin twice removed | 1st Cousin thrice removed |
| **`down=3`** | Great Grandchild       | Grand Niece or Nephew   | 1st Cousin once removed   | 2nd Cousin               | 2nd Cousin once removed  | 2nd Cousin twice removed  |
| **`down=4`** | Great Great Grandchild | Great Grand Nephew      | 1st Cousin twice removed  | 2nd Cousin once removed  | 3rd Cousin               | 3rd Cousin once removed   |
| **`down=5`** | 3rd Great Grandchild   | Great Great Grand Niece | 1st Cousin thrice removed | 2nd Cousin twice removed | 3rd Cousin once removed  | 4th Cousin                |
