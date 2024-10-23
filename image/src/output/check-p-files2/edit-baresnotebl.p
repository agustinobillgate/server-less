DEFINE INPUT PARAMETER resnr LIKE bk-veran.veran-nr.
DEFINE OUTPUT PARAMETER efield AS CHARACTER.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr EXCLUSIVE-LOCK.
efield = bk-veran.bemerkung.
