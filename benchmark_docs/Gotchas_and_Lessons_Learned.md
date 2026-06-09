# Gotchas and Lessons Learned

## 1. TopoIndex Does Not Always Converge

Problem:

TopoIndex repeatedly stopped during:

"Correcting cell index numbers"

without generating valid routing files.

Lesson:

A valid-looking flow direction grid is not sufficient. TopoIndex requires a fully convergent drainage network.

---

## 2. GRASS Flow Directions Are Not ESRI Directions

GRASS drainage outputs use their own numbering system.

TRIGRS TopoIndex expects a different numbering scheme.

Lesson:

Always verify direction numbering before conversion.

---

## 3. D8 Conversion Is Easy To Get Wrong

Several direction mappings were tested.

Different software packages use different conventions.

Lesson:

Never assume D8 codes are interchangeable.

---

## 4. TRIGRS Can Run Without TopoIndex

Using:

nxtfil = none
ndxfil = none
dscfil = none
wffil = none

TRIGRS successfully computed Factor of Safety.

Lesson:

TopoIndex is optional for basic TRIGRS implementation.

---

## 5. No Rainfall Means Almost No Temporal Change

Current run used:

rifil = none

Result:

FoS at 0 h, 10 h, 20 h and 40 h were nearly identical.

Lesson:

Rainfall forcing is required for meaningful transient behavior.

---

## 6. Current Results Are Not Wayanad-Specific

The DEM is real.

The soil parameters are not.

Current simulations use Srivastava and Yeh benchmark parameters.

Lesson:

These results validate workflow implementation, not real hazard conditions.

---

## 7. Save Progress Frequently

Multiple power outages interrupted work.

Lesson:

Commit successful milestones to GitHub immediately.

---

## 8. Verify Outputs Quantitatively

Do not rely only on maps.

Always compute:

* Min FoS
* Mean FoS
* Max FoS
* Stability class percentages

before interpretation.

---

## 9. Distinguish Validation From Scientific Analysis

Current work:

Workflow validation.

Future work:

Real Wayanad geotechnical parameters and rainfall forcing.

These are different objectives and should not be confused.

---

## Final Takeaway

The primary achievement of this phase was demonstrating a successful TRIGRS implementation on the Wayanad DEM and documenting the limitations before moving to realistic landslide simulations.

