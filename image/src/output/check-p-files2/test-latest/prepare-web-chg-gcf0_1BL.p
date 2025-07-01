DEF TEMP-TABLE t-nation1
    FIELD kurzbez LIKE nation.kurzbez.
DEF TEMP-TABLE t-nation2 LIKE t-nation1.
DEF TEMP-TABLE t-nation3 LIKE t-nation1.
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
    FIELD kurzbez AS CHAR
    FIELD bemerk LIKE history.bemerk
    FIELD arrangement LIKE history.arrangement.

DEF TEMP-TABLE t-segment1
    FIELD bezeich AS CHAR.

DEF TEMP-TABLE t-guest LIKE guest.

DEFINE TEMP-TABLE forecast /* RT - 11 JUN 2018 */
    FIELD ankunft AS DATE
    FIELD abreise AS DATE
    FIELD zinr AS CHAR
    FIELD kurzbez AS CHAR
    FIELD arrangement AS CHAR
    FIELD zipreis AS DECIMAL.

DEFINE TEMP-TABLE t-guestbook NO-UNDO LIKE vhp.guestbook.

DEF INPUT PARAMETER gastnr AS INT.
DEF INPUT PARAMETER  chg-gcf AS LOGICAL.
DEF INPUT-OUTPUT PARAMETER master-gastnr AS INT.

DEF OUTPUT PARAMETER read-birthdate AS LOGICAL.
DEF OUTPUT PARAMETER def-natcode AS CHAR.
DEF OUTPUT PARAMETER avail-mc-guest AS LOGICAL.
DEF OUTPUT PARAMETER avail-gentable AS LOGICAL.
DEF OUTPUT PARAMETER mc-license AS LOGICAL.
DEF OUTPUT PARAMETER pay-bezeich AS CHAR.
DEF OUTPUT PARAMETER payment AS INT.
DEF OUTPUT PARAMETER mainsegm AS CHAR.
DEF OUTPUT PARAMETER mastername AS CHAR.
DEF OUTPUT PARAMETER fname-flag AS LOGICAL.
DEF OUTPUT PARAMETER f-int AS INT.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL.
DEF OUTPUT PARAMETER record-use AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER init-time AS INT.
DEF OUTPUT PARAMETER init-date AS DATE.
DEF OUTPUT PARAMETER avail-genlayout AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER l-param472 AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER logic-param1109 AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER base64ImageFile AS LONGCHAR NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-segment1.
DEF OUTPUT PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER TABLE FOR t-nation1.
DEF OUTPUT PARAMETER TABLE FOR t-nation2.
DEF OUTPUT PARAMETER TABLE FOR t-nation3.
DEF OUTPUT PARAMETER TABLE FOR q2-history.
DEF OUTPUT PARAMETER TABLE FOR q1-akt-kont.
DEF OUTPUT PARAMETER TABLE FOR forecast. 
DEF OUTPUT PARAMETER TABLE FOR t-guestbook.

DEFINE BUFFER guest0 FOR guest.
DEFINE VAR flag-ok AS LOGICAL.
DEFINE VAR pointer AS MEMPTR.

DEFINE VARIABLE ci-date AS DATE INIT TODAY NO-UNDO. 

FIND FIRST genlayout WHERE genlayout.KEY = "Guest Card" NO-LOCK NO-ERROR.
IF AVAILABLE genlayout THEN avail-genlayout = YES.

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
/*MTIF chg-gcf THEN FIND FIRST guest WHERE guest.gastnr = gastnr.
ELSE FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.*/
FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
ASSIGN master-gastnr = guest.master-gastnr.

CREATE t-guest.
BUFFER-COPY guest TO t-guest.

FIND FIRST guestbook WHERE guestbook.gastnr EQ gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guestbook THEN 
DO:
    CREATE t-guestbook.
    BUFFER-COPY guestbook TO t-guestbook.
    COPY-LOB guestbook.imagefile TO pointer.
    base64ImageFile = BASE64-ENCODE(pointer).
END.

FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK. 
IF htparam.paramgr = 99 AND htparam.feldtyp = 4 THEN
ASSIGN l-param472 = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 1109 NO-LOCK.
logic-param1109 = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 937 NO-LOCK.
read-birthdate = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK.
FIND FIRST nation WHERE nation.kurzbez = htparam.fchar NO-LOCK NO-ERROR.
IF NOT AVAILABLE nation THEN 
DO:
  /*MTCURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").
  HIDE MESSAGE NO-PAUSE.
  MESSAGE translateExtended ("Default Country Code not defined (Param 153 / Grp 7).",lvCAREA,"") 
    VIEW-AS ALERT-BOX INFORMATION.*/
  RETURN.
END.
def-natcode = nation.kurzbez.

FIND FIRST mc-guest WHERE mc-guest.gastnr = gastnr AND mc-guest.activeflag = YES
    NO-LOCK NO-ERROR.
IF AVAILABLE mc-guest THEN avail-mc-guest = YES.

FIND FIRST gentable WHERE gentable.KEY = "Guest Card"
  AND gentable.number1 = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE gentable THEN avail-gentable = YES.

FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK. 
mc-license = htparam.flogical. 

FIND FIRST queasy WHERE queasy.KEY = 27 NO-LOCK NO-ERROR.
avail-queasy = AVAILABLE queasy.

payment = guest.zahlungsart. 
IF payment NE 0 THEN 
DO: 
  FIND FIRST artikel WHERE artikel.departement = 0 
    AND artikel.artnr = payment NO-LOCK NO-ERROR. 
  IF AVAILABLE artikel THEN pay-bezeich = artikel.bezeich. 
END.

FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr NO-LOCK: 
  FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE segment THEN 
  DO:
      CREATE t-segment1.
      ASSIGN t-segment1.bezeich = segment.bezeich.
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

IF master-gastnr NE 0 THEN 
DO: 
  FIND FIRST guest0 WHERE guest0.gastnr = master-gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE guest0 THEN mastername = guest0.name + ", " 
     + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1. 
  ELSE master-gastnr = 0.
END. 

FIND FIRST htparam WHERE htparam.paramnr = 939 NO-LOCK.
fname-flag = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 975 NO-LOCK.   /* VHP Front multi user */ 
f-int = htparam.finteger.
FOR EACH history NO-LOCK WHERE history.gastnr = gastnr:
  CREATE q2-history.
  BUFFER-COPY history TO q2-history.
  FIND FIRST zimmer WHERE zimmer.zinr = history.zinr NO-LOCK NO-ERROR.
  IF AVAILABLE zimmer THEN
  DO:
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN ASSIGN q2-history.kurzbez = zimkateg.kurzbez.
  END.
END.

FOR EACH akt-kont WHERE akt-kont.gastnr = gastnr
    NO-LOCK BY akt-kont.hauptkontakt DESCENDING BY akt-kont.NAME:
    CREATE q1-akt-kont.
    BUFFER-COPY akt-kont TO q1-akt-kont.
    /*MTFIELD NAME LIKE akt-kont.NAME
    FIELD vorname LIKE akt-kont.vorname
    FIELD anrede LIKE akt-kont.anrede
    FIELD hauptkontakt LIKE akt-kont.hauptkontakt.*/
END.

FOR EACH nation WHERE nation.natcode = 0:
    CREATE t-nation1.
    ASSIGN t-nation1.kurzbez = nation.kurzbez.
END.
FOR EACH nation WHERE nation.natcode > 0:
    CREATE t-nation2.
    ASSIGN t-nation2.kurzbez = nation.kurzbez.
END.
FOR EACH nation:
    CREATE t-nation3.
    ASSIGN t-nation3.kurzbez = nation.kurzbez.
END.

/* FORECAST REQ CHANTI SEMARANG : RT - 11 JUN 2018 */
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    ci-date = htparam.fdate.
END.    

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
DO:
    FOR EACH res-line WHERE res-line.gastnrmember = guest.gastnr AND
        ((res-line.ankunft GE ci-date AND res-line.resstatus LE 5) OR res-line.resstatus EQ 6 OR
         res-line.resstatus EQ 11 OR res-line.resstatus EQ 13) NO-LOCK:
            CREATE forecast.
            BUFFER-COPY res-line TO forecast.
            
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
            IF AVAILABLE zimmer THEN
            DO:
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
                IF AVAILABLE zimkateg THEN
                DO:
                    ASSIGN forecast.kurzbez = zimkateg.kurzbez.
                END.
            END.
    END.
END.
