  
DEF TEMP-TABLE segment1  
    FIELD bezeich LIKE segment.bezeich.  
  
DEF TEMP-TABLE sourccod1  
    FIELD source-code LIKE sourccod.source-code  
    FIELD bezeich LIKE sourccod.bezeich.  
  
DEF TEMP-TABLE sourccod-chg  
    FIELD source-code LIKE sourccod.source-code  
    FIELD bezeich LIKE sourccod.bezeich.  
  
DEF TEMP-TABLE t-guest LIKE guest.  
  
DEF TEMP-TABLE q1-akt-kont  
    FIELD NAME LIKE akt-kont.NAME  
    FIELD vorname LIKE akt-kont.vorname  
    FIELD anrede LIKE akt-kont.anrede  
    FIELD hauptkontakt LIKE akt-kont.hauptkontakt.  
DEF TEMP-TABLE q2-history  
    FIELD ankunft LIKE history.ankunft  
    FIELD abreise LIKE history.abreise  
    FIELD zinr LIKE history.zinr  
    FIELD zipreis LIKE history.zipreis  
    FIELD bemerk LIKE history.bemerk  
    FIELD arrangement LIKE history.arrangement.  
  
DEF INPUT  PARAMETER gastnr AS INT.  
DEF INPUT  PARAMETER chg-gcf AS LOGICAL.  
  
DEF OUTPUT PARAMETER record-use         AS LOGICAL INIT NO.  
DEF OUTPUT PARAMETER init-time          AS INT.  
DEF OUTPUT PARAMETER init-date          AS DATE.  
DEF OUTPUT PARAMETER avail-mcguest      AS LOGICAL.  
DEF OUTPUT PARAMETER lname              AS CHAR.  
DEF OUTPUT PARAMETER land               AS CHAR.  
DEF OUTPUT PARAMETER payment            AS INT.  
DEF OUTPUT PARAMETER pay-bezeich        AS CHAR.  
DEF OUTPUT PARAMETER master-gastnr      AS INT.  
DEF OUTPUT PARAMETER mastername         AS CHAR.  
DEF OUTPUT PARAMETER ref-nr1            AS INT.  
DEF OUTPUT PARAMETER ref-nr2            AS INT.  
DEF OUTPUT PARAMETER sales-id           AS CHAR.  
DEF OUTPUT PARAMETER sales-name         AS CHAR.  
DEF OUTPUT PARAMETER avail-gentable     AS LOGICAL.  
DEF OUTPUT PARAMETER avail-genlayout    AS LOGICAL.  
DEF OUTPUT PARAMETER avail-guestseg     AS LOGICAL INIT NO.  
DEF OUTPUT PARAMETER mc-license         AS LOGICAL.  
DEF OUTPUT PARAMETER maincontact        AS CHAR.  
DEF OUTPUT PARAMETER mainsegm           AS CHAR.  
DEF OUTPUT PARAMETER comments           AS CHAR.  
DEF OUTPUT PARAMETER email-adr          AS CHAR.  
DEF OUTPUT PARAMETER curr-source        AS CHAR.  
DEF OUTPUT PARAMETER pricecode          AS CHAR.  
DEF OUTPUT PARAMETER ena-btn-gcfinfo    AS LOGICAL.  
DEF OUTPUT PARAMETER f-int              AS INTEGER.  
  
DEF OUTPUT PARAMETER TABLE FOR segment1.  
DEF OUTPUT PARAMETER TABLE FOR t-guest.  
DEF OUTPUT PARAMETER TABLE FOR sourccod1.  
DEF OUTPUT PARAMETER TABLE FOR q1-akt-kont.  
DEF OUTPUT PARAMETER TABLE FOR q2-history.  
DEF OUTPUT PARAMETER TABLE FOR sourccod-chg.  
  
DEFINE buffer guest0 FOR guest.  
DEFINE buffer usr FOR bediener.  
DEF VAR flag-ok AS LOGICAL.  
  
IF chg-gcf THEN   
DO:  
    RUN check-timebl.p(1, gastnr, ?, "guest", ?, ?, OUTPUT flag-ok,  
                       OUTPUT init-time, OUTPUT init-date).  
    IF NOT flag-ok THEN  
    DO:  
        record-use = YES.  
        RETURN NO-APPLY.  
    END.  
END.  
/*MTIF chg-gcf THEN FIND FIRST guest WHERE guest.gastnr = gastnr  
    EXCLUSIVE-LOCK.   
ELSE FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. */  
FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.  
CREATE t-guest.  
BUFFER-COPY guest TO t-guest.  
  
FIND FIRST mc-guest WHERE mc-guest.gastnr = gastnr AND mc-guest.activeflag = YES  
    NO-LOCK NO-ERROR.  
IF AVAILABLE mc-guest THEN avail-mcguest = YES.  
  
lname = guest.name.   
land = guest.land.   
payment = guest.zahlungsart.   
IF payment NE 0 THEN   
DO:   
  FIND FIRST artikel WHERE artikel.departement = 0   
    AND artikel.artnr = payment NO-LOCK NO-ERROR.   
  IF AVAILABLE artikel THEN pay-bezeich = artikel.bezeich.   
END.   
  
master-gastnr = guest.master-gastnr.   
IF master-gastnr NE 0 THEN   
DO:   
  FIND FIRST guest0 WHERE guest0.gastnr = master-gastnr NO-LOCK NO-ERROR.   
  IF AVAILABLE guest0 THEN mastername = guest0.name + ", " + guest0.vorname1   
     + guest0.anredefirma + " " + guest0.anrede1.   
  ELSE master-gastnr = 0.   
END.   
  
ref-nr1 = guest.firmen-nr.   
IF ref-nr1 = ? THEN ref-nr1 = 0.   
ref-nr2 = guest.point-gastnr.   
  
  
sales-id = guest.phonetik3.   
IF sales-id NE "" THEN   
DO:   
  FIND FIRST usr WHERE usr.userinit = sales-id NO-LOCK NO-ERROR.   
  IF AVAILABLE usr THEN sales-name = usr.username.   
END.   
  
  
FIND FIRST gentable WHERE gentable.KEY = "Guest Card"  
  AND gentable.number1 = gastnr NO-LOCK NO-ERROR.  
IF AVAILABLE gentable THEN avail-gentable = YES.  
  
FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK.   
mc-license = htparam.flogical.  
  
FIND FIRST akt-kont WHERE akt-kont.gastnr = gastnr   
  AND akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR.   
IF AVAILABLE akt-kont THEN maincontact = akt-kont.name + ", "   
                   + akt-kont.vorname + " " + akt-kont.anrede.  
  
  
FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr:   
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode   
        NO-LOCK NO-ERROR.  
    IF AVAILABLE segment THEN  
    DO:  
        CREATE segment1.  
        ASSIGN segment1.bezeich = segment.bezeich.  
        /*MTIF AVAILABLE segment THEN guestsegm:ADD-LAST(ENTRY(1, segment.bezeich, "$$0")). */  
    END.  
END.   
  
  
FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr AND   
     guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.   
IF AVAILABLE guestseg THEN   
DO:   
  FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode   
    NO-LOCK NO-ERROR.   
  IF AVAILABLE segment THEN mainsegm = ENTRY(1, segment.bezeich, "$$0").   
END.   

ASSIGN
  comments  = guest.bemerkung  
  email-adr = guest.email-adr
.  
FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.  /* Indiv GastNo */
comments = comments + CHR(2) + STRING(htparam.finteger).
FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK.  /* WIG GastNo */
comments = comments + CHR(2) + STRING(htparam.finteger).
  
FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-ERROR.   
IF AVAILABLE guest-pr THEN   
DO:   
  FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = guest-pr.code   
       NO-ERROR.   
  IF AVAILABLE queasy THEN   
  DO:   
    pricecode = guest-pr.code + "  " + queasy.char2.  
  END.   
END.   
   
IF guest.segment3 NE 0 THEN  
DO:  
  FIND FIRST sourccod WHERE sourccod.source-code = guest.segment3  
    NO-LOCK NO-ERROR.   
  IF AVAILABLE sourccod THEN   
  DO:  
      curr-source = STRING(sourccod.source-code) + " " + sourccod.bezeich.  
    /*MTcurr-source:ADD-FIRST(STRING(sourccod.source-code) + " " + sourccod.bezeich).  
    ASSIGN curr-source:SCREEN-VALUE IN FRAME frame1 =   
      STRING(sourccod.source-code) + " " + sourccod.bezeich.*/  
  END.  
END.  
/*MTELSE curr-source:ADD-FIRST("").*/  
  
IF chg-gcf THEN  
FOR EACH sourccod WHERE sourccod.source-code NE guest.segment3  
  NO-LOCK BY sourccod.source-cod:  
    CREATE sourccod1.  
    ASSIGN  
        sourccod1.source-code = sourccod.source-code  
        sourccod1.bezeich = sourccod.bezeich.  
  /*MTcurr-source:ADD-LAST(STRING(sourccod.source-code) + " " + sourccod.bezeich)   
    IN FRAME frame1.*/  
END.  
  
  
  
  
FIND FIRST htparam WHERE paramnr = 975 no-lock.   /* VHP Front multi user */   
IF htparam.finteger NE 1 THEN ena-btn-gcfinfo = YES.  
    /*MTENABLE btn-gcfinfo btn-history WITH FRAME frame1*/ .  
  
FOR EACH akt-kont WHERE akt-kont.gastnr = gastnr  
    NO-LOCK BY akt-kont.hauptkontakt DESCENDING BY akt-kont.NAME:  
    CREATE q1-akt-kont.  
    ASSIGN  
      q1-akt-kont.NAME = akt-kont.NAME  
      q1-akt-kont.vorname = akt-kont.vorname  
      q1-akt-kont.anrede = akt-kont.anrede  
      q1-akt-kont.hauptkontakt = akt-kont.hauptkontakt.  
END.  
  
FOR EACH history WHERE history.gastnr = gastnr  
    NO-LOCK BY history.ankunft DESCENDING:  
    CREATE q2-history.  
    ASSIGN  
    q2-history.ankunft = history.ankunft  
    q2-history.abreise = history.abreise  
    q2-history.zinr = history.zinr  
    q2-history.zipreis = history.zipreis  
    q2-history.bemerk = history.bemerk  
    q2-history.arrangement = history.arrangement.  
END.  
  
/*MT  
OPEN QUERY q1 FOR EACH akt-kont WHERE akt-kont.gastnr = gastnr  
  NO-LOCK BY akt-kont.hauptkontakt DESCENDING BY akt-kont.NAME.   
  
OPEN QUERY q2 FOR EACH history WHERE history.gastnr = gastnr  
  NO-LOCK BY history.ankunft DESCENDING.*/  
  
  
/*waktu btn-chg*/  
FOR EACH sourccod WHERE sourccod.betriebsnr = 0  
    AND sourccod.source-code NE t-guest.segment3  
    NO-LOCK BY sourccod.source-cod:  
    CREATE sourccod-chg.  
    ASSIGN  
        sourccod-chg.source-code = sourccod.source-code  
        sourccod-chg.bezeich = sourccod.bezeich.  
END.  
  
FIND FIRST htparam WHERE paramnr = 975 no-lock.   /* VHP Front multi user */   
f-int = htparam.finteger.  
  
/*of btn-stop*/  
FIND FIRST guestseg WHERE guestseg.gastnr = gastnr NO-LOCK NO-ERROR.  
IF AVAILABLE guestseg THEN avail-guestseg = YES.  
  
/*PROCEDURE gcf-gentable*/  
FIND FIRST genlayout WHERE genlayout.KEY = "Guest Card" NO-LOCK NO-ERROR.  
IF AVAILABLE genlayout THEN avail-genlayout = YES.  
