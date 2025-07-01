DEF TEMP-TABLE coa-list2
    FIELD datum1 AS DATE COLUMN-LABEL "Date"
    FIELD wert1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "RECEIVING Amount"
    FIELD fibu1 LIKE gl-acct.fibukonto
    FIELD debitcredit AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "GL Jourrnal"
    FIELD diff AS DECIMAL FORMAT "->>>,>>>,>>9" LABEL "DIFF".

DEF TEMP-TABLE coa-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD datum     AS DATE COLUMN-LABEL "Date"
    FIELD wert      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0
    FIELD debit     LIKE gl-jouhdr.debit  INITIAL 0
    FIELD credit    LIKE gl-jouhdr.credit INITIAL 0.

DEF TEMP-TABLE art-list3
    FIELD datum     AS DATE
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF INPUT PARAMETER TABLE FOR coa-list.
DEF INPUT PARAMETER invType AS INT.
DEF INPUT PARAMETER d1      AS DATE.
DEF INPUT PARAMETER d2      AS DATE.
DEF OUTPUT PARAMETER frNr   AS INT.
DEF OUTPUT PARAMETER toNr   AS INT.
DEF OUTPUT PARAMETER saldo  AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR coa-list2.
DEF OUTPUT PARAMETER TABLE FOR art-list3.

DEF VAR d       AS DATE.
DEF VAR mon     AS INTEGER.
DEF VAR art1    AS INTEGER.
DEF VAR art2    AS INTEGER.
DEF VAR fibu    AS CHAR.

RUN create-list2.
FOR EACH coa-list2 BY coa-list2.datum:
    IF coa-list2.diff = 0 THEN DELETE coa-list2.     
END.

PROCEDURE create-list2:

  FOR EACH coa-list2:
     DELETE coa-list2.
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

  FIND FIRST l-op WHERE l-op.datum GE d1 AND l-op.datum LE d2 NO-LOCK NO-ERROR.
  IF AVAILABLE l-op THEN DO:
      DO d = d1 TO d2:
            FOR EACH l-op NO-LOCK WHERE 
              l-op.artnr GE frNr   AND
              l-op.artnr LE toNr   AND
              l-op.datum = d       AND
              l-op.op-art = 1      AND
              l-op.loeschflag LE 1:
              FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK.
              FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK.
              IF l-untergrup.fibukonto NE "" THEN fibu = l-untergrup.fibukonto.
              ELSE fibu = l-artikel.fibukonto.
              FIND FIRST coa-list WHERE coa-list.fibukonto = fibu AND 
                  coa-list.datum = d NO-ERROR.
              IF NOT AVAILABLE coa-list THEN
              DO:
                  CREATE coa-list.
                  ASSIGN coa-list.fibukonto = fibu
                         coa-list.datum     = d.
              END.
              ASSIGN coa-list.wert = coa-list.wert + l-op.warenwert.

              CREATE art-list3.
              ASSIGN 
                  art-list3.datum       = d
                  art-list3.artnr       = l-op.artnr
                  art-list3.artname     = l-artikel.bezeich
                  art-list3.saldo1      = l-op.warenwert
              .
                   
            END. /*for each l-op*/                                  
      END. /*do d= d1 ....*/
  END.
  ELSE DO:
      DO d = d1 TO d2:
            FOR EACH l-ophis NO-LOCK WHERE 
              l-ophis.artnr GE frNr   AND
              l-ophis.artnr LE toNr   AND
              l-ophis.datum = d       AND
              l-ophis.op-art = 1:

              FIND FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK.
              FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK.
              IF l-untergrup.fibukonto NE "" THEN fibu = l-untergrup.fibukonto.
              ELSE fibu = l-artikel.fibukonto.
              FIND FIRST coa-list WHERE coa-list.fibukonto = fibu AND 
                  coa-list.datum = d NO-ERROR.
              IF NOT AVAILABLE coa-list THEN
              DO:
                  CREATE coa-list.
                  ASSIGN coa-list.fibukonto = fibu
                         coa-list.datum     = d.
              END.
              ASSIGN coa-list.wert = coa-list.wert + l-ophis.warenwert.

              CREATE art-list3.
              ASSIGN 
                  art-list3.datum       = d
                  art-list3.artnr       = l-ophis.artnr
                  art-list3.artname     = l-artikel.bezeich
                  art-list3.saldo1      = l-ophis.warenwert
              .

            END. /*for each l-op*/                                  
      END. /*do d= d1 ....*/
  END.

  
  
  FOR EACH coa-list:
       FOR EACH gl-jouhdr WHERE gl-jouhdr.datum = coa-list.datum
            AND gl-jouhdr.jtyp = 6 NO-LOCK:
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
            AND gl-journal.fibukonto = coa-list.fibukonto NO-LOCK:
            ASSIGN coa-list.debit = coa-list.debit + gl-journal.debit
                    coa-list.credit = coa-list.credit + gl-journal.credit.
        END.

        FIND FIRST art-list3 WHERE art-list3.datum = coa-list.datum NO-ERROR.
        IF AVAILABLE art-list3 THEN DO:
            ASSIGN art-list3.saldo2 = coa-list.debit - coa-list.credit.            
        END.
      END.
  END.

 FOR EACH coa-list BY coa-list.datum:
     CREATE coa-list2.
     ASSIGN coa-list2.datum1 = coa-list.datum
            coa-list2.wert1 = coa-list.wert
            coa-list2.fibu1 = coa-list.fibukonto
            coa-list2.debitcredit = coa-list.debit - coa-list.credit
            coa-list2.diff = coa-list.wert - coa-list.debit + coa-list.credit.
  END.
  
END.


