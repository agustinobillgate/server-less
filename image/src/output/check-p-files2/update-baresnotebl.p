DEFINE INPUT PARAMETER resnr AS INT.
DEFINE INPUT PARAMETER efield-screen-value AS CHARACTER.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr EXCLUSIVE-LOCK.
FIND CURRENT bk-veran EXCLUSIVE-LOCK.
bk-veran.bemerkung = efield-screen-value.
FIND CURRENT bk-veran NO-LOCK.
