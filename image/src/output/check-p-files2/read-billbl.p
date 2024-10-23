
DEF TEMP-TABLE t-bill          LIKE bill.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER billNo     AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resNo      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER reslinNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER actFlag    AS INTEGER NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-bill.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST bill WHERE bill.rechnr = billNo NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
      CREATE t-bill.
      BUFFER-COPY bill TO t-bill.
      MESSAGE billNo VIEW-AS ALERT-BOX INFO.
    END.
  END.
  WHEN 2 THEN 
  DO:    
    FIND FIRST bill WHERE bill.resnr = resNo
      AND bill.reslinnr = reslinNo NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
      CREATE t-bill.
      BUFFER-COPY bill TO t-bill.
    END.
  END.
  WHEN 3 THEN
  FOR EACH bill WHERE bill.resnr = resNo
    AND bill.parent-nr = reslinNo AND bill.flag = 0 NO-LOCK:
    CREATE t-bill.
    BUFFER-COPY bill TO t-bill.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST bill WHERE bill.rechnr = billNo 
      AND bill.flag = actFLag NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
      CREATE t-bill.
      BUFFER-COPY bill TO t-bill.
    END.
  END.
  WHEN 5 THEN
  DO:
    FIND FIRST bill WHERE bill.rechnr2 = billNo
        AND bill.rechnr NE resNo NO-LOCK NO-ERROR. 
    IF AVAILABLE bill THEN
    DO:
      CREATE t-bill.
      BUFFER-COPY bill TO t-bill.
    END.
  END.
  WHEN 6 THEN
  DO:
    FIND FIRST bill WHERE bill.resnr = resNo 
        AND bill.reslinnr = reslinNo AND bill.flag = 0 
        AND bill.zinr = STRING(actFLag) NO-LOCK NO-ERROR. 
    IF AVAILABLE bill THEN
    DO:
      CREATE t-bill.
      BUFFER-COPY bill TO t-bill.
    END.
  END.
  WHEN 7 THEN
  DO:
    FIND FIRST bill WHERE bill.resnr = resNo 
        AND bill.zinr = "" NO-LOCK NO-ERROR. 
    IF AVAILABLE bill THEN
    DO:
      CREATE t-bill.
      BUFFER-COPY bill TO t-bill.
    END.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo
          AND bill.parent-nr = reslinNo NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 9 THEN
  DO: 
      FOR EACH bill WHERE bill.resnr = resNo AND bill.parent-nr = reslinNo NO-LOCK: 
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 10 THEN
  DO: 
      FIND FIRST bill WHERE bill.rechnr = billNo 
          AND bill.resnr = resNo 
          AND bill.reslinnr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 11 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo
          AND bill.zinr = ""
          AND bill.flag = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 12 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo
          AND bill.parent-nr = reslinNo
          AND bill.rechnr NE 0 NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 13 THEN
  DO: 
      FOR EACH bill WHERE bill.resnr = resNo 
          AND bill.reslinnr = reslinNo 
          AND bill.zinr = STRING(actFLag) NO-LOCK: 
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 14 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo
          AND bill.reslinnr = reslinNo
          AND bill.zinr = "" NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.     
  WHEN 15 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 16 THEN
  DO:
      FIND FIRST bill WHERE RECID(bill) = billNo NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 17 THEN
  DO: 
      FOR EACH bill WHERE bill.resnr = resNo AND bill.parent-nr = reslinNo 
          AND bill.zinr = STRING(actFLag) AND bill.flag = 0 NO-LOCK: 
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 18 THEN
  DO: 
      FOR EACH bill WHERE bill.rechnr = billNo NO-LOCK :
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 19 THEN
  DO:
      FIND FIRST bill WHERE bill.rechnr = billNo AND bill.resnr = resNo 
          NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 20 THEN
  DO: 
      FOR EACH bill WHERE bill.resnr = resNo AND bill.zinr = STRING(actFLag) AND bill.flag = 0 NO-LOCK: 
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.
  WHEN 21 THEN /*FDL Nov 15, 2023 => For vhpCloud*/
  DO:
      FIND FIRST bill WHERE bill.resnr EQ resNo
          AND bill.reslinnr EQ reslinNo
          AND bill.flag EQ actFlag NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN
      DO:
          CREATE t-bill.
          BUFFER-COPY bill TO t-bill.
      END.
  END.

END CASE.
