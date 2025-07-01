
DEF INPUT-OUTPUT PARAMETER b1-resnr     AS INT.
DEF INPUT-OUTPUT PARAMETER b1-reslinnr  AS INT.
DEF INPUT  PARAMETER t-resnr        AS INT.
DEF INPUT  PARAMETER t-reslinnr     AS INT.
DEF INPUT  PARAMETER cancel-str     AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER curr-resnr     AS INT.

DEF OUTPUT PARAMETER datum          AS DATE.
DEF OUTPUT PARAMETER raum           LIKE bk-reser.raum.
DEF OUTPUT PARAMETER von-zeit       LIKE bk-reser.von-zeit.
DEF OUTPUT PARAMETER bis-zeit       LIKE bk-reser.bis-zeit.
DEF OUTPUT PARAMETER resstatus      LIKE bk-reser.resstatus.

DEFINE BUFFER resline    FOR bk-reser.
DEFINE BUFFER mainres    FOR bk-veran.

FIND FIRST resline WHERE resline.veran-nr = t-resnr
    AND resline.veran-resnr = t-reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE resline THEN
DO:
    ASSIGN 
        datum     = resline.datum 
        raum      = resline.raum 
        von-zeit  = resline.von-zeit 
        bis-zeit  = resline.bis-zeit 
        resstatus = resline.resstatus 
        . 

    FIND FIRST mainres WHERE mainres.veran-nr = resline.veran-nr 
        NO-LOCK NO-ERROR. 

/** %%% NO-LOCK changed TO EXCLUSIVE-LOCK **/ 
    FIND FIRST b-storno WHERE b-storno.bankettnr = resline.veran-nr 
    AND b-storno.breslinnr = resline.veran-resnr 
    EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE b-storno THEN 
    DO: 
        CREATE b-storno. 
        b-storno.bankettnr = resline.veran-nr. 
        b-storno.breslinnr = resline.veran-resnr. 
        b-storno.gastnr = mainres.gastnr. 
        b-storno.betrieb-gast = mainres.gastnrver. 
        b-storno.datum = resline.datum. 
    END. 
    b-storno.grund[18] = CAPS(cancel-str) + " D*" 
    + STRING(TODAY,"99/99/99") + " " + STRING(TIME,"hh:mm:ss") 
    + " " + resline.raum. 
    b-storno.usercode = user-init. 
    curr-resnr = 0.

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    CREATE res-history. 
    ASSIGN 
        res-history.nr = bediener.nr 
        res-history.datum = TODAY 
        res-history.zeit = TIME 
        res-history.aenderung = "Cancel Banquet No: " + STRING(resline.veran-nr) + " Venue: " + resline.raum + " Reason: " + cancel-str
        res-history.action = "Banquet". 
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history.

    RUN ba-cancreslinebl.p(resline.veran-nr,resline.veran-resnr). 
    FIND FIRST mainres WHERE mainres.veran-nr = b1-resnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE mainres THEN 
    DO: 
      b1-resnr = 0. 
      b1-reslinnr = 0. 
    END.
END.
