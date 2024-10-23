DEF TEMP-TABLE t-zimkateg LIKE zimkateg.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER zikatNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER shortBez  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.

CASE case-type:
    WHEN 1 THEN
    DO:
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = zikatNo NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN
      DO:
        CREATE t-zimkateg.
        BUFFER-COPY zimkateg TO t-zimkateg.
      END.
    END.
    WHEN 2 THEN
    DO:
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = shortbez NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN
      DO:
        CREATE t-zimkateg.
        BUFFER-COPY zimkateg TO t-zimkateg.
      END.
    END.
    WHEN 3 THEN
    DO:
      FOR EACH zimkateg NO-LOCK BY zimkateg.kurzbez:
        FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN
        DO:
          CREATE t-zimkateg.
          BUFFER-COPY zimkateg TO t-zimkateg.
        END.
      END.
    END.
    WHEN 4 THEN
    DO:
      FOR EACH zimkateg NO-LOCK:
          CREATE t-zimkateg.
          BUFFER-COPY zimkateg TO t-zimkateg.
      END.
    END.
    WHEN 5 THEN
    DO:
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = shortbez
          AND zimkateg.zikatnr NE zikatNo NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN
      DO:
        CREATE t-zimkateg.
        BUFFER-COPY zimkateg TO t-zimkateg.
      END.
    END.
    WHEN 6 THEN
    DO:
      FOR EACH zimkateg WHERE zimkateg.typ = zikatNo NO-LOCK:
        CREATE t-zimkateg.
        BUFFER-COPY zimkateg TO t-zimkateg.
      END.
    END.
END CASE.
