DEFINE TEMP-TABLE t-l-artikel  
    FIELD artnr        AS INTEGER 
    FIELD bezeich      AS CHAR 
    FIELD masseinheit  AS CHAR
    FIELD inhalt       AS DECIMAL
    FIELD traubensorte AS CHAR
    FIELD unit-price   AS DECIMAL
    FIELD lief-einheit AS DECIMAL
    FIELD soh          AS DECIMAL. 

DEFINE INPUT PARAMETER sorttype            AS INT   NO-UNDO.
DEFINE INPUT PARAMETER last-art            AS CHAR  NO-UNDO.
DEFINE INPUT PARAMETER last-art1           AS INT   NO-UNDO.
DEFINE INPUT PARAMETER idFlag              AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-artikel.

DEFINE VARIABLE counter     AS INTEGER  NO-UNDO INIT 0.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

IF sorttype = 1 THEN
DO:
    IF last-art1 NE 0 THEN
    FOR EACH l-artikel WHERE l-artikel.artnr GE last-art1 NO-LOCK 
        BY l-artikel.artnr. 
        
        IF idFlag = "quotation" THEN DO:
            RUN create-artikel1.
        END.
        ELSE IF idFlag = "dml" THEN DO:
            RUN create-artikel2.
        END.
        ELSE IF idFlag = "pr" THEN DO:
            RUN create-artikel3.
        END.
        ELSE RUN create-artikel.
    END.
    ELSE
    FOR EACH l-artikel NO-LOCK BY l-artikel.artnr. 
        IF idFlag = "quotation" THEN DO:
            RUN create-artikel1.
        END.
        ELSE IF idFlag = "dml" THEN DO:
            RUN create-artikel2.
        END.
        ELSE IF idFlag = "pr" THEN DO:
            RUN create-artikel3.
        END.
        ELSE RUN create-artikel.
    END.
END.    
ELSE IF sorttype = 2 THEN
DO:    
    IF SUBSTR(last-art,1,1) = "*" THEN 
    DO:

      FOR EACH l-artikel NO-LOCK BY l-artikel.bezeich: 
      IF idFlag = "quotation" THEN DO:
        RUN create-artikel1.
      END.
      ELSE IF idFlag = "dml" THEN DO:
        RUN create-artikel2.
      END.
      ELSE IF idFlag = "pr" THEN DO:
        RUN create-artikel3.
      END.
      ELSE RUN create-artikel.
      END.
    END.
    /*start bernatd A0372A 2025*/
    ELSE IF last-art = "ALL" THEN 
    DO:
        FOR EACH l-artikel NO-LOCK BY l-artikel.artnr: 
            IF idFlag = "quotation" THEN 
            DO:
                RUN create-artikel1.
            END.
            ELSE IF idFlag = "dml" THEN DO:
                RUN create-artikel2.
            END.
            ELSE IF idFlag = "pr" THEN DO:
                RUN create-artikel3.
            END.
            ELSE RUN create-artikel.
        END.
    END.
    /*end bernatd A0372A 2025*/
    ELSE
    FOR EACH l-artikel WHERE l-artikel.bezeich GE (last-art) NO-LOCK 
        BY l-artikel.bezeich. 
    IF idFlag = "quotation" THEN DO:
        RUN create-artikel1.
    END.
    ELSE IF idFlag = "dml" THEN DO:
        RUN create-artikel2.
    END.
    ELSE IF idFlag = "pr" THEN DO:
        RUN create-artikel3.
    END.
    ELSE RUN create-artikel.
    END.
END.
ELSE
DO:
    IF last-art EQ "" THEN
    FOR EACH l-artikel WHERE l-artikel.artnr GT last-art1 NO-LOCK 
        BY l-artikel.artnr. 
        IF idFlag = "quotation" THEN DO:
            RUN create-artikel1.
        END.
        ELSE IF idFlag = "dml" THEN DO:
            RUN create-artikel2.
        END.
        ELSE IF idFlag = "pr" THEN DO:
            RUN create-artikel3.
        END.
        ELSE RUN create-artikel.
    END.
    ELSE 
    FOR EACH l-artikel WHERE l-artikel.bezeich GT last-art NO-LOCK 
    BY l-artikel.bezeich:
        IF idFlag = "quotation" THEN DO:
            RUN create-artikel1.
        END.
        ELSE IF idFlag = "dml" THEN DO:
            RUN create-artikel2.
        END.
        ELSE IF idFlag = "pr" THEN DO:
            RUN create-artikel3.
        END.
        ELSE RUN create-artikel.
    END.
END.

PROCEDURE create-artikel:
    CREATE t-l-artikel. 
        ASSIGN 
            t-l-artikel.artnr        = l-artikel.artnr
            t-l-artikel.bezeich      = l-artikel.bezeich
            t-l-artikel.masseinheit  = l-artikel.masseinheit
            t-l-artikel.traubensorte = l-artikel.traubensorte
            t-l-artikel.lief-einheit = l-artikel.lief-einheit
            t-l-artikel.inhalt       = l-artikel.inhalt.
END.

PROCEDURE create-artikel1:
    CREATE t-l-artikel. 
        ASSIGN 
            t-l-artikel.artnr        = l-artikel.artnr
            t-l-artikel.bezeich      = l-artikel.bezeich
            t-l-artikel.inhalt       = l-artikel.inhalt
            t-l-artikel.masseinheit  = l-artikel.masseinheit
            t-l-artikel.lief-einheit = l-artikel.lief-einheit
            t-l-artikel.traubensorte = l-artikel.traubensorte.
END.

PROCEDURE create-artikel2:
    CREATE t-l-artikel. 
        ASSIGN 
            t-l-artikel.artnr          = l-artikel.artnr
            t-l-artikel.bezeich        = l-artikel.bezeich
            t-l-artikel.masseinheit    = l-artikel.masseinheit
            t-l-artikel.inhalt         = l-artikel.inhalt
            t-l-artikel.lief-einheit   = l-artikel.lief-einheit
            t-l-artikel.traubensorte   = l-artikel.traubensorte.
            .
END.        

PROCEDURE create-artikel3:
    CREATE t-l-artikel. 
        ASSIGN 
            t-l-artikel.artnr          = l-artikel.artnr
            t-l-artikel.bezeich        = l-artikel.bezeich
            t-l-artikel.masseinheit    = l-artikel.masseinheit
            t-l-artikel.inhalt         = l-artikel.inhalt
            t-l-artikel.lief-einheit   = l-artikel.lief-einheit
            t-l-artikel.traubensorte   = l-artikel.traubensorte.
            .
     FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
     IF AVAILABLE l-bestand THEN
     DO:
         t-l-artikel.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.

     END.
END.        


