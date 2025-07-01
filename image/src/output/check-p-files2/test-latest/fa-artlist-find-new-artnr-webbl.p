DEFINE INPUT PARAMETER endkum AS INTEGER. 
DEFINE INPUT PARAMETER zwkum AS INTEGER. 
DEFINE OUTPUT PARAMETER new-artnr AS CHAR INITIAL 0.

/*
DEFINE VARIABLE endkum AS INTEGER INITIAL 13.             
DEFINE VARIABLE zwkum AS INTEGER INITIAL 21.              
DEFINE VARIABLE new-artnr AS CHARACTER . 

DEFINE TEMP-TABLE payload-list
    FIELD endkum AS INTEGER  
    FIELD zwkum AS INTEGER.

DEFINE TEMP-TABLE ouput-list
    FIELD new-artnr AS CHAR INITIAL 0
    FIELD flag AS LOGICAL INITIAL YES.

DEFINE INPUT PARAMETER TABLE FOR 
DEFINE OUTPUT PARAMETER TABLE FOR */

DEFINE VARIABLE l-end AS INTEGER.
DEFINE VARIABLE l-zw  AS INTEGER.
DEFINE VARIABLE ct    AS INTEGER.


DEFINE buffer buff-mathis FOR mathis. /* mhis -> buff-mathis */
DEFINE buffer b-mathis FOR mathis. /* bhis -> b-mathis */

/*
l-end = LENGTH(STRING(endkum)).
l-zw  = LENGTH(STRING(zwkum)). */

/* Comment for upcoming ticket */
FIND FIRST htparam WHERE htparam.paramnr = 293 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    IF htparam.flogical THEN
    DO:
        FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK
            by fa-artikel.nr DESC:
            FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mathis THEN 
            DO:
                IF LENGTH(TRIM(mathis.asset)) EQ 9 THEN
                DO:
                    /*
                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"999999"). */
                    new-artnr = STRING(endkum,"99") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                    DO WHILE TRUE:
                        FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                        IF AVAILABLE buff-mathis THEN 
                        DO:
                            new-artnr = STRING(endkum,"99") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                        END.
                        ELSE
                        DO:
                            new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(new-artnr,6)) ,"999999").
                            DO WHILE TRUE:
                                FIND FIRST b-mathis WHERE b-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                                IF AVAILABLE b-mathis THEN
                                DO:
                                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                            STRING(INTEGER(SUBSTR(b-mathis.asset,7))+ 1 ,"999999").
                                END.
                                ELSE
                                DO:
                                    LEAVE.
                                END.
                            END.
                            LEAVE.
                        END.
                    END.
                    RETURN.
                END.
                ELSE 
                DO:
                    /*
                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,7))+ 1 ,"999999").*/
                    /**/
                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,7))+ 1 ,"9999").
                    
                    IF LENGTH(TRIM(new-artnr)) NE LENGTH(TRIM(mathis.asset)) 
                        OR new-artnr MATCHES ("*?*") THEN 
                    DO:
                        new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,7))+ 1 ,"999999").
                    END.

                    DO WHILE TRUE:
                        FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                        IF AVAILABLE buff-mathis THEN 
                        DO:
                            IF LENGTH(TRIM(new-artnr)) EQ 12 THEN
                            DO:
                                new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(buff-mathis.asset,7))+ 1 ,"999999").
                            END.
                            ELSE
                            DO:
                                new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(buff-mathis.asset,7))+ 1 ,"9999").
                            END.
                            
                        END.
                        ELSE
                        DO:
                            new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(new-artnr,7)) ,"999999").
                            DO WHILE TRUE:
                                FIND FIRST b-mathis WHERE b-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                                IF AVAILABLE b-mathis THEN
                                DO:
                                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                            STRING(INTEGER(SUBSTR(b-mathis.asset,7))+ 1 ,"999999").
                                END.
                                ELSE
                                DO:
                                    LEAVE.
                                END.
                            END.
                            LEAVE.
                        END.
                    END.
                    RETURN.
                END.
            END.
        END.

        new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") + STRING(ct + 1,"999999").
    END.
    ELSE
    DO:
        FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK
            by fa-artikel.nr DESC:
            FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mathis THEN 
            DO:
                /*
                new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                        STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                DO WHILE TRUE:
                    FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                    IF AVAILABLE buff-mathis THEN 
                    DO:
                        new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                    END.
                    ELSE
                    DO:
                        LEAVE.
                    END.
                END.
                RETURN. */

                IF LENGTH(TRIM(mathis.asset)) EQ 9 THEN
                DO:
                    /*new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").*/
                    new-artnr = STRING(endkum,"99") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").

                    DO WHILE TRUE:
                        FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                        IF AVAILABLE buff-mathis THEN 
                        DO:
                            new-artnr = STRING(endkum,"99") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                        END.
                        ELSE
                        DO:
                            new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(new-artnr,6)) ,"9999").
                            LEAVE.
                        END.
                    END.
                    RETURN.
                END.
                ELSE 
                DO:
                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,7))+ 1 ,"9999").
                    DO WHILE TRUE:
                        FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                        IF AVAILABLE buff-mathis THEN 
                        DO:
                            new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                    STRING(INTEGER(SUBSTR(buff-mathis.asset,7))+ 1 ,"9999").
                        END.
                        ELSE
                        DO:
                            LEAVE.
                        END.
                    END.
                    RETURN.
                END.
            END.
        END.

        new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") + STRING(ct + 1,"9999").

    END.
END.
ELSE 
DO:
    FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK
        by fa-artikel.nr DESC:
        FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
        IF AVAILABLE mathis THEN 
        DO:
            IF LENGTH(TRIM(mathis.asset)) EQ 9 THEN
            DO:
                /*new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").*/
                new-artnr = STRING(endkum,"99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                DO WHILE TRUE:
                    FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                    IF AVAILABLE buff-mathis THEN 
                    DO:
                        new-artnr = STRING(endkum,"99") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                    END.
                    ELSE
                    DO:
                        new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(new-artnr,6)) ,"9999").
                        LEAVE.
                    END.
                END.
                RETURN.
            END.
            ELSE 
            DO:
                new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                        STRING(INTEGER(SUBSTR(mathis.asset,7))+ 1 ,"9999").
                DO WHILE TRUE:
                    FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                    IF AVAILABLE buff-mathis THEN 
                    DO:
                        new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(buff-mathis.asset,7))+ 1 ,"9999").
                    END.
                    ELSE
                    DO:
                        LEAVE.
                    END.
                END.
                RETURN.
            END.
        END.
    END.

    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") + STRING(ct + 1,"9999").
END. 

/*
FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK
    by fa-artikel.nr DESC:
    FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
    IF AVAILABLE mathis THEN 
    DO:
        IF LENGTH(TRIM(mathis.asset)) EQ 9 THEN
        DO:
            new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                        STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
            DO WHILE TRUE:
                FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                IF AVAILABLE buff-mathis THEN 
                DO:
                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                END.
                ELSE
                DO:
                    LEAVE.
                END.
            END.
            RETURN.
        END.
        ELSE 
        DO:
            new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                    STRING(INTEGER(SUBSTR(mathis.asset,7))+ 1 ,"9999").
            DO WHILE TRUE:
                FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                IF AVAILABLE buff-mathis THEN 
                DO:
                    new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(buff-mathis.asset,7))+ 1 ,"9999").
                END.
                ELSE
                DO:
                    LEAVE.
                END.
            END.
            RETURN.
        END.
    END.
END.

new-artnr = STRING(endkum,"999") + STRING(zwkum,"999") + STRING(ct + 1,"9999").
*/
/* Dump data 
    FOR EACH fa-artikel WHERE fa-artikel.subgrp = zwkum AND fa-artikel.gnr = endkum NO-LOCK
        by fa-artikel.nr DESC:
        FIND FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK NO-ERROR.
        IF AVAILABLE mathis THEN DO:
            IF l-end = 1 THEN DO:
                IF INTEGER(SUBSTR(mathis.asset,2,l-end)) = endkum 
                THEN DO:

                    new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                    DO WHILE TRUE:
                        FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                        IF AVAILABLE buff-mathis THEN 
                        DO:
                            IF l-end = 2 THEN 
                            DO:
                                FOR EACH buff-mathis WHERE INTEGER(SUBSTR(buff-mathis.asset,1,l-end)) = endkum 
                                    AND INTEGER(SUBSTR(buff-mathis.asset,3,3)) = zwkum BY buff-mathis.asset DESC:
                                    new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                                        STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                                    LEAVE. 
                                END.
                            END.
                            ELSE 
                            DO:
                                new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                                        STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                                FOR EACH buff-mathis WHERE INTEGER(SUBSTR(buff-mathis.asset,1,l-end)) = endkum 
                                    AND INTEGER(SUBSTR(buff-mathis.asset,4,3)) = zwkum BY buff-mathis.asset DESC:
                                    new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                                        STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                                    LEAVE. 
                                END.
                            END.
                        END.
                        ELSE
                        DO:
                            LEAVE.
                        END.
                    END.
                    RETURN.
                END.
            END.
            ELSE 
            DO:
                IF INTEGER(SUBSTR(mathis.asset,1,l-end)) = endkum THEN 
                DO:
                    new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                            STRING(INTEGER(SUBSTR(mathis.asset,6))+ 1 ,"9999").
                    
                    FIND FIRST buff-mathis WHERE buff-mathis.asset = TRIM(new-artnr) NO-LOCK NO-ERROR.
                    IF AVAILABLE buff-mathis THEN DO:
                        IF l-end = 2 THEN DO:
                        FOR EACH buff-mathis WHERE INTEGER(SUBSTR(buff-mathis.asset,1,l-end)) = endkum 
                        AND INTEGER(SUBSTR(buff-mathis.asset,3,3)) = zwkum BY buff-mathis.asset DESC:
                            new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
                            LEAVE. 
                        END.
                        END.
                        ELSE DO:
                            FOR EACH buff-mathis WHERE INTEGER(SUBSTR(buff-mathis.asset,1,l-end)) = endkum 
                            AND INTEGER(SUBSTR(buff-mathis.asset,4,3)) = zwkum BY buff-mathis.asset DESC:
                            new-artnr = STRING(endkum,">99") + STRING(zwkum,"999") +
                                STRING(INTEGER(SUBSTR(buff-mathis.asset,6))+ 1 ,"9999").
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

*/


