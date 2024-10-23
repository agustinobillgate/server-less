DEFINE TEMP-TABLE s-list
    FIELD invstr    AS CHAR    FORMAT "x(7)"                  LABEL "Invoice"
    FIELD deptstr   AS CHAR    FORMAT "x(24)"                 LABEL "Department"
    FIELD deptnr    AS INTEGER FORMAT ">9"                    LABEL "Dept"
    FIELD Gname     AS CHAR    FORMAT "x(30)"                 LABEL "GuestName"
    FIELD receiver  AS CHAR    FORMAT "x(30)"                 LABEL "Receiver"
    FIELD ggastnr   AS INTEGER
    FIELD rgastnr   AS INTEGER
    FIELD rechnr    AS INTEGER FORMAT ">>>>>>>>9"             LABEL "BillNo"
    FIELD refnr     AS INTEGER FORMAT "9999999"               LABEL "InvoiceNo"
    FIELD prdate    AS DATE    FORMAT "99/99/99"              LABEL "Printed Date"
    FIELD saldo     AS DECIMAL FORMAT ">,>>>,>>>,>>>,>>9.99"  LABEL "Balance"
    FIELD bill-date AS DATE.                       /*wenni 15/07/16*/
    /* FIELD saldo     AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Balance". */

DEF INPUT PARAMETER invno     AS INT.
DEF INPUT PARAMETER from-name AS CHAR.
DEF INPUT PARAMETER to-name   AS CHAR.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR s-list.

RUN create-data.

PROCEDURE create-data:
    DEFINE VARIABLE curr-ref AS INTEGER INITIAL 0.
    DEFINE VARIABLE do-it    AS LOGICAL INITIAL NO.
    DEFINE VARIABLE prdate   AS DATE NO-UNDO.
    DEFINE BUFFER sbuff FOR s-list.
    FOR EACH sbuff:
        DELETE sbuff.
    END.
    IF invno NE 0 THEN
    DO:
        FOR EACH debitor WHERE debitor.debref GT 0 AND debitor.debref = invno AND
            debitor.betriebsnr = 0 AND debitor.name GE from-name 
            AND debitor.name LE to-name NO-LOCK,
            FIRST bill WHERE bill.rechnr = debitor.rechnr AND
            bill.logidat GE from-date AND bill.logidat LE to-date NO-LOCK
            BY debref:
            IF debitor.name GE from-name AND debitor.name LE to-name THEN 

            FIND FIRST s-list WHERE s-list.deptnr = 0 AND s-list.rgastnr = debitor.gastnr
                AND s-list.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN 
                    s-list.deptnr   = 0
                    s-list.rechnr   = debitor.rechnr
                    s-list.rgastnr  = debitor.gastnr
                    s-list.refnr    = debitor.debref
                    s-list.prdate   = bill.logidat
                    s-list.bill-date = debitor.rgdatum.
                /*IF curr-ref NE debitor.debref THEN
                    s-list.invstr   = STRING(debitor.debref, "9999999").*/
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                    s-list.receiver = guest.NAME + " " + guest.vorname1 + 
                        guest.anredefirma + " " + guest.anrede1.
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                    s-list.gname = guest.NAME + " " + guest.vorname1 + 
                        guest.anredefirma + " " + guest.anrede1.
    
                FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN
                    s-list.deptstr = hoteldpt.depart.
            END.
            s-list.saldo = s-list.saldo + debitor.saldo.
            curr-ref = debitor.debref.
        END.

         curr-ref = 0.

        FOR EACH debitor WHERE debitor.debref GT 0 AND debitor.debref = invno
            AND debitor.betriebsnr GT 0 AND debitor.name GE from-name 
            AND debitor.name LE to-name NO-LOCK,
            FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr AND h-bill.departement = 
            debitor.betriebsnr NO-LOCK BY debitor.debref:
            do-it = NO.
            IF LENGTH(STRING(h-bill.service[7])) = 8 THEN
                prdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,2)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 3,2)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 5,4))).
            ELSE IF LENGTH(STRING(h-bill.service[7])) = 7 THEN
                prdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,1)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 2,2)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 4,4))).
            
            IF prdate GE from-date AND prdate LE to-date THEN
                do-it = YES.
            ELSE do-it = NO.
            IF do-it THEN
            DO:
                 FIND FIRST s-list WHERE s-list.deptnr = debitor.betriebsnr AND
                    s-list.rgastnr = debitor.gastnr AND s-list.rechnr = debitor.rechnr 
                     NO-LOCK NO-ERROR.
                IF NOT AVAILABLE s-list THEN
                DO:
                    CREATE s-list.
                    ASSIGN 
                        s-list.deptnr   = debitor.betriebsnr
                        s-list.rechnr   = debitor.rechnr
                        s-list.rgastnr  = debitor.gastnr
                        s-list.refnr    = debitor.debref
                        s-list.prdate   =  prdate
                        s-list.bill-date = debitor.rgdatum.
                    /*IF curr-ref NE debitor.debref THEN
                        s-list.invstr   = STRING(debitor.debref, "9999999").*/
                    
                    FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN
                        s-list.receiver = guest.NAME + " " + guest.vorname1 + 
                            guest.anredefirma + " " + guest.anrede1.
                    FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN
                        s-list.gname = guest.NAME + " " + guest.vorname1 + 
                            guest.anredefirma + " " + guest.anrede1.
        
                    FIND FIRST hoteldpt WHERE hoteldpt.num = debitor.betriebsnr NO-LOCK NO-ERROR.
                    IF AVAILABLE hoteldpt THEN
                        s-list.deptstr = hoteldpt.depart.
                END.
                s-list.saldo = s-list.saldo + debitor.saldo.
                
                curr-ref = debitor.debref.
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH debitor WHERE debitor.debref GT 0 AND
            debitor.betriebsnr = 0 AND debitor.name GE from-name 
            AND debitor.name LE to-name NO-LOCK,
            FIRST bill WHERE bill.rechnr = debitor.rechnr AND
            bill.logidat GE from-date AND bill.logidat LE to-date NO-LOCK
            BY debref:
            FIND FIRST s-list WHERE s-list.deptnr = 0 AND s-list.rgastnr = debitor.gastnr
                AND s-list.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE s-list THEN
            DO:
                CREATE s-list.
                ASSIGN 
                    s-list.deptnr   = 0
                    s-list.rechnr   = debitor.rechnr
                    s-list.rgastnr  = debitor.gastnr
                    s-list.refnr    = debitor.debref
                    s-list.prdate   = bill.logidat
                    s-list.bill-date = debitor.rgdatum.
                /*IF curr-ref NE debitor.debref THEN
                    s-list.invstr   = STRING(debitor.debref, "9999999").*/
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                    s-list.receiver = guest.NAME + " " + guest.vorname1 + 
                        guest.anredefirma + " " + guest.anrede1.
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                    s-list.gname = guest.NAME + " " + guest.vorname1 + 
                        guest.anredefirma + " " + guest.anrede1.
    
                FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN
                    s-list.deptstr = hoteldpt.depart.
            END.
            s-list.saldo = s-list.saldo + debitor.saldo.
            curr-ref = debitor.debref.
        END.

         curr-ref = 0.

        FOR EACH debitor WHERE debitor.debref GT 0 AND debitor.betriebsnr GT 0
            AND debitor.name GE from-name 
            AND debitor.name LE to-name NO-LOCK,
            FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr AND h-bill.departement = 
            debitor.betriebsnr NO-LOCK BY debitor.debref:
            do-it = NO.
            IF LENGTH(STRING(h-bill.service[7])) = 8 THEN
                prdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,2)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 3,2)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 5,4))).
            ELSE IF LENGTH(STRING(h-bill.service[7])) = 7 THEN
                prdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,1)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 2,2)),
                      INTEGER(SUBSTR(STRING(h-bill.service[7]), 4,4))).
            
            IF prdate GE from-date AND prdate LE to-date THEN
                do-it = YES.
            ELSE do-it = NO.
            IF do-it THEN
            DO:
                 FIND FIRST s-list WHERE s-list.deptnr = debitor.betriebsnr AND
                    s-list.rgastnr = debitor.gastnr AND s-list.rechnr = debitor.rechnr 
                     NO-LOCK NO-ERROR.
                IF NOT AVAILABLE s-list THEN
                DO:
                    CREATE s-list.
                    ASSIGN 
                        s-list.deptnr   = debitor.betriebsnr
                        s-list.rechnr   = debitor.rechnr
                        s-list.rgastnr  = debitor.gastnr
                        s-list.refnr    = debitor.debref
                        s-list.prdate   =  prdate
                        s-list.bill-date = debitor.rgdatum.
                    /*IF curr-ref NE debitor.debref THEN
                        s-list.invstr   = STRING(debitor.debref, "9999999").*/
                    
                    FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN
                        s-list.receiver = guest.NAME + " " + guest.vorname1 + 
                            guest.anredefirma + " " + guest.anrede1.
                    FIND FIRST guest WHERE guest.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN
                        s-list.gname = guest.NAME + " " + guest.vorname1 + 
                            guest.anredefirma + " " + guest.anrede1.
        
                    FIND FIRST hoteldpt WHERE hoteldpt.num = debitor.betriebsnr NO-LOCK NO-ERROR.
                    IF AVAILABLE hoteldpt THEN
                        s-list.deptstr = hoteldpt.depart.
                END.
                s-list.saldo = s-list.saldo + debitor.saldo.
                curr-ref     = debitor.debref.
            END.
        END.
    END.


    curr-ref = 0.
    FOR EACH sbuff BY sbuff.refnr:
        IF curr-ref = 0 OR curr-ref NE sbuff.refnr THEN
             ASSIGN sbuff.invstr   = STRING(sbuff.refnr, "9999999").
        
        curr-ref = sbuff.refnr.
    END.
END.
