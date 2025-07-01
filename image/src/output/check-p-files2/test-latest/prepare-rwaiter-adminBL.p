
DEFINE TEMP-TABLE q1-list
    FIELD kellner-nr    LIKE kellner.kellner-nr
    FIELD kellnername   LIKE kellner.kellnername
    FIELD kumsatz-nr    LIKE kellner.kumsatz-nr
    FIELD kumsatz-nr1   LIKE kellne1.kumsatz-nr
    FIELD kcredit-nr    LIKE kellner.kcredit-nr
    FIELD kzahl-nr      LIKE kellner.kzahl-nr
    FIELD kzahl-nr1     LIKE kellne1.kzahl-nr
    FIELD masterkey     LIKE kellner.masterkey
    FIELD sprachcode    LIKE kellner.sprachcode
    FIELD r-kellner AS INT
    FIELD r-kellne1 AS INT.

DEFINE TEMP-TABLE t-kellner LIKE kellner.

DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR t-kellner.

FOR EACH kellner WHERE kellner.departement = dept NO-LOCK BY kellner.kellner-nr: 
    FIND FIRST kellne1 WHERE kellne1.departement = kellner.departement AND kellne1.kellner-nr = kellner.kellner-nr NO-LOCK NO-ERROR.
    IF AVAILABLE kellne1 THEN
    DO:
        CREATE q1-list.
        ASSIGN
        q1-list.kellner-nr    = kellner.kellner-nr
        q1-list.kellnername   = kellner.kellnername
        q1-list.kumsatz-nr    = kellner.kumsatz-nr
        q1-list.kumsatz-nr1   = kellne1.kumsatz-nr
        q1-list.kcredit-nr    = kellner.kcredit-nr
        q1-list.kzahl-nr      = kellner.kzahl-nr
        q1-list.kzahl-nr1     = kellne1.kzahl-nr
        q1-list.masterkey     = kellner.masterkey
        q1-list.sprachcode    = kellner.sprachcode
        q1-list.r-kellner = RECID(kellner)
        q1-list.r-kellne1 = RECID(kellne1).
    END.
END.

FOR EACH kellner WHERE kellner.departement = dept NO-LOCK:
    CREATE t-kellner.
    BUFFER-COPY kellner TO t-kellner.
END.
