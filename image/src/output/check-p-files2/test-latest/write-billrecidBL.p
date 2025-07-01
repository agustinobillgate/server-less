DEF TEMP-TABLE t-bill   LIKE bill
    FIELD bl-recid AS INTEGER.

DEF INPUT PARAMETER TABLE FOR t-bill.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST t-bill NO-ERROR.
IF AVAILABLE t-bill THEN
DO:
  FIND FIRST bill WHERE RECID(bill) = t-bill.bl-recid
    EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE bill THEN
  DO:
    BUFFER-COPY t-bill TO bill.
    RELEASE bill.
    success-flag = YES.
  END.
END.
