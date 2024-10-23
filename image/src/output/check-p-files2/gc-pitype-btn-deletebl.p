
DEF INPUT PARAMETER nr AS INT.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST reservation WHERE reservation.resart = nr NO-LOCK NO-ERROR. 
IF AVAILABLE reservation THEN 
DO:
  success-flag = NO.
  RETURN.
  /*MTHIDE MESSAGE NO-PAUSE. 
  MESSAGE translateExtended ("Reservation exists, deleting not possible.",lvCAREA,"") VIEW-AS ALERT-BOX. */
END. 
ELSE 
DO: 
  FIND FIRST gc-pitype WHERE gc-pitype.nr = nr EXCLUSIVE-LOCK.
  DELETE gc-pitype.
  success-flag = YES.
END.
