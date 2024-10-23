DEFINE INPUT PARAMETER endkum AS INTEGER. 
DEFINE INPUT PARAMETER zwkum AS INTEGER. 
DEFINE OUTPUT PARAMETER new-artnr AS CHAR INITIAL 0.

/*
DEFINE VARIABLE endkum AS INTEGER INITIAL 13.             
DEFINE VARIABLE zwkum AS INTEGER INITIAL 21.              
DEFINE VARIABLE new-artnr AS CHARACTER . */


DEFINE VARIABLE l-end AS INTEGER.
DEFINE VARIABLE l-zw  AS INTEGER.
DEFINE VARIABLE ct    AS INTEGER.


DEFINE buffer mhis FOR mathis.
DEFINE buffer bhis FOR mathis.


l-end = LENGTH(STRING(endkum)).
l-zw  = LENGTH(STRING(zwkum)).

FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK
    by fa-artikel.nr DESC:
    FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
    IF AVAILABLE mathis THEN DO:
        IF l-end = 1 THEN DO:
            IF INTEGER(SUBSTR(mathis.asset,2,l-end)) = endkum 
            THEN DO:

                new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                        STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                
                FIND FIRST mhis WHERE mhis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                IF AVAILABLE mhis THEN DO:
                    IF l-end = 2 THEN DO:
                    FOR EACH mhis WHERE INTEGER(SUBSTR(mhis.asset,1,l-end)) = endkum 
                    AND INTEGER(SUBSTR(mhis.asset,3,3)) = zwkum BY mhis.asset DESC:
                        new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mhis.asset,6))+ 1 ,"9999").
                        LEAVE. 
                    END.
                    END.
                    ELSE DO:
                        FOR EACH mhis WHERE INTEGER(SUBSTR(mhis.asset,1,l-end)) = endkum 
                        AND INTEGER(SUBSTR(mhis.asset,4,3)) = zwkum BY mhis.asset DESC:
                           new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mhis.asset,6))+ 1 ,"9999").
                           LEAVE. 
                        END.
                    END.
                END.
                RETURN.
            END.
        END.
        ELSE DO:
            IF INTEGER(SUBSTR(mathis.asset,1,l-end)) = endkum 
            THEN DO:
                new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                        STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                
                FIND FIRST mhis WHERE mhis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                IF AVAILABLE mhis THEN DO:
                    IF l-end = 2 THEN DO:
                    FOR EACH mhis WHERE INTEGER(SUBSTR(mhis.asset,1,l-end)) = endkum 
                    AND INTEGER(SUBSTR(mhis.asset,3,3)) = zwkum BY mhis.asset DESC:
                        new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mhis.asset,6))+ 1 ,"9999").
                        LEAVE. 
                    END.
                    END.
                    ELSE DO:
                        FOR EACH mhis WHERE INTEGER(SUBSTR(mhis.asset,1,l-end)) = endkum 
                        AND INTEGER(SUBSTR(mhis.asset,4,3)) = zwkum BY mhis.asset DESC:
                           new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mhis.asset,6))+ 1 ,"9999").
                           LEAVE. 
                        END.
                    END.
                END.
                RETURN.
            END.
        END.
    END.
END.

new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") + STRING(ct + 1,"9999").



