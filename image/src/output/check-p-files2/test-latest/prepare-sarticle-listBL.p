DEFINE TEMP-TABLE t-l-artikel  LIKE l-artikel.
    

DEFINE OUTPUT PARAMETER first-artnr        AS INT   NO-UNDO.
DEFINE OUTPUT PARAMETER curr-art           AS CHAR  NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR t-l-artikel.

DEFINE VARIABLE counter     AS INTEGER  NO-UNDO INIT 0.

FIND FIRST l-artikel NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel AND NOT l-artikel.herkunft MATCHES ("*;*") THEN
  RUN add-sunits.

FOR EACH l-artikel NO-LOCK BY l-artikel.bezeich. 
    counter = counter + 1.
    IF counter = 1 THEN first-artnr = l-artikel.artnr.
    IF (counter GE 30) AND (curr-art NE l-artikel.bezeich) THEN LEAVE.
    
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
    curr-art = l-artikel.bezeich.
END.


/***************************** PROCEDURES *****************************/
PROCEDURE add-sunits:
DEF BUFFER sbuff FOR l-artikel.
    FIND FIRST l-artikel NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-artikel:
        IF NOT l-artikel.herkunft MATCHES("*;*") THEN
        DO TRANSACTION:
            FIND FIRST sbuff WHERE RECID(sbuff) = RECID(l-artikel)
                EXCLUSIVE-LOCK.
            sbuff.herkunft = sbuff.herkunft + ";;".
            FIND CURRENT sbuff NO-LOCK.
        END.
        FIND NEXT l-artikel NO-LOCK NO-ERROR.
    END.
END.

