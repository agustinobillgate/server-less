
DEFINE TEMP-TABLE t-kartentext
    FIELD kartentext AS CHAR
    FIELD curr-i     AS INT.

DEFINE TEMP-TABLE t-sonstiges
    FIELD sonstiges  AS CHAR
    FIELD curr-i     AS INT.

DEF INPUT PARAMETER TABLE FOR t-kartentext.
DEF INPUT PARAMETER TABLE FOR t-sonstiges.
DEF INPUT PARAMETER resnr AS INT.
DEF INPUT PARAMETER resline AS INT.

DEF VAR kartentext AS CHAR EXTENT 8.
DEF VAR sonstiges  AS CHAR EXTENT 4.

FOR EACH t-kartentext NO-LOCK:
    ASSIGN kartentext[t-kartentext.curr-i] = t-kartentext.kartentext.
END.

FOR EACH t-sonstiges NO-LOCK:
    ASSIGN sonstiges[t-sonstiges.curr-i] = t-sonstiges.sonstiges.
END.

FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
    AND bk-func.veran-seite = resline NO-LOCK NO-ERROR. 
FIND CURRENT bk-func EXCLUSIVE-LOCK.
ASSIGN
    bk-func.kartentext[1] = kartentext[1]
    bk-func.kartentext[2] = kartentext[2] 
    bk-func.kartentext[3] = kartentext[3] 
    bk-func.kartentext[4] = kartentext[4] 
    bk-func.kartentext[5] = kartentext[5]
    bk-func.kartentext[6] = kartentext[6]
    bk-func.kartentext[7] = kartentext[7]
    bk-func.kartentext[8] = kartentext[8]
    bk-func.sonstiges[1]  = sonstiges[1]
    bk-func.sonstiges[2]  = sonstiges[2]
    bk-func.sonstiges[3]  = sonstiges[3]
    bk-func.sonstiges[4]  = sonstiges[4]
    . 
FIND CURRENT bk-func NO-LOCK.
