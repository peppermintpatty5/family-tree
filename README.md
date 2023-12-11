# family-tree

## How it works

Biologically speaking, every person has a mother and father.
Therefore a family tree can be represented as a [directed acyclic graph][1] with edges from each person to their parents.
Here is an example of a family tree with characters from *The Simpsons*.

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
> I have used "random" hex IDs rather than sequential IDs so that no person appears more important than another.

### Relationship diagram

I recently discovered a photocopy of an interesting family relationship diagram.
Since the [original diagram][2] looks less than perfect, I have [recreated it here](./docs/relationship.pdf) using $\mathrm{\LaTeX}$ (no copyright infringement is intended).

<!-- Link definitions -->

[1]: <https://en.wikipedia.org/wiki/Directed_acyclic_graph> "Directed acyclic graph - Wikipedia"
[2]: <https://www.washingtonpost.com/news/wonk/wp/2015/11/26/a-great-big-guide-to-family-relations-you-never-understood/> "How to make sense of your family, in one chart - The Washington Post"
