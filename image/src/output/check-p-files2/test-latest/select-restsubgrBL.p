
DEFINE TEMP-TABLE t-wgrpdep
    FIELD zknr      LIKE wgrpdep.zknr
    FIELD bezeich   LIKE wgrpdep.bezeich.

DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-wgrpdep.

FOR EACH wgrpdep WHERE wgrpdep.departement = dept NO-LOCK:
    CREATE t-wgrpdep.
    ASSIGN
    t-wgrpdep.zknr      = wgrpdep.zknr
    t-wgrpdep.bezeich   = wgrpdep.bezeich. 
END.
