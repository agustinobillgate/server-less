DEFINE TEMP-TABLE rmcat-list
  FIELD rmcat AS CHAR.

DEF INPUT PARAMETER currcode AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rmcat-list.

RUN create-rmtype-list.

PROCEDURE create-rmtype-list:
DEF VAR i AS INTEGER INIT 0 NO-UNDO.

  FOR EACH kontline WHERE kontline.kontcode = currcode
      AND kontline.kontstat = 1 NO-LOCK:
    IF kontline.zikatnr = 0 THEN
    DO:
      FOR EACH zimkateg NO-LOCK:
        FIND FIRST rmcat-list WHERE rmcat-list.rmcat = zimkateg.kurzbez
            NO-ERROR.
        IF NOT AVAILABLE rmcat-list THEN
        DO:
          CREATE rmcat-list.
          ASSIGN rmcat-list.rmcat = zimkateg.kurzbez.
        END.
      END.
      LEAVE.
    END.
    ELSE
    DO:
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK.
      FIND FIRST rmcat-list WHERE rmcat-list.rmcat = zimkateg.kurzbez
          NO-ERROR.
      IF NOT AVAILABLE rmcat-list THEN
      DO:
          CREATE rmcat-list.
          ASSIGN rmcat-list.rmcat = zimkateg.kurzbez.
      END.
    END.
  END.
  
END.
