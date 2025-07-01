
DEF INPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER lscheinnr AS CHAR.

RUN new-lscheinnr.

PROCEDURE new-lscheinnr:
DEFINE buffer l-ophdr1 FOR l-ophdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
  s = "I" + SUBSTR(STRING(year(billdate)),3,2) + STRING(month(billdate), "99") 
     + STRING(day(billdate), "99"). 
  lscheinnr = s + STRING(i, "999"). 
  FIND FIRST l-ophdr1 WHERE l-ophdr1.datum =  billdate 
    AND l-ophdr1.op-typ = "STI" 
    AND SUBSTR(l-ophdr1.lscheinnr, 1, 10) = lscheinnr NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE l-ophdr1: 
    i = i + 1. 
    lscheinnr = s + STRING(i, "999"). 
    FIND FIRST l-ophdr1 WHERE l-ophdr1.datum =  billdate 
      AND l-ophdr1.op-typ = "STI" 
      AND SUBSTR(l-ophdr1.lscheinnr, 1, 10) = lscheinnr NO-LOCK NO-ERROR. 
  END. 
END. 
