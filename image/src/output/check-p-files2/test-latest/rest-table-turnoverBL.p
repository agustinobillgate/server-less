DEFINE TEMP-TABLE turnover-table-list    
    FIELD table-no          AS CHARACTER
    FIELD table-desc        AS CHARACTER
    FIELD pax               AS INTEGER
    FIELD food-amount       AS CHARACTER EXTENT 4 /*1=morning;2=afternoon/evening;3=night;4=supper*/   
    FIELD bev-amount        AS CHARACTER EXTENT 4   
    FIELD other-amount      AS CHARACTER EXTENT 4
    FIELD mtd-pax           AS INTEGER
    FIELD mtd-food-amount   AS CHARACTER EXTENT 4    
    FIELD mtd-bev-amount    AS CHARACTER EXTENT 4   
    FIELD mtd-other-amount  AS CHARACTER EXTENT 4
    FIELD ytd-pax           AS INTEGER
    FIELD ytd-food-amount   AS CHARACTER EXTENT 4    
    FIELD ytd-bev-amount    AS CHARACTER EXTENT 4   
    FIELD ytd-other-amount  AS CHARACTER EXTENT 4
    .

DEFINE TEMP-TABLE t-table-list    
    FIELD table-no          AS INTEGER
    FIELD table-desc        AS CHARACTER
    FIELD pax               AS INTEGER
    FIELD food-amount       AS DECIMAL EXTENT 4 /*1=morning;2=afternoon/evening;3=night;4=supper*/   
    FIELD bev-amount        AS DECIMAL EXTENT 4   
    FIELD other-amount      AS DECIMAL EXTENT 4
    FIELD mtd-pax           AS INTEGER
    FIELD mtd-food-amount   AS DECIMAL EXTENT 4    
    FIELD mtd-bev-amount    AS DECIMAL EXTENT 4   
    FIELD mtd-other-amount  AS DECIMAL EXTENT 4
    FIELD ytd-pax           AS INTEGER
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
DEFINE VARIABLE curr-rechnr             AS INTEGER.
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
DEFINE VARIABLE total-pax               AS INTEGER.
DEFINE VARIABLE total-mtd-pax           AS INTEGER.
DEFINE VARIABLE total-ytd-pax           AS INTEGER.
DEFINE VARIABLE servtax-use-foart       AS LOGICAL.       
DEFINE VARIABLE serv-percent            AS DECIMAL INITIAL 0.  
DEFINE VARIABLE mwst-percent            AS DECIMAL INITIAL 0.
DEFINE VARIABLE fact                    AS DECIMAL INITIAL 1.
DEFINE VARIABLE bill-date110            AS DATE.  
DEFINE VARIABLE bill-date               AS DATE.
DEFINE VARIABLE service-taxable         AS LOGICAL NO-UNDO.

start-jan = DATE(1,1, YEAR(to-date)).
FIND FIRST hoteldpt WHERE hoteldpt.num EQ dept-number NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN
DO:
    servtax-use-foart = hoteldpt.defult.
END. 

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK NO-ERROR.   
IF AVAILABLE htparam THEN
DO:
    ASSIGN  
        bill-date110 = vhp.htparam.fdate  
        bill-date    = vhp.htparam.fdate  
        .
END.
  
RUN create-turnover-table.

PROCEDURE create-turnover-table:    
    FOR EACH h-bill-line WHERE h-bill-line.departement EQ dept-number
        AND h-bill-line.bill-datum GE start-jan AND h-bill-line.bill-datum LE to-date NO-LOCK,
        FIRST h-bill WHERE h-bill.rechnr EQ h-bill-line.rechnr 
        AND h-bill.departement EQ h-bill-line.departement NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr
        AND h-artikel.departement EQ h-bill-line.departement
        AND h-artikel.artart EQ 0 NO-LOCK,
        FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
        AND artikel.departement EQ h-bill-line.departement NO-LOCK
        BY h-bill-line.bill-datum BY h-bill-line.rechnr BY h-bill-line.tischnr:        

        IF excl-compli THEN
        DO:
            FIND FIRST h-compli WHERE h-compli.rechnr EQ h-bill-line.rechnr
                AND h-compli.departement EQ h-bill-line.departement NO-LOCK NO-ERROR.
            IF AVAILABLE h-compli THEN NEXT.
        END.

        RUN cal-servat (h-artikel.departement, h-artikel.artnr, h-artikel.service-code, 
                        h-artikel.mwst-code, h-bill-line.bill-datum,  
                        OUTPUT serv-percent, OUTPUT mwst-percent, OUTPUT fact).

        IF excl-taxserv THEN curr-amount = h-bill-line.betrag / fact.
        ELSE curr-amount = h-bill-line.betrag.

        FIND FIRST t-table-list WHERE t-table-list.table-no EQ h-bill-line.tischnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-table-list THEN
        DO:
            CREATE t-table-list.
            t-table-list.table-no = h-bill-line.tischnr.

            FIND FIRST tisch WHERE tisch.tischnr EQ h-bill-line.tischnr
                AND tisch.departement EQ h-bill-line.departement NO-LOCK NO-ERROR.
            IF AVAILABLE tisch THEN t-table-list.table-desc = tisch.bezeich.
        END.        

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

            IF h-bill-line.betriebsnr NE 0 AND curr-rechnr NE h-bill-line.rechnr THEN
            DO:
                t-table-list.pax = t-table-list.pax + h-bill.belegung.
                total-pax = total-pax + h-bill.belegung.
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

            IF h-bill-line.betriebsnr NE 0 AND curr-rechnr NE h-bill-line.rechnr THEN
            DO:
                t-table-list.mtd-pax = t-table-list.mtd-pax + h-bill.belegung.
                total-mtd-pax = total-mtd-pax + h-bill.belegung.
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

        IF h-bill-line.betriebsnr NE 0 AND curr-rechnr NE h-bill-line.rechnr THEN
        DO:
            t-table-list.ytd-pax = t-table-list.ytd-pax + h-bill.belegung.
            total-ytd-pax = total-ytd-pax + h-bill.belegung.
        END.

        curr-rechnr = h-bill-line.rechnr.
    END.

    FOR EACH t-table-list NO-LOCK BY INT(t-table-list.table-no):
        CREATE turnover-table-list.
        ASSIGN
            turnover-table-list.table-no    = STRING(t-table-list.table-no, ">>>,>>>")
            turnover-table-list.table-desc  = t-table-list.table-desc
            turnover-table-list.pax         = t-table-list.pax    
            turnover-table-list.mtd-pax     = t-table-list.mtd-pax
            turnover-table-list.ytd-pax     = t-table-list.ytd-pax
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
        ASSIGN
            turnover-table-list.table-desc  = "T O T A L"
            turnover-table-list.pax         = total-pax    
            turnover-table-list.mtd-pax     = total-mtd-pax
            turnover-table-list.ytd-pax     = total-ytd-pax
            .
        
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

PROCEDURE cal-servat:  
DEFINE INPUT PARAMETER depart           AS INT.  
DEFINE INPUT PARAMETER h-artnr          AS INT.  
DEFINE INPUT PARAMETER service-code     AS INT.  
DEFINE INPUT PARAMETER mwst-code        AS INT.
DEFINE INPUT PARAMETER inpDate          AS DATE.
DEFINE OUTPUT PARAMETER serv-percent    AS DECIMAL INITIAL 0.  
DEFINE OUTPUT PARAMETER mwst-percent    AS DECIMAL INITIAL 0.  
DEFINE OUTPUT PARAMETER servat          AS DECIMAL INITIAL 0.  
 
DEFINE VARIABLE serv-htp    AS DECIMAL          NO-UNDO.  
DEFINE VARIABLE vat-htp     AS DECIMAL          NO-UNDO.  
DEFINE VARIABLE ct          AS CHAR             NO-UNDO.
DEFINE VARIABLE l-deci      AS INTEGER          NO-UNDO INIT 2.
  
DEF BUFFER hbuff FOR vhp.h-artikel.  
DEF BUFFER aBuff FOR vhp.artikel.  
  
    IF bill-date LT bill-date110 AND (service-code NE 0 OR mwst-code NE 0) THEN  
    DO:  
        FIND FIRST hbuff WHERE hbuff.artnr = h-artnr  
            AND hbuff.departement = depart NO-LOCK.  
        
        FIND FIRST abuff WHERE abuff.artnr = hbuff.artnrfront  
            AND abuff.departement = depart NO-LOCK.  
        
        FIND FIRST kontplan NO-LOCK WHERE kontplan.betriebsnr = depart   
            AND kontplan.kontignr = abuff.artnr AND kontplan.datum = inpDate  NO-ERROR.
        IF AVAILABLE kontplan THEN  
        DO:  
            ASSIGN  
                serv-htp = kontplan.anzkont / 10000  
                vat-htp  = kontplan.anzconf / 10000  
                .  
/*            
          IF service-taxable THEN  
          ASSIGN  
            serv-percent  = serv-htp  
            mwst-percent  = (1 + serv-htp) * vat-htp  
            servat = 1 + serv-percent + mwst-percent  
          .   
          ELSE  
*/            
        
            ASSIGN  
                serv-percent  = serv-htp  
                mwst-percent  = vat-htp              
                servat = 1 + serv-percent + mwst-percent          
                .               
            RETURN.  
        END.  
    END.  
    
    ASSIGN  
        serv-htp = 0  
        vat-htp  = 0  
        .  

    /*FD Dec 13, 2021*/
    IF servtax-use-foart THEN
    DO:
        FIND FIRST hbuff WHERE hbuff.artnr = h-artnr  
            AND hbuff.departement = depart NO-LOCK.
        FIND FIRST abuff WHERE abuff.artnr = hbuff.artnrfront  
            AND abuff.departement = depart NO-LOCK. 
        IF AVAILABLE abuff THEN 
        DO:
            service-code = abuff.service-code.
            mwst-code = abuff.mwst-code.
        END.  
    END.
    ELSE
    DO: 
        FIND FIRST hbuff WHERE hbuff.artnr = h-artnr  
            AND hbuff.departement = depart NO-LOCK.
        IF AVAILABLE hbuff THEN 
        DO:
            service-code = hbuff.service-code.
            mwst-code = hbuff.mwst-code.        
        END.    
    END.
    /*End FD*/

    IF service-code NE 0 THEN   
    DO:   
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = service-code NO-LOCK.   
        serv-htp = vhp.htparam.fdecimal / 100.   
    END.   
    IF mwst-code NE 0 THEN   
    DO:   
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = mwst-code NO-LOCK.   
        vat-htp = vhp.htparam.fdecimal / 100.  
    END.  
    
    IF service-taxable THEN  
    ASSIGN  
        serv-percent  = serv-htp  
        mwst-percent  = (1 + serv-htp) * vat-htp      
        servat = 1 + serv-percent + mwst-percent  
        .   
    ELSE    
    ASSIGN  
        serv-percent  = serv-htp  
        mwst-percent  = vat-htp  
        servat = 1 + serv-percent + mwst-percent  
        .      
    
    /*FDL Sept, 05 2024: Ticket 196BEE*/
    ASSIGN 
        ct     = REPLACE(STRING(mwst-percent), ".", ",")
        l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
        .
    IF l-deci LE 2 THEN mwst-percent = ROUND(mwst-percent, 2).
    ELSE IF l-deci EQ 3 THEN mwst-percent = ROUND(mwst-percent, 3).
    ELSE mwst-percent = ROUND(mwst-percent, 4).
    
    ASSIGN 
        ct     = REPLACE(STRING(servat), ".", ",")
        l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
        .
    IF l-deci LE 2 THEN servat = ROUND(servat, 2).
    ELSE IF l-deci EQ 3 THEN servat = ROUND(servat, 3).
    ELSE servat = ROUND(servat, 4).
    /*END*/
END PROCEDURE.  
