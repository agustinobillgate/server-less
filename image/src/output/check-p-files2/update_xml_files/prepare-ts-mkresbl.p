DEF TEMP-TABLE t-tisch
    FIELD tischnr LIKE tisch.tischnr.

DEF INPUT  PARAMETER s-recid AS INT.
DEF INPUT  PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER gname AS CHAR.
DEF OUTPUT PARAMETER telefon AS CHAR.
DEF OUTPUT PARAMETER comments AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-tisch.

IF s-recid NE 0 THEN
DO:
    FIND FIRST queasy WHERE RECID(queasy) = s-recid EXCLUSIVE-LOCK.
    ASSIGN
      gname = ENTRY(1, queasy.char2, "&&")
      telefon = TRIM(SUBSTR(queasy.char1,10))
      comments = ENTRY(2, queasy.char3, ";") NO-ERROR
    .
END.

  FOR EACH tisch WHERE departement = curr-dept:
      CREATE t-tisch.
      ASSIGN t-tisch.tischnr = tisch.tischnr.
  END.
