/*ragung 1B5600 web custom change str to temp-table*/
DEFINE TEMP-TABLE cancel-journal 
  FIELD dept        AS INTEGER
  FIELD rechnr      AS INTEGER
  FIELD billdate    AS DATE
  FIELD srecid      AS INTEGER
  FIELD depart      AS CHAR
  FIELD tbno        AS CHAR
  FIELD artno       AS CHAR
  FIELD bezeich     AS CHAR
  FIELD cancel      AS CHAR
  FIELD qty         AS CHAR
  FIELD amount      AS DECIMAL FORMAT "->,>>>,>>>,>>9"
  FIELD zeit        AS CHAR
  FIELD cname       AS CHAR
  . 

DEF INPUT PARAMETER from-dept AS INT.
DEF INPUT PARAMETER to-dept AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR cancel-journal.

RUN journal-list.

PROCEDURE journal-list: 
DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
DEFINE VARIABLE it-exist AS LOGICAL. 
DEFINE VARIABLE kname AS CHAR. 
 
  FOR EACH cancel-journal: 
    delete cancel-journal. 
  END. 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
      AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
      FOR EACH h-journal WHERE h-journal.stornogrund NE "" 
        AND h-journal.departement = hoteldpt.num 
        AND bill-datum = curr-date NO-LOCK BY h-journal.sysdate descending 
        BY h-journal.zeit descending: 

        FIND FIRST kellner WHERE kellner.kellner-nr = h-journal.kellner-nr 
          AND kellner.departement = h-journal.departement NO-LOCK NO-ERROR. 
        kname = "". 
        IF AVAILABLE kellner THEN kname = kellner.kellnername. 
        create cancel-journal.
        ASSIGN
            cancel-journal.dept     = h-journal.departement
            cancel-journal.rechnr   = h-journal.rechnr
            cancel-journal.billdate = h-journal.bill-datum
            cancel-journal.srecid   = RECID(h-journal)
        .

        IF AVAILABLE kellner THEN 
        DO: 
            ASSIGN 
            cancel-journal.depart       = TRIM(STRING(hoteldpt.depart, "x(30)"))
            cancel-journal.tbno         = TRIM(STRING(h-journal.tischnr, ">>>>>9"))	/*gerald tambah digit B27E0F*/
            cancel-journal.artno        = TRIM(STRING(h-journal.artnr, ">>>>>>>>>>>>9"))  /*william tambah digit 302eb8*/      
            cancel-journal.bezeich      = TRIM(STRING(h-journal.bezeich, "x(30)"))      
            cancel-journal.cancel       = h-journal.stornogrund        /* Dzikri DE9BA1 - remove cancel reason string length STRING(h-journal.stornogrund, "x(30)")  */
            cancel-journal.qty          = STRING(h-journal.anzahl, "-9999")       
            cancel-journal.amount       = h-journal.betrag
            cancel-journal.zeit         = STRING(h-journal.zeit, "HH:MM:SS") 
            cancel-journal.cname        = kname
            .
        END. 
        ELSE DO:        
            ASSIGN 
            cancel-journal.depart       = TRIM(STRING(hoteldpt.depart, "x(30)"))
            cancel-journal.tbno         = TRIM(STRING(h-journal.tischnr, ">>>>>9"))	/*gerald tambah digit B27E0F*/
            cancel-journal.artno        = TRIM(STRING(h-journal.artnr, ">>>>>>>>>>>>9"))  /*william tambah digit 302eb8*/         
            cancel-journal.bezeich      = TRIM(STRING(h-journal.bezeich, "x(30)"))      
            cancel-journal.cancel       = h-journal.stornogrund        /* Dzikri DE9BA1 - remove cancel reason string length STRING(h-journal.stornogrund, "x(30)")  */
            cancel-journal.qty          = STRING(h-journal.anzahl, "-9999")       
            cancel-journal.amount       = h-journal.betrag
            cancel-journal.zeit         = STRING(h-journal.zeit, "HH:MM:SS") 
            cancel-journal.cname        = kname
            .
        END. 
      END. 
    END. 
  END. 
END. 
