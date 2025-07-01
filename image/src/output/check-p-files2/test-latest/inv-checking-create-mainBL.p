DEF TEMP-TABLE artikel1
    FIELD art LIKE l-artikel.artnr
    FIELD ekum LIKE l-artikel.endkum
    FIELD zeich LIKE l-artikel.bezeich.

DEF OUTPUT PARAMETER TABLE FOR artikel1.

RUN create-main.

PROCEDURE create-main:
    FOR EACH artikel1:
        DELETE artikel1.
    END.

    FOR EACH l-artikel NO-LOCK:
        IF SUBSTR(STRING(l-artikel.artnr),1,1) NE STRING(l-artikel.endkum) THEN
        DO:
            CREATE artikel1.
            ASSIGN
                artikel1.art = l-artikel.artnr
                artikel1.ekum = l-artikel.endkum
                artikel1.zeich = l-artikel.bezeich.
        END.  
    END.
END.


