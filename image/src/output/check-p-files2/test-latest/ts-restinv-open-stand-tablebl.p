
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER curr-waiter AS INT.

DEF OUTPUT PARAMETER tischNo AS INT.
DEF OUTPUT PARAMETER openbill-found AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER tbuff       FOR vhp.tisch.
DEF BUFFER tbuff1      FOR vhp.tisch.
DEF BUFFER hbuff       FOR vhp.h-bill.

  FIND FIRST tbuff WHERE tbuff.departement = curr-dept 
    AND tbuff.roomcharge NO-LOCK NO-ERROR.
  IF NOT AVAILABLE tbuff THEN
  DO:
    fl-code = 1.
    RETURN.
  END.
  FIND FIRST tbuff WHERE tbuff.departement = curr-dept 
    AND tbuff.roomcharge 
    AND tbuff.kellner-nr = curr-waiter NO-LOCK NO-ERROR.
  IF AVAILABLE tbuff THEN 
  DO:
    ASSIGN tischNo = tbuff.tischnr.
    FIND FIRST hbuff WHERE hbuff.departement = curr-dept
      AND hbuff.tischnr = tbuff.tischnr AND hbuff.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE hbuff AND hbuff.saldo NE 0 THEN openbill-found = YES.
  END.
  ELSE
  DO:
    FOR EACH tbuff WHERE tbuff.departement = curr-dept 
      AND tbuff.roomcharge AND tbuff.kellner-nr = 0 NO-LOCK BY tbuff.tischnr:
      FIND FIRST hbuff WHERE hbuff.departement = curr-dept
        AND hbuff.tischnr = tbuff.tischnr AND hbuff.flag = 0 NO-LOCK NO-ERROR.
      IF NOT AVAILABLE hbuff THEN
      DO TRANSACTION:
        tischNo = tbuff.tischnr.
        FIND FIRST tbuff1 WHERE RECID(tbuff1) = RECID(tbuff) EXCLUSIVE-LOCK.
        ASSIGN tbuff1.kellner-nr = curr-waiter.
        FIND CURRENT tbuff1 NO-LOCK.
        LEAVE.
      END.
    END.
  END.
  IF tischNo = 0 THEN
  DO:
    fl-code = 2.
    RETURN.
  END.
