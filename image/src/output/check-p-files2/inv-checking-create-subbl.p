DEF TEMP-TABLE artikel2
    FIELD art LIKE l-artikel.artnr
    FIELD ekum LIKE l-artikel.endkum
    FIELD zeich LIKE l-artikel.bezeich
    FIELD zeich2 LIKE l-untergrup.bezeich
    FIELD numb LIKE queasy.number1 FORMAT "9" COLUMN-LABEL "Main".

DEF OUTPUT PARAMETER TABLE FOR artikel2.

RUN create-sub.

PROCEDURE create-sub:
    FOR EACH artikel2:
        DELETE artikel2.
    END.

    FOR EACH l-artikel NO-LOCK:
      FIND FIRST queasy WHERE queasy.KEY = 29 AND queasy.number2 = l-artikel.zwkum
          NO-LOCK NO-ERROR.
      IF AVAILABLE queasy AND queasy.number1 NE l-artikel.endkum THEN
      DO:
          FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK.
          CREATE artikel2.
          ASSIGN
                artikel2.art = l-artikel.artnr
                artikel2.zeich = l-artikel.bezeich 
                artikel2.ekum = l-artikel.endkum
                artikel2.zeich2 = l-untergrup.bezeich
                artikel2.numb = queasy.number1.
      END.
    END.
END. 


