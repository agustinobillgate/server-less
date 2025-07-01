DEFINE TEMP-TABLE t-bill LIKE bill.

DEF INPUT PARAMETER TABLE FOR t-bill.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST t-bill NO-ERROR.
IF AVAILABLE t-bill THEN
DO:
  FIND FIRST bill WHERE bill.rechnr = t-bill.rechnr
    EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE bill THEN CREATE bill.

  BUFFER-COPY t-bill TO bill.
  success-flag = YES.
  IF bill.reslinnr NE bill.parent-nr THEN /* = Additional Bill */
  DO:
      FIND FIRST res-line WHERE res-line.resnr = bill.resnr
        AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line AND res-line.resstatus = 12 
          AND res-line.zinr NE bill.zinr THEN
      DO:
        FIND CURRENT res-line EXCLUSIVE-LOCK.
        ASSIGN res-line.zinr = bill.zinr.
        FIND CURRENT res-line NO-LOCK.
      END.
  END.
  FIND CURRENT bill NO-LOCK.
END.
