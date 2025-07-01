
DEF TEMP-TABLE t-debitor     LIKE debitor
    FIELD tb-recid      AS INTEGER.

DEF INPUT  PARAMETER case-type   AS INTEGER            NO-UNDO.
DEF INPUT  PARAMETER TABLE       FOR t-debitor.
DEF OUTPUT PARAMETER successFlag AS LOGICAL INITIAL YES NO-UNDO.

FIND FIRST t-debitor NO-ERROR.
IF NOT AVAILABLE t-debitor THEN RETURN.

CASE case-type:
  WHEN 1 THEN
  DO:
    CREATE debitor.
    BUFFER-COPY t-debitor TO debitor.
    ASSIGN successFlag = YES.
  END.
  WHEN 2 THEN 
  DO:
      FIND FIRST debitor WHERE RECID(debitor) = t-debitor.tb-recid 
          EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE debitor THEN
      DO:
          debitor.vesrcod    = t-debitor.vesrcod.
          debitor.versanddat = t-debitor.versanddat.
          debitor.mahnstufe  = t-debitor.mahnstufe. 
          RELEASE debitor.
          ASSIGN successFlag = YES.
      END.
  END.
END CASE.
