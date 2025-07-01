DEFINE TEMP-TABLE rsl 
    FIELD resnr       AS INTEGER 
    FIELD reslinnr    AS INTEGER 
    FIELD resstatus   AS INTEGER 
    FIELD sdate       AS DATE COLUMN-LABEL "Beg-Date" FONT 2 
    FIELD ndate       AS DATE COLUMN-LABEL "End-Date" FONT 2 
    FIELD stime       LIKE bk-reser.von-zeit COLUMN-LABEL "Start" FONT 2 
    FIELD ntime       LIKE bk-reser.bis-zeit COLUMN-LABEL " End" FONT 2
    FIELD created-date AS DATE COLUMN-LABEL "Created" FONT 2
    FIELD venue       LIKE bk-raum.raum COLUMN-LABEL "Venue" FONT 2
    FIELD userinit    AS CHAR FORMAT "x(4)" COLUMN-LABEL "ID" FONT 2
. 

DEF INPUT  PARAMETER rml-raum   LIKE bk-rset.raum.
DEF INPUT  PARAMETER t-resnr    AS INT.
DEF INPUT  PARAMETER t-reslinnr AS INT.
DEF OUTPUT PARAMETER info1      AS CHAR.
DEF OUTPUT PARAMETER info2      AS CHAR.
DEF OUTPUT PARAMETER info3      AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR rsl.

DEFINE BUFFER mainres   FOR bk-veran.
DEFINE BUFFER resline   FOR bk-reser.
DEFINE BUFFER gast      FOR guest.
DEFINE BUFFER bbuff     FOR bediener.

DEFINE VARIABLE stat AS CHAR FORMAT "x(10)" 
    EXTENT 9 INITIAL ["Fix", "Tentative", /*"Cancel"*/ "", "WaitingList", "", "", "", "Actual", "Cancel"]. 

FOR EACH bk-rset WHERE bk-rset.raum = rml-raum NO-LOCK, 
    FIRST bk-setup WHERE bk-setup.setup-id = bk-rset.setup-id NO-LOCK: 
    info1 = info1 + bk-setup.bezeich + ":  Sz: " 
        + STRING(bk-rset.groesse) + "  Cp: " 
        + STRING(bk-rset.personen) + "  P:" 
        + STRING(bk-rset.preis,">>>,>>>,>>9.99") + chr(10). 
END. 
FIND FIRST mainres WHERE mainres.veran-nr = t-resnr NO-LOCK NO-ERROR.
IF AVAILABLE mainres THEN 
DO: 
    FIND FIRST resline WHERE resline.veran-nr = mainres.veran-nr 
        AND resline.veran-resnr = t-reslinnr NO-LOCK.
    FIND FIRST gast WHERE gast.gastnr = mainres.gastnr NO-LOCK.
    FIND FIRST bk-func WHERE bk-func.veran-nr = t-resnr 
        AND bk-func.veran-seite = t-reslinnr NO-LOCK.
    info3 = gast.name + " " + gast.vorname1 + ", " 
        + gast.anrede1 + gast.anredefirma + chr(10) 
        + "RefNo: " + STRING(resline.veran-nr) + "-" + STRING(resline.veran-resnr) 
        + "  Status: " + stat[resline.resstatus] 
        + "  InvNo: " + STRING(mainres.rechnr) + chr(10) 
        + "Date: " + STRING(resline.datum) + " - " + STRING(resline.bis-datum) 
        + "  Time: " + STRING(resline.von-zeit,"99:99") + " - " 
        + STRING(resline.bis-zeit,"99:99") + chr(10)
        + "Weekday: " + STRING(bk-func.wochentag)
        + " Total Pax: " + STRING(bk-func.rpersonen[1]).
    IF bk-func.raumbezeichnung[8] NE "" THEN
        info3 = info3 + chr(10) + "Event: " + STRING(bk-func.raumbezeichnung[8]).
END. 
FOR EACH resline WHERE resline.veran-nr = mainres.veran-nr 
    AND (resline.resstatus LE 4 OR resline.resstatus EQ 8) NO-LOCK: 
    FIND FIRST bbuff WHERE bbuff.nr = resline.bediener-nr NO-LOCK NO-ERROR.
    CREATE rsl. 
    ASSIGN 
        rsl.resnr = resline.veran-nr 
        rsl.reslinnr = resline.veran-resnr 
        rsl.resstatus = resline.resstatus 
        rsl.sdate = resline.datum 
        rsl.ndate = resline.bis-datum 
        rsl.stime = resline.von-zeit 
        rsl.ntime = resline.bis-zeit 
        rsl.venue = resline.raum
        rsl.created-date = mainres.kontaktfirst. 
    IF AVAILABLE bbuff THEN ASSIGN rsl.userinit = bbuff.userinit.
END. 
