"""Demo: how to use is_reflexive from relations.py

Run this from the repository root or from the Relations directory. It prints
whether example relations are reflexive over a given domain.
"""

from relations import is_reflexive


def main() -> None:
    domain = {"a", "b", "c"}

    # A reflexive relation (contains (x,x) for every x in domain)
    rel1 = {("a", "a"), ("b", "b"), ("c", "c")}

    # Not reflexive (missing (b,b))
    rel2 = {("a", "a"), ("c", "c")}

    print("Domain:", domain)
    print("Relation 1:", rel1)
    print("is_reflexive(rel1, domain)", is_reflexive(rel1, domain))
    print()
    print("Relation 2:", rel2)
    print("is_reflexive(rel2, domain)", is_reflexive(rel2, domain))


if __name__ == "__main__":
    main()
