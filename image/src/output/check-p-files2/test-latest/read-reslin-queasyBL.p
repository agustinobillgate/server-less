
DEF TEMP-TABLE t-reslin-queasy    LIKE reslin-queasy.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER rkey       AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER inpChar    AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER resNo      AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER reslinNo   AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER inpNum1    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER inpNum2    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER inpNum3    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER datum1     AS DATE     NO-UNDO.
DEF INPUT  PARAMETER datum2     AS DATE     NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-reslin-queasy.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = rKey 
      AND reslin-queasy.resnr = resNo AND reslin-queasy.reslinnr = reslinNo
      NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN
    DO:
      CREATE t-reslin-queasy.
      BUFFER-COPY reslin-queasy TO t-reslin-queasy.
    END.
  END.
  WHEN 2 THEN
  DO:    
    IF inpChar = "" AND inpNum2 = 0 THEN /* res-rmrateUI.p */
    FOR EACH reslin-queasy WHERE reslin-queasy.key  = rkey
      AND reslin-queasy.resnr                       = resNo 
      AND reslin-queasy.reslinnr                    = reslinNo NO-LOCK:
      CREATE t-reslin-queasy.
      BUFFER-COPY reslin-queasy TO t-reslin-queasy.
    END.
    ELSE
    FOR EACH reslin-queasy WHERE reslin-queasy.key  = rkey
      AND reslin-queasy.char1                       = inpChar
      AND reslin-queasy.resnr                       = resNo 
      AND reslin-queasy.reslinnr                    = reslinNo 
      AND reslin-queasy.number2                     = inpNum2 NO-LOCK:
      CREATE t-reslin-queasy.
      BUFFER-COPY reslin-queasy TO t-reslin-queasy.
    END.
  END.
  WHEN 3 THEN /* used IN mk-reslineUI:check-fixrate) */
  DO:
    DEF VAR curr-datum AS DATE NO-UNDO.
    DO curr-datum = datum1 TO datum2:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey
        AND reslin-queasy.resnr       EQ resNo 
        AND reslin-queasy.reslinnr    EQ reslinNo 
        AND reslin-queasy.date1       LE curr-datum 
        AND reslin-queasy.date2       GE curr-datum NO-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN
      DO:
        FIND FIRST t-reslin-queasy NO-ERROR.
        IF NOT AVAILABLE t-reslin-queasy THEN CREATE t-reslin-queasy.
        BUFFER-COPY reslin-queasy TO t-reslin-queasy.
      END.
      ELSE
      DO:
        DELETE t-reslin-queasy NO-ERROR.
        RETURN.
      END.
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey
      AND reslin-queasy.char1       EQ inpChar
      AND reslin-queasy.reslinnr    EQ reslinNo 
      AND reslin-queasy.number1     EQ inpNum1
      AND reslin-queasy.number2     EQ inpNum2
      NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN
    DO:
      CREATE t-reslin-queasy.
      BUFFER-COPY reslin-queasy TO t-reslin-queasy.
    END.
  END.
  WHEN 5 THEN
  DO:
    FOR EACH reslin-queasy WHERE reslin-queasy.key = rkey
      AND reslin-queasy.char1       EQ inpChar
      AND reslin-queasy.reslinnr    EQ reslinNo 
      AND reslin-queasy.number1     EQ inpNum1
      AND reslin-queasy.number2     EQ inpNum2 NO-LOCK USE-INDEX argt_ix
      BY reslin-queasy.resnr BY reslin-queasy.number3 BY reslin-queasy.date1: 
      CREATE t-reslin-queasy.
      BUFFER-COPY reslin-queasy TO t-reslin-queasy.
    END.
  END.
  WHEN 6 THEN
  DO:
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey
      AND reslin-queasy.char1    = inpChar 
      AND reslin-queasy.resnr    = resNo 
      AND reslin-queasy.reslinnr = reslinNo
      AND reslin-queasy.number1  = inpNum1 
      AND reslin-queasy.number2  = inpNum2 
      AND reslin-queasy.number3  = inpNum3 
      AND datum1 GE reslin-queasy.date1 
      AND datum1 LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN
    DO:
      CREATE t-reslin-queasy.
      BUFFER-COPY reslin-queasy TO t-reslin-queasy.
    END.
  END.
  WHEN 7 THEN
  DO:
      FOR EACH reslin-queasy NO-LOCK:
          CREATE t-reslin-queasy.
          BUFFER-COPY reslin-queasy TO t-reslin-queasy.
      END.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey 
          AND reslin-queasy.resnr = resNo 
          AND reslin-queasy.reslinnr = reslinNo 
          AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN
      DO:
          CREATE t-reslin-queasy.
          BUFFER-COPY reslin-queasy TO t-reslin-queasy.
      END.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey
        AND reslin-queasy.resnr = resNo
        AND reslin-queasy.reslinnr = reslinNo
        AND datum1 GE reslin-queasy.date1 
        AND datum1 LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN
      DO:
          CREATE t-reslin-queasy.
          BUFFER-COPY reslin-queasy TO t-reslin-queasy.
      END.
  END.
  WHEN 10 THEN
  DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey
          AND reslin-queasy.char1   = InpChar
          AND reslin-queasy.number1 = InpNum1
          AND reslin-queasy.number2 = InpNum2
          AND reslin-queasy.reslinnr = reslinNo
          AND reslin-queasy.deci1 NE 0 NO-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN
      DO:
          CREATE t-reslin-queasy.
          BUFFER-COPY reslin-queasy TO t-reslin-queasy.
      END.
  END.
  WHEN 11 THEN
  DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = rkey
          AND reslin-queasy.resnr = resNo
          AND reslin-queasy.reslinnr = reslinNo 
          AND reslin-queasy.betriebsnr = inpNum1
          AND (reslin-queasy.logi1 = YES OR reslin-queasy.logi2 = YES 
               OR reslin-queasy.logi3 = YES) NO-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN
      DO:
          CREATE t-reslin-queasy.
          BUFFER-COPY reslin-queasy TO t-reslin-queasy.
      END.
  END.
END CASE.
