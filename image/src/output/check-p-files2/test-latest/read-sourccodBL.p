
DEF TEMP-TABLE t-sourccod         LIKE sourccod.

DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER sourceNo     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-sourccod.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST sourccod WHERE sourccod.source-code = sourceNo 
      AND sourccod.betriebsnr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE sourccod THEN
    DO:
      CREATE t-sourccod.
      BUFFER-COPY sourccod TO t-sourccod.
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST sourccod WHERE sourccod.betriebsnr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE sourccod THEN
    DO:
      CREATE t-sourccod.
      BUFFER-COPY sourccod TO t-sourccod.
    END.
  END.
  WHEN 3 THEN
  FOR EACH sourccod WHERE sourccod.betriebsnr = 0 
    NO-LOCK BY sourccod.source-code:
    CREATE t-sourccod.
    BUFFER-COPY sourccod TO t-sourccod.
  END.
  WHEN 4 THEN
  DO:
     FIND FIRST sourccod WHERE sourccod.source-code = sourceNo 
         NO-LOCK NO-ERROR.  
     IF AVAILABLE sourccod THEN
     DO:
       CREATE t-sourccod.
       BUFFER-COPY sourccod TO t-sourccod.
     END.
  END.
  WHEN 5 THEN
  DO:
      FOR EACH sourccod WHERE sourccod.betriebsnr = 0
        AND sourccod.source-code NE sourceNo
        NO-LOCK BY sourccod.source-cod:
          CREATE t-sourccod.
          BUFFER-COPY sourccod TO t-sourccod.
      END.
  END.
  WHEN 6 THEN
  DO:
      FOR EACH sourccod WHERE sourccod.source-code NE sourceNo
        NO-LOCK BY sourccod.source-cod:
          CREATE t-sourccod.
          BUFFER-COPY sourccod TO t-sourccod.
      END.
  END.
  WHEN 7 THEN
  DO:
     FIND FIRST sourccod NO-LOCK NO-ERROR.  
     IF AVAILABLE sourccod THEN
     DO:
       CREATE t-sourccod.
       BUFFER-COPY sourccod TO t-sourccod.
     END.
  END.
  WHEN 8 THEN
  DO:
      FOR EACH sourccod NO-LOCK BY sourccod.source-cod:
          CREATE t-sourccod.
          BUFFER-COPY sourccod TO t-sourccod.
      END.
  END.
END CASE.

