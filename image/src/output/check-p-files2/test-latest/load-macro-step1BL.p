DEFINE TEMP-TABLE coa-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD anzahl    AS   INTEGER INIT 0
    INDEX fibu_ix fibukonto.
DEFINE TEMP-TABLE art-list
    FIELD CODE AS CHAR.

DEF INPUT  PARAMETER briefnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR coa-list.
DEF OUTPUT PARAMETER TABLE FOR art-list.

DEF BUFFER parambuff FOR parameters.

DEF VARIABLE vstring          AS CHARACTER NO-UNDO INIT "".
DEF VARIABLE i                AS INT NO-UNDO.
DEF VARIABLE j                AS INT NO-UNDO INIT 0.

FIND FIRST coa-list NO-ERROR.
IF NOT AVAILABLE coa-list THEN
DO:
  FOR EACH gl-acct NO-LOCK:
    CREATE coa-list.
    ASSIGN coa-list.fibukonto = gl-acct.fibukonto.
  END.
  /*FOR EACH artikel WHERE artikel.artnr GE 1 AND artikel.artnr LE 50 NO-LOCK:
    vstring = STRING(artikel.artnr).
    j = 4 - LENGTH(vstring).
    IF LENGTH(vstring) LT 4 THEN
    DO:
      DO i = 1 TO j:
        vstring = "0" + vstring.
      END.
    END.
    FIND FIRST coa-list WHERE coa-list.fibukonto = vstring NO-LOCK NO-ERROR.
    IF NOT AVAILABLE coa-list THEN
    DO:
      CREATE coa-list.
      ASSIGN 
        coa-list.fibukonto = vstring
        coa-list.anzahl = 5.
    END.
  END.*/
END.
ELSE
FOR EACH coa-list WHERE coa-list.anzahl NE 0:
  coa-list.anzahl = 0.
END.

FOR EACH art-list:
    DELETE art-list.
END.

FOR EACH artikel NO-LOCK:
  CREATE art-list.
  ASSIGN 
    art-list.CODE = STRING(departement,"99") + STRING(artnr,"9999").
END.

/*FOR EACH artikel WHERE artikel.artnr GE 1 AND artikel.artnr LE 50 NO-LOCK:
  FIND FIRST art-list WHERE art-list.artnr = artikel.artnr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE art-list THEN
  DO:
    CREATE art-list.
    ASSIGN art-list.artnr = artikel.artnr.
  END.
END.*/

FIND FIRST parameters WHERE
    parameters.progname            = "GL-Macro"      AND
    parameters.SECTION             = STRING(briefnr) 
    NO-LOCK NO-ERROR.
DO WHILE AVAILABLE parameters:
    DO TRANSACTION:
      FIND FIRST parambuff WHERE RECID(parambuff) = RECID(parameters).
      DELETE parambuff.
    END.
    FIND NEXT parameters WHERE
      parameters.progname            = "GL-Macro"      AND
      parameters.SECTION             = STRING(briefnr)
      NO-LOCK NO-ERROR.
END.
