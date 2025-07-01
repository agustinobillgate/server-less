
DEF BUFFER sub FOR eg-staff.

DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER staff-nr AS INT.
DEF INPUT PARAMETER curr-select AS CHAR.
DEF OUTPUT PARAMETER avail-sub AS LOGICAL INIT NO.

FIND FIRST eg-staff WHERE RECID(eg-staff) = rec-id.

IF curr-select = "chg" THEN
    FIND FIRST sub WHERE sub.nr = staff-nr AND 
    ROWID(sub) NE ROWID(eg-staff) NO-LOCK NO-ERROR.
ELSE IF curr-select = "add" THEN
    FIND FIRST sub WHERE sub.nr = staff-nr NO-LOCK NO-ERROR.

IF AVAILABLE sub THEN avail-sub = YES.
