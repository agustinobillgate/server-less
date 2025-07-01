DEFINE INPUT PARAMETER gName        AS CHARACTER.
DEFINE INPUT PARAMETER startDate    AS DATE.
DEFINE OUTPUT PARAMETER blockCode   AS CHARACTER.

DEFINE VARIABLE iCounter            AS INTEGER      NO-UNDO.

ASSIGN 
    iCounter    = 0
    gName       = REPLACE(gName, " ", "")
    gName       = SUBSTRING(gName, 1, 4).

FIND LAST bk-master WHERE bk-master.name EQ gName
  AND bk-master.startdate EQ startDate NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN 
DO:
    iCounter    = INTEGER(ENTRY(2, bk-master.block-code, "/")) + 1.
END.
ELSE 
DO:
    iCounter    = 1.
END.

blockCode   = gName + STRING(YEAR(startDate), "9999") + STRING(MONTH(startDate), "99") + STRING(DAY(startDate), "99") + "/" + STRING(iCounter, "99").
