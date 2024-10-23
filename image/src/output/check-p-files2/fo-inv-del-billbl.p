DEFINE INPUT PARAMETER bil-recid    AS INTEGER.
DEFINE OUTPUT PARAMETER msgStr      AS CHARACTER.

DEFINE VARIABLE curr-recid AS INTEGER.
DEFINE BUFFER t-bill FOR bill.

FIND FIRST t-bill WHERE RECID(t-bill) = bil-recid EXCLUSIVE-LOCK.
IF AVAILABLE t-bill THEN
DO:
    DELETE t-bill NO-ERROR.
    RELEASE t-bill NO-ERROR.
    msgStr = "Bill Deleted".
END.
ELSE
DO:
    msgStr = "Can't found bill record id".
END.

