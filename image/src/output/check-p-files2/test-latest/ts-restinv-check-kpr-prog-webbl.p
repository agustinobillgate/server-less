DEFINE INPUT-OUTPUT PARAMETER kpr-time AS INT.
DEFINE INPUT-OUTPUT PARAMETER kpr-recid AS INT.
DEFINE INPUT PARAMETER bill-date AS DATE.
DEFINE OUTPUT PARAMETER fl-code AS INT INIT 0.

IF (kpr-time - TIME) GE 300 THEN kpr-time = TIME.
IF kpr-recid = 0 THEN
DO:
    FIND FIRST vhp.queasy WHERE vhp.queasy.key = 3 
      AND vhp.queasy.number1 NE 0 
      AND (vhp.queasy.char1 NE "" OR vhp.queasy.char3 NE "") 
      AND (queasy.date1 EQ bill-date) NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN 
    ASSIGN kpr-recid = INTEGER(RECID(vhp.queasy)).
    kpr-time = TIME.
END.
ELSE IF kpr-recid NE 0 AND (TIME GT (kpr-time + 30)) THEN
DO:
    FIND FIRST vhp.queasy WHERE RECID(vhp.queasy) = kpr-recid
        NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy AND vhp.queasy.number1 NE 0 THEN
    DO:
        fl-code = 1.
    END.
    ASSIGN
      kpr-recid = 0
      kpr-time  = TIME
    .
END.
