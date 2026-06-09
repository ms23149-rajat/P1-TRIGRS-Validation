# TopoIndex Investigation

## Objective

Generate runoff-routing files for TRIGRS using TopoIndex.

## Problem

TopoIndex repeatedly stopped during:

"Correcting cell index numbers"

without successfully completing.

## Approaches Tested

### Attempt 1

Python-generated D8 flow directions.

Result:
Non-convergence.

### Attempt 2

GRASS-generated flow directions.

Result:
Direction-format mismatch.

### Attempt 3

ESRI D8 conversion.

Result:
TopoIndex still failed to converge.

### Attempt 4

Increased correction iterations.

Result:
No improvement.

### Attempt 5

Loop-detection and correction.

Result:
Did not fully resolve the issue.

## Observations

The flow network repeatedly produced non-converging correction cycles.

## Decision

Proceed with TRIGRS without runoff-routing files.

TRIGRS allows:

nxtfil = none

ndxfil = none

dscfil = none

wffil = none

and still computes infiltration and Factor of Safety.

## Conclusion

TopoIndex remains unresolved for the Wayanad dataset and requires future investigation.
