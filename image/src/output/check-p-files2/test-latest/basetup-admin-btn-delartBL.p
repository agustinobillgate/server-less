
DEF INPUT PARAMETER recid-bk-setup AS INT.

/* Rd, if available, recid, #369, 12-Des-24 */
/* FIND FIRST bk-setup WHERE RECID(bk-setup) = recid-bk-setup EXCLUSIVE-LOCK.
DELETE bk-setup.
RELEASE bk-setup. */

FIND FIRST bk-setup WHERE RECID(bk-setup) = recid-bk-setup NO-LOCK NO-ERROR.
IF AVAILABLE bk-setup THEN 
DO:
    FIND FIRST bk-setup EXCLUSIVE-LOCK.
    DELETE bk-setup.
END.
