
DEFINE TEMP-TABLE t-wgrpgen
    FIELD eknr      LIKE wgrpgen.eknr
    FIELD bezeich   LIKE wgrpgen.bezeich.

DEF OUTPUT PARAMETER TABLE FOR t-wgrpgen.

FOR EACH wgrpgen NO-LOCK:
    CREATE t-wgrpgen.
    ASSIGN
    t-wgrpgen.eknr      = wgrpgen.eknr
    t-wgrpgen.bezeich   = wgrpgen.bezeich.
END.
