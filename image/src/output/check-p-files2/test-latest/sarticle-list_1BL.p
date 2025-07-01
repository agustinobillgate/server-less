DEFINE TEMP-TABLE t-l-artikel  LIKE l-artikel
    FIELD stock-onhand AS DECIMAL. /*FD March 01, 2022*/

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
    FOR EACH l-artikel WHERE l-artikel.artnr GE last-art1 NO-LOCK BY l-artikel.artnr. 

        RUN cr-artikel1.
        IF (counter GE 30) AND (curr-art1 NE l-artikel.artnr) THEN LEAVE.
    END.
    ELSE
    FOR EACH l-artikel NO-LOCK BY l-artikel.artnr. 

        RUN cr-artikel1.
        IF (counter GE 30) AND (curr-art1 NE l-artikel.artnr) THEN LEAVE.
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
          IF (counter GE 30) AND (curr-art NE l-artikel.bezeich) THEN LEAVE.
      END.
    END.
    /*MTIF SUBSTR(last-art,1,1) = "*" THEN 
        last-art = last-art + "*".
    ELSE last-art = last-art + "*". 
    last-art = last-art + "*".*/
    ELSE
    FOR EACH l-artikel WHERE l-artikel.bezeich GE (last-art) NO-LOCK 
        BY l-artikel.bezeich. 

        RUN cr-artikel2.
        IF (counter GE 30) AND (curr-art NE l-artikel.bezeich) THEN LEAVE.
    END.
    /*M  only retieve all macthes input
    ELSE
    FOR EACH l-artikel WHERE l-artikel.bezeich GE last-art NO-LOCK 
        BY l-artikel.bezeich. 
        RUN cr-artikel2.
    END. */
END.
ELSE
DO:
    IF last-art EQ "" THEN
    FOR EACH l-artikel WHERE l-artikel.artnr GT last-art1 NO-LOCK        
        BY l-artikel.artnr. 

        RUN cr-artikel1.
        IF (counter GE 30) AND (curr-art1 NE l-artikel.artnr) THEN LEAVE.
    END.
    ELSE 
    FOR EACH l-artikel WHERE l-artikel.bezeich GT last-art NO-LOCK        
        BY l-artikel.bezeich.

        RUN cr-artikel2.
        IF (counter GE 30) AND (curr-art NE l-artikel.bezeich) THEN LEAVE.
    END.
END.

PROCEDURE cr-artikel1 :
    counter = counter + 1.
    IF counter = 1 THEN first-artnr = l-artikel.artnr.
    IF (counter GE 30) AND (curr-art1 NE l-artikel.artnr) THEN LEAVE.
    
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.

    FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN
    DO:
        t-l-artikel.stock-onhand = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.
    END.
    
    curr-art1 = l-artikel.artnr.
END.

PROCEDURE cr-artikel2 :
    counter = counter + 1.
    IF counter = 1 THEN first-artnr = l-artikel.artnr.
    IF (counter GE 30) AND (curr-art NE l-artikel.bezeich) THEN LEAVE.
    
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
    
    FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN
    DO:
        t-l-artikel.stock-onhand = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.
    END.

    curr-art = l-artikel.bezeich.
END.
