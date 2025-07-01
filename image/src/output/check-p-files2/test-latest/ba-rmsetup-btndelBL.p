
DEFINE INPUT PARAMETER rset-bezeich AS CHARACTER.

/* Rd, bezeich -> nung, 12-Des-24, #366 */

/* FIND FIRST bk-rset WHERE bk-rset.bezeich = rset-bezeich EXCLUSIVE-LOCK.
DELETE bk-rset. */

FIND FIRST bk-rset WHERE bk-rset.bezeichnung = rset-bezeich NO-LOCK NO-ERROR.
IF AVAILABLE bk-rset THEN 
DO:
    FIND CURRENT bk-rset EXCLUSIVE-LOCK.
    DELETE bk-rset.
END.
