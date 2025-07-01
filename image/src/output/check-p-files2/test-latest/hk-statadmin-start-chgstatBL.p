DEFINE TEMP-TABLE bline-list 
  FIELD zinr AS CHAR 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD bl-recid AS INTEGER. 

DEF INPUT PARAMETER chgsort AS INT.
DEF INPUT PARAMETER TABLE FOR bline-list.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER t-zinr AS CHAR.
DEF OUTPUT PARAMETER t-zistatus AS INT INIT 0.

RUN start-chgstat.

PROCEDURE start-chgstat:
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE answer AS LOGICAL INITIAL NO. 
DEFINE buffer room FOR zimmer. 
 
  FIND FIRST bline-list WHERE selected = YES NO-ERROR. 
  IF NOT AVAILABLE bline-list THEN 
  DO: 
    flag = 1.
    RETURN. 
  END. 
 
  FIND FIRST zimmer WHERE zimmer.zinr = bline-list.zinr NO-LOCK NO-ERROR. 
  t-zinr = zimmer.zinr.
  t-zistatus = zimmer.zistatus.
  IF zimmer.zistatus = 8 AND chgsort NE 3 THEN 
  DO: 
    flag = 2.
    RETURN. 
  END. 
 
  IF chgsort = 8 AND zimmer.zistatus NE 4 THEN 
  DO: 
    flag = 3.
    RETURN. 
  END. 
 
  IF chgsort = 5 THEN 
  DO: 
    FIND NEXT bline-list WHERE selected = YES NO-LOCK NO-ERROR. 
    IF AVAILABLE bline-list THEN 
    DO: 
      flag = 4.
      RETURN. 
    END. 
 
    IF zimmer.zistatus GE 6 AND zimmer.zistatus LE 7 THEN 
    DO: 
      flag = 5.
      RETURN. 
    END. 
  END. 
 
  flag = 6.
END. 
