DEF TEMP-TABLE t-reservation LIKE reservation.

DEF INPUT  PARAMETER case-type AS INTEGER    NO-UNDO.
DEF INPUT  PARAMETER resNo     AS INTEGER    NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR t-reservation.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.
    
DEF VARIABLE hHandle AS HANDLE NO-UNDO.
hHandle = THIS-PROCEDURE.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST t-reservation NO-ERROR.
    FIND FIRST reservation WHERE reservation.resnr = resNo
      EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN
    DO:
      BUFFER-COPY t-reservation TO reservation.
      FIND CURRENT reservation NO-LOCK.
      RELEASE reservation.
      ASSIGN success-flag = YES.
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST reservation WHERE reservation.resnr = resNo
      EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
    IF AVAILABLE reservation THEN ASSIGN success-flag = YES.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST reservation WHERE reservation.resnr = resNo 
      EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN 
    DO:
      DELETE reservation.
      ASSIGN success-flag = YES.
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST t-reservation NO-ERROR.
    IF AVAILABLE t-reservation THEN
    DO:
        CREATE reservation.
        BUFFER-COPY t-reservation TO reservation.
        FIND CURRENT reservation NO-LOCK.
        success-flag = YES.
    END.
  END.
  WHEN 5 THEN
  DO:
      FIND FIRST reservation WHERE reservation.resnr = resNo 
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reservation THEN
      DO:
          reservation.activeflag = 0.
          FIND CURRENT reservation NO-LOCK.
          success-flag = YES.
      END.                                 
  END.
  WHEN 6 THEN
  DO:
      FIND FIRST reservation WHERE reservation.resnr = resNo 
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reservation THEN
      DO:
          reservation.verstat = 1.
          FIND CURRENT reservation NO-LOCK.
          success-flag = YES.
      END.                                 
  END.
  WHEN 7 THEN
  DO:
      FIND FIRST reservation WHERE reservation.resnr = resNo 
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reservation THEN
      DO:
          reservation.verstat = 0.
          FIND CURRENT reservation NO-LOCK.
          success-flag = YES.
      END.                                 
  END.
  WHEN 8 THEN
  DO:
  DEF VAR deposit       AS DECIMAL NO-UNDO.
  DEF VAR deposit-pay1  AS DECIMAL NO-UNDO.
  DEF VAR deposit-pay2  AS DECIMAL NO-UNDO.
      FIND FIRST t-reservation NO-ERROR.
      FIND FIRST reservation WHERE reservation.resnr = resNo
        EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reservation THEN
      DO:
        BUFFER-COPY t-reservation TO reservation.
        ASSIGN
            deposit = reservation.depositgef
            deposit-pay1 = reservation.depositbez
            deposit-pay2 = reservation.depositbez2
        .
        IF (- deposit-pay1 - deposit-pay2 ) GT deposit THEN
        ASSIGN reservation.depositgef = - deposit-pay1 - deposit-pay2.
        FIND CURRENT reservation NO-LOCK.
        RELEASE reservation.
        ASSIGN success-flag = YES.
      END.
  END.
  WHEN 9 THEN /* SY 02/12/2013 */
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo NO-LOCK NO-ERROR.
      IF NOT AVAILABLE res-line THEN
      DO:
        FIND FIRST reservation WHERE reservation.resnr = resNo 
          EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN 
        DO:
          DELETE reservation.
          ASSIGN success-flag = YES.
        END.
      END.
  END.

END CASE.

PROCEDURE delete-procedure:
    DELETE PROCEDURE hHandle NO-ERROR.
END.
