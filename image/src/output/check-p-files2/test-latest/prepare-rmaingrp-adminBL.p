
DEFINE TEMP-TABLE t-wgrpgen LIKE wgrpgen.

DEF OUTPUT PARAMETER TABLE FOR t-wgrpgen.

FOR EACH wgrpgen NO-LOCK BY wgrpgen.eknr:
    CREATE t-wgrpgen.
    BUFFER-COPY wgrpgen TO t-wgrpgen.
END.
