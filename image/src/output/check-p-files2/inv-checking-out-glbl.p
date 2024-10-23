DEF TEMP-TABLE coa-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD datum     AS DATE COLUMN-LABEL "Date"
    FIELD wert      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0
    FIELD debit     LIKE gl-jouhdr.debit  INITIAL 0
    FIELD credit    LIKE gl-jouhdr.credit INITIAL 0.

DEF TEMP-TABLE coa-list3
    FIELD datum2 AS DATE COLUMN-LABEL "Date"
    FIELD wert2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "OUTGOING Amount"
    FIELD fibu2 LIKE coa-list.fibukonto
    FIELD creditdebit AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "GL Jourrnal"
    FIELD diff AS DECIMAL FORMAT "->>>,>>>,>>9" LABEL "DIFF".

DEF TEMP-TABLE art-list4
    FIELD datum     AS DATE
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF INPUT PARAMETER invType AS INT.
DEF INPUT PARAMETER d1 AS DATE.
DEF INPUT PARAMETER d2      AS DATE.
DEF OUTPUT PARAMETER frNr AS INT.
DEF OUTPUT PARAMETER toNr AS INT.
DEF OUTPUT PARAMETER saldo   AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR coa-list3.
DEF OUTPUT PARAMETER TABLE FOR art-list4.

DEF VAR d       AS DATE.
DEF VAR mon     AS INTEGER.
DEF VAR art1    AS INTEGER.
DEF VAR art2    AS INTEGER.
DEF VAR fibu    AS CHAR.

RUN out-gl.
FOR EACH coa-list3 BY coa-list3.datum:
    IF coa-list3.diff = 0 THEN DELETE coa-list3.
END.

PROCEDURE out-gl:
  FOR EACH coa-list:
       DELETE coa-list.
  END.
  FOR EACH coa-list3:
       DELETE coa-list3.
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

  DO d = d1 TO d2:
      
    FOR EACH l-op NO-LOCK WHERE 
      l-op.artnr GE frNr        AND
      l-op.artnr LE toNr        AND
      l-op.datum = d            AND
      l-op.op-art = 3           AND
      SUBSTR(l-op.stornogrund,1,8) NE "00000000" AND
      l-op.loeschflag LE 1:
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK.
      FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
          NO-LOCK.
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

      CREATE art-list4.
      ASSIGN 
          art-list4.datum       = d
          art-list4.artnr       = l-op.artnr
          art-list4.artname     = l-artikel.bezeich
          art-list4.saldo1      = l-op.warenwert
      .      
    END.
    FIND FIRST l-ophis NO-LOCK WHERE 
          l-ophis.artnr GE frNr   AND
          l-ophis.artnr LE toNr   AND
          l-ophis.datum = d       AND
          l-ophis.op-art = 3      NO-ERROR.
    IF AVAILABLE l-ophis THEN
    FOR EACH l-ophis NO-LOCK WHERE 
      l-ophis.artnr GE frNr   AND
      l-ophis.artnr LE toNr   AND
      l-ophis.datum = d       AND
      SUBSTR(l-ophis.fibukonto,1,8) NE "00000000" AND
      l-ophis.op-art = 3:
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK.
      FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
          NO-LOCK.
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
      CREATE art-list4.
      ASSIGN 
          art-list4.datum       = d
          art-list4.artnr       = l-ophis.artnr
          art-list4.artname     = l-artikel.bezeich
          art-list4.saldo1      = l-ophis.warenwert
      .
    END.
  END.

  FOR EACH coa-list:
    FOR EACH gl-jouhdr WHERE gl-jouhdr.datum = coa-list.datum
      AND gl-jouhdr.jtyp = 3 
      AND SUBSTR(gl-jouhdr.refNo,1,LENGTH(refNo)) = refNo NO-LOCK:
      FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
          AND gl-journal.fibukonto = coa-list.fibukonto 
          AND SUBSTR(gl-journal.bemer,1,1) NE "*" NO-LOCK:
          ASSIGN coa-list.debit = coa-list.debit + gl-journal.debit
                 coa-list.credit = coa-list.credit + gl-journal.credit.
      END.

      FIND FIRST art-list4 WHERE art-list4.datum = coa-list.datum NO-ERROR.
        IF AVAILABLE art-list4 THEN DO:
            ASSIGN art-list4.saldo2 = coa-list.debit - coa-list.credit.            
        END.
    END.
  END.
  FOR EACH coa-list BY coa-list.datum:
    CREATE coa-list3.
    ASSIGN coa-list3.datum2 = coa-list.datum
           coa-list3.wert2 = coa-list.wert
           coa-list3.fibu = coa-list.fibukonto
           coa-list3.creditdebit = coa-list.credit - coa-list.debit
           coa-list3.diff = coa-list.wert - coa-list.credit + coa-list.debit.
  END.
END.

