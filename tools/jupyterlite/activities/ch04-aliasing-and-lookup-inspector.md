---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Aliasing and Lookup Inspector: predict → run → explain → revise

**Predict.** A shallow copy makes a new outer list but can retain its inner
lists. Before running the cells, predict which copy mode—`"assignment"`,
`"shallow"`, or `"deep"`—will change the original center temperature after the
working grid is changed. The temperatures are in degrees Celsius.

```{code-cell} python
import copy


def copy_grid(grid, copy_mode):
    """Return a grid under an explicit ownership contract.

    ``assignment`` shares every object, ``shallow`` creates a new outer list,
    and ``deep`` recursively copies this built-in nested-list grid.
    """
    if copy_mode == "assignment":
        return grid
    if copy_mode == "shallow":
        return grid.copy()
    if copy_mode == "deep":
        return copy.deepcopy(grid)
    raise ValueError("copy_mode must be assignment, shallow, or deep")
```

```{code-cell} python
# Cell 2: change one copy mode at a time and predict before rerunning.
initial_grid_C = [
    [20.0, 20.0, 20.0],
    [20.0, 50.0, 20.0],
    [20.0, 20.0, 20.0],
]

for copy_mode in ("assignment", "shallow", "deep"):
    original = copy.deepcopy(initial_grid_C)
    working = copy_grid(original, copy_mode)
    working[1][1] = 35.0
    print(
        f"{copy_mode:10s}; original center={original[1][1]:4.1f} C; "
        f"same middle row? {original[1] is working[1]}"
    )
```

```{code-cell} python
# Cell 3: a representation decision is a contract, not an automatic upgrade.
particle_ids_in_order = ["p004", "p002", "p004", "p009"]
particle_records = {
    "p002": {"mass_g": 2.0e30},
    "p004": {"mass_g": 1.0e30},
    "p009": {"mass_g": 3.0e30},
}
processed_ids = set(particle_ids_in_order)

print("List preserves arrival order and duplicates:", particle_ids_in_order)
print("Set records unique processed IDs:", processed_ids)
print("Dict maps a known ID to its record:", particle_records["p004"])
```

## Explain the result

1. Which modes changed the original grid? Which nested object was shared?
2. A numerical time-stepper needs both the previous and next temperature field.
   Which ownership contract would you choose, and why might a ping-pong buffer
   be preferable to a deep copy in a long run?
3. If an analysis must preserve arrival order, retain duplicates, and look up a
   record by ID, why might it legitimately use all three structures above?

## Revise the design

Change `copy_mode` to one value at a time and add an assertion that expresses
the ownership contract you expect. Then add one particle ID to
`particle_ids_in_order` and decide whether the set or the list should preserve
that change for your stated question.

**Success condition.** You can identify shared versus independent nested state,
write an ownership expectation, and justify a list, set, or dictionary from an
access requirement rather than from a generic speed claim.

This activity demonstrates Python object ownership and simple collection
contracts. It does **not** select a production data layout, benchmark a
simulation, choose a physical spatial-index policy, or validate a numerical
model.
