
DEFINE TEMP-TABLE t-noshow
    FIELD resnr             LIKE res-line.resnr
    FIELD gastnr            LIKE res-line.gastnr
    FIELD rsname            LIKE res-line.NAME
    FIELD gsname            LIKE guest.NAME
    FIELD ankunft           LIKE res-line.ankunft
    FIELD abreise           LIKE res-line.abreise
    FIELD zimmeranz         LIKE res-line.zimmeranz
    FIELD kurzbez           LIKE zimkateg.kurzbez
    FIELD erwachs           LIKE res-line.erwachs
    FIELD gratis            LIKE res-line.gratis
    FIELD arrangement       LIKE res-line.arrangement
    FIELD zinr              LIKE res-line.zinr
    FIELD zipreis           LIKE res-line.zipreis
    FIELD vesrdepot2        LIKE reservation.vesrdepot2
    FIELD bemerk            LIKE res-line.bemerk
    FIELD bemerk1           LIKE reservation.bemerk
    FIELD rsvname           LIKE reservation.NAME
    FIELD rsv-gastnr        LIKE reservation.gastnr
    FIELD vip               AS CHAR
    FIELD nat               AS CHAR
    FIELD rate-code         AS CHAR
    FIELD segment           AS CHAR
    FIELD bill-detail       AS CHAR
    FIELD usr-id            AS CHAR
    FIELD reslinnr          LIKE res-line.reslinnr
    FIELD flag              AS INT.

DEFINE INPUT PARAMETER case-type            AS INTEGER.
DEFINE INPUT PARAMETER gname                AS CHAR.
DEFINE INPUT PARAMETER fdate                AS DATE.
DEFINE INPUT PARAMETER tdate                AS DATE.
DEFINE INPUT PARAMETER resNo                AS INTEGER.
DEFINE INPUT PARAMETER gastNo               AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER comments      AS CHAR.
DEFINE OUTPUT PARAMETER resname             AS CHAR.
DEFINE OUTPUT PARAMETER address             AS CHAR.
DEFINE OUTPUT PARAMETER city                AS CHAR.
DEFINE OUTPUT PARAMETER stat-avail          AS LOGICAL.
DEFINE OUTPUT PARAMETER tot-rm              AS INTEGER. 
DEFINE OUTPUT PARAMETER tot-pax             AS INTEGER.
DEFINE OUTPUT PARAMETER tot-com             AS INTEGER. 
DEFINE OUTPUT PARAMETER TABLE FOR t-noshow.
DEFINE OUTPUT PARAMETER tot-rm-reactive      AS INTEGER.
DEFINE OUTPUT PARAMETER tot-nite-reactive    AS INTEGER.
DEFINE OUTPUT PARAMETER tot-pax-reactive     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-ch1-reactive     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-com-reactive     AS INTEGER.

DEFINE BUFFER r-guest FOR guest. 
DEFINE VARIABLE vip-nr  AS INTEGER EXTENT 10 NO-UNDO. 


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

CASE case-type :
    WHEN 1 THEN RUN disp-noshow1.
    WHEN 2 THEN RUN disp-noshow2.
END CASE.

PROCEDURE disp-noshow1: 
  ASSIGN
    tot-rm  = 0 
    tot-pax = 0
    tot-com = 0
  . 
  IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
  DO:
      FOR EACH res-line WHERE resstatus = 10 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
         AND res-line.name MATCHES(gname) 
         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST r-guest WHERE r-guest.gastnr = res-line.gastnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
         NO-LOCK BY res-line.ankunft : /* Malik Serverless : BY ankunft -> BY res-line.ankunft */
          RUN create-t-noshow.
          IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1 
          OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
          THEN .
          ELSE tot-rm = tot-rm + res-line.zimmeranz. 
          tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz. 
          tot-com = tot-com + res-line.gratis * res-line.zimmeranz. 
      END.
      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
          AND history.ankunft GE fdate
          AND history.ankunft LE tdate NO-LOCK,
          FIRST res-line WHERE res-line.resnr = history.resnr
              AND res-line.reslinnr = history.reslinnr 
              AND res-line.name MATCHES(gname)  
              AND res-line.l-zuordnung[3] = 0 
              AND res-line.betrieb-gastpay = 10 /*ragung*/  
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
          BY history.ankunft BY history.gastinfo:
          FIND FIRST t-noshow WHERE t-noshow.resnr = history.resnr
              AND t-noshow.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE t-noshow THEN
              RUN assign-it-reactive.
      END.
  END.
  ELSE 
  DO:
      FOR EACH res-line WHERE resstatus = 10 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
         AND res-line.name GE gname 
         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST r-guest WHERE r-guest.gastnr = res-line.gastnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
         NO-LOCK BY res-line.ankunft : /* Malik Serverless : BY ankunft -> BY res-line.ankunft */

          RUN create-t-noshow.
          IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1 
          OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
          THEN .
          ELSE tot-rm = tot-rm + res-line.zimmeranz. 
          tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz. 
          tot-com = tot-com + res-line.gratis * res-line.zimmeranz. 
      END.
      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
          AND history.ankunft GE fdate
          AND history.ankunft LE tdate NO-LOCK,
          FIRST res-line WHERE res-line.resnr = history.resnr
              AND res-line.reslinnr = history.reslinnr 
              AND res-line.name GE gname  
              AND res-line.l-zuordnung[3] = 0 
              AND res-line.betrieb-gastpay = 10 /*ragung*/
          NO-LOCK,
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
          BY history.ankunft BY history.gastinfo:
          FIND FIRST t-noshow WHERE t-noshow.resnr = history.resnr
              AND t-noshow.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE t-noshow THEN
              RUN assign-it-reactive.
      END.
  END.
  RUN view-resline.
END. 

PROCEDURE disp-noshow2: 

  ASSIGN
    tot-rm  = 0 
    tot-pax = 0
    tot-com = 0
  . 

  DEF BUFFER res-buff FOR res-line.
  IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
  DO:
     FOR EACH res-line WHERE resstatus = 10 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
         AND res-line.name MATCHES(gname) 
         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST r-guest WHERE r-guest.gastnr = res-line.gastnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
         NO-LOCK BY res-line.ankunft : /* Malik Serverless : BY ankunft -> BY res-line.ankunft */
          RUN create-t-noshow.
           
         IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1 
          OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
         THEN .
         ELSE tot-rm = tot-rm + res-line.zimmeranz. 
         tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz. 
         tot-com = tot-com + res-line.gratis * res-line.zimmeranz.
     END.
     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
         AND history.ankunft GE fdate
         AND history.ankunft LE tdate NO-LOCK,
         FIRST res-line WHERE res-line.resnr = history.resnr
             AND res-line.reslinnr = history.reslinnr 
             AND res-line.name MATCHES(gname)  
             AND res-line.l-zuordnung[3] = 0 
             AND res-line.betrieb-gastpay = 10 /*ragung*/ 
         NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
         BY history.ankunft BY history.gastinfo:
         FIND FIRST t-noshow WHERE t-noshow.resnr = history.resnr
             AND t-noshow.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
         IF NOT AVAILABLE t-noshow THEN
             RUN assign-it-reactive.
     END.
  END.
  ELSE 
  DO:
      FOR EACH res-line WHERE resstatus = 10 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
         AND res-line.name GE gname 
         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST r-guest WHERE r-guest.gastnr = res-line.gastnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
         NO-LOCK BY res-line.ankunft : /* Malik Serverless : BY ankunft -> BY res-line.ankunft */
          RUN create-t-noshow.
          
         IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1 
          OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
         THEN .
         ELSE tot-rm = tot-rm + res-line.zimmeranz. 
         tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz. 
         tot-com = tot-com + res-line.gratis * res-line.zimmeranz. 
      END.
      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
          AND history.ankunft GE fdate
          AND history.ankunft LE tdate NO-LOCK,
          FIRST res-line WHERE res-line.resnr = history.resnr
              AND res-line.reslinnr = history.reslinnr 
              AND res-line.name GE gname  
              AND res-line.l-zuordnung[3] = 0
              AND res-line.betrieb-gastpay = 10 /*ragung*/
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
          BY history.ankunft BY history.gastinfo:
          FIND FIRST t-noshow WHERE t-noshow.resnr = history.resnr
              AND t-noshow.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE t-noshow THEN
              RUN assign-it-reactive.
      END.
  END.
  RUN view-resline.
END. 

PROCEDURE view-resline :
  FIND FIRST t-noshow NO-LOCK NO-ERROR.
  IF AVAILABLE t-noshow THEN
  DO:
     stat-avail = YES.
     resname = t-noshow.rsvname. 
     FIND FIRST guest WHERE guest.gastnr = t-noshow.rsv-gastnr NO-LOCK NO-ERROR. 
     address = guest.adresse1. 
     city = guest.wohnort + " " + guest.plz. 
     IF t-noshow.vesrdepot2 NE "" THEN 
      comments = t-noshow.vesrdepot2 + CHR(10). 
      comments = t-noshow.bemerk1 + chr(10) + t-noshow.bemerk.
  END.
END.

PROCEDURE create-t-noshow :
    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    DEFINE VARIABLE str   AS CHAR    NO-UNDO.
    
    CREATE t-noshow.
    ASSIGN 
       t-noshow.resnr       = res-line.resnr
       t-noshow.gastnr      = res-line.gastnr 
       t-noshow.rsname      = res-line.name
       t-noshow.gsname      = r-guest.name
       t-noshow.ankunft     = res-line.ankunft
       t-noshow.abreise     = res-line.abreise
       t-noshow.zimmeranz   = res-line.zimmeranz
       t-noshow.kurzbez     = zimkateg.kurzbez 
       t-noshow.erwachs     = res-line.erwachs
       t-noshow.gratis      = res-line.gratis
       t-noshow.arrangement = res-line.arrangement
       t-noshow.zinr        = res-line.zinr
       t-noshow.zipreis     = res-line.zipreis
       t-noshow.vesrdepot2  = reservation.vesrdepot2
       t-noshow.bemerk      = res-line.bemerk
       t-noshow.bemerk1     = reservation.bemerk
       t-noshow.rsvname     = reservation.NAME
       t-noshow.rsv-gastnr  = reservation.gastnr
       t-noshow.reslinnr    = res-line.reslinnr.

    /*ITA 25Sept 2017*/
    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN t-noshow.segment = ENTRY(1, segment.bezeich, "$$0").
    ASSIGN t-noshow.usr-id = ENTRY(1, res-line.cancelled-id, ";").  

    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN 
        DO:
          t-noshow.rate-code  = SUBSTR(str,7).
          LEAVE.
        END.
    END.
    
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
          IF AVAILABLE segment THEN ASSIGN t-noshow.vip = segment.bezeich.
        END.
        ASSIGN t-noshow.nat = guest.nation1.  
    END.    
    /*end*/
END.

PROCEDURE assign-it-reactive:
   DEFINE VARIABLE night AS INT.
   DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
   DEFINE VARIABLE str   AS CHAR    NO-UNDO.
    
    IF res-line.abreise = res-line.ankunft THEN night = 1.
    ELSE night = res-line.abreise - res-line.ankunft.

    IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1
        OR res-line.betrieb-gastpay = 11
        OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
        THEN .
    ELSE 
        ASSIGN
          tot-rm-reactive = tot-rm-reactive + res-line.zimmeranz
          tot-nite-reactive = tot-nite-reactive + night * res-line.zimmeranz.
        ASSIGN
          tot-pax-reactive = tot-pax-reactive + res-line.erwachs * res-line.zimmeranz
          tot-ch1-reactive = tot-ch1-reactive + res-line.kind1 * res-line.zimmeranz
          tot-com-reactive = tot-com-reactive + res-line.gratis * res-line.zimmeranz.

    CREATE t-noshow.
    ASSIGN 
        t-noshow.resnr             = res-line.resnr 
        t-noshow.gastnr            = res-line.gastnr
        t-noshow.gsname            = guest.name 
        t-noshow.rsname            = res-line.name 
        t-noshow.ankunft           = res-line.ankunft 
        t-noshow.abreise           = res-line.abreise 
        t-noshow.zimmeranz         = res-line.zimmeranz 
        t-noshow.kurzbez           = zimkateg.kurzbez
        t-noshow.erwachs           = res-line.erwachs 
        t-noshow.gratis            = res-line.gratis 
        t-noshow.arrangement       = res-line.arrangement 
        t-noshow.zinr              = res-line.zinr 
        t-noshow.zipreis           = res-line.zipreis
        t-noshow.vesrdepot2        = reservation.vesrdepot2 
        t-noshow.bemerk            = res-line.bemerk
        t-noshow.bemerk1           = reservation.bemerk
        t-noshow.rsvname           = reservation.name
        t-noshow.rsv-gastnr        = reservation.gastnr
        t-noshow.flag              = 1.

        /*ITA 25Sept 2017*/
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN t-noshow.segment = ENTRY(1, segment.bezeich, "$$0").
        ASSIGN t-noshow.usr-id = reservation.useridanlage.  
    
        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              t-noshow.rate-code  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
    
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
          IF AVAILABLE segment THEN ASSIGN t-noshow.vip = segment.bezeich.
        END.
        ASSIGN t-noshow.nat = guest.nation1.  
        /*end*/
END.
