
DEFINE BUFFER queasy1 FOR eg-vendor.

DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER vendor-bezeich AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER avail-sub AS LOGICAL INIT NO.

FIND FIRST eg-vendor WHERE RECID(eg-vendor) = rec-id.
IF curr-select = "chg" THEN
FIND FIRST queasy1 WHERE queasy1.bezeich = vendor-bezeich AND 
    ROWID(queasy1) NE ROWID(eg-vendor) NO-LOCK NO-ERROR.  
ELSE IF curr-select = "add" THEN
FIND FIRST queasy1 WHERE queasy1.bezeich = vendor-bezeich NO-LOCK NO-ERROR.  

if available queasy1 THEN avail-sub = YES.
