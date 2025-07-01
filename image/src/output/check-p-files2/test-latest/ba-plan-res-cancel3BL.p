
DEF INPUT-OUTPUT PARAMETER b1-resnr     AS INT.
DEF INPUT-OUTPUT PARAMETER b1-reslinnr  AS INT.
DEF INPUT  PARAMETER t-veran-nr     AS INT.
DEF INPUT  PARAMETER t-veran-resnr  AS INT.
DEF INPUT  PARAMETER t-datum        AS DATE.
DEF INPUT  PARAMETER t-raum         AS CHAR.
DEF INPUT  PARAMETER cancel-str     AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER curr-resnr     AS INT.

DEFINE BUFFER mainres    FOR bk-veran. 

FIND FIRST mainres WHERE mainres.veran-nr = t-veran-nr 
    NO-LOCK NO-ERROR. 

/** %%% NO-LOCK changed TO EXCLUSIVE-LOCK **/ 
FIND FIRST b-storno WHERE b-storno.bankettnr = t-veran-nr 
    AND b-storno.breslinnr = t-veran-resnr 
    EXCLUSIVE-LOCK NO-ERROR. 
IF NOT AVAILABLE b-storno THEN 
DO: 
    CREATE b-storno. 
    b-storno.bankettnr = t-veran-nr. 
    b-storno.breslinnr = t-veran-resnr. 
    b-storno.gastnr = mainres.gastnr. 
    b-storno.betrieb-gast = mainres.gastnrver. 
    b-storno.datum = t-datum. 
END. 
b-storno.grund[18] = CAPS(cancel-str) + " D*" 
+ STRING(TODAY,"99/99/99") + " " + STRING(TIME,"hh:mm:ss") 
+ " " + t-raum. 
b-storno.usercode = user-init. 
curr-resnr = 0. 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
CREATE res-history. 
ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.aenderung = "Cancel Banquet No: " + STRING(t-veran-nr) + " Venue: " + t-raum + " Reason: " + cancel-str
    res-history.action = "Banquet". 
FIND CURRENT res-history NO-LOCK. 
RELEASE res-history.

RUN ba-cancreslinebl.p(t-veran-nr,t-veran-resnr). 

FIND FIRST mainres WHERE mainres.veran-nr = b1-resnr 
    NO-LOCK NO-ERROR. 
IF NOT AVAILABLE mainres THEN 
DO: 
    b1-resnr = 0. 
    b1-reslinnr = 0. 
END.

