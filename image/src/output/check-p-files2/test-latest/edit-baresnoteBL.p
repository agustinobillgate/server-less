DEFINE INPUT PARAMETER resnr LIKE bk-veran.veran-nr.
DEFINE OUTPUT PARAMETER efield AS CHARACTER.

/* Rulita 200225 | Fixing serverless issue git 617 */
FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN efield = bk-veran.bemerkung.
/* End Rulita*/