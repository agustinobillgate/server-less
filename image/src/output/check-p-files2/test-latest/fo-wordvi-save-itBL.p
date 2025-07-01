DEF TEMP-TABLE t-list
    FIELD texte AS CHAR.

DEF INPUT PARAMETER TABLE FOR t-list.
DEF INPUT PARAMETER briefnr AS INT.

DEF BUFFER bzeile   FOR briefzei.
DEF VAR counter     AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR reihenfolge AS INTEGER INITIAL 0 NO-UNDO.

FOR EACH t-list:
      IF counter = 0 THEN
      DO:
        FIND FIRST bzeile WHERE bzeile.briefnr = briefnr NO-LOCK NO-ERROR.
        reihenfolge = reihenfolge + 1.
        FIND FIRST bzeile WHERE bzeile.briefnr = briefnr 
          AND bzeile.briefzeilnr = reihenfolge EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE bzeile THEN
        DO:
            CREATE bzeile.
            ASSIGN
                bzeile.briefnr = briefnr
                bzeile.briefzeilnr = reihenfolge
            .
        END.
        bzeile.texte = "".
      END.
      
      ASSIGN
          bzeile.texte = bzeile.texte + t-list.texte + CHR(10)
          counter = counter + LENGTH(t-list.texte) + 1.
      IF counter GE 20000 THEN counter = 0.
END.

FIND CURRENT bzeile NO-LOCK NO-ERROR.
FOR EACH bzeile WHERE bzeile.briefnr = briefnr 
    AND bzeile.briefzeilnr GT reihenfolge:
    DELETE bzeile.
END.
