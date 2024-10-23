DEFINE TEMP-TABLE res-listmain
    FIELD resdat       LIKE reservation.resdat 
    FIELD resnr        LIKE reservation.resnr 
    FIELD name         LIKE reservation.name 
    FIELD groupname    LIKE reservation.groupname 
    FIELD depositgef   LIKE reservation.depositgef 
    FIELD limitdate    LIKE reservation.limitdate
    FIELD depositbez   LIKE reservation.depositbez
    FIELD zahldatum    LIKE reservation.zahldatum
    FIELD depositbez2  LIKE reservation.depositbez2
    FIELD zahldatum2   LIKE reservation.zahldatum2
    FIELD useridanlage LIKE reservation.useridanlage 
    FIELD mutdat       LIKE reservation.mutdat
    FIELD useridmutat  LIKE reservation.useridmutat
    FIELD gastnr       LIKE reservation.gastnr
    FIELD bemerk       LIKE reservation.bemerk
    FIELD grpflag      LIKE reservation.grpflag
    FIELD activeflag   LIKE reservation.activeflag

    FIELD resname      AS CHAR
    FIELD address      AS CHAR
    FIELD city         AS CHAR
    .

DEFINE TEMP-TABLE res-listmember
    FIELD name LIKE res-line.name 
    FIELD ankunft     LIKE res-line.ankunft
    FIELD abreise     LIKE res-line.abreise
    FIELD zinr        LIKE res-line.zinr
    FIELD kurzbez     LIKE zimkateg.kurzbez
    FIELD zipreis     LIKE res-line.zipreis
    FIELD arrangement LIKE res-line.arrangement
    FIELD erwachs     LIKE res-line.erwachs
    FIELD gratis      LIKE res-line.gratis
    FIELD zimmeranz   LIKE res-line.zimmeranz
    FIELD anztage     LIKE res-line.anztage
    FIELD changed-id  LIKE res-line.changed-id
    FIELD changed     LIKE res-line.changed
    FIELD gastnr      LIKE res-line.gastnr
    FIELD resstatus   AS INTEGER
    FIELD zikatnr     LIKE res-line.zikatnr
    FIELD resnr       LIKE res-line.resnr
    FIELD bemerk      LIKE res-line.bemerk
    FIELD active-flag LIKE res-line.active-flag
    FIELD l-zuordnung LIKE res-line.l-zuordnung
    FIELD reslinnr    LIKE res-line.reslinnr
    FIELD res-recid   AS INTEGER
    .


DEFINE VARIABLE curr-select         AS CHAR. 
/*DEFINE VARIABLE comments  AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE resname  AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE address  AS CHAR FORMAT "x(30)". 
DEFINE VARIABLE city     AS CHAR FORMAT "x(30)". */


DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER from-date  AS DATE.
DEFINE INPUT PARAMETER to-date  AS DATE.
DEFINE INPUT PARAMETER resnr AS INTEGER.
DEFINE INPUT PARAMETER gastnr AS INTEGER.
DEFINE INPUT PARAMETER search-resno AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR res-listmain.
DEFINE OUTPUT PARAMETER TABLE FOR res-listmember.


/**************** MAIN LOGIC *******************/
FOR EACH res-listmain:
    DELETE res-listmain.
END.
FOR EACH res-listmember:
    DELETE res-listmember.
END.
IF case-type = 1 THEN
DO: 
    RUN update-browse-b2.
    /*itung browse sblah kiri*/
END.
ELSE
DO:
    RUN calc-br1.
    /*itung browse sblah kanan*/
END.


/**************** PROCEDURE *******************/
PROCEDURE calc-br1:
    FOR EACH res-listmain:
        DELETE res-listmain.
    END.
    FOR EACH res-listmember:
        DELETE res-listmember.
    END.
  curr-select = "". 

        FOR EACH res-line WHERE res-line.resnr = resnr 
          AND res-line.resstatus NE 12 /*AND res-line.gastnr = gastnr*/
          AND res-line.resstatus NE 99 NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY res-line.resnr BY res-line.reslinnr 
          BY res-line.zinr BY res-line.ankunft
          /*BY (res-line.kontakt-nr * res-line.resnr) */
          BY res-line.resstatus BY SUBSTR(res-line.NAME,1,32):
            CREATE res-listmember.
            ASSIGN
                res-listmember.name           = res-line.name 
                res-listmember.ankunft        = res-line.ankunft
                res-listmember.abreise        = res-line.abreise
                res-listmember.zinr           = res-line.zinr
                res-listmember.kurzbez        = zimkateg.kurzbez
                res-listmember.zipreis        = res-line.zipreis
                res-listmember.arrangement    = res-line.arrangement
                res-listmember.erwachs        = res-line.erwachs
                res-listmember.gratis         = res-line.gratis
                res-listmember.zimmeranz      = res-line.zimmeranz
                res-listmember.anztage        = res-line.anztage
                res-listmember.changed-id     = res-line.changed-id
                res-listmember.changed        = res-line.changed
                res-listmember.gastnr         = res-line.gastnr
                res-listmember.resstatus      = res-line.resstatus + res-line.l-zuordnung[3]
                res-listmember.zikatnr        = res-line.zikatnr
                res-listmember.resnr          = res-line.resnr
                res-listmember.bemerk         = res-line.bemerk
                res-listmember.active-flag    = res-line.active-flag
                res-listmember.l-zuordnung    = res-line.l-zuordnung
                res-listmember.reslinnr       = res-line.reslinnr
                res-listmember.res-recid      = RECID(res-line).
  END.
END PROCEDURE.

PROCEDURE update-browse-b2: 
    FOR EACH res-listmain:
        DELETE res-listmain.
    END.
    FOR EACH res-listmember:
        DELETE res-listmember.
    END.

    IF search-resno = 0 THEN
    DO:
        curr-select = "". 

        FOR EACH reservation WHERE reservation.resdat GE from-date 
          AND reservation.resdat LE to-date AND reservation.activeflag LE 1 
          NO-LOCK BY reservation.resnr BY reservation.resdat BY SUBSTR(reservation.name,1,32):
          FIND FIRST res-line WHERE res-line.resnr = reservation.resnr
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
            AND res-line.resstatus NE 12 AND res-line.resstatus NE 99 NO-LOCK NO-ERROR.
          IF AVAILABLE res-line THEN
          DO:
            CREATE res-listmain.
            ASSIGN
              res-listmain.resdat       = reservation.resdat 
              res-listmain.resnr        = reservation.resnr 
              res-listmain.name         = reservation.name 
              res-listmain.groupname    = reservation.groupname 
              res-listmain.depositgef   = reservation.depositgef 
              res-listmain.limitdate    = reservation.limitdate
              res-listmain.depositbez   = reservation.depositbez
              res-listmain.zahldatum    = reservation.zahldatum
              res-listmain.depositbez2  = reservation.depositbez2
              res-listmain.zahldatum2   = reservation.zahldatum2
              res-listmain.useridanlage = reservation.useridanlage 
              res-listmain.mutdat       = reservation.mutdat
              res-listmain.useridmutat  = reservation.useridmutat
              res-listmain.gastnr       = reservation.gastnr
              res-listmain.bemerk       = reservation.bemerk
              res-listmain.grpflag      = reservation.grpflag
              res-listmain.activeflag   = reservation.activeflag.

            FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
              ASSIGN
                res-listmain.resname      = guest.name + ", " + guest.vorname1 
                                          + guest.anredefirma + " " + guest.anrede1
                res-listmain.address      = guest.adresse1 + " " + guest.adresse2
                res-listmain.city         = guest.land + " " + guest.wohnort + " " 
                                          + guest.plz.
            END.
          END.
        END.

        FIND FIRST reservation WHERE reservation.resdat GE from-date 
          AND reservation.resdat LE to-date 
          AND reservation.activeflag LE 1 
          NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN 
        DO: 
          curr-select = "mainres". 
        END. 
    END.
    ELSE
    DO:
        curr-select = "". 

        FOR EACH reservation WHERE reservation.resnr EQ search-resno 
          AND reservation.activeflag LE 1 
          NO-LOCK BY reservation.resdat BY SUBSTR(reservation.name,1,32):
          FIND FIRST res-line WHERE res-line.resnr = reservation.resnr
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
            AND res-line.resstatus NE 12 NO-LOCK NO-ERROR.
          IF AVAILABLE res-line THEN
          DO:
            CREATE res-listmain.
            ASSIGN
              res-listmain.resdat       = reservation.resdat 
              res-listmain.resnr        = reservation.resnr 
              res-listmain.name         = reservation.name 
              res-listmain.groupname    = reservation.groupname 
              res-listmain.depositgef   = reservation.depositgef 
              res-listmain.limitdate    = reservation.limitdate
              res-listmain.depositbez   = reservation.depositbez
              res-listmain.zahldatum    = reservation.zahldatum
              res-listmain.depositbez2  = reservation.depositbez2
              res-listmain.zahldatum2   = reservation.zahldatum2
              res-listmain.useridanlage = reservation.useridanlage 
              res-listmain.mutdat       = reservation.mutdat
              res-listmain.useridmutat  = reservation.useridmutat
              res-listmain.gastnr       = reservation.gastnr
              res-listmain.bemerk       = reservation.bemerk
              res-listmain.grpflag      = reservation.grpflag
              res-listmain.activeflag   = reservation.activeflag.

            FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
              ASSIGN
                res-listmain.resname      = guest.name + ", " + guest.vorname1 
                                          + guest.anredefirma + " " + guest.anrede1
                res-listmain.address      = guest.adresse1 + " " + guest.adresse2
                res-listmain.city         = guest.land + " " + guest.wohnort + " " 
                                          + guest.plz.
            END.
          END.
        END.

        FIND FIRST reservation WHERE reservation.resnr EQ search-resno 
          AND reservation.activeflag LE 1 
          NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN 
        DO: 
          curr-select = "mainres". 
        END. 
    END.
END.
