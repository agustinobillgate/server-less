DEFINE TEMP-TABLE tlist
    FIELD invno     AS CHAR
    FIELD datum-trx AS CHAR
    FIELD subtotal  AS DECIMAL
    FIELD diskon    AS DECIMAL
    FIELD service   AS DECIMAL
    FIELD other     AS DECIMAL
    FIELD pajak     AS DECIMAL
    FIELD amount    AS DECIMAL
    FIELD depart    AS INTEGER
.

DEFINE INPUT PARAMETER fdate AS DATE NO-UNDO.
DEFINE INPUT PARAMETER tdate AS DATE NO-UNDO.

DEFINE OUTPUT PARAMETER hotel-name AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER hotel-id   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tlist.

DEFINE VARIABLE bill-date               AS DATE       NO-UNDO.
DEFINE VARIABLE do-it                   AS LOGICAL    NO-UNDO.
DEFINE VARIABLE serv                    AS DECIMAL    NO-UNDO.
DEFINE VARIABLE vat                     AS DECIMAL    NO-UNDO.
DEFINE VARIABLE netto                   AS DECIMAL    NO-UNDO.
DEFINE VARIABLE serv-betrag             AS DECIMAL    NO-UNDO.
DEFINE VARIABLE vat-betrag              AS DECIMAL    NO-UNDO.
DEFINE VARIABLE serv-taxable            AS LOGICAL    NO-UNDO.
DEFINE VARIABLE service-code            AS INTEGER    NO-UNDO.
DEFINE VARIABLE vat-proz                AS DECIMAL    NO-UNDO INIT 10.
DEFINE VARIABLE service-proz            AS DECIMAL    NO-UNDO INIT 10.
DEFINE VARIABLE count-int               AS INTEGER    NO-UNDO.
DEFINE VARIABLE datum                   AS DATE       NO-UNDO.
DEFINE VARIABLE disc-art1               AS INTEGER    NO-UNDO.
DEFINE VARIABLE disc-art2               AS INTEGER    NO-UNDO.
DEFINE VARIABLE disc-art3               AS INTEGER    NO-UNDO.

DEF TEMP-TABLE hbill-list
    FIELD dept      AS INTEGER
    FIELD rechnr    AS INTEGER
    FIELD i-fact    AS INTEGER INIT 0
    FIELD do-it     AS LOGICAL INIT YES
    FIELD tot-sales AS DECIMAL INIT 0
.


DEFINE BUFFER hbill-buff FOR h-bill-line.
DEFINE BUFFER bline FOR h-bill-line.
DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.


FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK.
serv-taxable = htparam.flogical.

/* VAT code */
FIND FIRST htparam WHERE htparam.paramnr = 1 NO-LOCK.
IF htparam.fdecimal NE 0 THEN vat-proz = htparam.fdecimal.

/* service code */
FIND FIRST htparam WHERE htparam.paramnr = 136 NO-LOCK.
ASSIGN service-code = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr = service-code NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN service-proz = htparam.fdecimal.

FIND FIRST htparam WHERE htparam.paramnr = 556 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN disc-art1 = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 557 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN disc-art2 = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 596 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN disc-art3 = htparam.finteger.

FUNCTION datetime2char RETURNS CHAR
    (INPUT datum AS DATE,
     INPUT zeit  AS INTEGER).
DEF VAR str AS CHAR.
  ASSIGN
      str = STRING(YEAR(datum),"9999") + "-"
          + STRING(MONTH(datum),"99")  + "-"
          + STRING(DAY(datum),"99")    + " "
          + SUBSTR(STRING(zeit,"HH:MM:SS"),1,2) + ":"
          + SUBSTR(STRING(zeit,"HH:MM:SS"),4,2) + ":"
          + SUBSTR(STRING(zeit,"HH:MM:SS"),7,2) 
      .
  RETURN str.
END FUNCTION.

FIND FIRST queasy WHERE queasy.KEY = 291 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN DO:
    CREATE queasy.
    ASSIGN queasy.KEY   = 291
           queasy.date1 = fdate
           queasy.date2 = TODAY.
END.
ELSE DO:
    IF (queasy.date1 + 1) GT fdate THEN.
    ELSE ASSIGN fdate = queasy.date1 + 1. 

END.

FIND FIRST paramtext WHERE txtnr = 200 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN ASSIGN hotel-name = paramtext.ptexte.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
    RUN decode-string(paramtext.ptexte, OUTPUT hotel-id). 

DO datum = fdate TO tdate:
    RUN step-1(datum).

    FIND FIRST bqueasy WHERE bqueasy.KEY = 291 NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN DO:
        IF datum GE (bqueasy.date1 + 1) THEN DO:
            FIND FIRST tqueasy WHERE tqueasy.KEY = 291 NO-LOCK NO-ERROR.
            IF AVAILABLE tqueasy THEN DO:
                FIND CURRENT tqueasy EXCLUSIVE-LOCK.
                ASSIGN tqueasy.date1 = datum
                       tqueasy.date2 = TODAY.
                FIND CURRENT tqueasy NO-LOCK.
                RELEASE tqueasy.
            END.
        END.
    END.
END.

PROCEDURE step-1:    
    DEF INPUT PARAMETER bill-date AS DATE.


    FOR EACH billjournal NO-LOCK WHERE
          billjournal.bill-datum = bill-date AND
          billjournal.anzahl NE 0 AND
          billjournal.betrag NE 0 BY billjournal.rechnr
          BY billjournal.departement BY billjournal.artnr:

        ASSIGN do-it     = YES.        
        IF do-it THEN 
        DO:
            FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
              AND artikel.departement = billjournal.departement NO-LOCK NO-ERROR.
            do-it = AVAILABLE artikel AND 
                (artikel.mwst-code NE 0 OR artikel.service-code NE 0).
            IF do-it THEN
            DO:
              do-it = (artikel.artart = 0 OR artikel.artart = 8).
            END.
        END.
    
        IF do-it AND artikel.bezeich MATCHES("*Remain*")
              AND artikel.bezeich MATCHES("*Balance*") THEN do-it = NO.
    
        IF do-it THEN DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK.
                    
            ASSIGN
              serv        = 0
              vat         = 0
              netto       = 0
              serv-betrag = 0
              vat-betrag  = 0
            .
            RUN calc-servvat.p (artikel.departement, artikel.artnr, billjournal.bill-datum,
              artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                    
            IF vat = 1 THEN
              ASSIGN netto = billjournal.betrag * 100 / vat-proz.
            ELSE 
            DO:    
              IF serv = 1 THEN ASSIGN serv-betrag = netto.
              ELSE IF vat GT 0 THEN
              ASSIGN 
                  netto = billjournal.betrag / (1 + serv + vat)
                  serv-betrag = netto * serv
                  vat-betrag  = netto * vat
              .
            END.       
    
    
            IF netto NE 0 THEN DO:                
                FIND FIRST tlist WHERE tlist.invno = STRING(billjournal.rechnr)
                    AND tlist.depart  = billjournal.departement NO-LOCK NO-ERROR.
                IF NOT AVAILABLE tlist THEN DO:
                    CREATE tlist.
                    ASSIGN 
                        tlist.invno         = STRING(billjournal.rechnr)
                        tlist.depart        = billjournal.departement
                    .
                END.
                ASSIGN                
                    tlist.subtotal        = tlist.subtotal + netto
                    tlist.service         = tlist.service + serv-betrag
                    tlist.pajak           = tlist.pajak + vat-betrag
                    tlist.datum-trx       = datetime2char(billjournal.bill-datum, billjournal.zeit)
                    tlist.amount          = tlist.amount + billjournal.betrag                   
                 .            
            END.        
      END.
    END.


 FOR EACH h-bill-line NO-LOCK WHERE 
      h-bill-line.rechnr GT 0 AND
      h-bill-line.bill-datum EQ bill-date AND
      h-bill-line.zeit GE 0 AND
      h-bill-line.artnr GT 0 AND 
      h-bill-line.betrag NE 0 USE-INDEX bildat_index
      BY h-bill-line.departement BY h-bill-line.rechnr
      BY h-bill-line.sysdate DESCENDING
      BY h-bill-line.zeit DESCENDING:
      FIND FIRST hbill-list WHERE hbill-list.dept = h-bill-line.departement
          AND hbill-list.rechnr = h-bill-line.rechnr NO-ERROR.      
      IF NOT AVAILABLE hbill-list THEN
      DO:          
        CREATE hbill-list.
        ASSIGN
            hbill-list.dept   = h-bill-line.departement
            hbill-list.rechnr = h-bill-line.rechnr
        .
        FIND FIRST hbill-buff WHERE hbill-buff.departement = h-bill-line.departement
            AND hbill-buff.rechnr = h-bill-line.rechnr
            /*MT 29/05/15
            AND hbill-buff.sysdate GT h-bill-line.sysdate
            */
            AND hbill-buff.bill-datum GT h-bill-line.bill-datum
            NO-LOCK NO-ERROR.
        hbill-list.do-it = NOT AVAILABLE hbill-buff.
      END.
  END.

  FOR EACH hbill-list WHERE hbill-list.do-it = YES:                                        
    FOR EACH h-bill-line WHERE h-bill-line.departement = hbill-list.dept
        AND h-bill-line.rechnr = hbill-list.rechnr 
        AND h-bill-line.artnr GT 0 NO-LOCK,
        FIRST h-artikel WHERE h-artikel.departement = h-bill-line.departement
        AND h-artikel.artnr = h-bill-line.artnr AND h-artikel.artart = 0  NO-LOCK:
        hbill-list.tot-sales = hbill-list.tot-sales + h-bill-line.betrag.                
    END.
  END.

  FOR EACH hbill-list WHERE hbill-list.do-it = YES
    AND hbill-list.tot-sales NE 0:
    FOR EACH h-bill-line WHERE h-bill-line.departement = hbill-list.dept
        AND h-bill-line.rechnr = hbill-list.rechnr 
        /*MT 06/05/15 AND h-bill-line.sysdate = bill-date */
        AND h-bill-line.bill-datum = bill-date
        NO-LOCK BY h-bill-line.zeit DESC:
        IF h-bill-line.artnr = 0 THEN
        DO:
            IF hbill-list.tot-sales * h-bill-line.betrag LE 0 THEN
            DO:
              IF hbill-list.i-fact LE 0 THEN
                hbill-list.i-fact = hbill-list.i-fact + 1.
            END.
            ELSE 
            DO:    
              IF hbill-list.i-fact GE 0 THEN
                hbill-list.i-fact = hbill-list.i-fact - 1.
            END.
        END.
        ELSE
        DO:
            FIND FIRST h-artikel WHERE h-artikel.departement = h-bill-line.departement
                AND h-artikel.artnr = h-bill-line.artnr NO-LOCK.
            IF h-artikel.artart = 2 OR h-artikel.artart = 6
                OR h-artikel.artart = 7 THEN
            DO:
              IF NOT h-bill-line.bezeich MATCHES ("*(Change)*") THEN
              DO:
                IF hbill-list.tot-sales * h-bill-line.betrag LE 0 THEN
                DO:
                  IF hbill-list.i-fact LE 0 THEN
                    hbill-list.i-fact = hbill-list.i-fact + 1.
                END.
                ELSE 
                DO:    
                  IF hbill-list.i-fact GT 0 THEN
                    hbill-list.i-fact = hbill-list.i-fact - 1.
                END.
              END.
            END.
        END.
    END.
  END.
  
  
  FOR EACH hbill-list WHERE hbill-list.do-it AND hbill-list.i-fact NE 0:
    FOR EACH h-bill-line WHERE h-bill-line.departement = hbill-list.dept
      AND h-bill-line.rechnr = hbill-list.rechnr 
      AND h-bill-line.artnr GT 0 NO-LOCK,
      FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
      AND h-artikel.departement = h-bill-line.departement 
      AND h-artikel.artart = 0 NO-LOCK:

        IF h-artikel.artart = 0 OR h-artikel.artart = 8 THEN DO:
            ASSIGN
              serv        = 0
              vat         = 0
              netto       = 0
              serv-betrag = 0
              vat-betrag  = 0
            .

            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                 AND artikel.departement = h-artikel.departement NO-LOCK.
            IF AVAILABLE artikel THEN DO:

                RUN calc-servvat.p (artikel.departement, artikel.artnr, h-bill-line.bill-datum,
                    artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                /*IF h-bill-line.betrag GT 0 THEN*/ DO:
                   IF vat = 1 THEN
                      ASSIGN netto = h-bill-line.betrag * 100 / vat-proz.
                    ELSE 
                    DO:    
                      IF serv = 1 THEN ASSIGN serv-betrag = netto.
                      ELSE IF vat GT 0 THEN
                      ASSIGN 
                          netto = h-bill-line.betrag / (1 + serv + vat)
                          serv-betrag = netto * serv
                          vat-betrag  = netto * vat
                      .
                    END.

                    
                    IF netto NE 0 THEN DO:                            
                          FIND FIRST tlist WHERE tlist.invno = STRING(h-bill-line.rechnr)
                              AND tlist.depart = h-bill-line.departement NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE tlist THEN DO:
                              CREATE tlist.
                              ASSIGN 
                                  tlist.invno  = STRING(h-bill-line.rechnr)
                                  tlist.depart = h-bill-line.departement 
                               .                                                                                                       
                          END.
                       
                          ASSIGN                
                                tlist.subtotal        = tlist.subtotal + netto
                                tlist.service         = tlist.service + serv-betrag
                                tlist.pajak           = tlist.pajak + vat-betrag
                                tlist.datum-trx       = datetime2char(h-bill-line.bill-datum, h-bill-line.zeit)
                                tlist.amount          = tlist.amount + h-bill-line.betrag                   
                         .                                                                                       
                    END.
                END.
            END.
       END.
    END.
  END.
END.


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 
