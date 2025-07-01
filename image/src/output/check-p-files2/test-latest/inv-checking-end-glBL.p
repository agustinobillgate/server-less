DEF TEMP-TABLE s-list
    FIELD fibu LIKE gl-acct.fibukonto
    FIELD saldo1 AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2 AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo  AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0.

DEF TEMP-TABLE s-list3
    FIELD fibu2 LIKE gl-acct.fibukonto
    FIELD saldo1b AS DECIMAL LABEL "INVENTORY" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo2b AS DECIMAL LABEL "G/L" FORMAT "->>>,>>>,>>9" INITIAL 0
    FIELD saldo3a AS DECIMAL LABEL "DIFF" format "->>>,>>>,>>9"
    FIELD saldo11  AS DECIMAL LABEL "Total DIFF" FORMAT "->>>,>>>,>>9" INITIAL 0.

DEF TEMP-TABLE art-list
    FIELD artnr     AS INTEGER
    FIELD artname   AS CHAR
    FIELD saldo1    AS DECIMAL
    FIELD saldo2    AS DECIMAL.

DEF INPUT PARAMETER frNr AS INT.
DEF INPUT PARAMETER toNr AS INT.
DEF INPUT PARAMETER d2 AS DATE.
DEF INPUT PARAMETER saldo AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR s-list3.
DEF OUTPUT PARAMETER TABLE FOR art-list.

DEFINE VARIABLE inv-date AS DATE    NO-UNDO.
DEFINE VARIABLE saldo1   AS DECIMAL NO-UNDO.
DEFINE VARIABLE saldo2   AS DECIMAL NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN inv-date = htparam.fdate.

IF d2 LT inv-date THEN RUN end-glhis.
ELSE RUN end-gl.
FOR EACH s-list3:
  IF s-list3.saldo3a = 0 THEN DELETE s-list3.
END.

PROCEDURE end-glhis:
  FOR EACH s-list:
      DELETE s-list.
  END.
  FOR EACH s-list3:
      DELETE s-list3.
  END.
  
  IF MONTH(d2) = 1 THEN d2 = DATE(12, 31, YEAR(d2) - 1).
  ELSE d2 = DATE(MONTH(d2), 1, YEAR(d2)) - 1.

  FOR EACH l-artikel WHERE l-artikel.artnr GE frNr 
      AND l-artikel.artnr LE toNr NO-LOCK:
    
    ASSIGN 
        saldo1 = 0
        saldo2 = 0.

    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto
      NO-LOCK.
    FIND FIRST s-list WHERE s-list.fibu = gl-acct.fibukonto NO-ERROR.
    IF NOT AVAILABLE s-list THEN
    DO:
      CREATE s-list.
      ASSIGN s-list.fibu    = gl-acct.fibukonto
             s-list.saldo2  = gl-acct.actual[MONTH(d2)]
             saldo2         = gl-acct.actual[MONTH(d2)].
    END.
    FIND FIRST l-besthis WHERE l-besthis.anf-best-dat = d2
      AND l-besthis.artnr = l-artikel.artnr
      AND l-besthis.lager-nr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-besthis THEN 
        ASSIGN
            s-list.saldo1 = s-list.saldo1 + l-besthis.val-anf-best + l-besthis.wert-eingang
                            - l-besthis.wert-ausgang
            saldo1        = l-besthis.val-anf-best + l-besthis.wert-eingang
                            - l-besthis.wert-ausgang.

    CREATE art-list.
    ASSIGN
        art-list.artnr    = l-artikel.artnr
        art-list.artname  = l-artikel.bezeich
        art-list.saldo1   = saldo1
        art-list.saldo2   = saldo2
    .
  END.

  FOR EACH s-list:
      s-list.saldo = saldo.

      CREATE s-list3.
      ASSIGN s-list3.fibu2 =  s-list.fibu
             s-list3.saldo1b = s-list.saldo1
             s-list3.saldo2b = s-list.saldo2
             s-list3.saldo3a = s-list.saldo1 - s-list.saldo2.
  END.
END.



PROCEDURE end-gl:
  FOR EACH s-list:
      DELETE s-list.
  END.
  FOR EACH s-list3:
      DELETE s-list3.
  END.
  FOR EACH l-artikel WHERE l-artikel.artnr GE frNr 
      AND l-artikel.artnr LE toNr NO-LOCK:

    ASSIGN 
        saldo1 = 0
        saldo2 = 0.

    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto
      NO-LOCK.
    FIND FIRST s-list WHERE s-list.fibu = gl-acct.fibukonto NO-ERROR.
    IF NOT AVAILABLE s-list THEN
    DO:
      CREATE s-list.
      ASSIGN s-list.fibu   = gl-acct.fibukonto
             s-list.saldo2 = gl-acct.actual[MONTH(d2)]
             saldo2        = gl-acct.actual[MONTH(d2)].
    END.
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr
      AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN 
        ASSIGN
        s-list.saldo1 = s-list.saldo1 + l-bestand.val-anf-best + l-bestand.wert-eingang
                        - l-bestand.wert-ausgang
        saldo1        = l-bestand.val-anf-best + l-bestand.wert-eingang
                        - l-bestand.wert-ausgang.

    CREATE art-list.
    ASSIGN
        art-list.artnr    = l-artikel.artnr
        art-list.artname  = l-artikel.bezeich
        art-list.saldo1   = saldo1
        art-list.saldo2   = saldo2
    .

  END.

  FOR EACH s-list:
      s-list.saldo = saldo.

      CREATE s-list3.
      ASSIGN s-list3.fibu2 =  s-list.fibu
             s-list3.saldo1b = s-list.saldo1
             s-list3.saldo2b = s-list.saldo2
             s-list3.saldo3a = s-list.saldo1 - s-list.saldo2.
  END.
END.

