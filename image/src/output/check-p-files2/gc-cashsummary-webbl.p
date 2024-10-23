/*FD October 18, 2021 => BL for VHP WEB*/
DEFINE TEMP-TABLE cash-list
    FIELD flag      AS INTEGER
    FIELD datum     AS DATE
    FIELD artnr     AS INTEGER EXTENT 20
        INITIAL[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    FIELD bezeich   AS CHARACTER EXTENT 20
        INITIAL["","","","","","","","","","","","","","","","","","","",""]
    FIELD amount    AS DECIMAL EXTENT 20
        INITIAL[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    FIELD str-amount AS CHARACTER EXTENT 20
        INITIAL["","","","","","","","","","","","","","","","","","","",""]
    FIELD tot-str-amount AS CHARACTER
.

DEFINE TEMP-TABLE cash-art
    FIELD pos-nr        AS INTEGER
    FIELD datum         AS DATE
    FIELD artnr         AS INTEGER
    FIELD bezeich       AS CHARACTER
    FIELD amount        AS DECIMAL
.

DEFINE TEMP-TABLE t-cash-art
    FIELD artnr         AS INTEGER
    FIELD bezeich       AS CHARACTER
.

DEFINE INPUT PARAMETER pvILanguage AS INTEGER.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE OUTPUT PARAMETER total-cash-fo AS CHARACTER.
DEFINE OUTPUT PARAMETER total-cash-ou AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-cash-art.
DEFINE OUTPUT PARAMETER TABLE FOR cash-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gc-cashsummary".

DEFINE VARIABLE tot-cash-fo AS DECIMAL.
DEFINE VARIABLE tot-cash-ou AS DECIMAL.
DEFINE VARIABLE p-9900 AS INTEGER.
DEFINE VARIABLE tot-amount AS DECIMAL.

RUN htpint.p(855, OUTPUT p-9900).

RUN cash-summ.

/****************************************************************************************************/
PROCEDURE cash-summ:
DEFINE VARIABLE do-it AS LOGICAL INITIAL NO.
DEFINE VARIABLE i-cash AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE i AS INTEGER NO-UNDO.
DEFINE VARIABLE j AS INTEGER NO-UNDO.
DEFINE VARIABLE loop-date AS DATE.
DEFINE VARIABLE count-date AS DATE.

    FOR EACH cash-list:
        DELETE cash-list.
    END.

    FOR EACH cash-art:
        DELETE cash-art.
    END.    

    FOR EACH t-cash-art:
        DELETE t-cash-art.
    END.       

    /*Create Cash FO*/
    FOR EACH billjournal WHERE billjournal.bill-datum GE from-date 
        AND billjournal.bill-datum LE to-date
        AND billjournal.departement EQ 0 
        AND billjournal.anzahl NE 0 NO-LOCK,    
        FIRST artikel WHERE artikel.artnr EQ billjournal.artnr 
            AND artikel.departement EQ 0 AND artikel.artart EQ 6 
            /*AND artikel.bezeich MATCHES "*Cash*"*/ NO-LOCK 
            BY billjournal.bill-datum BY billjournal.artnr:
        
        do-it = YES.
        IF do-it THEN
        DO:
            FIND FIRST t-cash-art WHERE t-cash-art.artnr = artikel.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE t-cash-art THEN
            DO:
                CREATE t-cash-art.
                ASSIGN
                    t-cash-art.artnr = artikel.artnr
                    t-cash-art.bezeich = artikel.bezeich
                .
            END.

            FIND FIRST cash-art WHERE cash-art.artnr = artikel.artnr 
                AND cash-art.datum = billjournal.bill-datum NO-LOCK NO-ERROR.
            IF NOT AVAILABLE cash-art THEN
            DO:
                i-cash = i-cash + 1.                

                /*CREATE t-cash-art.
                ASSIGN
                    t-cash-art.artnr = artikel.artnr
                    t-cash-art.bezeich = artikel.bezeich
                    t-cash-art.datum = billjournal.bill-datum
                .*/

                CREATE cash-art.
                ASSIGN
                    cash-art.pos-nr     = i-cash
                    cash-art.datum      = billjournal.bill-datum
                    cash-art.artnr      = artikel.artnr
                    cash-art.bezeich    = artikel.bezeich
                    cash-art.amount     = cash-art.amount + billjournal.betrag
                .                
            END. 
            ELSE cash-art.amount = cash-art.amount + billjournal.betrag.   

            tot-cash-fo = tot-cash-fo - billjournal.betrag.
        END.
    END.
    
    /*Create Cash OU*/
    FOR EACH h-journal WHERE h-journal.bill-datum GE from-date
        AND h-journal.bill-datum LE to-date 
        AND h-journal.artnr EQ p-9900 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr
            AND h-artikel.departement EQ h-journal.departement NO-LOCK 
            BY h-journal.bill-datum:

        FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
            AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
        DO:
            FIND FIRST t-cash-art WHERE t-cash-art.artnr = artikel.artnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE t-cash-art THEN
            DO:
                CREATE t-cash-art.
                ASSIGN
                    t-cash-art.artnr = artikel.artnr
                    t-cash-art.bezeich = artikel.bezeich
                .
            END.

            FIND FIRST cash-art WHERE cash-art.artnr = h-artikel.artnrfront 
                AND cash-art.datum = h-journal.bill-datum NO-LOCK NO-ERROR.
            IF NOT AVAILABLE cash-art THEN
            DO:
                i-cash = i-cash + 1.                   

                /*CREATE t-cash-art.
                ASSIGN
                    t-cash-art.artnr = artikel.artnr
                    t-cash-art.bezeich = artikel.bezeich
                    t-cash-art.datum = h-journal.bill-datum
                .*/

                CREATE cash-art.
                ASSIGN
                    cash-art.pos-nr     = i-cash
                    cash-art.datum      = h-journal.bill-datum
                    cash-art.artnr      = artikel.artnr
                    cash-art.bezeich    = artikel.bezeich
                    cash-art.amount     = cash-art.amount + h-journal.betrag
                .                
            END. 
            ELSE cash-art.amount = cash-art.amount + h-journal.betrag.

            tot-cash-ou = tot-cash-ou - h-journal.betrag.
        END.        
    END.

    /*Create Cash List*/
    DO count-date = from-date TO to-date:
        CREATE cash-list.
        cash-list.datum = count-date.
        
        i = 0.
        FOR EACH t-cash-art:
            i = i + 1.
            ASSIGN
                cash-list.artnr[i]      = t-cash-art.artnr
                cash-list.bezeich[i]    = t-cash-art.bezeich
            .
        END.
    END.
    
    /*Assign Amount Cash List*/
    FOR EACH cash-list NO-LOCK BY cash-list.datum:
        FOR EACH cash-art WHERE cash-art.amount NE 0 AND cash-art.datum EQ cash-list.datum NO-LOCK:
            DO j = 1 TO i:
                IF cash-list.artnr[j] EQ cash-art.artnr THEN
                DO:
                    ASSIGN                    
                        cash-list.amount[j] = cash-list.amount[j] + cash-art.amount
                        cash-list.str-amount[j] = STRING(cash-list.amount[j], "->>>,>>>,>>>,>>9.99")    
                    .
                END.                
            END.
        END.        
    END.
    /*Create Cash List => Not Used
    FOR EACH cash-art WHERE cash-art.amount NE 0 NO-LOCK BY cash-art.datum BY cash-art.artnr:        
        
        IF loop-date NE cash-art.datum THEN i = 0.
            
        FIND FIRST cash-list WHERE cash-list.datum EQ cash-art.datum NO-LOCK NO-ERROR.
        IF NOT AVAILABLE cash-list THEN 
        DO:            
            i = i + 1.                
            CREATE cash-list.
            ASSIGN
                cash-list.datum         = cash-art.datum
                cash-list.artnr[i]      = cash-art.artnr
                cash-list.bezeich[i]    = cash-art.bezeich
                cash-list.amount[i]     = cash-art.amount
                cash-list.str-amount[i] = STRING(cash-list.amount[i], "->>>,>>>,>>>,>>9.99")
            .
            loop-date = cash-art.datum.
        END.
        ELSE
        DO:
            i = i + 1.
            ASSIGN
                cash-list.artnr[i]      = cash-art.artnr
                cash-list.bezeich[i]    = cash-art.bezeich
                cash-list.amount[i]     = cash-list.amount[i] + cash-art.amount
                cash-list.str-amount[i] = STRING(cash-list.amount[i], "->>>,>>>,>>>,>>9.99")
            .
            loop-date = cash-art.datum.
        END.
    END. 
    */
    DO i = 1 TO 20:
        FOR EACH cash-list:
            ASSIGN 
                cash-list.amount[i] = - cash-list.amount[i]
                cash-list.str-amount[i] = STRING(cash-list.amount[i], "->>>,>>>,>>>,>>9.99").            
        END.
    END.

    FOR EACH cash-list:
        tot-amount = 0.
        ASSIGN
            tot-amount = cash-list.amount[1] + cash-list.amount[2] + cash-list.amount[3] + cash-list.amount[4] 
                        + cash-list.amount[5] + cash-list.amount[6] + cash-list.amount[7] + cash-list.amount[8]
                        + cash-list.amount[9] + cash-list.amount[10] + cash-list.amount[11] + cash-list.amount[12]
                        + cash-list.amount[13] + cash-list.amount[14] + cash-list.amount[15] + cash-list.amount[16]
                        + cash-list.amount[17] + cash-list.amount[18] + cash-list.amount[19] + cash-list.amount[20]
            .
            cash-list.tot-str-amount = STRING(tot-amount, "->>>,>>>,>>>,>>9.99").
    END.

    total-cash-fo = STRING(tot-cash-fo, "->>>,>>>,>>>,>>9.99").
    total-cash-ou = STRING(tot-cash-ou, "->>>,>>>,>>>,>>9.99").
END PROCEDURE.
