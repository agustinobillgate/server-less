
DEFINE TEMP-TABLE t-queasy      LIKE queasy
    FIELD comp-name AS CHAR.


DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE BUFFER gbuff FOR guest.

FOR EACH queasy WHERE queasy.key = 19 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.

    FIND FIRST gbuff WHERE gbuff.gastnr = queasy.number2 NO-LOCK NO-ERROR.
    IF AVAILABLE gbuff THEN
       t-queasy.comp-name = gbuff.NAME + " " + gbuff.anredefirma. 
    ELSE t-queasy.comp-name = "".
END.
