DEF TEMP-TABLE t-mc-fee LIKE mc-fee.
DEF TEMP-TABLE t-mc-types LIKE mc-types
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-mc-guest LIKE mc-guest.

DEF OUTPUT PARAMETER TABLE FOR t-mc-types.
DEF OUTPUT PARAMETER TABLE FOR t-mc-fee.
DEF OUTPUT PARAMETER TABLE FOR t-mc-guest.

FOR EACH mc-types no-lock by mc-types.nr:
    CREATE t-mc-types.
    BUFFER-COPY mc-types TO t-mc-types.
    ASSIGN t-mc-types.rec-id = RECID(mc-types).
END.

FOR EACH mc-fee WHERE mc-fee.KEY = 1:
    CREATE t-mc-fee.
    BUFFER-COPY mc-fee TO t-mc-fee.
END.

FOR EACH mc-guest:
    CREATE t-mc-guest.
    BUFFER-COPY mc-guest TO t-mc-guest.
END.
