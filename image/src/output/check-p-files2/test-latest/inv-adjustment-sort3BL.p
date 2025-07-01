
DEF INPUT PARAMETER cbuff-zwkum AS INT.
DEF OUTPUT PARAMETER a-bez AS CHAR.

FIND FIRST l-untergrup WHERE l-untergrup.zwkum = cbuff-zwkum NO-LOCK.
a-bez = l-untergrup.bezeich.
