DEF TEMP-TABLE aktkont-list LIKE akt-kont
    FIELD nat   AS CHAR LABEL "Nat" FORMAT "x(3)"
    FIELD email AS CHAR LABEL "Email".
DEF TEMP-TABLE akt-kont1
    FIELD gastnr        LIKE akt-kont.gastnr
    FIELD name          LIKE akt-kont.name
    FIELD vorname       LIKE akt-kont.vorname
    FIELD anrede        LIKE akt-kont.anrede
    FIELD hauptkontakt  LIKE akt-kont.hauptkontakt.
DEFINE TEMP-TABLE t-akt-kont LIKE akt-kont
    FIELD p-bezeich AS CHAR
    FIELD rec-id    AS INTEGER.
DEFINE TEMP-TABLE t-queasy13
    FIELD number1 LIKE queasy.number1
    FIELD char1   LIKE queasy.char1.

DEF INPUT  PARAMETER gastnr       AS INTEGER.

DEF OUTPUT PARAMETER f-title      AS CHAR.
DEF OUTPUT PARAMETER main-kont    AS CHAR.
DEF OUTPUT PARAMETER p-bezeich    AS CHAR.
DEF OUTPUT PARAMETER maincontact  AS CHAR.
DEF OUTPUT PARAMETER fname-flag   AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-akt-kont.
DEF OUTPUT PARAMETER TABLE FOR akt-kont1.
DEF OUTPUT PARAMETER TABLE FOR t-queasy13.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
 
f-title = f-title + guest.name + ", " + guest.vorname1.

FIND FIRST htparam WHERE htparam.paramnr = 939 NO-LOCK.
fname-flag = htparam.flogical.

CREATE aktkont-list. 
 
FIND FIRST akt-kont WHERE akt-kont.gastnr = gastnr 
  AND akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
IF AVAILABLE akt-kont THEN 
DO: 
  main-kont = akt-kont.name + ", " 
     + akt-kont.vorname + " " + akt-kont.anrede. 
  FIND FIRST queasy WHERE queasy.key = 13 AND queasy.number1 = 
    akt-kont.pers-bez NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN p-bezeich = queasy.char1. 
  ELSE p-bezeich = "". 
END. 
maincontact = main-kont. 

FOR EACH akt-kont WHERE akt-kont.gastnr = gastnr NO-LOCK BY akt-kont.name:
    CREATE t-akt-kont.
    BUFFER-COPY akt-kont TO t-akt-kont.
    t-akt-kont.rec-id    = RECID(akt-kont).
    


    FIND FIRST queasy WHERE queasy.key = 13 AND queasy.number1 = 
        akt-kont.pers-bez NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN t-akt-kont.p-bezeich = queasy.char1.
    ELSE t-akt-kont.p-bezeich = "".

    CREATE akt-kont1.
    ASSIGN akt-kont1.hauptkontakt = akt-kont.hauptkontakt.
END.

FOR EACH queasy WHERE queasy.key = 13:
    CREATE t-queasy13.
    ASSIGN
    t-queasy13.number1 = queasy.number1
    t-queasy13.char1   = queasy.char1.
END.
/*MT
IF AVAILABLE akt-kont THEN 
DO: 
  selected = YES. 
  RUN fill-aktkont-list. 
  DISPLAY aktkont-list.name aktkont-list.anrede aktkont-list.vorname 
    aktkont-list.telefon aktkont-list.telefon-privat aktkont-list.fax
    aktkont-list.nat aktkont-list.email aktkont-list.geburtdatum1 aktkont-list.geburt-ort1 
    aktkont-list.ausweis-nr1 aktkont-list.ausweis-art 
    aktkont-list.pass-aust1 aktkont-list.pers-bez p-bezeich 
    aktkont-list.email-adr aktkont-list.briefanrede 
    aktkont-list.v-titel aktkont-list.a-titel aktkont-list.nation2 
    WITH FRAME frame1. 
END. 
  
ENABLE aktkont-list.name aktkont-list.vorname aktkont-list.anrede 
       aktkont-list.telefon aktkont-list.telefon-privat aktkont-list.fax
       aktkont-list.email aktkont-list.geburtdatum1 aktkont-list.nat
       aktkont-list.geburt-ort1 
       aktkont-list.ausweis-nr1 aktkont-list.ausweis-art 
       aktkont-list.pass-aust1 aktkont-list.pers-bez 
       aktkont-list.email-adr aktkont-list.briefanrede 
       aktkont-list.v-titel aktkont-list.a-titel 
       aktkont-list.nation2
    b1 btn-mainkont btn-addname btn-chgname btn-delname 
    btn-exit btn-cancel main-kont WITH FRAME frame1. 
 
ASSIGN
    aktkont-list.NAME:READ-ONLY         = YES
    aktkont-list.vorname:READ-ONLY      = YES 
    aktkont-list.anrede:READ-ONLY       = YES
    aktkont-list.telefon:READ-ONLY      = YES
    aktkont-list.telefon-privat:READ-ONLY = YES
    aktkont-list.email:READ-ONLY = YES 
    aktkont-list.fax:READ-ONLY          = YES
    aktkont-list.geburtdatum1:READ-ONLY = YES 
    aktkont-list.nat:READ-ONLY = YES 
    aktkont-list.geburt-ort1:READ-ONLY  = YES 
    aktkont-list.ausweis-nr1:READ-ONLY  = YES 
    aktkont-list.ausweis-art:READ-ONLY  = YES 
    aktkont-list.pass-aust1:READ-ONLY   = YES 
    aktkont-list.pers-bez:READ-ONLY     = YES 
    aktkont-list.email-adr:READ-ONLY    = YES 
    aktkont-list.briefanrede:READ-ONLY  = YES 
    aktkont-list.v-titel:READ-ONLY      = YES 
    aktkont-list.a-titel:READ-ONLY      = YES 
    aktkont-list.nation2:READ-ONLY      = YES
.
*/
