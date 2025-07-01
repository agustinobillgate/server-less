DEFINE TEMP-TABLE t-Sourccod
    FIELD source-code LIKE Sourccod.source-code
    FIELD bezeich LIKE Sourccod.bezeich.

DEF OUTPUT PARAMETER TABLE FOR t-Sourccod.

FOR EACH Sourccod:
    CREATE t-Sourccod.
    ASSIGN
    t-Sourccod.source-code = Sourccod.source-code
    t-Sourccod.bezeich = Sourccod.bezeich.
END.
