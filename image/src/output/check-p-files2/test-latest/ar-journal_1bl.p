
DEFINE TEMP-TABLE output-list 
    FIELD datum         AS DATE
    FIELD room-no       AS CHAR
    FIELD bill-no       AS INTEGER
    FIELD art-no        AS INTEGER
    FIELD DESCRIPTION   AS CHAR
    FIELD voucher-no    AS CHAR
    FIELD departement   AS CHAR     FORMAT "x(20)"
    FIELD qty           AS INTEGER  FORMAT ">>>>>"
    FIELD amount        AS DECIMAL  FORMAT "->>>>>>>>>>>>>>"
    FIELD zeit          AS CHAR
    FIELD id            AS CHAR.


DEFINE INPUT  PARAMETER from-art        AS INTEGER.
DEFINE INPUT  PARAMETER to-art          AS INTEGER.
DEFINE INPUT  PARAMETER from-dept       AS INTEGER.
DEFINE INPUT  PARAMETER to-dept         AS INTEGER.
DEFINE INPUT  PARAMETER from-date       AS DATE.
DEFINE INPUT  PARAMETER to-date         AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
/*
DEFINE VARIABLE from-art  AS INTEGER INIT 1.
DEFINE VARIABLE to-art    AS INTEGER INIT 24.
DEFINE VARIABLE from-dept AS INTEGER INIT 0.
DEFINE VARIABLE to-dept   AS INTEGER INIT 0.
DEFINE VARIABLE from-date AS DATE    INIT 10/26/18.
DEFINE VARIABLE to-date   AS DATE    INIT 10/26/18.
*/

DEFINE VARIABLE long-digit  AS LOGICAL. 
DEFINE VARIABLE qty         AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date   AS DATE. 
DEFINE VARIABLE last-dept   AS INTEGER INITIAL -1. 
DEFINE VARIABLE it-exist    AS LOGICAL. 

DEFINE VARIABLE descr1      AS CHAR    NO-UNDO.
DEFINE VARIABLE voucher-no  AS CHAR    NO-UNDO.
DEFINE VARIABLE ind         AS INTEGER NO-UNDO.
DEFINE VARIABLE gdelimiter  AS CHAR    NO-UNDO.
DEFINE VARIABLE cnt         AS INTEGER NO-UNDO.
DEFINE VARIABLE i           AS INTEGER NO-UNDO.

 
FOR EACH output-list: 
    DELETE output-list. 
END. 
 
FOR EACH artikel WHERE artikel.artnr GE from-art AND artikel.artnr LE to-art 
    AND (artart EQ 2 OR artart EQ 7) 
    AND artikel.departement GE from-dept 
    AND artikel.departement LE to-dept NO-LOCK 
    BY (artikel.departement * 10000 + artikel.artnr): 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
        FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
            AND billjournal.departement = artikel.departement 
            AND billjournal.bill-datum = curr-date AND billjournal.anzahl NE 0 NO-LOCK                  /* Rulita 041224 | Fixing for serverless issue git 276 */
            BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
            it-exist = YES. 
            FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE bill THEN
            DO:
                FIND FIRST hoteldpt WHERE hoteldpt.num = bill.billtyp NO-LOCK NO-ERROR.
            END.

            CREATE output-list.
            IF AVAILABLE hoteldpt THEN
            DO:
                ASSIGN 
                output-list.datum       = billjournal.bill-datum                                        /* Rulita 041224 | Fixing for serverless issue git 276 */
                output-list.room-no     = billjournal.zinr
                output-list.bill-no     = billjournal.rechnr
                output-list.art-no      = billjournal.artnr
                output-list.DESCRIPTION = billjournal.bezeich
                output-list.departement = hoteldpt.depart
                output-list.qty         = billjournal.anzahl
                output-list.amount      = billjournal.betrag                                            /* Rulita 041224 | Fixing for serverless issue git 276 */
                output-list.zeit        = STRING(billjournal.zeit, "HH:MM:SS")                          /* Rulita 201224 | Fixing for serverless issue git 276 */
                output-list.id          = billjournal.userinit.
            END.
            ELSE 
            DO:
                ASSIGN 
                output-list.datum       = billjournal.bill-datum                                        /* Rulita 041224 | Fixing for serverless issue git 276 */
                output-list.room-no     = billjournal.zinr
                output-list.bill-no     = billjournal.rechnr
                output-list.art-no      = billjournal.artnr
                output-list.DESCRIPTION = billjournal.bezeich
                output-list.qty         = billjournal.anzahl
                output-list.amount      = billjournal.betrag                                            /* Rulita 041224 | Fixing for serverless issue git 276 */
                output-list.zeit        = STRING(billjournal.zeit, "HH:MM:SS")                          /* Rulita 201224 | Fixing for serverless issue git 276 */
                output-list.id          = billjournal.userinit.
            
            END.

            descr1     = "".
            voucher-no = "".

            IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR billjournal.kassarapport THEN
            DO:
                ASSIGN
                    descr1     = billjournal.bezeich
                    voucher-no = "".
            END.
            ELSE IF SUBSTR(billjournal.bezeich,1,19) EQ "Release A/R Payment" THEN
            DO:
                ASSIGN
                    output-list.DESCRIPTION = SUBSTR(billjournal.bezeich,1,19)
                    voucher-no = "".
            END.
            ELSE
            DO:
                IF NOT artikel.bezaendern THEN
                DO:
                    ind = INDEX(billjournal.bezeich, "/").
                    IF ind NE 0 THEN gdelimiter = "/".
                    ELSE
                    DO:
                        ind = INDEX(billjournal.bezeich, "]").
                        IF ind NE 0 THEN gdelimiter = "]".
                    END.
                    IF ind NE 0 THEN
                    DO: 
                        IF ind GT LENGTH(artikel.bezeich) THEN
                            ASSIGN
                                descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                        ELSE
                        DO:
                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                            DO i = 1 TO cnt:
                                IF descr1 = "" THEN
                                    descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                            END.
                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
                        END.
                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                    END.
                    ELSE descr1 = billjournal.bezeich.
                END.
                ELSE    /*got voucher info if desc contains "/"*/
                DO:                    
                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                    IF ind LE 1 THEN
                    ASSIGN 
                        descr1     = billjournal.bezeich
                        voucher-no = "".
                    ELSE
                    ASSIGN 
                        descr1     = ENTRY(1, billjournal.bezeich, "/")    /*change from ind - 1*/
                        voucher-no = ENTRY(2, billjournal.bezeich, "/").   /*change from ind*/
                    
                    IF descr1 EQ "" OR descr1 EQ " " THEN descr1 = artikel.bezeich.
                END.
            END.
            output-list.voucher-no = voucher-no.

            qty = qty + billjournal.anzahl. 
            IF billjournal.anzahl NE 0 THEN 
            DO: 
                sub-tot = sub-tot + billjournal.betrag. 
                tot = tot + billjournal.betrag. 
            END. 
        END. 
    END. 
    IF it-exist THEN 
    DO: 
        create output-list. 
        ASSIGN 
        output-list.departement   = "T O T A L"
        output-list.qty           = qty 
        output-list.amount        = sub-tot
        .
    END. 
END. 
CREATE output-list. 
ASSIGN 
    output-list.departement     = "Grand TOTAL"
    output-list.amount          = tot.

