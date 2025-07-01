

DEF INPUT  PARAMETER pvILanguage   AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER fl-temp AS LOGICAL INIT NO.

DEF VAR close-year AS DATE.
DEF VAR curr-month AS DATE.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "gljour-list". 

FIND FIRST htparam WHERE paramnr = 983 NO-LOCK. 
IF flogical THEN 
DO: 
  msg-str = translateExtended ("G/L closing process is running, journal transaction not possible",lvCAREA,"").
  fl-temp = NO.
END. 
ELSE
DO:
    FIND FIRST htparam WHERE paramnr = 795 NO-LOCK.
    close-year = htparam.fdate.
    FIND FIRST htparam WHERE paramnr = 597 NO-LOCK.
    curr-month = htparam.fdate.
    IF (YEAR(close-year) + 1) NE YEAR(curr-month) THEN 
    DO: 
        msg-str = msg-str + CHR(2) + "&W"
                + translateExtended ("Closing year has not been done.",lvCAREA,"").
    END.
    fl-temp = YES.
END.
