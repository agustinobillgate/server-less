DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE INPUT PARAMETER efield-screen-value AS CHARACTER.

/* Rulita 200225 | Fixing serverless issue git 616 */
FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN
DO:
    FIND CURRENT bk-veran EXCLUSIVE-LOCK.
    bk-veran.bemerkung = efield-screen-value.
    FIND CURRENT bk-veran NO-LOCK.
    RELEASE bk-veran.
END.
/* End Rulita*/
