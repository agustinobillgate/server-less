
DEF TEMP-TABLE t-gc-piacct LIKE gc-piacct.

DEF OUTPUT PARAMETER TABLE FOR t-gc-piacct.

FOR EACH gc-piacct NO-LOCK 
    BY gc-piacct.activeflag BY gc-piacct.nr:
    CREATE t-gc-piacct.
    BUFFER-COPY gc-piacct TO t-gc-piacct.
END.
