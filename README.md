# family-tree

## How it works

Biologically speaking, every person has a mother and father.
Therefore a family tree can be represented as a [directed acyclic graph][1] with edges from each person to their parents.
Here is an example of a family tree with characters from *The Simpsons*.

| ID     | First name | Last name | Gender | Mother | Father |
| :----- | :--------- | :-------- | :----- | :----- | :----- |
| `4b78` | Abe        | Simpson   | ♂️      |        |        |
| `203c` | Bart       | Simpson   | ♂️      | `d4ed` | `57b9` |
| `b72b` | Clancy     | Bouvier   | ♂️      |        |        |
| `44f6` | Herb       | Powell    | ♂️      |        | `4b78` |
| `57b9` | Homer      | Simpson   | ♂️      | `8cc4` | `4b78` |
| `67cb` | Jackie     | Gurney    | ♀️      |        |        |
| `8c5d` | Lisa       | Simpson   | ♀️      | `d4ed` | `57b9` |
| `4b3c` | Maggie     | Simpson   | ♀️      | `d4ed` | `57b9` |
| `d4ed` | Marge      | Bouvier   | ♀️      | `67cb` | `b72b` |
| `7d2e` | Patty      | Bouvier   | ♀️      | `67cb` | `b72b` |
| `8cc4` | Mona       | Olsen     | ♀️      |        |        |
| `e049` | Selma      | Bouvier   | ♀️      | `67cb` | `b72b` |

> [!NOTE]
> I have used "random" hex IDs rather than sequential IDs so that no person appears more important than another.

### Relationship diagram

I recently discovered a photocopy of an interesting family relationship diagram.
Since the [original diagram][2] looks less than perfect, I have [recreated it here](./docs/relationship.pdf) using $\mathrm{\LaTeX}$ (no copyright infringement is intended).

<!-- Link definitions -->

[1]: <https://en.wikipedia.org/wiki/Directed_acyclic_graph> "Directed acyclic graph - Wikipedia"
[2]: <https://www.washingtonpost.com/news/wonk/wp/2015/11/26/a-great-big-guide-to-family-relations-you-never-understood/> "How to make sense of your family, in one chart - The Washington Post"
