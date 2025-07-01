DEF TEMP-TABLE t-master LIKE master.

DEF INPUT  PARAMETER case-type AS INTEGER.
DEF INPUT  PARAMETER resNo  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER gastNo AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-master.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST master WHERE master.resnr = resNo NO-LOCK NO-ERROR.
    IF AVAILABLE master THEN
    DO:
      CREATE t-master.
      BUFFER-COPY master TO t-master.
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST master WHERE master.resnr = resNo 
        AND master.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE master THEN
    DO:
      CREATE t-master.
      BUFFER-COPY master TO t-master.
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST master WHERE master.resnr = resNo 
        AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE master THEN
    DO:
      CREATE t-master.
      BUFFER-COPY master TO t-master.
    END.
  END.
  WHEN 4 THEN
  DO:
      FIND FIRST master WHERE master.gastnr = gastNo
          AND master.resnr = resNo NO-LOCK NO-ERROR. 
      IF AVAILABLE master THEN 
      DO:
          CREATE t-master.
          BUFFER-COPY master TO t-master.
      END.
  END.
  WHEN 5 THEN
  DO:
  DEF VAR billno AS INTEGER NO-UNDO.
  DEF BUFFER mbill FOR bill.
      ASSIGN billno = gastNo. /* use gastNo info as guest billNo */

      FIND FIRST bill WHERE bill.rechnr = billno NO-LOCK.
      FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
          AND res-line.reslinnr = bill.parent-nr NO-LOCK.
      
      IF res-line.l-zuordnung[5] NE 0 THEN
      FIND FIRST mbill WHERE mbill.resnr = res-line.l-zuordnung[5]
        AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.
      
      ELSE FIND FIRST mbill WHERE mbill.resnr = res-line.resnr 
        AND mbill.reslinnr = 0 NO-LOCK NO-ERROR. 
      
      IF NOT AVAILABLE mbill THEN RETURN.
      FIND FIRST master WHERE master.resnr = mbill.resnr 
          NO-LOCK NO-ERROR.
      IF AVAILABLE master THEN 
      DO:
          CREATE t-master.
          BUFFER-COPY master TO t-master.
      END.
  END.
END CASE.

