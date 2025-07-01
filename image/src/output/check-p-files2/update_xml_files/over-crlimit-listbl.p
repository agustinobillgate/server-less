DEFINE TEMP-TABLE c-list
    FIELD NAME     AS CHAR
    FIELD rechnr   AS INTEGER
    FIELD p-artnr  AS INTEGER
    FIELD datum    AS DATE
    FIELD dept     AS INTEGER
    FIELD betrag   AS DECIMAL
    FIELD f-betrag AS DECIMA
.

DEFINE TEMP-TABLE output-list
    FIELD guest-name   AS CHAR
    FIELD artnr        AS INTEGER
    FIELD art-desc     AS CHAR
    FIELD card-no      AS CHAR
    FIELD credit-limit AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD amount       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD balanced     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
.

DEFINE TEMP-TABLE out-list 
    FIELD guest-name   AS CHAR
    FIELD artnr        AS INTEGER
    FIELD art-desc     AS CHAR
    FIELD card-no      AS CHAR
    FIELD credit-limit AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD amount       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD balanced     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
.

DEFINE INPUT PARAMETER from-date       AS DATE.
DEFINE INPUT PARAMETER to-date         AS DATE.
DEFINE INPUT PARAMETER from-dept       AS INTEGER.
DEFINE INPUT PARAMETER to-dept         AS INTEGER.
DEFINE INPUT PARAMETER from-art        AS INTEGER.
DEFINE INPUT PARAMETER to-art          AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR out-list.

DEFINE VARIABLE foreign-nr AS INTEGER INIT 0.

/* Dzikri EA93D8 - Handling null guest name */
FUNCTION handle-null-char RETURNS CHAR(inp-char AS CHAR):
  IF inp-char EQ ? THEN
  DO:
      RETURN "".
  END.
  ELSE
  DO:
      RETURN inp-char.
  END.
END FUNCTION.
/* Dzikri EA93D8 - END */

RUN create-list.

PROCEDURE create-list:
  DEFINE VARIABLE f-endkum        AS INTEGER. 
  DEFINE VARIABLE b-endkum        AS INTEGER. 
  DEFINE VARIABLE rate            AS DECIMAL INITIAL 1.
  DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1.
  DEFINE VARIABLE curr-datum      AS DATE.
  DEFINE VARIABLE double-currency AS LOGICAL.
  DEFINE VARIABLE bezeich         AS CHARACTER.
  
  DEFINE BUFFER h-art  FOR h-artikel. 

  FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
  IF htparam.flogical THEN 
  DO: 
    double-currency = YES. 
  END. 

  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  IF htparam.fchar NE "" THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
    DO: 
      exchg-rate = waehrung.ankauf / waehrung.einheit. 
      foreign-nr = waehrung.waehrungsnr. 
    END. 
    ELSE exchg-rate = 1. 
  END. 

  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK :
    FOR EACH h-compli WHERE h-compli.datum GE from-date AND h-compli.datum LE to-date 
        AND h-compli.departement = hoteldpt.num AND h-compli.betriebsnr = 0 NO-LOCK, 
      FIRST h-art WHERE h-art.departement = h-compli.departement 
        AND h-art.artnr = h-compli.p-artnr AND h-art.artart = 11 NO-LOCK BY h-compli.rechnr: 

      IF double-currency AND curr-datum NE h-compli.datum THEN 
      DO: 
        curr-datum = h-compli.datum. 
        RUN find-exrate(curr-datum). 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = exchg-rate. 
      END. 

      FIND FIRST c-list WHERE c-list.datum = h-compli.datum AND c-list.dept = h-compli.departement 
        AND c-list.rechnr = h-compli.rechnr AND c-list.p-artnr = h-compli.p-artnr NO-ERROR. 
      IF NOT AVAILABLE c-list THEN 
      DO: 
        create c-list. 
        c-list.datum    = h-compli.datum. 
        c-list.dept     = h-compli.departement. 
        c-list.rechnr   = h-compli.rechnr. 
        c-list.p-artnr  = h-compli.p-artnr. 
        FIND FIRST h-bill WHERE h-bill.rechnr = h-compli.rechnr AND h-bill.departement = h-compli.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN c-list.name = handle-null-char(h-bill.bilname). 
        ELSE 
        DO: 
          FIND FIRST h-journal WHERE h-journal.bill-datum = h-compli.datum AND h-journal.departement = h-compli.departement 
            AND h-journal.segmentcode = h-compli.p-artnr AND h-journal.zeit GE 0 USE-INDEX segment_ix NO-LOCK NO-ERROR. 
          IF AVAILABLE h-journal AND h-journal.aendertext NE "" THEN 
            c-list.name = handle-null-char(h-journal.aendertext). 
        END. 
      END. 

      ASSIGN c-list.betrag = c-list.betrag + h-compli.anzahl * h-compli.epreis * rate. 
    END.
  END.
  /* Dzikri EA93D8 - show all data */
  FOR EACH queasy WHERE queasy.KEY = 105 NO-LOCK:
      bezeich = queasy.char1 + " - " + STRING(MONTH(to-date),"99") + "/" + string(YEAR(to-date),"9999").
      FIND FIRST output-list WHERE output-list.guest-name EQ bezeich NO-ERROR.
      IF NOT AVAILABLE output-list THEN
      DO:
          CREATE output-list.
          ASSIGN
            output-list.guest-name       = bezeich
            output-list.credit-limit     = queasy.deci3
            output-list.artnr            = queasy.number3
            output-list.card-no          = queasy.char2
          .
        
          FIND FIRST h-artikel WHERE h-artikel.departement = 1 AND h-artikel.artnr = queasy.number3 NO-LOCK NO-ERROR.
          IF AVAILABLE h-artikel THEN ASSIGN output-list.art-desc = h-artikel.bezeich.
      END.
      
      output-list.amount   = 0.
      output-list.balanced = queasy.deci3 - output-list.amount.
  END.
  /* Dzikri EA93D8 - END */
  
  FOR EACH c-list :
      /* Dzikri EA93D8 - find compliment that match the card */
      FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ c-list.rechnr AND h-bill-line.artnr EQ c-list.p-artnr NO-LOCK NO-ERROR.
      IF AVAILABLE h-bill-line THEN 
      DO:
          FIND FIRST queasy WHERE queasy.KEY = 105 AND queasy.char1 EQ h-bill-line.bezeich AND queasy.number3 EQ h-bill-line.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              bezeich = queasy.char1 + " - " + STRING(MONTH(c-list.datum),"99") + "/" + string(YEAR(c-list.datum),"9999").
              FIND FIRST output-list WHERE output-list.guest-name EQ bezeich NO-ERROR.
              IF NOT AVAILABLE output-list THEN
              DO:
                  CREATE output-list.
                  ASSIGN
                    output-list.guest-name       = bezeich
                    output-list.credit-limit     = queasy.deci3
                    output-list.artnr            = queasy.number3
                    output-list.card-no          = queasy.char2
                  .
                
                  FIND FIRST h-artikel WHERE h-artikel.departement = 1 AND h-artikel.artnr = queasy.number3 NO-LOCK NO-ERROR.
                  IF AVAILABLE h-artikel THEN ASSIGN output-list.art-desc = h-artikel.bezeich.
              END.
              output-list.amount = output-list.amount + c-list.betrag.
              output-list.balanced = queasy.deci3 - output-list.amount.
          END.
      END.
      /* Dzikri EA93D8 - END */
  END.

  FOR EACH output-list WHERE output-list.artnr GE from-art AND output-list.artnr LE to-art  
       NO-LOCK BY output-list.guest-name :
      
      CREATE out-list.
      ASSIGN
          out-list.guest-name    = output-list.guest-name   
          out-list.artnr         = output-list.artnr        
          out-list.art-desc      = output-list.art-desc     
          out-list.card-no       = output-list.card-no      
          out-list.credit-limit  = output-list.credit-limit 
          out-list.amount        = output-list.amount       
          out-list.balanced      = output-list.balanced     
      .
  END.

END.

PROCEDURE find-exrate: 
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
  IF foreign-nr NE 0 THEN 
      FIND FIRST exrate WHERE exrate.artnr = foreign-nr AND exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE 
      FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. 
END.
