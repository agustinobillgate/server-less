DEF TEMP-TABLE output-list 
    FIELD h-recid               AS INTEGER INITIAL 0 
    FIELD STR                   AS CHAR
    FIELD gname                 AS CHAR FORMAT "x(32)" LABEL "Guest Name"
    FIELD fart-bez              AS CHAR FORMAT "x(32)" LABEL "F/O Artikel"  /*gerald B0AEC7 19/11/20*/
    FIELD total-trans           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "Total Bill Amount"
    FIELD total-afterdisc       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "Bill After Disc"
    FIELD total-afterdisc-extns AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "Bill Excl Service & Tax"
    FIELD member-code           AS CHAR FORMAT "x(15)" LABEL "Member Code"
    FIELD member-email          AS CHAR FORMAT "x(30)" LABEL "Member Email"
    FIELD department            AS CHAR FORMAT "x(20)" LABEL "Department" 
    FIELD art-amount            AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"  LABEL "Article Amount" 
    FIELD gastno                AS INT
    FIELD deptno                AS INT
    FIELD payment               AS CHAR FORMAT "x(25)" LABEL "Payment"
    FIELD datum                 AS CHAR
    FIELD tableno               AS CHAR
    FIELD bill-no               AS INT
    FIELD art-no                AS INT
    FIELD descr                 AS CHAR
    FIELD qty                   AS INT
    FIELD time-str              AS CHAR
    FIELD id-str                AS CHAR
    FIELD order-taker           AS CHAR
    FIELD room-no               AS CHAR
    . 

DEF INPUT PARAMETER od-taker    AS CHAR.
DEF INPUT PARAMETER from-art    AS INT.
DEF INPUT PARAMETER to-art      AS INT.
DEF INPUT PARAMETER from-dept   AS INT.
DEF INPUT PARAMETER to-dept     AS INT.
DEF INPUT PARAMETER from-date    AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER sorttype     AS INT.
DEF INPUT PARAMETER long-digit  AS LOGICAL.
DEF INPUT PARAMETER mc-sort         AS CHARACTER.         
DEF OUTPUT PARAMETER TABLE FOR output-list.

RUN journal-list.

DEF VAR billnumber      AS INT.
DEF VAR total-bill      AS DECIMAL.
DEF VAR total-amt       AS DECIMAL.
DEF VAR total-billextns AS DECIMAL.
DEF VAR total-qty       AS DECIMAL.
DEF VAR dept-str        AS CHAR.

DEF VAR grandtotal-bill            AS DECIMAL.
DEF VAR grandtotal-afterdisc       AS DECIMAL.
DEF VAR grandtotal-amt             AS DECIMAL.
DEF VAR grandtotal-afterdisc-extns AS DECIMAL.
DEF VAR gtotal-bill                AS DECIMAL.
DEF VAR gtotal-afterdisc           AS DECIMAL.
DEF VAR gtotal-amt                 AS DECIMAL.
DEF VAR gtotal-afterdisc-extns     AS DECIMAL.
DEF VAR total-amtincltns           AS DECIMAL.    

FOR EACH output-list:
    output-list.datum       = SUBSTRING(output-list.STR,1,8).           
    output-list.tableno     = SUBSTRING(output-list.STR,9,6).           
    output-list.bill-no     = INTEGER(SUBSTRING(output-list.STR,15,9)). 
    output-list.art-no      = INTEGER(SUBSTRING(output-list.STR,24,5)). 
    output-list.descr       = SUBSTRING(output-list.STR,29, 28).        
    output-list.qty         = INTEGER(SUBSTRING(output-list.STR,77,5)). 
    output-list.time-str    = SUBSTRING(output-list.STR,99, 8).         
    output-list.id-str      = SUBSTRING(output-list.STR,107, 3).        
    output-list.order-taker = SUBSTRING(output-list.STR,110, 8).        
    output-list.room-no     = SUBSTRING(output-list.STR,119, 8).        

    dept-str = SUBSTRING(output-list.STR,57, 20).
    IF SUBSTRING(output-list.STR,57, 20) MATCHES "*T O T A L*" THEN 
    DO:
        ASSIGN
        output-list.department            = "T O T A L"
        output-list.total-trans           = grandtotal-bill            
        output-list.total-afterdisc       = grandtotal-afterdisc       
        output-list.total-afterdisc-extns = grandtotal-afterdisc-extns              
        output-list.art-amount            = grandtotal-amt.  
                                                        
        gtotal-bill            = gtotal-bill            + grandtotal-bill.           
        gtotal-afterdisc       = gtotal-afterdisc       + grandtotal-afterdisc.      
        gtotal-amt             = gtotal-amt             + grandtotal-amt.
        gtotal-afterdisc-extns = gtotal-afterdisc-extns + grandtotal-afterdisc-extns.       

        grandtotal-bill            = 0.
        grandtotal-afterdisc       = 0.
        grandtotal-afterdisc-extns = 0.
        grandtotal-amt             = 0.
    END.
    ELSE IF SUBSTRING(output-list.STR,57, 20) MATCHES "*TOTAL*" THEN
    DO:
        ASSIGN
        output-list.department            = "GRAND T O T A L"
        output-list.total-trans           = gtotal-bill            
        output-list.total-afterdisc       = gtotal-afterdisc       
        output-list.total-afterdisc-extns = gtotal-afterdisc-extns              
        output-list.art-amount            = gtotal-amt.  

        gtotal-bill            = 0. 
        gtotal-afterdisc       = 0. 
        gtotal-amt             = 0. 
        gtotal-afterdisc-extns = 0. 
    END.
    ELSE
    DO:
        output-list.department = SUBSTRING(output-list.STR,57, 20). 
        output-list.art-amount = DEC(SUBSTRING(output-list.STR,82,17)).

        billnumber      = INTEGER(SUBSTRING(output-list.STR,15,9)).
        /*total-amt  = DEC(SUBSTRING(output-list.STR,82,17)).*/
        total-bill      = 0.
        total-billextns = 0.
        total-qty       = 0.
        total-amt       = 0.
        total-amtincltns = 0.
    
        FOR EACH h-bill-line WHERE h-bill-line.departemen EQ output-list.deptno
            AND h-bill-line.rechnr EQ billnumber 
            AND h-bill-line.artnr NE 8911 NO-LOCK:
            FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr 
                AND h-artikel.departemen EQ h-bill-line.departemen
                AND h-artikel.artart NE 2
                AND h-artikel.artart NE 7 
                AND h-artikel.artart NE 6 
                AND h-artikel.artart NE 11 
                AND h-artikel.artart NE 12 NO-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN 
            DO:
                total-bill      = total-bill + h-bill-line.betrag.
                total-billextns = total-billextns + (h-bill-line.epreis * h-bill-line.anzahl).  
                /*total-qty       = total-qty + h-bill-line.anzahl.*/
            END.
        END.
        FOR EACH h-bill-line WHERE h-bill-line.departemen EQ output-list.deptno
            AND h-bill-line.rechnr EQ billnumber 
            AND h-bill-line.artnr GE 8911 
            AND h-bill-line.artnr LE 8912 
            AND h-bill-line.epreis LT 0 NO-LOCK:
            total-amt = total-amt + h-bill-line.epreis.
            total-amtincltns = total-amtincltns + h-bill-line.betrag.
        END.
        FOR EACH h-bill-line WHERE h-bill-line.departemen EQ output-list.deptno
            AND h-bill-line.rechnr EQ billnumber NO-LOCK:
            IF h-bill-line.artnr EQ 0 THEN output-list.payment = h-bill-line.bezeich.
            ELSE
            DO:
                FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr 
                    AND h-artikel.departemen EQ h-bill-line.departemen
                    AND h-artikel.artart NE 0 NO-LOCK NO-ERROR.
                IF AVAILABLE h-artikel AND h-bill-line.betrag LT 0 THEN 
                DO:
                    output-list.payment = STRING(h-artikel.artnr) + "-" + h-artikel.bezeich.
                END.
            END.
        END.
        output-list.total-trans           = total-bill.
        output-list.total-afterdisc       = total-bill + total-amtincltns.
        output-list.total-afterdisc-extns = total-billextns + total-amt.

        /*output-list.total-afterdisc-extns = total-billextns /* * total-qty*/ .*/

        IF dept-str NE SUBSTRING(output-list.STR,57, 20) THEN
        DO: 
            dept-str = SUBSTRING(output-list.STR,57, 20).
            grandtotal-bill            = 0.
            grandtotal-afterdisc       = 0.
            grandtotal-afterdisc-extns = 0.
            grandtotal-amt             = 0.

        END.
        ELSE
        DO:
            grandtotal-bill            = grandtotal-bill            + output-list.total-trans.             
            grandtotal-afterdisc       = grandtotal-afterdisc       + output-list.total-afterdisc.       
            grandtotal-afterdisc-extns = grandtotal-afterdisc-extns + output-list.total-afterdisc-extns. 
            grandtotal-amt             = grandtotal-amt             + output-list.art-amount.                                   
        END.

    END.
    IF output-list.gastno NE 0 THEN
    DO:
        FIND FIRST guest WHERE guest.gastnr EQ output-list.gastno NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN output-list.member-email = guest.email-adr.
        FIND FIRST mc-guest WHERE mc-guest.gastnr EQ output-list.gastno NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN output-list.member-code = mc-guest.cardnum.
    END.

END.


DEF VAR guestno AS INT.

FIND FIRST output-list NO-LOCK NO-ERROR.
DO WHILE AVAILABLE output-list:
    

    FIND NEXT output-list NO-LOCK NO-ERROR.
END.

PROCEDURE journal-list: 
    DEFINE VARIABLE last-dept   AS INTEGER INITIAL -1. 
    DEFINE VARIABLE qty         AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE takerNum    AS INTEGER INITIAL 0.
    
    DEFINE VARIABLE sub-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    
    DEFINE VARIABLE curr-date   AS DATE. 
    DEFINE VARIABLE it-exist    AS LOGICAL. 
    DEFINE VARIABLE do-it       AS LOGICAL.
      
    DEFINE VARIABLE curr-guest  AS CHAR INITIAL "" NO-UNDO.
    DEFINE VARIABLE curr-gastnr AS INT  INITIAL 0 NO-UNDO.
    DEFINE VARIABLE curr-room   AS CHAR INITIAL "" NO-UNDO. /*DO 231219*/
    DEFINE VARIABLE membercode  AS CHAR INITIAL "" NO-UNDO.
    DEFINE VARIABLE guest-mail  AS CHAR INITIAL "" NO-UNDO. 

    DEFINE VARIABLE tot-qty     AS INTEGER.
    DEFINE VARIABLE order-taker AS CHARACTER NO-UNDO. /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */

    DEFINE VARIABLE dept AS INT.
    
    FOR EACH output-list: 
        DELETE output-list. 
    END. 
 
    IF od-taker NE "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 10 AND queasy.char2 = od-taker NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN takerNum = queasy.number1.
    END.
 
    /*gerald B0AEC7 19/11/20*/
    IF mc-sort = 'sart' THEN
    DO:
        last-dept = - 1. 
        FOR EACH h-artikel WHERE h-artikel.artnr GE from-art 
            AND h-artikel.artnr LE to-art 
            AND h-artikel.departement GE from-dept 
            AND h-artikel.departement LE to-dept NO-LOCK, 
            FIRST hoteldpt WHERE hoteldpt.num = h-artikel.departement NO-LOCK
            BY artikel.bezeich BY h-artikel.departement BY h-artikel.artnr: 
            last-dept   = h-artikel.departement. 
            sub-tot     = 0. 
            it-exist    = NO. 
            qty         = 0. 

            IF h-artikel.artart LE 1 THEN dept = h-artikel.departement.
            ELSE dept = 0.

            DO curr-date = from-date TO to-date: 
                IF sorttype = 0 THEN
                DO:
                    FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
                        AND h-journal.departement = h-artikel.departement 
                        AND h-journal.bill-datum = curr-date AND h-journal.artnr GT 0
                        AND h-journal.anzahl NE 0 NO-LOCK: 
                        
                        RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                        
                        curr-guest = "".
                        curr-room  = "".
                        membercode = "".
                        guest-mail = "".
                        curr-gastnr = 0.
                        FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr
                        AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        DO:
                            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                            DO:
                                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr 
                                    AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE res-line THEN
                                    ASSIGN
                                    curr-guest = res-line.NAME
                                    curr-room  = res-line.zinr.
                                    curr-gastnr = res-line.gastnrmember.
                            END.
                            ELSE IF h-bill.resnr GT 0 THEN
                            DO:
                                FIND FIRST guest WHERE h-bill.resnr = guest.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest THEN 
                                DO: 
                                    curr-guest  = guest.NAME + "," + guest.vorname1.
                                    curr-gastnr = guest.gastnr.
                                    
                                END.
                            END.
                            ELSE IF h-bill.resnr = 0 THEN DO: /*ITA 081216*/
                                curr-guest = h-bill.bilname.
                            END.
                        END.
                        
                        IF takerNum = 0 THEN do-it = YES.
                        ELSE
                        DO:
                            do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                        END.
                        
                        IF do-it THEN
                        DO:
                            it-exist = YES. 
                            CREATE output-list. 
                            ASSIGN
                              output-list.gname   = curr-guest
                              output-list.h-recid = RECID(h-journal)
                              output-list.gastno  = curr-gastnr
                              output-list.deptno  = h-artikel.departement
                            . 

                            /*gerald B0AEC7 19/11/20*/
                            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                                AND artikel.departement = dept NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                output-list.fart-bez = artikel.bezeich.

                            IF NOT long-digit THEN STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)") /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            ELSE STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room                                      
                                    .
                            qty = qty + h-journal.anzahl. 
                            sub-tot = sub-tot + h-journal.betrag. 
                            tot = tot + h-journal.betrag. 
                        END.
                    END.
                END.
                ELSE IF sorttype = 1 THEN
                DO:
                    FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
                        AND h-journal.departement = h-artikel.departement 
                        AND h-journal.bill-datum = curr-date NO-LOCK: 
                        RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                        
                        curr-guest = "".
                        curr-room  = "".
                        curr-gastnr = 0.
                        FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        DO:
                            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                            DO:
                                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE res-line THEN
                                    ASSIGN
                                    curr-guest = res-line.NAME
                                    curr-room  = res-line.zinr.
                                    curr-gastnr = res-line.gastnrmember.
                            END.
                            ELSE IF h-bill.resnr GT 0 THEN
                            DO:
                                FIND FIRST guest WHERE h-bill.resnr = guest.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest THEN 
                                DO: 
                                    curr-guest = guest.NAME + "," + guest.vorname1.
                                    curr-gastnr = guest.gastnr.
                                END.
                            END.
                            ELSE IF h-bill.resnr = 0 THEN DO: /*ITA 081216*/
                                curr-guest = h-bill.bilname.
                            END.
                        END.
                        
                        IF takerNum = 0 THEN do-it = YES.
                        ELSE
                        DO:
                            do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                        END.
                        
                        IF do-it THEN
                        DO:
                            it-exist = YES. 
                            CREATE output-list.
                            ASSIGN
                              output-list.gname = curr-guest
                              output-list.h-recid = RECID(h-journal)
                              output-list.gastno  = curr-gastnr 
                              output-list.deptno  = h-artikel.departement
                              /*output-list.fart-bez = artikel.bezeich /*gerald B0AEC7 19/11/20*/*/
                            . 

                            /*gerald B0AEC7 19/11/20*/
                            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                                AND artikel.departement = dept NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                output-list.fart-bez = artikel.bezeich.

                            IF NOT long-digit THEN STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            ELSE STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            qty = qty + h-journal.anzahl. 
                            sub-tot = sub-tot + h-journal.betrag. 
                            tot = tot + h-journal.betrag. 
                        END.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
                        AND h-journal.departement = h-artikel.departement 
                        AND h-journal.bill-datum = curr-date AND h-journal.anzahl = 0
                        AND h-journal.artnr = 0 NO-LOCK: 
                        RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
            
                        curr-guest = "".
                        curr-room = "".
                        curr-gastnr = 0.
                        FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        DO:
                            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                            DO:
                                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE res-line THEN
                                    ASSIGN
                                    curr-guest = res-line.NAME
                                    curr-room  = res-line.zinr.
                                    curr-gastnr = res-line.gastnrmember.
                           
                            END.
                            ELSE IF h-bill.resnr GT 0 THEN
                            DO:
                                FIND FIRST guest WHERE h-bill.resnr = guest.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest THEN 
                                DO: 
                                    curr-guest = guest.NAME + "," + guest.vorname1.
                                    curr-gastnr = guest.gastnr.
                                END.
                            END.
                            ELSE IF h-bill.resnr = 0 THEN DO: /*ITA 081216*/
                                curr-guest = h-bill.bilname.
                            END.
                        END.
                        
                        IF takerNum = 0 THEN do-it = YES.
                        ELSE
                        DO:
                            do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                        END.
                        
                        IF do-it THEN
                        DO:
                            it-exist = YES. 
                            CREATE output-list.
                            ASSIGN
                            output-list.gname   = curr-guest
                            output-list.h-recid = RECID(h-journal)
                            output-list.gastno = curr-gastnr
                            output-list.deptno  = h-artikel.departement

                            /*output-list.fart-bez = artikel.bezeich gerald B0AEC7 19/11/20*/
                            .  

                            /*gerald B0AEC7 19/11/20*/
                            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                                AND artikel.departement = dept NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                output-list.fart-bez = artikel.bezeich.

                            IF NOT long-digit THEN STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)")    
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            ELSE STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)") /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            qty = qty + h-journal.anzahl. 
                            sub-tot = sub-tot + h-journal.betrag. 
                            tot = tot + h-journal.betrag.
                        END.
                    END.
                END.
            END. 
            IF it-exist THEN 
            DO: 
                tot-qty = qty + tot-qty.
                create output-list. 
                IF NOT long-digit THEN STR = STRING("", "x(56)") 
                  + STRING("T O T A L   ", "x(20)") 
                  + STRING(qty, "->>>9") 
                  + STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                ELSE STR = STRING("", "x(56)") 
                  + STRING("T O T A L   ", "x(20)") 
                  + STRING(qty, "->>>9") 
                  + STRING(sub-tot, " ->>>,>>>,>>>,>>9") . 
            END.  
        END. 
    END.
    ELSE IF mc-sort = 'sdept' THEN     /*gerald B0AEC7 19/11/20*/
    DO:
        last-dept = - 1. 
        FOR EACH h-artikel WHERE h-artikel.artnr GE from-art 
            AND h-artikel.artnr LE to-art 
            AND h-artikel.departement GE from-dept 
            AND h-artikel.departement LE to-dept NO-LOCK, 
            FIRST hoteldpt WHERE hoteldpt.num = h-artikel.departement NO-LOCK
            /*,FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront AND artikel.departement = h-artikel.departement
            NO-LOCK*/ BY h-artikel.departement BY h-artikel.artnr: 
            last-dept   = h-artikel.departement. 
            sub-tot     = 0. 
            it-exist    = NO. 
            qty         = 0. 

            IF h-artikel.artart LE 1 THEN dept = h-artikel.departement.
            ELSE dept = 0.

            DO curr-date = from-date TO to-date: 
                IF sorttype = 0 THEN
                DO:
                    FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
                        AND h-journal.departement = h-artikel.departement 
                        AND h-journal.bill-datum = curr-date AND h-journal.artnr GT 0
                        AND h-journal.anzahl NE 0 NO-LOCK: 
                        
                        RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                        
                        curr-guest = "".
                        curr-room  = "".
                        curr-gastnr = 0.
                        FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr
                        AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        DO:
                            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                            DO:
                                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE res-line THEN
                                    ASSIGN
                                    curr-guest = res-line.NAME
                                    curr-room  = res-line.zinr.
                                    curr-gastnr = res-line.gastnrmember.
                           
                            END.
                            ELSE IF h-bill.resnr GT 0 THEN
                            DO:
                                FIND FIRST guest WHERE h-bill.resnr = guest.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest THEN 
                                DO: 
                                    curr-guest = guest.NAME + "," + guest.vorname1.
                                    curr-gastnr = guest.gastnr.
                                END.
                            END.
                            ELSE IF h-bill.resnr = 0 THEN DO: /*ITA 081216*/
                                curr-guest = h-bill.bilname.
                            END.
                        END.
                        
                        IF takerNum = 0 THEN do-it = YES.
                        ELSE
                        DO:
                            do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                        END.
                        
                        IF do-it THEN
                        DO:
                            it-exist = YES. 
                            CREATE output-list. 
                            ASSIGN
                              output-list.gname   = curr-guest
                              output-list.h-recid = RECID(h-journal)
                              output-list.gastno = curr-gastnr
                              output-list.deptno  = h-artikel.departement
                              /*output-list.fart-bez = artikel.bezeich /*gerald B0AEC7 19/11/20*/ */
                            .                                     

                            /*gerald B0AEC7 19/11/20*/
                            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                                AND artikel.departement = dept NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                output-list.fart-bez = artikel.bezeich.

                            IF NOT long-digit THEN STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)") /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            ELSE STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room                                      
                                    .
                            qty = qty + h-journal.anzahl. 
                            sub-tot = sub-tot + h-journal.betrag. 
                            tot = tot + h-journal.betrag. 
                        END.
                    END.
                END.
                ELSE IF sorttype = 1 THEN
                DO:
                    FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
                        AND h-journal.departement = h-artikel.departement 
                        AND h-journal.bill-datum = curr-date NO-LOCK: 
                        RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                        
                        curr-guest = "".
                        curr-room  = "".
                        curr-gastnr = 0.
                        FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        DO:
                            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                            DO:
                                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE res-line THEN
                                    ASSIGN
                                    curr-guest = res-line.NAME
                                    curr-room  = res-line.zinr.
                                    curr-gastnr = res-line.gastnrmember.
                            END.
                            ELSE IF h-bill.resnr GT 0 THEN
                            DO:
                                FIND FIRST guest WHERE h-bill.resnr = guest.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest THEN 
                                DO: 
                                    curr-guest = guest.NAME + "," + guest.vorname1.
                                    curr-gastnr = guest.gastnr.
                                END.
                            END.
                            ELSE IF h-bill.resnr = 0 THEN DO: /*ITA 081216*/
                                curr-guest = h-bill.bilname.
                            END.
                        END.
                        
                        IF takerNum = 0 THEN do-it = YES.
                        ELSE
                        DO:
                            do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                        END.
                        
                        IF do-it THEN
                        DO:
                            it-exist = YES. 
                            CREATE output-list.
                            ASSIGN
                              output-list.gname = curr-guest
                              output-list.h-recid = RECID(h-journal)
                              output-list.gastno = curr-gastnr 
                              output-list.deptno  = h-artikel.departement

                              /*output-list.fart-bez = artikel.bezeich /*gerald B0AEC7 19/11/20*/*/
                            . 

                            /*gerald B0AEC7 19/11/20*/
                            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                                AND artikel.departement = dept NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                output-list.fart-bez = artikel.bezeich.

                            IF NOT long-digit THEN STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            ELSE STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            qty = qty + h-journal.anzahl. 
                            sub-tot = sub-tot + h-journal.betrag. 
                            tot = tot + h-journal.betrag. 
                        END.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
                        AND h-journal.departement = h-artikel.departement 
                        AND h-journal.bill-datum = curr-date AND h-journal.anzahl = 0
                        AND h-journal.artnr = 0 NO-LOCK: 
                        RUN search-ot(h-journal.rechnr, h-journal.tischnr, OUTPUT order-taker). /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
            
                        curr-guest = "".
                        curr-room = "".
                        curr-gastnr = 0.
                        
                        FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        DO:
                            IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                            DO:
                                FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                IF AVAILABLE res-line THEN
                                    ASSIGN
                                    curr-guest = res-line.NAME
                                    curr-room  = res-line.zinr.
                                    curr-gastnr = res-line.gastnrmember.
                            
                                
                            END.
                            ELSE IF h-bill.resnr GT 0 THEN
                            DO:
                                FIND FIRST guest WHERE h-bill.resnr = guest.gastnr NO-LOCK NO-ERROR.
                                IF AVAILABLE guest THEN 
                                DO: 
                                    curr-guest = guest.NAME + "," + guest.vorname1.
                                    curr-gastnr = guest.gastnr.
                                END.
                            END.
                            ELSE IF h-bill.resnr = 0 THEN DO: /*ITA 081216*/
                                curr-guest = h-bill.bilname.
                            END.
                        END.
                        
                        IF takerNum = 0 THEN do-it = YES.
                        ELSE
                        DO:
                            do-it = AVAILABLE h-bill AND (h-bill.betriebsnr = takerNum).
                        END.
                        
                        IF do-it THEN
                        DO:
                            it-exist = YES. 
                            CREATE output-list.
                            ASSIGN
                            output-list.gname   = curr-guest
                            output-list.h-recid = RECID(h-journal)
                            output-list.gastno = curr-gastnr
                            output-list.deptno  = h-artikel.departement
                            /*output-list.fart-bez = artikel.bezeich /*gerald B0AEC7 19/11/20*/*/
                            .   

                            /*gerald B0AEC7 19/11/20*/
                            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
                                AND artikel.departement = dept NO-LOCK NO-ERROR.
                            IF AVAILABLE artikel THEN
                                output-list.fart-bez = artikel.bezeich.

                            IF NOT long-digit THEN STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)")    
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)")  /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            ELSE STR = STRING(h-journal.bill-datum) 
                                    + STRING(h-journal.tischnr, ">>>>>9") 
                                    + STRING(h-journal.rechnr, ">,>>>,>>9") 
                                    + STRING(h-journal.artnr, ">>>>>") 
                                    + STRING(h-journal.bezeich, "x(28)") 
                                    + STRING(hoteldpt.depart, "x(20)") 
                                    + STRING(h-journal.anzahl, "->>>9") 
                                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                                    + STRING(h-journal.zeit, "HH:MM:SS") 
                                    + STRING(h-journal.kellner-nr, "999") 
                                    + STRING(order-taker, "x(8)") /* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
                                    + "|" + curr-room
                                    .
                            qty = qty + h-journal.anzahl. 
                            sub-tot = sub-tot + h-journal.betrag. 
                            tot = tot + h-journal.betrag.
                        END.
                    END.
                END.
            END. 
            IF it-exist THEN 
            DO: 
                tot-qty = qty + tot-qty.
                create output-list. 
                IF NOT long-digit THEN STR = STRING("", "x(56)") 
                  + STRING("T O T A L   ", "x(20)") 
                  + STRING(qty, "->>>9") 
                  + STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
                ELSE STR = STRING("", "x(56)") 
                  + STRING("T O T A L   ", "x(20)") 
                  + STRING(qty, "->>>9") 
                  + STRING(sub-tot, " ->>>,>>>,>>>,>>9") . 
            END.  
        END. 
    END.
    CREATE output-list. 
    IF NOT long-digit THEN STR = STRING("", "x(56)") 
    + STRING("Grand TOTAL ", "x(20)") 
    + STRING(tot-qty, "->>>9") 
    + STRING(tot, "->,>>>,>>>,>>9.99"). 
    ELSE STR = STRING("", "x(56)") 
    + STRING("Grand TOTAL ", "x(20)") 
    + STRING(tot-qty, "->>>9") 
    + STRING(tot, " ->>>,>>>,>>>,>>9"). 
END.

/* Add by Michael @ 11/12/2018 for Harris Tebet request - ticket no 4709D0 */
PROCEDURE search-ot:
    DEFINE INPUT PARAMETER r-nr AS INTEGER NO-UNDO.
    DEFINE INPUT PARAMETER t-nr AS INTEGER NO-UNDO.
    DEFINE OUTPUT PARAMETER order-taker AS CHARACTER NO-UNDO.

    FIND FIRST h-bill WHERE h-bill.rechnr EQ r-nr AND h-bill.tischnr EQ t-nr NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN FIND FIRST queasy WHERE queasy.KEY EQ 10 AND queasy.number1 EQ h-bill.betriebsnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN ASSIGN order-taker = queasy.char2.
END.
/* End of add */
