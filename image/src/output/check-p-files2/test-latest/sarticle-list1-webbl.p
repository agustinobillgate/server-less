DEFINE TEMP-TABLE t-l-artikel  LIKE l-artikel
    FIELD is-delete     AS LOGICAL  INIT NO
    FIELD is-select     AS LOGICAL  INIT NO
.

DEFINE INPUT PARAMETER sorttype            AS INT   NO-UNDO.
DEFINE INPUT PARAMETER last-art            AS CHAR  NO-UNDO.
DEFINE INPUT PARAMETER last-art1           AS INT   NO-UNDO.
DEFINE OUTPUT PARAMETER first-artnr        AS INT   NO-UNDO.
DEFINE OUTPUT PARAMETER curr-art           AS CHAR  NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER curr-art1          AS INT   NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-artikel.

DEFINE VARIABLE counter     AS INTEGER  NO-UNDO INIT 0.

IF sorttype = 1 THEN
DO:
    IF last-art1 NE 0 THEN
    FOR EACH l-artikel WHERE l-artikel.artnr GE last-art1 NO-LOCK 
        BY l-artikel.artnr. 
        RUN cr-artikel1.
    END.
    ELSE
    FOR EACH l-artikel NO-LOCK BY l-artikel.artnr. 
        RUN cr-artikel1.
    END.
END.    
ELSE IF sorttype = 2 THEN
DO:    
    IF SUBSTR(last-art,1,1) = "*" THEN 
    DO: 
      IF SUBSTR(last-art, LENGTH(last-art), 1) NE "*" THEN 
        last-art = last-art + "*". 
      FOR EACH l-artikel WHERE l-artikel.bezeich MATCHES last-art NO-LOCK 
        BY l-artikel.bezeich. 
        RUN cr-artikel2.
      END.
    END.
    
    ELSE
    FOR EACH l-artikel WHERE l-artikel.bezeich GE (last-art) NO-LOCK 
        BY l-artikel.bezeich. 
        RUN cr-artikel2.
    END.
    
END.
ELSE
DO:
    IF last-art EQ "" THEN
    FOR EACH l-artikel WHERE l-artikel.artnr GT last-art1 NO-LOCK 
        BY l-artikel.artnr. 
        RUN cr-artikel1.
    END.
    ELSE 
    FOR EACH l-artikel WHERE l-artikel.bezeich GT last-art NO-LOCK 
        BY l-artikel.bezeich. 
        RUN cr-artikel2.
    END.
END.

PROCEDURE cr-artikel1 :
    counter = counter + 1.
    IF counter = 1 THEN first-artnr = l-artikel.artnr.
    IF (counter GE 30) AND (curr-art1 NE l-artikel.artnr) THEN LEAVE.
    
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
    RUN delete-check(t-l-artikel.artnr, OUTPUT t-l-artikel.is-delete).
    curr-art1 = l-artikel.artnr.
END.

PROCEDURE cr-artikel2 :
    counter = counter + 1.
    IF counter = 1 THEN first-artnr = l-artikel.artnr.
    IF (counter GE 30) AND (curr-art NE l-artikel.bezeich) THEN LEAVE.
    
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
    RUN delete-check(t-l-artikel.artnr, OUTPUT t-l-artikel.is-delete).
    curr-art = l-artikel.bezeich.
END.

PROCEDURE delete-check:
    DEFINE INPUT PARAMETER artnr        AS INTEGER.
    DEFINE OUTPUT PARAMETER delete-it   AS LOGICAL.
    delete-it = YES.

    FIND FIRST l-bestand WHERE l-bestand.artnr = artnr 
        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
        delete-it = NO. 
        RETURN. 
    END. 

    FIND FIRST l-order WHERE l-order.artnr = artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-order THEN 
    DO: 
        delete-it = NO. 
        RETURN. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST l-op WHERE l-op.artnr = artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE l-op THEN 
        DO: 
            delete-it = NO. 
            RETURN. 
        END. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST h-rezlin WHERE h-rezlin.artnrlager = artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE h-rezlin THEN 
        DO: 
            delete-it = NO. 
            RETURN. 
        END. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST h-artikel WHERE h-artikel.artnrlager = artnr NO-LOCK NO-ERROR. 
        IF AVAILABLE h-artikel THEN 
        DO: 
            delete-it = NO. 
            RETURN. 
        END. 
    END. 

    IF delete-it THEN 
    DO: 
        FIND FIRST dml-art WHERE  dml-art.artnr EQ artnr NO-LOCK NO-ERROR.
        IF AVAILABLE dml-art THEN 
        DO: 
            delete-it = NO. 
            RETURN. 
        END. 
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ artnr NO-LOCK NO-ERROR.      
        IF AVAILABLE reslin-queasy THEN 
        DO: 
            delete-it = NO. 
            RETURN. 
        END. 
        FIND FIRST dml-artdep WHERE dml-artdep.artnr EQ artnr NO-LOCK NO-ERROR.
        IF AVAILABLE dml-artdep THEN 
        DO: 
            delete-it = NO. 
            RETURN. 
        END. 
    END. 
END PROCEDURE.

