DEFINE INPUT PARAMETER rml-raum     AS CHAR.
DEFINE INPUT PARAMETER rml-nr       AS INT.
DEFINE INPUT PARAMETER rml-resnr    AS INT.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE OUTPUT PARAMETER mess-str AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER remark AS CHAR.

DEFINE VARIABLE curr-room     AS CHAR.
DEFINE VARIABLE curr-status   AS INT.
DEFINE VARIABLE t-veran-nr    AS INT.
DEFINE VARIABLE avail-mainres AS LOGICAL INIT NO.

curr-room   = rml-raum. 
curr-status = rml-nr. 

IF case-type EQ 1 THEN /*LOAD*/
DO:
    RUN ba-plan-btn-notebl.p (rml-resnr, OUTPUT t-veran-nr,OUTPUT avail-mainres).

    IF avail-mainres THEN RUN edit-baresnotebl.p (rml-resnr, OUTPUT remark).
    ELSE 
    DO :
        mess-str = "Main Reservation Unavailable!".
        RETURN.
    END.
END.
ELSE IF case-type EQ 2 THEN /*ADD, UPDATE, DELETE*/
DO:
    RUN update-baresnotebl.p (rml-resnr, remark).
END.

