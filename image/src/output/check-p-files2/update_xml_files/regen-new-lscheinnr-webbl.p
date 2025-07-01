DEF INPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER lscheinnr AS CHAR.

DEF VAR s AS CHAR NO-UNDO.

s = "I" + SUBSTR(STRING(year(billdate)),3,2) + STRING(month(billdate), "99") + STRING(day(billdate), "99").

FOR EACH l-ophdr WHERE l-ophdr.op-typ EQ "STI" 
AND SUBSTR(l-ophdr.lscheinnr, 1, 7) EQ s
NO-LOCK BY l-ophdr.lscheinnr DESCENDING:
    lscheinnr = s + STRING(INT(SUBSTR(l-ophdr.lscheinnr, 8, 3)) + 1, "999").
    LEAVE.
END.

IF NOT AVAILABLE l-ophdr THEN 
    lscheinnr = s + STRING(1, "999").

