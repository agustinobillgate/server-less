DEF TEMP-TABLE t-res-line
    FIELD rec-id      AS INTEGER
    FIELD ziwech-zeit LIKE res-line.ziwech-zeit.

DEFINE INPUT PARAMETER i AS INTEGER.
DEFINE INPUT PARAMETER curr-date AS DATE.
DEFINE INPUT PARAMETER zinr AS CHAR.
DEFINE INPUT PARAMETER gstatus AS INTEGER.
DEFINE INPUT PARAMETER recid1 AS INTEGER.

DEFINE OUTPUT PARAMETER n-edit AS CHARACTER.
DEFINE OUTPUT PARAMETER c-edit AS CHARACTER.

DEF VAR fgcol-n AS INT.
DEF VAR fgcol-c AS INT.

IF (i GT 17) OR (i LT 0) THEN 
DO: 
    n-edit = "". 
    c-edit = "".
END.
ELSE
DO: 
    IF i = 0 THEN
        RUN hk-roomplan-disp-resdatabl.p (i, curr-date, zinr, ?, ?, OUTPUT n-edit, 
                                          OUTPUT c-edit, OUTPUT fgcol-n, 
                                          OUTPUT fgcol-c,OUTPUT TABLE t-res-line).
    ELSE
        RUN hk-roomplan-disp-resdatabl.p (i, curr-date, zinr, gstatus,recid1, 
                                          OUTPUT n-edit, OUTPUT c-edit, 
                                          OUTPUT fgcol-n, OUTPUT fgcol-c, 
                                          OUTPUT TABLE t-res-line).
END.



