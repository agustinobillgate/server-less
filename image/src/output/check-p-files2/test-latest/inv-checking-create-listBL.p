DEF TEMP-TABLE s-list2
    FIELD fibu1 LIKE gl-acct.fibukonto
    FIELD saldo1a AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2a AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo1  AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo3 AS DECIMAL LABEL "DIFF" format "->>>,>>>,>>9".

DEF TEMP-TABLE s-list
    FIELD fibu LIKE gl-acct.fibukonto
    FIELD saldo1 AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2 AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo  AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0.

DEF TEMP-TABLE coa-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD datum     AS DATE COLUMN-LABEL "Date"
    FIELD wert      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0
    FIELD debit     LIKE gl-jouhdr.debit  INITIAL 0
    FIELD credit    LIKE gl-jouhdr.credit INITIAL 0.

DEF TEMP-TABLE art-list2
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF INPUT PARAMETER invType  AS INT.
DEF INPUT PARAMETER d1       AS DATE.
DEF OUTPUT PARAMETER saldo   AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR s-list2.
DEF OUTPUT PARAMETER TABLE FOR art-list2.

DEF VAR mon     AS INTEGER.
DEF VAR art1    AS INTEGER.
DEF VAR art2    AS INTEGER.
DEF VAR frNr    AS INTEGER.
DEF VAR toNr    AS INTEGER.
DEFINE VARIABLE saldo1   AS DECIMAL NO-UNDO.
DEFINE VARIABLE saldo2   AS DECIMAL NO-UNDO.

DEFINE VARIABLE inv-date AS DATE NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN inv-date = htparam.fdate.

IF d1 LT inv-date THEN RUN create-listhis.
ELSE RUN create-list.

PROCEDURE create-listhis:

  FOR EACH coa-list:
      DELETE coa-list.
  END.
  FOR EACH s-list:
      DELETE s-list.
  END.
  FOR EACH s-list2:
      DELETE s-list2.
  END.
  
  IF invType = 0 THEN RETURN.

  ASSIGN mon = MONTH(d1) - 1
         d1  = DATE(MONTH(d1), DAY(d1), YEAR(d1)) - 1
         d1  = DATE(MONTH(d1), 1, YEAR(d1)).
 

  IF invType = 1 THEN 
    ASSIGN
    art1 = 3
    art2 = 5
    frNr = 1000000
    toNr = 1999999.
  ELSE IF invType = 2 THEN 
    ASSIGN
    art1 = 6
    art2 = 6
    frNr = 2000000
    toNr = 2999999.
  IF invType = 3 THEN 
    ASSIGN
    frNr = 3000000
    toNr = 9999999.
     FOR EACH l-artikel WHERE artnr GE frNr AND artnr LE toNr NO-LOCK:

         ASSIGN 
            saldo1 = 0
            saldo2 = 0.

         FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK.
         FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto
            NO-LOCK.
         FIND FIRST s-list WHERE s-list.fibu = gl-acct.fibukonto NO-ERROR.
         IF NOT AVAILABLE s-list THEN
         DO:
            CREATE s-list.
            IF mon GT 0 THEN
                ASSIGN s-list.fibu = gl-acct.fibukonto
                       s-list.saldo2 = gl-acct.actual[mon]
                       saldo2      = gl-acct.actual[mon].
            ELSE
                ASSIGN s-list.fibu = gl-acct.fibukonto
                       s-list.saldo2 = gl-acct.last-yr[12]
                       saldo2      = gl-acct.last-yr[12].
          END.
          FIND FIRST l-besthis WHERE l-besthis.anf-best-dat = d1
                AND l-besthis.artnr = l-artikel.artnr
                AND l-besthis.lager-nr = 0 NO-LOCK NO-ERROR.
          IF AVAILABLE l-besthis THEN 
              ASSIGN
                s-list.saldo1 = s-list.saldo1 + l-besthis.val-anf-best
                saldo1        = l-besthis.val-anf-best. 

          CREATE art-list2.
          ASSIGN
                art-list2.artnr    = l-artikel.artnr
                art-list2.artname  = l-artikel.bezeich
                art-list2.saldo1   = saldo1
                art-list2.saldo2   = saldo2
            .
     END.

  saldo = 0.
  FOR EACH s-list:
    saldo = saldo + s-list.saldo1 - s-list.saldo2.
    s-list.saldo = saldo.
    CREATE s-list2.
    ASSIGN s-list2.fibu = s-list.fibu
           s-list2.saldo1a = s-list.saldo1
           s-list2.saldo2a = s-list.saldo2
           s-list2.saldo3 = s-list.saldo1 - s-list.saldo2
           s-list2.saldo1 = s-list.saldo.
  END.
END.




PROCEDURE create-list:

  FOR EACH coa-list:
      DELETE coa-list.
  END.
  FOR EACH s-list:
      DELETE s-list.
  END.
  FOR EACH s-list2:
      DELETE s-list2.
  END.
  
  IF invType = 0 THEN RETURN.

  ASSIGN mon = MONTH(d1) - 1.
 

  IF invType = 1 THEN 
    ASSIGN
    art1 = 3
    art2 = 5
    frNr = 1000000
    toNr = 1999999.
  ELSE IF invType = 2 THEN 
    ASSIGN
    art1 = 6
    art2 = 6
    frNr = 2000000
    toNr = 2999999.
  IF invType = 3 THEN 
    ASSIGN
    frNr = 3000000
    toNr = 9999999.
     FOR EACH l-artikel WHERE artnr GE frNr AND artnr LE toNr NO-LOCK:
         ASSIGN 
            saldo1 = 0
            saldo2 = 0.
         FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK.
         FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto
            NO-LOCK.
         FIND FIRST s-list WHERE s-list.fibu = gl-acct.fibukonto NO-ERROR.
         IF NOT AVAILABLE s-list THEN
         DO:
            CREATE s-list.
            IF mon GT 0 THEN
                ASSIGN s-list.fibu = gl-acct.fibukonto
                       s-list.saldo2 = gl-acct.actual[mon]
                       saldo2        = gl-acct.actual[mon].
            ELSE
                ASSIGN s-list.fibu = gl-acct.fibukonto
                       s-list.saldo2 = gl-acct.last-yr[12]
                       saldo2        = gl-acct.last-yr[12].
          END.
          FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr
                AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
          IF AVAILABLE l-bestand THEN 
              ASSIGN s-list.saldo1 = s-list.saldo1 + l-bestand.val-anf-best
                     saldo1        = l-bestand.val-anf-best. 
           
          CREATE art-list2.
          ASSIGN
                art-list2.artnr    = l-artikel.artnr
                art-list2.artname  = l-artikel.bezeich
                art-list2.saldo1   = saldo1
                art-list2.saldo2   = saldo2
            .
     END.
  saldo = 0.
  FOR EACH s-list:
    saldo = saldo + s-list.saldo1 - s-list.saldo2.
    s-list.saldo = saldo.
    CREATE s-list2.
    ASSIGN s-list2.fibu = s-list.fibu
           s-list2.saldo1a = s-list.saldo1
           s-list2.saldo2a = s-list.saldo2
           s-list2.saldo3 = s-list.saldo1 - s-list.saldo2
           s-list2.saldo1 = s-list.saldo.
  END.
END.


