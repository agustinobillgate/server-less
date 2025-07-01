
DEF INPUT PARAMETER g-nr AS INT.
DEF OUTPUT PARAMETER  flag AS INT INIT 0.

FIND FIRST reservation WHERE 
  reservation.resart = g-nr NO-LOCK NO-ERROR. 
IF AVAILABLE reservation THEN flag = 1.
ELSE 
DO: 
    FIND FIRST gc-piacct WHERE gc-piacct.nr = g-nr.
    FIND CURRENT gc-piacct EXCLUSIVE-LOCK. 
    DELETE gc-piacct.
    RELEASE gc-piacct.
END.
