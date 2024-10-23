
DEFINE TEMP-TABLE t-nation
    FIELD nationnr LIKE nation.nationnr
    FIELD bezeich LIKE nation.bezeich.

DEF OUTPUT PARAMETER TABLE FOR t-nation.

FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich:
    CREATE t-nation.
    ASSIGN
    t-nation.nationnr = nation.nationnr
    t-nation.bezeich = nation.bezeich.
END.
