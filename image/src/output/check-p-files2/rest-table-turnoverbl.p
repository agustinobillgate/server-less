DEFINE TEMP-TABLE turnover-table-list    
    FIELD table-no          AS CHARACTER
    FIELD table-desc        AS CHARACTER
    FIELD food-amount       AS CHARACTER EXTENT 4 /*1=morning;2=afternoon/evening;3=night;4=supper*/   
    FIELD bev-amount        AS CHARACTER EXTENT 4   
    FIELD other-amount      AS CHARACTER EXTENT 4
    FIELD mtd-food-amount   AS CHARACTER EXTENT 4    
    FIELD mtd-bev-amount    AS CHARACTER EXTENT 4   
    FIELD mtd-other-amount  AS CHARACTER EXTENT 4
    FIELD ytd-food-amount   AS CHARACTER EXTENT 4    
    FIELD ytd-bev-amount    AS CHARACTER EXTENT 4   
    FIELD ytd-other-amount  AS CHARACTER EXTENT 4
    .

DEFINE TEMP-TABLE t-table-list    
    FIELD table-no          AS INTEGER
    FIELD table-desc        AS CHARACTER
    FIELD food-amount       AS DECIMAL EXTENT 4 /*1=morning;2=afternoon/evening;3=night;4=supper*/   
    FIELD bev-amount        AS DECIMAL EXTENT 4   
    FIELD other-amount      AS DECIMAL EXTENT 4
    FIELD mtd-food-amount   AS DECIMAL EXTENT 4    
    FIELD mtd-bev-amount    AS DECIMAL EXTENT 4   
    FIELD mtd-other-amount  AS DECIMAL EXTENT 4
    FIELD ytd-food-amount   AS DECIMAL EXTENT 4    
    FIELD ytd-bev-amount    AS DECIMAL EXTENT 4   
    FIELD ytd-other-amount  AS DECIMAL EXTENT 4
    .

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER dept-number  AS INTEGER.
DEFINE INPUT PARAMETER excl-compli  AS LOGICAL.
DEFINE INPUT PARAMETER excl-taxserv AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR turnover-table-list.

DEFINE VARIABLE start-jan               AS DATE.
DEFINE VARIABLE i                       AS INTEGER.
DEFINE VARIABLE curr-amount             AS DECIMAL.
DEFINE VARIABLE tot-food-amount         AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-bev-amount          AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-other-amount        AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-mtd-food-amount     AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-mtd-bev-amount      AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-mtd-other-amount    AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-ytd-food-amount     AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-ytd-bev-amount      AS DECIMAL EXTENT 4.
DEFINE VARIABLE tot-ytd-other-amount    AS DECIMAL EXTENT 4.

start-jan = DATE(1,1, YEAR(to-date)).

RUN create-turnover-table.

PROCEDURE create-turnover-table:    
    FOR EACH h-bill-line WHERE h-bill-line.departement EQ dept-number
        AND h-bill-line.bill-datum GE start-jan AND h-bill-line.bill-datum LE to-date NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr
        AND h-artikel.departement EQ h-bill-line.departement
        AND h-artikel.artart EQ 0 NO-LOCK,
        FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
        AND artikel.departement EQ h-bill-line.departement NO-LOCK
        BY h-bill-line.bill-datum BY h-bill-line.tischnr:

        IF excl-compli THEN
        DO:
            FIND FIRST h-compli WHERE h-compli.rechnr EQ h-bill-line.rechnr
                AND h-compli.departement EQ h-bill-line.departement NO-LOCK NO-ERROR.
            IF AVAILABLE h-compli THEN NEXT.
        END.

        FIND FIRST t-table-list WHERE t-table-list.table-no EQ h-bill-line.tischnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-table-list THEN
        DO:
            CREATE t-table-list.
            t-table-list.table-no = h-bill-line.tischnr.

            FIND FIRST tisch WHERE tisch.tischnr EQ h-bill-line.tischnr
                AND tisch.departement EQ h-bill-line.departement NO-LOCK NO-ERROR.
            IF AVAILABLE tisch THEN t-table-list.table-desc = tisch.bezeich.
        END.

        IF excl-taxserv THEN curr-amount = h-artikel.epreis1 * h-bill-line.anzahl.
        ELSE curr-amount = h-bill-line.betrag.

        IF h-bill-line.bill-datum EQ to-date THEN
        DO:
            IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
            DO:  
                IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.food-amount[1] = t-table-list.food-amount[1] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.food-amount[2] = t-table-list.food-amount[2] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.food-amount[3] = t-table-list.food-amount[3] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.food-amount[4] = t-table-list.food-amount[4] + curr-amount.                        
            END.  
            ELSE IF artikel.umsatzart EQ 6 THEN
            DO:
                IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.bev-amount[1] = t-table-list.bev-amount[1] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.bev-amount[2] = t-table-list.bev-amount[2] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.bev-amount[3] = t-table-list.bev-amount[3] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.bev-amount[4] = t-table-list.bev-amount[4] + curr-amount.
            END.
            ELSE
            DO:
                IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.other-amount[1] = t-table-list.other-amount[1] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.other-amount[2] = t-table-list.other-amount[2] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.other-amount[3] = t-table-list.other-amount[3] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.other-amount[4] = t-table-list.other-amount[4] + curr-amount.
            END.
        END.  
        IF h-bill-line.bill-datum GE from-date AND h-bill-line.bill-datum LE to-date THEN /*MTD*/
        DO:
            IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
            DO:  
                IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.mtd-food-amount[1] = t-table-list.mtd-food-amount[1] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.mtd-food-amount[2] = t-table-list.mtd-food-amount[2] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.mtd-food-amount[3] = t-table-list.mtd-food-amount[3] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.mtd-food-amount[4] = t-table-list.mtd-food-amount[4] + curr-amount.                        
            END.  
            ELSE IF artikel.umsatzart EQ 6 THEN
            DO:
                IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.mtd-bev-amount[1] = t-table-list.mtd-bev-amount[1] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.mtd-bev-amount[2] = t-table-list.mtd-bev-amount[2] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.mtd-bev-amount[3] = t-table-list.mtd-bev-amount[3] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.mtd-bev-amount[4] = t-table-list.mtd-bev-amount[4] + curr-amount.
            END.
            ELSE
            DO:
                IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.mtd-other-amount[1] = t-table-list.mtd-other-amount[1] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.mtd-other-amount[2] = t-table-list.mtd-other-amount[2] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.mtd-other-amount[3] = t-table-list.mtd-other-amount[3] + curr-amount.
                ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.mtd-other-amount[4] = t-table-list.mtd-other-amount[4] + curr-amount.
            END.
        END. 

        /*YTD*/
        IF (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) THEN
        DO:  
            IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.ytd-food-amount[1] = t-table-list.ytd-food-amount[1] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.ytd-food-amount[2] = t-table-list.ytd-food-amount[2] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.ytd-food-amount[3] = t-table-list.ytd-food-amount[3] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.ytd-food-amount[4] = t-table-list.ytd-food-amount[4] + curr-amount.                        
        END.  
        ELSE IF artikel.umsatzart EQ 6 THEN
        DO:
            IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.ytd-bev-amount[1] = t-table-list.ytd-bev-amount[1] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.ytd-bev-amount[2] = t-table-list.ytd-bev-amount[2] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.ytd-bev-amount[3] = t-table-list.ytd-bev-amount[3] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.ytd-bev-amount[4] = t-table-list.ytd-bev-amount[4] + curr-amount.
        END.
        ELSE
        DO:
            IF h-bill-line.betriebsnr EQ 1 THEN t-table-list.ytd-other-amount[1] = t-table-list.ytd-other-amount[1] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 2 THEN t-table-list.ytd-other-amount[2] = t-table-list.ytd-other-amount[2] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 3 THEN t-table-list.ytd-other-amount[3] = t-table-list.ytd-other-amount[3] + curr-amount.
            ELSE IF h-bill-line.betriebsnr EQ 4 THEN t-table-list.ytd-other-amount[4] = t-table-list.ytd-other-amount[4] + curr-amount.
        END.
    END.

    FOR EACH t-table-list NO-LOCK BY INT(t-table-list.table-no):
        CREATE turnover-table-list.
        ASSIGN
            turnover-table-list.table-no = STRING(t-table-list.table-no, ">>>,>>>")
            turnover-table-list.table-desc = t-table-list.table-desc
            .

        DO i = 1 TO 4:
            ASSIGN
                turnover-table-list.food-amount[i]      = STRING(t-table-list.food-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.bev-amount[i]       = STRING(t-table-list.bev-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.other-amount[i]     = STRING(t-table-list.other-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.mtd-food-amount[i]  = STRING(t-table-list.mtd-food-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.mtd-bev-amount[i]   = STRING(t-table-list.mtd-bev-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.mtd-other-amount[i] = STRING(t-table-list.mtd-other-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.ytd-food-amount[i]  = STRING(t-table-list.ytd-food-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.ytd-bev-amount[i]   = STRING(t-table-list.ytd-bev-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.ytd-other-amount[i] = STRING(t-table-list.ytd-other-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                .

            ASSIGN
                tot-food-amount[i]      = tot-food-amount[i]        + t-table-list.food-amount[i]      
                tot-bev-amount[i]       = tot-bev-amount[i]         + t-table-list.bev-amount[i]
                tot-other-amount[i]     = tot-other-amount[i]       + t-table-list.other-amount[i]
                tot-mtd-food-amount[i]  = tot-mtd-food-amount[i]    + t-table-list.mtd-food-amount[i]
                tot-mtd-bev-amount[i]   = tot-mtd-bev-amount[i]     + t-table-list.mtd-bev-amount[i] 
                tot-mtd-other-amount[i] = tot-mtd-other-amount[i]   + t-table-list.mtd-other-amount[i]
                tot-ytd-food-amount[i]  = tot-ytd-food-amount[i]    + t-table-list.ytd-food-amount[i]
                tot-ytd-bev-amount[i]   = tot-ytd-bev-amount[i]     + t-table-list.ytd-bev-amount[i] 
                tot-ytd-other-amount[i] = tot-ytd-other-amount[i]   + t-table-list.ytd-other-amount[i]
                .
        END.        
    END.

    FIND FIRST turnover-table-list NO-LOCK NO-ERROR.
    IF AVAILABLE turnover-table-list THEN
    DO:
        CREATE turnover-table-list.
        turnover-table-list.table-desc = "T O T A L".
        
        DO i = 1 TO 4:
            ASSIGN
                turnover-table-list.food-amount[i]      = STRING(tot-food-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.bev-amount[i]       = STRING(tot-bev-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.other-amount[i]     = STRING(tot-other-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.mtd-food-amount[i]  = STRING(tot-mtd-food-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.mtd-bev-amount[i]   = STRING(tot-mtd-bev-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.mtd-other-amount[i] = STRING(tot-mtd-other-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.ytd-food-amount[i]  = STRING(tot-ytd-food-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.ytd-bev-amount[i]   = STRING(tot-ytd-bev-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                turnover-table-list.ytd-other-amount[i] = STRING(tot-ytd-other-amount[i], "->>,>>>,>>>,>>>,>>9.99")
                .
        END.
    END.
END PROCEDURE.
