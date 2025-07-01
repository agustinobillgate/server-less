
DEF TEMP-TABLE t-eg-property
    FIELD nr      LIKE eg-property.nr
    FIELD bezeich LIKE eg-property.bezeich.

DEF INPUT PARAMETER maintask AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-eg-property.

FOR EACH eg-property WHERE eg-property.maintask = maintask /*AND 
    eg-property.location = location*/  NO-LOCK BY eg-property.nr:
    CREATE t-eg-property.
    ASSIGN
    t-eg-property.nr      = eg-property.nr
    t-eg-property.bezeich = eg-property.bezeich.
END.
