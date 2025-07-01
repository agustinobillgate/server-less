DEF TEMP-TABLE t-zimkateg LIKE zimkateg.

DEF INPUT  PARAMETER room-exist-only AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER sleeping-only   AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.

DEF VAR do-it AS LOGICAL                        NO-UNDO.

FOR EACH zimkateg NO-LOCK BY zimkateg.kurzbez:    
    IF sleeping-only THEN FIND FIRST zimmer WHERE zimmer.zikatnr
        = zimkateg.zikatnr AND zimmer.sleeping NO-LOCK NO-ERROR.
    IF NOT AVAILABLE zimmer AND room-exist-only THEN
    FIND FIRST zimmer WHERE zimmer.zikatnr= zimkateg.zikatnr NO-LOCK NO-ERROR.
    do-it = (NOT room-exist-only AND NOT sleeping-only) OR AVAILABLE zimmer. 
    IF do-it THEN
    DO:
      CREATE t-zimkateg.
      BUFFER-COPY zimkateg TO t-zimkateg.
    END.
END.
