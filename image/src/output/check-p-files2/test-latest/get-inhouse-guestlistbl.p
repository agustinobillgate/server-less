
DEFINE TEMP-TABLE guest-list
    FIELD resnr             AS INT
    FIELD reslinnr          AS INT
    FIELD roomnumber        AS CHAR
    FIELD checkindate       AS DATE
    FIELD checkoutdate      AS DATE
    FIELD guest-nr          AS INT
    FIELD guest-lastname    LIKE guest.NAME
    FIELD guest-firstname   LIKE guest.vorname1
    FIELD guest-title       LIKE guest.anrede1
    FIELD guest-nation      LIKE nation.bezeich
    FIELD guest-country     LIKE nation.bezeich
    FIELD guest-region      LIKE nation.bezeich
    FIELD guest-mobile      LIKE guest.mobil-telefon
    FIELD guest-email       LIKE guest.email
    FIELD guest-bemerk      LIKE guest.bemerk
    FIELD guest-birthday    AS DATE
    FIELD recid-resline     AS INTEGER
    FIELD wifi-password     AS CHAR
    .

DEFINE OUTPUT PARAMETER TABLE FOR guest-list.

DEFINE VARIABLE i         AS INTEGER NO-UNDO.
DEFINE VARIABLE i-counter AS INTEGER NO-UNDO.
DEFINE VARIABLE str       AS CHAR    NO-UNDO.
DEFINE VARIABLE ci-date   AS DATE NO-UNDO.

DEFINE VARIABLE active-flag AS INTEGER INIT 1 NO-UNDO.

RUN htpdate.p(87, OUTPUT ci-date).

FOR EACH res-line WHERE res-line.active-flag = active-flag
    AND res-line.l-zuordnung[3] = 0 
    AND (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13) NO-LOCK:
    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.

    CREATE guest-list.
    ASSIGN 
    guest-list.resnr           = res-line.resnr 
    guest-list.reslinnr        = res-line.reslinnr 
    guest-list.roomnumber      = res-line.zinr 
    guest-list.checkindate     = res-line.ankunft 
    guest-list.checkoutdate    = res-line.abreise 
    guest-list.guest-nr        = guest.gastnr 
    guest-list.guest-lastname  = guest.NAME 
    guest-list.guest-firstname = guest.vorname1 
    guest-list.guest-title     = guest.anrede1  
    guest-list.guest-mobile    = guest.mobil-telefon 
    guest-list.guest-email     = guest.email  
    guest-list.guest-bemerk    = guest.bemerk  
    guest-list.guest-birthday  = guest.geburtdatum1 
    guest-list.recid-resline   = RECID(res-line). 

    FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR. 
    IF AVAILABLE nation  THEN guest-list.guest-nation  = ENTRY(1,nation.bezeich,";").
    
    FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR. 
    IF AVAILABLE nation  THEN guest-list.guest-country = ENTRY(1,nation.bezeich,";").
    
    FIND FIRST nation WHERE nation.kurzbez = guest.nation2 NO-LOCK NO-ERROR. /*IT*/
    IF AVAILABLE nation  THEN guest-list.guest-region  = ENTRY(1,nation.bezeich,";").
END.


