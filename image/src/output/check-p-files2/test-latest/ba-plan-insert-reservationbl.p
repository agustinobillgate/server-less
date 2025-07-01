DEFINE INPUT PARAMETER rml-resnr AS INT. 

DEFINE OUTPUT PARAMETER mess-result      AS CHAR.
DEFINE OUTPUT PARAMETER insert-flag      AS LOGICAL.  
DEFINE OUTPUT PARAMETER main-exist       AS LOGICAL.
DEFINE OUTPUT PARAMETER curr-resnr       AS INT.
DEFINE OUTPUT PARAMETER reslinnr         AS INT.
DEFINE OUTPUT PARAMETER guest-gastnr     AS INT.
DEFINE OUTPUT PARAMETER recid-guest      AS INT.
DEFINE OUTPUT PARAMETER guest-full-name  AS CHAR.

DEF VAR mainres-gastnr   AS INT.
DEF VAR mainres-veran-nr AS INT.
DEF VAR mainres-resnr    AS INT.
DEF VAR avail-mainres    AS LOGICAL INIT NO.
DEF VAR avail-guest      AS LOGICAL INIT NO.
DEF VAR gast-karteityp   AS INT.

RUN ba-plan-read-mainresbl.p (rml-resnr, OUTPUT mainres-gastnr,
                            OUTPUT mainres-veran-nr, OUTPUT mainres-resnr,
                            OUTPUT gast-karteityp, OUTPUT avail-mainres).

IF avail-mainres THEN 
DO: 
    RUN ba-plan-get-guestbl.p (mainres-gastnr, OUTPUT avail-guest,OUTPUT guest-gastnr, 
                               OUTPUT recid-guest, OUTPUT guest-full-name).

    insert-flag = YES. 
    main-exist  = YES. 
    curr-resnr  = mainres-veran-nr. 
    reslinnr    = mainres-resnr. 

    mess-result = "Get Main Reservation Success".
END. 
ELSE
DO:
    mess-result = "Get Main Reservation Failed".
END.
