.
DEF TEMP-TABLE t-billhis        LIKE billhis.

DEF INPUT  PARAMETER case-type  AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER billNo     AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER resNo      AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER reslinNo   AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER bill-exist AS LOGICAL INIT NO  NO-UNDO.
DEF OUTPUT PARAMETER TABLE      FOR t-billhis.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST billhis WHERE billhis.rechnr = billNo NO-LOCK NO-ERROR.
    IF AVAILABLE billhis THEN
    DO:
      CREATE t-billhis.
      BUFFER-COPY billhis TO t-billhis.
      bill-exist = YES.
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST billhis WHERE billhis.rechnr = billNo NO-LOCK NO-ERROR.
    IF AVAILABLE billhis THEN bill-exist = YES.
  END.
END CASE.
