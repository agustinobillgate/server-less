DEFINE TEMP-TABLE t-queasy      LIKE queasy.

DEF INPUT  PARAMETER rmCat AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEF VARIABLE create-it AS LOGICAL NO-UNDO.

FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmCat NO-LOCK NO-ERROR.
create-it = NOT AVAILABLE zimkateg.

FOR EACH queasy WHERE  queasy.key = 2 AND NOT queasy.logi2 
  NO-LOCK BY queasy.char1:


  FIND FIRST ratecode WHERE ratecode.CODE = queasy.char1
      AND ratecode.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR.
  IF AVAILABLE ratecode OR create-it THEN
  DO:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
  END.
END.

