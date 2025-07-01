DEF TEMP-TABLE t-res-line LIKE res-line.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resNo     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinNo  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resstat   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER actFlag   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER rmNo      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER arrive    AS DATE    NO-UNDO.
DEF INPUT PARAMETER depart    AS DATE    NO-UNDO.
DEF INPUT PARAMETER gastNo    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kontigNo  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER kontcode  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.

DEFINE VARIABLE delichr4 AS CHARACTER.
delichr4 = CHR(4).
/*DEF VAR case-type AS INTEGER INITIAL 101 NO-UNDO.
DEF VAR resNo     AS INTEGER INITIAL ? NO-UNDO.
DEF VAR reslinNo  AS INTEGER INITIAL ? NO-UNDO.
DEF VAR resstat   AS INTEGER INITIAL ? NO-UNDO.
DEF VAR actFlag   AS INTEGER INITIAL ? NO-UNDO.
DEF VAR rmNo      AS CHAR    INITIAL "1021" NO-UNDO.
DEF VAR arrive    AS DATE    INITIAL ? NO-UNDO.
DEF VAR depart    AS DATE    INITIAL ? NO-UNDO.
DEF VAR gastNo    AS INTEGER INITIAL ? NO-UNDO.
DEF VAR kontigNo  AS INTEGER INITIAL ? NO-UNDO.
DEF VAR kontcode  AS CHAR    INITIAL "" NO-UNDO.*/
/*
DEF VARIABLE hHandle AS HANDLE NO-UNDO.
hHandle = THIS-PROCEDURE.*/

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr = reslinNo NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.

      /*FDL: Ticket DE4077*/
      IF LENGTH(t-res-line.bemerk) EQ 1 THEN t-res-line.bemerk = "".
      IF t-res-line.bemerk EQ ? OR t-res-line.bemerk EQ "\u0000" OR t-res-line.bemerk EQ CHR(4) THEN t-res-line.bemerk = "".
      ELSE IF t-res-line.bemerk MATCHES "*\u0000*" THEN t-res-line.bemerk = REPLACE(t-res-line.bemerk, "\u0000", "").
      ELSE IF t-res-line.bemerk MATCHES "*" + CHR(4) + "*" THEN t-res-line.bemerk = REPLACE(t-res-line.bemerk, CHR(4), "").
    END.
  END.
  WHEN 2 THEN
  DO:
    IF kontigNo > 0 THEN
    FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.gastnr = gastNo 
      AND res-line.active-flag LE 2 AND res-line.resstatus LE 6 NO-LOCK, 
      FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
      AND kontline.kontcode = kontcode AND kontline.kontstatus = 1 NO-LOCK: 
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
    ELSE IF kontigNo < 0 THEN
    FOR EACH res-line WHERE res-line.kontignr LT 0 
      AND res-line.gastnr = gastNo 
      AND res-line.active-flag LT 2 AND res-line.resstatus LE 6 
      AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 NO-LOCK, 
      FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
      AND kontline.kontcode = kontcode AND kontline.kontstatus = 1 NO-LOCK: 
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag = actFlag NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 4 THEN
  FOR EACH res-line WHERE res-line.resnr = resNo
    AND res-line.active-flag    LE 1 
    AND res-line.resstatus      NE 12 
    AND res-line.l-zuordnung[3] EQ 0 NO-LOCK: 
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
  END.
  WHEN 5 THEN
  DO:
    IF rmNo NE "" THEN
    FIND FIRST res-line WHERE res-line.active-flag = actFlag
      AND res-line.resstatus = resStat AND res-line.zinr = rmNo
      AND res-line.resnr = resNo
      AND res-line.reslinnr NE reslinNo NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST res-line WHERE res-line.active-flag = actFlag
      AND res-line.resstatus = resStat AND res-line.resnr = resNo
      NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 6 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr NE reslinNo
      AND res-line.resstatus = resStat AND res-line.zinr = rmNo
      NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 7 THEN
  DO:
    FIND FIRST res-line WHERE res-line.zinr = rmNo
      AND res-line.active-flag = actFlag AND res-line.resnr NE resNo
      NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 8 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr NE reslinNo
      AND res-line.active-flag LE actFLag  
      AND res-line.zipreis GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 9 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = actFLag
      AND res-line.zinr = rmNo
      AND res-line.ankunft   GE arrive
      AND res-line.ankunft   LT depart 
      AND res-line.resnr     NE resNo
      AND res-line.resstatus NE resStat NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 10 THEN  /* accompanying guest */
  FOR EACH res-line WHERE res-line.resnr = resNo
    AND res-line.active-flag    LE 1 
    AND res-line.kontakt-nr     EQ reslinNo 
    AND res-line.l-zuordnung[3] EQ 1 NO-LOCK: 
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
  END.
  WHEN 11 THEN  /* insert or split res-line */
  FOR EACH res-line WHERE res-line.resnr = resNo NO-LOCK: 
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
  END.
  WHEN 12 THEN
  DO:
    IF rmNo GT "" THEN
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag LE actFlag
      AND res-line.resstatus NE resStat AND res-line.zinr = rmNo
      AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag LE actFlag
      AND res-line.resstatus NE resStat
      AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.   
  END.
  WHEN 13 THEN /* confirmed booking for a certain resNo and RmNo */
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 OR res-line.resstatus = 6)
      AND res-line.zinr = rmNo NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.   
  END.
  WHEN 14 THEN
  FOR EACH res-line WHERE res-line.gastnr = gastNo
    AND res-line.active-flag    LE 1 
    AND res-line.resstatus      NE 12 
    AND res-line.l-zuordnung[3] EQ 0 NO-LOCK: 
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
  END.
  WHEN 15 THEN 
  DO:
    FIND FIRST res-line WHERE RECID(res-line) = resNo NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.   
  END.
  WHEN 16 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr EQ reslinNo
      AND res-line.active-flag LE actFLag NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 17 THEN
  DO:
    FOR EACH res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag LE actFLag 
      AND (res-line.resstatus = 11 OR res-line.resstatus = 13)
      NO-LOCK:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 18 THEN 
  DO:
    FOR EACH res-line WHERE res-line.gastnr = gastNo 
      AND res-line.active-flag LE 1 NO-LOCK:
      IF AVAILABLE res-line THEN
      DO:
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
      END.   
    END.
  END.
  WHEN 19 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag LE actFlag AND 
      res-line.pin-code = kontcode NO-LOCK NO-ERROR. 
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 20 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag EQ actFlag
          AND res-line.resstatus EQ resstat
          AND res-line.zinr EQ rmNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 21 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr EQ resNo
          AND res-line.active-flag LE actFlag 
          AND res-line.resstatus NE resstat NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 22 THEN
  DO: 
      IF actflag LE 1 THEN
      FIND FIRST res-line WHERE res-line.resnr = resNo 
          AND res-line.active-flag LE actFlag
          AND res-line.resstatus NE 8
          AND res-line.resstatus NE 9
          AND res-line.resstatus NE 10
          AND res-line.resstatus NE 12
          NO-LOCK NO-ERROR.
      ELSE
      FIND FIRST res-line WHERE res-line.resnr = resNo 
          AND res-line.active-flag = 2
          AND (res-line.resstatus EQ 8 OR res-line.resstatus EQ 9
               OR res-line.resstatus EQ 10)
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 23 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo 
           AND res-line.gastnr = gastNo 
           AND ((res-line.resstatus GE 1 
           AND res-line.resstatus LE 4) OR res-line.resstatus EQ 11) 
           AND res-line.zimmeranz GT 1 NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 24 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.zinr = rmNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 25 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 1 AND 
        (res-line.resstatus = 6 OR res-line.resstatus = 13) AND 
        res-line.pin-code = rmNo AND res-line.resnr = resNo
        AND res-line.reslinnr = reslinNo
        NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 26 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag LE 1 AND 
      res-line.abreise = arrive AND res-line.zinr = rmNo 
      AND res-line.resstatus NE 12 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 27 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
        AND res-line.zinr = rmNo AND res-line.resstatus = 1 
        NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 28 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resstatus = 6 
        AND res-line.zinr = rmNo
        AND (res-line.resnr NE resNo
             AND res-line.reslinnr NE reslinNo) 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 29 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo 
        AND res-line.resstatus LE 6 
        AND res-line.zinr = rmNo 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 30 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.kontakt-nr = reslinNo
      AND res-line.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 31 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
        AND res-line.reslinnr NE reslinNo
        AND res-line.resstatus = 11 
        AND res-line.zinr = rmNo NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 32 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
        AND res-line.reslinnr NE resNo 
        AND res-line.zinr = rmNo 
        AND res-line.betrieb-gast > 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 33 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
        AND res-line.reslinnr = reslinNo 
        AND res-line.zinr = "" 
        AND res-line.active-flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 34 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resstatus = 6 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 35 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 1 
        AND res-line.zinr = rmNo NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 36 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo 
           AND res-line.gastnr = gastNo 
           AND ((res-line.resstatus GE 1 
           AND res-line.resstatus LE 5) OR res-line.resstatus EQ 11) 
           AND res-line.zimmeranz GT 1 NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 37 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 1 
        AND res-line.zinr = rmNo AND res-line.abreise = arrive NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 38 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 1 
        AND res-line.resstatus = 6 AND res-line.zinr = rmNo NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line AND resstat = 13 THEN
    FIND FIRST res-line WHERE res-line.active-flag = 1 
        AND res-line.resstatus = 13 AND res-line.zinr = rmNo 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 39 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 1 
        AND res-line.resstatus = 13 AND res-line.zinr = rmNo 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 40 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo 
        AND res-line.zinr = "" NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 41 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
              AND res-line.zinr = rmNo
              AND res-line.resstatus = 13
              AND res-line.abreise GT arrive
              AND res-line.zipreis = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 42 THEN
  DO:
      FOR EACH res-line WHERE res-line.kontignr GT 0 
          AND res-line.gastnr = gastNo 
          AND res-line.active-flag LE 2 AND res-line.resstatus LE 6 NO-LOCK, 
          FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
          AND kontline.kontcode = kontcode AND kontline.kontstatus = 1 NO-LOCK: 
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 43 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.active-flag = 1 AND res-line.resstatus EQ 6 
          NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE res-line THEN
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.active-flag = 1 AND res-line.resstatus EQ 13
          AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 44 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag = actFlag
          AND res-line.zinr = rmNo AND res-line.reslinnr NE reslinNo
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 45 THEN
  DO:
       FOR EACH res-line WHERE res-line.resnr = resNo
           AND res-line.active-flag = actFlag
           AND res-line.l-zuordnung[3] = 1
           AND res-line.kontakt-nr = reslinNo NO-LOCK:
           CREATE t-res-line.
           BUFFER-COPY res-line TO t-res-line.
       END.
  END.
  WHEN 46 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag LE actFlag 
          AND ((res-line.ankunft = arrive) OR 
               (res-line.abreise = arrive)) 
          AND res-line.zinr = rmNo AND res-line.betrieb-gast > 0 
          AND res-line.resnr NE resNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 47 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.reslinnr NE resNo
          AND res-line.zinr = rmNo
          AND res-line.active-flag LE actFlag
          AND res-line.betrieb-gast > 0 NO-LOCK NO-ERROR.     
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 48 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND (res-line.resstatus = 11 OR res-line.resstatus = 13) 
          AND res-line.zinr = rmNo AND res-line.betrieb-gast GT 0 
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 49 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo 
          AND res-line.active-flag = actFlag AND res-line.zinr NE "" 
          AND res-line.betrieb-gast = 0 NO-LOCK : 
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 50 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo 
          AND res-line.kontakt-nr = reslinNo 
          AND res-line.l-zuordnung[3] = 1 NO-LOCK : 
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 51 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo 
          AND res-line.active-flag EQ 1 NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 52 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo 
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 53 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo 
          AND (res-line.resstatus = 6 OR res-line.resstatus = 8)
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 54 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag LE actFLag  
      AND res-line.zipreis GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 55 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 0 
        AND res-line.zinr = rmNo 
        AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) 
        AND res-line.ankunft = arrive NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 56 THEN
  DO:
    FOR EACH res-line WHERE res-line.active-flag = 0 
        AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) 
        AND res-line.zinr = rmNo 
        NO-LOCK :
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 57 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resstatus = resstat
      AND res-line.abreise = arrive
      AND res-line.zinr = rmNo NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 58 THEN
  DO:
    FOR EACH res-line WHERE res-line.resstatus = resstat 
        AND res-line.zinr = rmNo 
        AND res-line.abreise = arrive 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK :
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 59 THEN
  DO:
    FOR EACH res-line WHERE res-line.kontignr LT 0 
        AND res-line.gastnr = gastNo
        AND res-line.active-flag LT actFlag
        AND res-line.resstatus LT resstat
        AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
        FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
        AND kontline.kontcode = kontcode 
        AND kontline.kontstat = 1 NO-LOCK: 
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END. 
  END.
  WHEN 60 THEN
  DO:
    FOR EACH res-line WHERE res-line.kontignr LT 0 
        AND res-line.gastnr = gastNo
        AND res-line.active-flag LT actFlag
        AND res-line.resstatus LT resstat
        AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
        FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
        AND kontline.kontcode = kontcode
        AND kontline.betriebsnr = 1
        AND kontline.kontstat = 1 NO-LOCK: 
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END. 
  END.
  WHEN 61 THEN
  DO:
    FOR EACH res-line WHERE res-line.kontignr NE 0 
        AND res-line.gastnr = gastNo
        AND res-line.active-flag LT actFlag
        AND res-line.resstatus LT resstat NO-LOCK,
        FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
        AND kontline.kontcode = kontcode
        AND kontline.kontstat = 1 NO-LOCK: 
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END. 
  END.
  WHEN 62 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
          AND (res-line.resstatus NE 9 
               AND res-line.resstatus NE 10 
               AND res-line.resstatus NE 12) NO-LOCK :
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 63 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
          AND res-line.reslinnr NE reslinNo
          AND res-line.resstatus = resstat 
          AND (res-line.betrieb-gastpay LE 2 OR res-line.betrieb-gastpay = 5)
          NO-LOCK :
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 64 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
          AND res-line.reslinnr NE reslinNo
          AND (res-line.resstatus = 9 OR res-line.resstatus = 10)
          AND res-line.l-zuordnung[3] = 0 NO-LOCK:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 65 THEN
  DO:
    FOR EACH res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag LE actFLag 
      AND (res-line.resstatus = 11 OR res-line.resstatus = 13)
      AND (res-line.kontakt-nr = reslinNo)
      NO-LOCK:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 66 THEN
  DO:
      FIND FIRST res-line WHERE res-line.gastnrmember = gastNo
          AND (res-line.resstatus = 6 OR res-line.resstatus = 13)
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 67 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr GE reslinNo NO-LOCK :
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 68 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag = actFlag
          AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.abreise = depart NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 69 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr NE resNo
          AND res-line.active-flag EQ actFlag
          AND res-line.l-zuordnung[5] = reslinNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 70 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.reslinnr = reslinNo 
          AND res-line.zinr = rmNo NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 71 THEN
  DO:
      FIND FIRST res-line WHERE res-line.zinr = rmNo
          AND res-line.resstatus = resstat NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 72 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag LE actFlag
          AND ( 
                (res-line.ankunft GE arrive AND res-line.ankunft LE depart) OR 
                (res-line.abreise GE arrive AND res-line.abreise LE depart) OR 
                (arrive GE res-line.ankunft AND arrive LE res-line.abreise)
              )
          AND res-line.zinr EQ rmNo
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 73 THEN
  DO:
      FOR EACH res-line WHERE res-line.zinr = rmNo AND 
          (res-line.resstatus = 6 OR res-line.resstatus = 13 
           OR res-line.active-flag = actFlag) NO-LOCK :
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 74 THEN
  DO:
      FIND FIRST res-line WHERE res-line.betriebsnr = resNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 75 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag = actFlag
          AND res-line.zinr = rmNo AND res-line.resstatus NE 12
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 76 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
          AND res-line.resstatus NE 9
          AND res-line.resstatus NE 10
          AND res-line.l-zuordnung[3] = 0 NO-LOCK:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 77 THEN
  DO:
      FOR EACH res-line WHERE res-line.l-zuordnung[5] = reslinNo
          AND res-line.resstatus NE 12 AND res-line.active-flag LE 1
          AND res-line.resnr NE resNo
          NO-LOCK:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 78 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND (res-line.active-flag = actFlag OR res-line.resstatus = resStat) 
          NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 79 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 0 
        AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 OR res-line.resstatus = 11) 
        AND res-line.ankunft = arrive NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 80 THEN
  DO:
    FOR EACH res-line WHERE res-line.active-flag = actFlag
        AND res-line.resstatus NE resstat 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK:
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 81 THEN
  DO:
    FOR EACH res-line WHERE res-line.active-flag LE actFlag
        AND res-line.resstatus NE resstat NO-LOCK,
        FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
        AND MONTH(guest.geburtdatum1) = MONTH(TODAY) 
        AND DAY(guest.geburtdatum1) = DAY(TODAY) NO-LOCK:
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 82 THEN
  DO:
    FOR EACH res-line WHERE res-line.active-flag EQ actFlag
        AND res-line.resstatus EQ resstat NO-LOCK:
        CREATE t-res-line.
        BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 83 THEN
  DO:
    FIND FIRST res-line WHERE res-line.active-flag = 1 
        AND res-line.zinr = rmNo 
        AND res-line.l-zuordnung[3] = 0
        AND res-line.resnr NE resNo
        AND res-line.reslinnr NE reslinNo NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 84 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr NE resNo
        AND res-line.active-flag = 1 
        AND res-line.l-zuordnung[2] = 0
        AND res-line.l-zuordnung[5] = reslinNo NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.
  WHEN 85 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr EQ resNo
          AND res-line.active-flag EQ actFlag 
          AND res-line.resstatus NE resstat NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 86 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag = actFlag
          AND res-line.resstatus EQ resstat 
          AND res-line.resnr = resNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 87 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.resstatus GE 6 AND res-line.resstatus LE 8 
          AND res-line.betriebsnr NE 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 88 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.gastnrmember = gastNo
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 12 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 89 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag LE 1
          AND res-line.resnr NE resNo AND res-line.resstatus NE 12
          AND NOT res-line.abreise LE arrive
          AND NOT res-line.ankunft GT depart
          AND res-line.zinr EQ rmNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 90 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag LE 1
          AND res-line.resstatus NE 12
          AND NOT res-line.abreise LE arrive
          AND NOT res-line.ankunft GT depart
          AND res-line.zinr EQ rmNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 91 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo 
          AND res-line.resstatus GE 6 AND res-line.resstatus LE 8 
          AND res-line.gratis EQ 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 91 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo 
          AND res-line.active-flag LE actFlag :
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 92 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
          AND res-line.zinr = rmNo
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
          AND res-line.resstatus NE 12 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 93 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
           AND res-line.reslinnr = reslinNo NO-LOCK NO-ERROR.
      IF NOT AVAILABLE res-line THEN
      DO:
          IF arrive GT depart THEN
          DO:
              FIND FIRST res-line WHERE res-line.zinr = rmNo
                  AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                  AND res-line.resstatus NE 10 
                  AND res-line.ankunft LE depart
                  AND res-line.abreise GT depart NO-LOCK NO-ERROR.
          END.
          ELSE
          DO:
              FIND FIRST res-line WHERE res-line.zinr = rmNo
                  AND res-line.resstatus NE 12 AND res-line.resstatus NE 9
                  AND res-line.resstatus NE 10
                  AND res-line.ankunft LE depart
                  AND res-line.abreise GE depart NO-LOCK NO-ERROR.
          END.
      END.

      IF AVAILABLE res-line THEN
      DO:
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 94 THEN
  DO:
      FOR EACH res-line WHERE res-line.resnr = resNo
          AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
          AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 
          NO-LOCK: 
          CREATE t-res-line.
          BUFFER-COPY res-line TO t-res-line.
      END.
  END.
  WHEN 95 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr = resNo
        AND res-line.reslinnr = reslinNo NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE res-line THEN 
        FIND FIRST res-line WHERE res-line.zinr = rmNo
          AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
          AND res-line.resstatus NE 10 
          AND res-line.active-flag GE 1 AND res-line.active-flag LE 2 
          AND res-line.ankunft LE arrive
          AND res-line.abreise GT arrive NO-LOCK NO-ERROR.

        IF AVAILABLE res-line THEN
        DO:
            CREATE t-res-line.
            BUFFER-COPY res-line TO t-res-line.
        END.
  END.
  WHEN 96 THEN
  DO:
      FIND FIRST res-line WHERE res-line.active-flag LE 1
          AND INTEGER(res-line.code) EQ resNo NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
            CREATE t-res-line.
            BUFFER-COPY res-line TO t-res-line.
      END.
  END.

  
  WHEN 99 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr = reslinNo EXCLUSIVE-LOCK NO-WAIT NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.

  WHEN 100 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = resNo NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      CREATE t-res-line.
      BUFFER-COPY res-line TO t-res-line.
    END.
  END.

  /* SY 05 JUL 2017 */
  WHEN 101 THEN /* used in telop --> wake up call */
  DO:
  DEF BUFFER rbuff FOR res-line.
  DEF VARIABLE rmNoPattern AS CHAR NO-UNDO INIT "".
  DEF VARIABLE c-room AS CHAR NO-UNDO INIT "".
      FIND FIRST zimmer WHERE zimmer.zinr = rmNo NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
          FIND FIRST rbuff WHERE rbuff.zinr = rmNo 
              AND rbuff.active-flag = 1 NO-LOCK NO-ERROR.
          IF AVAILABLE rbuff THEN
          FOR EACH res-line WHERE res-line.resnr = rbuff.resnr
              AND res-line.active-flag = 1
              AND (res-line.resstatus = 6 OR res-line.resstatus = 13)
              NO-LOCK BY res-line.zinr BY res-line.resstatus.
              FIND FIRST t-res-line WHERE 
                  t-res-line.zinr = res-line.zinr NO-ERROR.
              IF NOT AVAILABLE t-res-line THEN
              DO:
                  CREATE t-res-line.
                  BUFFER-COPY res-line TO t-res-line.
              END.
          END.
      END.
      ELSE
      DO:
          rmNoPattern = "*" + rmNo + "*".
          FIND FIRST reservation WHERE reservation.activeflag = 0 
              AND reservation.groupname MATCHES rmNoPattern NO-LOCK NO-ERROR. /* Naufal Afthar - 7E116A -> handle leading and trailing whitespace*/
          IF AVAILABLE reservation THEN
          DO:
              FOR EACH res-line WHERE res-line.resnr = reservation.resnr
              AND res-line.active-flag = 1
              AND (res-line.resstatus = 6 OR res-line.resstatus = 13)
              NO-LOCK BY res-line.zinr BY res-line.resstatus:
                  FIND FIRST t-res-line WHERE t-res-line.zinr = res-line.zinr NO-LOCK NO-ERROR.
                  IF NOT AVAILABLE t-res-line THEN
                  DO:
                      CREATE t-res-line.
                      BUFFER-COPY res-line TO t-res-line.
                  END.
              END.
          END.
      END.
  END.

END CASE.
/*
PROCEDURE delete-procedure:
    DELETE PROCEDURE hHandle NO-ERROR.
END.*/

