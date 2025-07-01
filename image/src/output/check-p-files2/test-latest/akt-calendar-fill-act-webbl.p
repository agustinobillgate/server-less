
DEFINE TEMP-TABLE act
    FIELD linenr AS INT
    FIELD datum  AS DATE
    FIELD ftime  AS INT  
    FIELD ttime  AS INT 
    FIELD aktion  AS CHAR
    FIELD lname  AS CHAR
    FIELD kontakt  AS CHAR
    FIELD regard  AS CHAR 
    FIELD sales  AS CHAR
    FIELD priority AS INT
    FIELD flag  AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER all-flag AS LOGICAL.
DEF INPUT PARAMETER curr-month AS INT.
DEF INPUT PARAMETER curr-year AS INT.
DEF OUTPUT PARAMETER TABLE FOR act.

DEFINE VARIABLE lname       AS CHAR.

FOR EACH act:
    DELETE act.
END.

IF all-flag THEN
DO:
  FOR EACH akt-line WHERE akt-line.flag = 0 AND MONTH(akt-line.datum) = curr-month
    AND YEAR(akt-line.datum) = curr-year  NO-LOCK,
    FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
    FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK:

      FIND FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
        lname = guest.NAME + ", " + guest.anredefirma.
      CREATE act.
        ASSIGN
            act.linenr = akt-line.linenr
            act.datum = akt-line.datum
            act.ftime = akt-line.zeit 
            act.ttime = akt-line.dauer
            act.aktion = akt-code.bezeich 
            act.kontakt = akt-line.kontakt
            act.lname = lname
            act.regard = akt-line.regard
            act.sales = bediener.userinit
            act.priority = akt-line.prioritaet
            act.flag = akt-line.flag.
  END.
END.
ELSE
DO:
  FOR EACH akt-line WHERE akt-line.flag = 0 AND akt-line.userinit = user-init AND
    MONTH(akt-line.datum) = curr-month AND year(akt-line.datum) = curr-year  NO-LOCK,
    FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
    FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK:

      FIND FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
        lname = guest.NAME + ", " + guest.anredefirma.
      CREATE act.

        ASSIGN
            act.linenr = akt-line.linenr
            act.datum = akt-line.datum
            act.ftime = akt-line.zeit 
            act.ttime = akt-line.dauer
            act.aktion = akt-code.bezeich 
            act.kontakt = akt-line.kontakt
            act.lname = lname
            act.regard = akt-line.regard
            act.sales = bediener.userinit
            act.priority = akt-line.prioritaet
            act.flag = akt-line.flag.
  END.
END.
