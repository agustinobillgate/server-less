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
    FIELD arrangement AS CHARACTER FORMAT "x(8)"
    FIELD erwachs     LIKE res-line.erwachs
    FIELD gratis      LIKE res-line.gratis
    FIELD zimmeranz   LIKE res-line.zimmeranz
    FIELD anztage     LIKE res-line.anztage
    FIELD changed-id  LIKE res-line.changed-id
    FIELD changed     AS CHAR
    FIELD gastnr      LIKE res-line.gastnr
    FIELD resstatus   AS INTEGER
    FIELD zikatnr     LIKE res-line.zikatnr
    FIELD resnr       LIKE res-line.resnr
    FIELD bemerk      LIKE res-line.bemerk
    FIELD active-flag LIKE res-line.active-flag
    FIELD l-zuordnung LIKE res-line.l-zuordnung
    FIELD reslinnr    LIKE res-line.reslinnr
    FIELD res-recid   AS INTEGER
    FIELD vip         AS CHAR
    FIELD nat         AS CHAR
    FIELD rate-code   AS CHAR
    FIELD segment     AS CHAR
    FIELD sp-req      AS CHAR
    FIELD usr-id      AS CHAR
    FIELD ratecode    AS CHAR /* Add by Michael @ 20/09/2018 for Archipelago International request - ticket no FF7A71 */ 
    FIELD voucher-no  AS CHARACTER FORMAT "x(50)"
/* Add by Michael @ 08/04/2019 for Bisma Eight Ubud request - ticket no 167FDB */
    FIELD email       AS CHARACTER FORMAT "x(32)"
    FIELD phone-no    AS CHARACTER FORMAT "x(20)"
/* End of add */
    FIELD sob         AS CHARACTER. /*gerald 35A3B2*/


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


DEFINE VARIABLE vip-nr  AS INTEGER EXTENT 10 NO-UNDO. 
DEF VARIABLE res-bemerk AS CHARACTER NO-UNDO.
DEF VARIABLE loopk AS INTEGER NO-UNDO.
/**************** MAIN LOGIC *******************/
FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
vip-nr[1] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
vip-nr[2] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr =  702 NO-LOCK. 
vip-nr[3] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
vip-nr[4] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
vip-nr[5] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
vip-nr[6] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
vip-nr[7] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
vip-nr[8] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
vip-nr[9] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 712 NO-LOCK. 
vip-nr[10] = htparam.finteger. 

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
ELSE IF case-type = 2 THEN
DO:
    RUN calc-br1.
    /*itung browse sblah kanan*/
END.
/* Add by Michael @ 08/04/2019 for Bisma Eight Ubud request - ticket no 167FDB */
ELSE
DO:
    RUN prepare-csv.
END.
/* End of add */
/**************** PROCEDURE *******************/
PROCEDURE calc-br1:
    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    DEFINE VARIABLE str   AS CHAR    NO-UNDO.

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
          NO-LOCK BY res-line.zinr BY res-line.ankunft
          BY (res-line.kontakt-nr * res-line.resnr) 
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
                res-listmember.changed        = STRING(res-line.changed)
                res-listmember.gastnr         = res-line.gastnr
                res-listmember.resstatus      = res-line.resstatus + res-line.l-zuordnung[3]
                res-listmember.zikatnr        = res-line.zikatnr
                res-listmember.resnr          = res-line.resnr
                res-listmember.bemerk         = res-line.bemerk
                res-listmember.active-flag    = res-line.active-flag
                res-listmember.l-zuordnung[3] = res-line.l-zuordnung[3]
                res-listmember.reslinnr       = res-line.reslinnr
                res-listmember.res-recid      = RECID(res-line).

            /*FDL August 28, 2023 => Ticket 024948 - vhpCloud*/
            ASSIGN  
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,CHR(10),"").
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,CHR(13),"").
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,"~n","").
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,"\n","").
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,"~r","").
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,"~r~n","").
              res-listmember.bemerk = REPLACE(res-listmember.bemerk,CHR(10) + CHR(13),"").
           
            res-bemerk = "".
            DO loopk = 1 TO LENGTH(res-listmember.bemerk):
                IF ASC(SUBSTR(res-listmember.bemerk, loopk, 1)) = 0 THEN.
                ELSE res-bemerk = res-bemerk + SUBSTR(res-listmember.bemerk, loopk, 1). 
            END.
            ASSIGN res-listmember.bemerk = res-bemerk.
           
            IF LENGTH(res-listmember.bemerk) LT 3 THEN res-listmember.bemerk = REPLACE(res-listmember.bemerk,CHR(32),"").
            IF LENGTH(res-listmember.bemerk) EQ ? THEN res-listmember.bemerk = "".
            /*End FDL*/
            
            FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. /* Add by Michael @ 08/04/2019 for Bisma Eight Ubud request - ticket no 167FDB */
            IF AVAILABLE guest THEN
            DO:
                IF guest.mobil-telefon NE "" THEN ASSIGN res-listmember.phone-no = guest.mobil-telefon.
                IF guest.mobil-telefon EQ "" AND guest.telefon NE "" THEN ASSIGN res-listmember.phone-no = guest.telefon.
                IF guest.email-adr NE "" THEN ASSIGN res-listmember.email = guest.email-adr.
            END.
            ELSE
            ASSIGN
                res-listmember.email          = ""
                res-listmember.phone-no       = ""
                .
            
            /*ITA 25Sept 2017*/
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
            IF AVAILABLE reservation THEN DO:
                FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN res-listmember.segment = ENTRY(1, segment.bezeich, "$$0").
                ASSIGN 
                    res-listmember.usr-id       = reservation.useridanlage
                    res-listmember.voucher-no   = reservation.vesrdepot. /*wen 090819*/  

               FIND FIRST sourccod WHERE sourccod.source-code = reservation.resart
               AND sourccod.betriebsnr = reservation.betriebsnr NO-LOCK NO-ERROR.
               IF AVAILABLE sourccod THEN
               DO:
                 res-listmember.sob = sourccod.bezeich.
               END.
            END.

            DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str,1,6) = "$CODE$" THEN 
                DO:
                  res-listmember.rate-code  = SUBSTR(str,7).
                  LEAVE.
                END.
            END.

            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
                 AND reslin-queasy.resnr = res-line.resnr 
                 AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
                 ASSIGN res-listmember.sp-req = reslin-queasy.char3 + "," + res-listmember.sp-req
                        res-listmember.ratecode = reslin-queasy.char2.  /* Add by Michael @ 20/09/2018 for Archipelago International request - ticket no FF7A71 */
            ELSE ASSIGN res-listmember.ratecode = "Undefined".
                
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr AND 
                  (guestseg.segmentcode = vip-nr[1] OR 
                   guestseg.segmentcode = vip-nr[2] OR 
                   guestseg.segmentcode = vip-nr[3] OR 
                   guestseg.segmentcode = vip-nr[4] OR 
                   guestseg.segmentcode = vip-nr[5] OR 
                   guestseg.segmentcode = vip-nr[6] OR 
                   guestseg.segmentcode = vip-nr[7] OR 
                   guestseg.segmentcode = vip-nr[8] OR 
                   guestseg.segmentcode = vip-nr[9] OR 
                   guestseg.segmentcode = vip-nr[10]) NO-LOCK NO-ERROR.
                IF AVAILABLE guestseg THEN
                DO:
                  FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
                  IF AVAILABLE segment THEN ASSIGN res-listmember.vip = segment.bezeich.
                END.
                ASSIGN res-listmember.nat = guest.nation1.                       
            END. /*end*/
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
          NO-LOCK BY reservation.resdat BY SUBSTR(reservation.name,1,32):
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

PROCEDURE prepare-csv:
    FOR EACH res-listmain:
        DELETE res-listmain.
    END.
    FOR EACH res-listmember:
        DELETE res-listmember.
    END.
  curr-select = "". 

  FOR EACH reservation WHERE reservation.resdat GE from-date 
    AND reservation.resdat LE to-date AND reservation.activeflag LE 1 
    NO-LOCK BY reservation.resdat BY SUBSTR(reservation.name,1,32):
    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr
      AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
      AND res-line.resstatus NE 12 AND res-line.resstatus NE 99 NO-LOCK NO-ERROR.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    FIND FIRST guest WHERE guest.gastnr EQ reservation.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
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
            res-listmember.changed        = STRING(res-line.changed)
            /*res-listmember.changed        = res-line.changed*/
            res-listmember.gastnr         = res-line.gastnr
            res-listmember.resstatus      = res-line.resstatus + res-line.l-zuordnung[3]
            res-listmember.zikatnr        = res-line.zikatnr
            res-listmember.resnr          = res-line.resnr
            res-listmember.bemerk         = res-line.bemerk
            res-listmember.active-flag    = res-line.active-flag
            res-listmember.l-zuordnung[3] = res-line.l-zuordnung[3]
            res-listmember.reslinnr       = res-line.reslinnr
            res-listmember.res-recid      = RECID(res-line).
            IF AVAILABLE guest THEN
                DO:
                    IF guest.mobil-telefon NE "" THEN ASSIGN res-listmember.phone-no = guest.mobil-telefon.
                    IF guest.mobil-telefon EQ "" AND guest.telefon NE "" THEN ASSIGN res-listmember.phone-no = guest.telefon.
                    IF guest.email-adr NE "" THEN ASSIGN res-listmember.email = guest.email-adr.
                END.
            ELSE
                ASSIGN
                    res-listmember.email          = ""
                    res-listmember.phone-no       = ""
                    .
    END.
  END.
END PROCEDURE.
