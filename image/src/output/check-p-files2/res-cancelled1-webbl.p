
DEFINE TEMP-TABLE res-cancelled-list
    FIELD resnr             LIKE res-line.resnr 
    FIELD columnr           LIKE res-line.storno-nr
    FIELD reslinnr          LIKE res-line.reslinnr
    FIELD gastnr            LIKE res-line.gastnr
    FIELD rsv-gastnr        LIKE reservation.gastnr
    FIELD zinr              LIKE res-line.zinr 
    FIELD name              LIKE res-line.name 
    FIELD rsv-name          LIKE reservation.name 
    FIELD ankunft           LIKE res-line.ankunft 
    FIELD bemerk            LIKE res-line.bemerk
    FIELD rsv-bemerk        LIKE reservation.bemerk
    FIELD anztage           LIKE res-line.anztage 
    FIELD abreise           LIKE res-line.abreise 
    FIELD zimmeranz         LIKE res-line.zimmeranz 
    FIELD kurzbez           LIKE zimkateg.kurzbez
    FIELD erwachs           LIKE res-line.erwachs 
    FIELD kind1             LIKE res-line.kind1
    FIELD gratis            LIKE res-line.gratis 
    FIELD arrangement       LIKE res-line.arrangement 
    FIELD zipreis           LIKE res-line.zipreis
    FIELD betrieb-gastpay   LIKE res-line.betrieb-gastpay
    FIELD cancelled         LIKE res-line.cancelled
    FIELD cancelled-id      LIKE res-line.cancelled-id
    FIELD resdat            LIKE reservation.resdat
    FIELD vesrdepot2        LIKE reservation.vesrdepot2
    FIELD address           AS CHAR 
    FIELD city              AS CHAR
    FIELD res-resnr         LIKE reservation.resnr
    FIELD groupname         LIKE reservation.groupname
    FIELD flag              AS INT
    FIELD vip               AS CHAR
    FIELD nat               AS CHAR
    FIELD rate-code         AS CHAR
    FIELD segment           AS CHAR
    FIELD sp-req            AS CHAR
    FIELD usr-id            AS CHAR
    FIELD vesrdepot         LIKE reservation.vesrdepot
    FIELD firma             AS CHAR.


DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER show-rate    AS LOGICAL.
DEFINE INPUT PARAMETER curr-rmType  AS CHAR.
DEFINE INPUT PARAMETER do-it        AS LOGICAL.
DEFINE INPUT PARAMETER gname        AS CHAR.
DEFINE INPUT PARAMETER tname        AS CHAR.
DEFINE INPUT PARAMETER res-status   AS INTEGER.
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER tdate        AS DATE.
DEFINE INPUT PARAMETER kart         AS INT.
DEFINE INPUT PARAMETER res-number   AS INTEGER. /*FDL April 18, 2024 => Ticket FEE854|*/

DEFINE OUTPUT PARAMETER tot-rm      AS INTEGER.
DEFINE OUTPUT PARAMETER tot-pax     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-ch1     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-com     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-nite    AS INTEGER.

DEFINE OUTPUT PARAMETER tot-rm-reactive      AS INTEGER.
DEFINE OUTPUT PARAMETER tot-pax-reactive     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-ch1-reactive     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-com-reactive     AS INTEGER.
DEFINE OUTPUT PARAMETER tot-nite-reactive    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR res-cancelled-list.


DEFINE VARIABLE vip-nr  AS INTEGER EXTENT 10 NO-UNDO. 
DEFINE VARIABLE resline-remark AS CHARACTER NO-UNDO.
DEFINE VARIABLE rsv-remark AS CHARACTER NO-UNDO.

IF case-type EQ 1 THEN RUN disp-noshow.
ELSE IF case-type EQ 2 THEN RUN disp-noshowC.
 
FOR EACH res-cancelled-list:
    resline-remark = res-cancelled-list.bemerk.
    resline-remark = REPLACE(resline-remark,CHR(10),"").
    resline-remark = REPLACE(resline-remark,CHR(13),"").
    resline-remark = REPLACE(resline-remark,"~n","").
    resline-remark = REPLACE(resline-remark,"\n","").
    resline-remark = REPLACE(resline-remark,"~r","").
    resline-remark = REPLACE(resline-remark,"~r~n","").
    resline-remark = REPLACE(resline-remark,"&nbsp;"," ").
    resline-remark = REPLACE(resline-remark,"</p>","</p></p>").
    resline-remark = REPLACE(resline-remark,"</p>",CHR(13)).
    resline-remark = REPLACE(resline-remark,"<BR>",CHR(13)).
    resline-remark = REPLACE(resline-remark,CHR(10) + CHR(13),"").

    IF LENGTH(resline-remark) LT 3 THEN resline-remark = REPLACE(resline-remark,CHR(32),"").
    IF resline-remark EQ ? THEN resline-remark = "".

    res-cancelled-list.bemerk = resline-remark.
    resline-remark = "".

    rsv-remark = res-cancelled-list.rsv-bemerk.
    rsv-remark = REPLACE(rsv-remark,CHR(10),"").
    rsv-remark = REPLACE(rsv-remark,CHR(13),"").
    rsv-remark = REPLACE(rsv-remark,"~n","").
    rsv-remark = REPLACE(rsv-remark,"\n","").
    rsv-remark = REPLACE(rsv-remark,"~r","").
    rsv-remark = REPLACE(rsv-remark,"~r~n","").
    rsv-remark = REPLACE(rsv-remark,"&nbsp;"," ").
    rsv-remark = REPLACE(rsv-remark,"</p>","</p></p>").
    rsv-remark = REPLACE(rsv-remark,"</p>",CHR(13)).
    rsv-remark = REPLACE(rsv-remark,"<BR>",CHR(13)).
    rsv-remark = REPLACE(rsv-remark,CHR(10) + CHR(13),"").

    IF LENGTH(rsv-remark) LT 3 THEN rsv-remark = REPLACE(rsv-remark,CHR(32),"").
    IF rsv-remark EQ ? THEN rsv-remark = "".

    res-cancelled-list.rsv-bemerk = rsv-remark.
    rsv-remark = "".
END.
/***************************  PROCEDURE   **************************************/ 

FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
vip-nr[1] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
vip-nr[2] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
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

PROCEDURE disp-noshow: 
  IF show-rate THEN RUN disp-noshow1. 
  ELSE RUN disp-noshow2. 
END. 
 
PROCEDURE disp-noshowC: 
  IF show-rate THEN RUN disp-noshowC1. 
  ELSE RUN disp-noshowC2.
END. 
 
PROCEDURE disp-noshow1: 
  IF do-it THEN
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshow1-a.
      ELSE
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN    /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                       BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart 
                         NO-LOCK BY res-line.ankunft BY res-line.name:
                       RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.      
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                       BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY ankunft BY res-line.name:
                       RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.      
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
          ELSE 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
       END.
  END.
  ELSE
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshow1-b.
      ELSE
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) /*wen*/
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 AND res-line.active-flag = 2 /*wen*/ NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                         BY res-line.ankunft BY res-line.name:
                         RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" 
                        AND history.ankunft GE fdate AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                            
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" 
                        AND history.ankunft GE fdate AND history.ankunft LE tdate 
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) /*wen*/
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 AND res-line.active-flag = 2 /*wen*/ NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" 
                        AND history.ankunft GE fdate AND history.ankunft LE tdate  NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:

                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" 
                        AND history.ankunft GE fdate AND history.ankunft LE tdate  NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" 
                        AND history.ankunft GE fdate AND history.ankunft LE tdate  NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY ankunft BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" 
                        AND history.ankunft GE fdate AND history.ankunft LE tdate  NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
          ELSE 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN
                DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
      END.
  END.
END.

PROCEDURE disp-noshow2: 
  IF do-it THEN
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshow2-a.
      ELSE 
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK
                        BY ankunft BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate 
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.ankunft BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate 
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK
                        BY ankunft BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate 
                       AND res-line.ankunft LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY ankunft BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:

                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY ankunft BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:

                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY ankunft BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
          ELSE 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        /*RUN assign-it2.*/
                        RUN assign-it.
    
                    END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END.
       END.
  END.
  ELSE
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshow2-b.
      ELSE
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
                IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
                DO:
                    IF res-status = 1 THEN DO:
                        FOR EACH res-line WHERE resstatus = 9 
                           AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                           AND res-line.ankunft GE fdate 
                           AND res-line.ankunft LE tdate 
                           AND res-line.resnr EQ res-number
                           AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                           FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY res-line.ankunft BY res-line.name:
    
                            /*RUN assign-it2.*/
                            RUN assign-it.
                        END.

                        FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                            AND history.ankunft GE fdate
                            AND history.ankunft LE tdate
                            AND history.resnr EQ res-number NO-LOCK,
                            FIRST res-line WHERE res-line.resnr = history.resnr
                                AND res-line.reslinnr = history.reslinnr                                 
                                AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY history.ankunft BY history.gastinfo:
                            FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                                AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE res-cancelled-list THEN
                                RUN assign-it-reactive.
                        END.
                    END.
                    ELSE DO:
                        FOR EACH res-line WHERE resstatus = 9 
                           AND res-line.betrieb-gastpay = 3
                           AND res-line.ankunft GE fdate 
                           AND res-line.ankunft LE tdate 
                           AND res-line.resnr EQ res-number
                           AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                           FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                            BY res-line.ankunft BY res-line.name:
    
                            /*RUN assign-it2.*/
                            RUN assign-it.
    
                        END.

                        FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                            AND history.ankunft GE fdate
                            AND history.ankunft LE tdate
                            AND history.resnr EQ res-number NO-LOCK,
                            FIRST res-line WHERE res-line.resnr = history.resnr
                                AND res-line.reslinnr = history.reslinnr                                 
                                AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY history.ankunft BY history.gastinfo:
                            FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                                AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE res-cancelled-list THEN
                                RUN assign-it-reactive.
                        END.
                    END.
                END.
                ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
                DO:
                    IF res-status = 1 THEN DO:
                        FOR EACH res-line WHERE resstatus = 9 
                           AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                           AND res-line.ankunft GE fdate 
                           AND res-line.ankunft LE tdate 
                           AND res-line.name MATCHES(gname) 
                           AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                           FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY ankunft BY res-line.name:
    
                            /*RUN assign-it2.*/
                            RUN assign-it.
                        END.

                        FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                            AND history.ankunft GE fdate
                            AND history.ankunft LE tdate NO-LOCK,
                            FIRST res-line WHERE res-line.resnr = history.resnr
                                AND res-line.reslinnr = history.reslinnr 
                                AND res-line.name MATCHES(gname) 
                                AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY history.ankunft BY history.gastinfo:
                            FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                                AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE res-cancelled-list THEN
                                RUN assign-it-reactive.
                        END.
                    END.
                    ELSE DO:
                        FOR EACH res-line WHERE resstatus = 9 
                           AND res-line.betrieb-gastpay = 3
                           AND res-line.ankunft GE fdate 
                           AND res-line.ankunft LE tdate 
                           AND res-line.name MATCHES(gname) 
                           AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                           FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                            BY ankunft BY res-line.name:
    
                            /*RUN assign-it2.*/
                            RUN assign-it.
    
                        END.

                        FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                            AND history.ankunft GE fdate
                            AND history.ankunft LE tdate NO-LOCK,
                            FIRST res-line WHERE res-line.resnr = history.resnr
                                AND res-line.reslinnr = history.reslinnr 
                                AND res-line.name MATCHES(gname) 
                                AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY history.ankunft BY history.gastinfo:
                            FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                                AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE res-cancelled-list THEN
                                RUN assign-it-reactive.
                        END.
                    END.
                END.
                ELSE 
                DO:
                    IF res-status = 1 THEN DO:

                        FOR EACH res-line WHERE resstatus = 9 
                           AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                           AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                           AND res-line.name GE gname AND res-line.name LE tname 
                           AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                           FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                            BY ankunft BY res-line.name:
    
                            /*RUN assign-it2.*/
                            RUN assign-it.
    
                        END.

                        FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                            AND history.ankunft GE fdate
                            AND history.ankunft LE tdate NO-LOCK,
                            FIRST res-line WHERE res-line.resnr = history.resnr
                                AND res-line.reslinnr = history.reslinnr 
                                AND res-line.name GE gname AND res-line.name LE tname  
                                AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY history.ankunft BY history.gastinfo:
                            FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                                AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE res-cancelled-list THEN
                                RUN assign-it-reactive.
                        END.
                    END.
                    ELSE DO:
                        FOR EACH res-line WHERE resstatus = 9 
                           AND res-line.betrieb-gastpay = 3
                           AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                           AND res-line.name GE gname AND res-line.name LE tname 
                           AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                           FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                            BY ankunft BY res-line.name:
    
                            /*RUN assign-it2.*/
                            RUN assign-it.
    
                        END.

                        FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                            AND history.ankunft GE fdate
                            AND history.ankunft LE tdate NO-LOCK,
                            FIRST res-line WHERE res-line.resnr = history.resnr
                                AND res-line.reslinnr = history.reslinnr 
                                AND res-line.name GE gname AND res-line.name LE tname  
                                AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                            BY history.ankunft BY history.gastinfo:
                            FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                                AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE res-cancelled-list THEN
                                RUN assign-it-reactive.
                        END.
                    END.
                END.
          END. 
          ELSE 
          DO: 
              IF res-number GT 0 THEN   /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
              DO:
                  IF res-status = 1 THEN DO:
                      FOR EACH res-line WHERE resstatus = 9 
                         AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                         AND res-line.resnr EQ res-number
                         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK, 
                         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                          BY res-line.name:
    
                          /*RUN assign-it2.*/
                          RUN assign-it.
    
                      END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                          AND history.ankunft GE fdate
                          AND history.ankunft LE tdate
                          AND history.resnr EQ res-number NO-LOCK,
                          FIRST res-line WHERE res-line.resnr = history.resnr
                              AND res-line.reslinnr = history.reslinnr                               
                              AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                          BY history.ankunft BY history.gastinfo:
                          FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                              AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE res-cancelled-list THEN
                              RUN assign-it-reactive.
                      END.
                  END.
                  ELSE DO:
                      FOR EACH res-line WHERE resstatus = 9 
                         AND res-line.betrieb-gastpay = 3
                         AND res-line.resnr EQ res-number
                         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                          BY res-line.name:
    
                          /*RUN assign-it2.*/
                          RUN assign-it.
    
                      END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                          AND history.ankunft GE fdate
                          AND history.ankunft LE tdate
                          AND history.resnr EQ res-number NO-LOCK,
                          FIRST res-line WHERE res-line.resnr = history.resnr
                              AND res-line.reslinnr = history.reslinnr                               
                              AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                          BY history.ankunft BY history.gastinfo:
                          FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                              AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE res-cancelled-list THEN
                              RUN assign-it-reactive.
                      END.
                  END.
              END.
              ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
              DO:
                  IF res-status = 1 THEN DO:
                      FOR EACH res-line WHERE resstatus = 9 
                         AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                         AND res-line.name MATCHES(gname) 
                         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK, 
                         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                          BY res-line.name:
    
                          /*RUN assign-it2.*/
                          RUN assign-it.
    
                      END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                          AND history.ankunft GE fdate
                          AND history.ankunft LE tdate NO-LOCK,
                          FIRST res-line WHERE res-line.resnr = history.resnr
                              AND res-line.reslinnr = history.reslinnr 
                              AND res-line.name MATCHES(gname) 
                              AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                          BY history.ankunft BY history.gastinfo:
                          FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                              AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE res-cancelled-list THEN
                              RUN assign-it-reactive.
                      END.
                  END.
                  ELSE DO:
                      FOR EACH res-line WHERE resstatus = 9 
                         AND res-line.betrieb-gastpay = 3
                         AND res-line.name MATCHES(gname) 
                         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                          BY res-line.name:
    
                          /*RUN assign-it2.*/
                          RUN assign-it.
    
                      END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                          AND history.ankunft GE fdate
                          AND history.ankunft LE tdate NO-LOCK,
                          FIRST res-line WHERE res-line.resnr = history.resnr
                              AND res-line.reslinnr = history.reslinnr 
                              AND res-line.name MATCHES(gname) 
                              AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                          BY history.ankunft BY history.gastinfo:
                          FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                              AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE res-cancelled-list THEN
                              RUN assign-it-reactive.
                      END.
                  END.
              END.
              ELSE 
              DO:
                  IF res-status = 1 THEN DO:
                      FOR EACH res-line WHERE resstatus = 9 
                         AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                         AND res-line.name GE gname AND res-line.name LE tname 
                         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                           BY res-line.name:
                          
                          /*RUN assign-it2.*/
                          RUN assign-it.
    
                      END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                          AND history.ankunft GE fdate
                          AND history.ankunft LE tdate NO-LOCK,
                          FIRST res-line WHERE res-line.resnr = history.resnr
                              AND res-line.reslinnr = history.reslinnr 
                              AND res-line.name GE gname AND res-line.name LE tname  
                              AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                          BY history.ankunft BY history.gastinfo:
                          FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                              AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE res-cancelled-list THEN
                              RUN assign-it-reactive.
                      END.
                  END.
                  ELSE DO:
                      FOR EACH res-line WHERE resstatus = 9 
                         AND res-line.betrieb-gastpay = 3
                         AND res-line.name GE gname AND res-line.name LE tname 
                         AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                         FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                          BY res-line.name:
    
                          /*RUN assign-it2.*/
                          RUN assign-it.
    
                      END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                          AND history.ankunft GE fdate
                          AND history.ankunft LE tdate NO-LOCK,
                          FIRST res-line WHERE res-line.resnr = history.resnr
                              AND res-line.reslinnr = history.reslinnr 
                              AND res-line.name GE gname AND res-line.name LE tname  
                              AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                          BY history.ankunft BY history.gastinfo:
                          FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                              AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                          IF NOT AVAILABLE res-cancelled-list THEN
                              RUN assign-it-reactive.
                      END.
                  END.
              END.
          END.
      END.
  END.
END. 

PROCEDURE disp-noshowC1:   
  IF do-it THEN
  DO:
    IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshowC1-a.
    ELSE
    DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart
                        NO-LOCK BY res-line.CANCELLED BY res-line.NAME:
                        RUN assign-it.
                    END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK, 
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.CANCELLED BY res-line.name:
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart
                        NO-LOCK BY res-line.CANCELLED BY res-line.NAME:
                        RUN assign-it.
                    END.

                      FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK, 
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.CANCELLED BY res-line.name:
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.active-flag = 2 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.CANCELLED BY res-line.name:
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
               ELSE DO:
                   FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr  AND guest.karteityp = kart NO-LOCK 
                       BY res-line.CANCELLED BY res-line.name:
                       RUN assign-it.
                   END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
               END.
            END.
          END. 
          ELSE DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr  AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
    
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr  AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
    
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK
                         BY res-line.name:
    
                        RUN assign-it.
    
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
      END.
  END.
  ELSE
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshowC1-b.
      ELSE
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK
                         BY res-line.CANCELLED BY res-line.NAME:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK, 
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate 
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK
                         BY res-line.CANCELLED BY res-line.NAME:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK, 
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.active-flag = 2 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
               ELSE DO:
                   FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                       BY res-line.CANCELLED BY res-line.name:
    
                       RUN assign-it.
                   END.

                    FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
               END.
            END.
          END. 
          ELSE DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK
                         BY res-line.name:
                        
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
      END.
  END.
END. 

PROCEDURE disp-noshowC2: 
  
  IF do-it THEN
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshowC2-a.
      ELSE
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
          ELSE DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.name:
                        
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
      END.
  END.
  ELSE
  DO:
      IF curr-rmType MATCHES ("*-ALL-*") THEN RUN disp-noshowC2-b.
      ELSE
      DO:
          IF fdate NE ? AND tdate NE ? THEN 
          DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.resnr EQ res-number 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.cancelled GE fdate 
                       AND res-line.cancelled LE tdate 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.CANCELLED BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
          END. 
          ELSE DO: 
            IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                             
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.resnr EQ res-number
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate
                        AND history.resnr EQ res-number NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr                              
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name MATCHES(gname) 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name MATCHES(gname) 
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
            END.
            ELSE 
            DO:
                IF res-status = 1 THEN DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.
                END.
                ELSE DO:
                    FOR EACH res-line WHERE resstatus = 9 
                       AND res-line.betrieb-gastpay = 3
                       AND res-line.active-flag = 2 
                       AND res-line.name GE gname AND res-line.name LE tname 
                       AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                       FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                        BY res-line.name:
    
                        RUN assign-it.
                    END.

                     FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                        AND history.ankunft GE fdate
                        AND history.ankunft LE tdate NO-LOCK,
                        FIRST res-line WHERE res-line.resnr = history.resnr
                            AND res-line.reslinnr = history.reslinnr 
                            AND res-line.name GE gname AND res-line.name LE tname  
                            AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr AND zimkateg.kurzbez = curr-rmType NO-LOCK,
                        FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                        BY history.ankunft BY history.gastinfo:
                        FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                            AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE res-cancelled-list THEN
                            RUN assign-it-reactive.
                    END.

                END.
            END.
          END. 
      END.
  END.
END. 

PROCEDURE disp-noshow1-a:
    IF fdate NE ? AND tdate NE ? THEN 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart 
                    NO-LOCK BY res-line.ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
      ELSE 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.

            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.resnr EQ res-number 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.

            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
END.

PROCEDURE disp-noshow1-b:
IF fdate NE ? AND tdate NE ? THEN 
      DO:         
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate 
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate 
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate 
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate 
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate 
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY ankunft BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate 
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
      ELSE 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname)
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname)
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr  NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*" NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
END.

PROCEDURE disp-noshow2-a: 
IF fdate NE ? AND tdate NE ? THEN 
  DO: 
    IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
    DO:
        IF res-status = 1 THEN DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
               AND res-line.ankunft GE fdate 
               AND res-line.ankunft LE tdate 
               AND res-line.resnr EQ res-number
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK
                BY ankunft BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate
                AND history.resnr EQ res-number NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr                     
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
        ELSE DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND res-line.betrieb-gastpay = 3
               AND res-line.ankunft GE fdate 
               AND res-line.ankunft LE tdate 
               AND res-line.resnr EQ res-number
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.ankunft BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
        END.
    END.
    ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN
    DO:
        IF res-status = 1 THEN DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
               AND res-line.ankunft GE fdate 
               AND res-line.ankunft LE tdate 
               AND res-line.name MATCHES(gname) 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK
                BY ankunft BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name MATCHES(gname) 
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
        ELSE DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND res-line.betrieb-gastpay = 3
               AND res-line.ankunft GE fdate 
               AND res-line.ankunft LE tdate 
               AND res-line.name MATCHES(gname) 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY ankunft BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
        END.
    END.
    ELSE 
    DO:
        IF res-status = 1 THEN DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
               AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
               AND res-line.name GE gname AND res-line.name LE tname 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY ankunft BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name GE gname AND res-line.name LE tname  
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
        ELSE DO:
             FOR EACH res-line WHERE resstatus = 9 
               AND res-line.betrieb-gastpay = 3
               AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
               AND res-line.name GE gname AND res-line.name LE tname 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY ankunft BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name GE gname AND res-line.name LE tname  
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
    END.
  END. 
  ELSE 
  DO: 
    IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
    DO:
        IF res-status = 1 THEN DO:
              FOR EACH res-line WHERE resstatus = 9 
               AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
               AND res-line.resnr EQ res-number
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.name:
    
                RUN assign-it.
            END.  

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate
                AND history.resnr EQ res-number NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr                     
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
        ELSE DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND res-line.betrieb-gastpay = 3
               AND res-line.resnr EQ res-number
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate
                AND history.resnr EQ res-number NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr                     
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
    END.
    ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
    DO:
        IF res-status = 1 THEN DO:
              FOR EACH res-line WHERE resstatus = 9 
               AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
               AND res-line.name MATCHES(gname) 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.name:
    
                RUN assign-it.
            END.  

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name MATCHES(gname) 
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
        ELSE DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND res-line.betrieb-gastpay = 3
               AND res-line.name MATCHES(gname) 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name MATCHES(gname) 
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
    END.
    ELSE 
    DO:
        IF res-status = 1 THEN DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
               AND res-line.name GE gname AND res-line.name LE tname 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.name:
    
                RUN assign-it.
            END.
            
            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name GE gname AND res-line.name LE tname  
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
        ELSE DO:
            FOR EACH res-line WHERE resstatus = 9 
               AND res-line.betrieb-gastpay = 3
               AND res-line.name GE gname AND res-line.name LE tname 
               AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
               FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY res-line.name:
    
                RUN assign-it.
            END.

            FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                AND history.ankunft GE fdate
                AND history.ankunft LE tdate NO-LOCK,
                FIRST res-line WHERE res-line.resnr = history.resnr
                    AND res-line.reslinnr = history.reslinnr 
                    AND res-line.name GE gname AND res-line.name LE tname  
                    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                BY history.ankunft BY history.gastinfo:
                FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                    AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                IF NOT AVAILABLE res-cancelled-list THEN
                    RUN assign-it-reactive.
            END.
        END.
    END.
  END.
END.

PROCEDURE disp-noshow2-b: 
IF fdate NE ? AND tdate NE ? THEN 
  DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY ankunft BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                    BY res-line.ankunft BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY ankunft BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate 
                   AND res-line.ankunft LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                    BY ankunft BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                    BY ankunft BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                    BY ankunft BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
  END. 
  ELSE 
  DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                     BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK   
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END.
 END.

 PROCEDURE disp-noshowC1-a: 
 IF fdate NE ? AND tdate NE ? THEN 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart
                    NO-LOCK BY res-line.CANCELLED BY res-line.NAME:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                        
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.

            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart
                    NO-LOCK BY res-line.CANCELLED BY res-line.NAME:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.

            END.
        END.
        ELSE 
        DO:
           IF res-status = 1 THEN DO:
               FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.active-flag = 2 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
           END.
           ELSE DO:
               FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr  AND guest.karteityp = kart NO-LOCK 
                   BY res-line.CANCELLED BY res-line.name:
    
                   RUN assign-it.
               END.

               FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
           END.
        END.
      END. 
      ELSE DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr  AND guest.karteityp = kart NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr  AND guest.karteityp = kart NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK
                     BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END.
 END.

 PROCEDURE disp-noshowC1-b: 
  IF fdate NE ? AND tdate NE ? THEN 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:                
                FOR EACH res-line WHERE resstatus = 9
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK
                     BY res-line.CANCELLED BY res-line.NAME:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:

                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.                    
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:                
                FOR EACH res-line WHERE resstatus = 9
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK
                     BY res-line.CANCELLED BY res-line.NAME:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:

                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.                    
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
           IF res-status = 1 THEN DO:
               FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.active-flag = 2 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
           END.
           ELSE DO:
               FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                   BY res-line.CANCELLED BY res-line.name:
    
                   RUN assign-it.
               END.

               FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
           END.
        END.
      END. 
      ELSE DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr  NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr  NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK
                     BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
END.

PROCEDURE disp-noshowC2-a: 
IF fdate NE ? AND tdate NE ? THEN 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK   
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
      ELSE DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK  
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.karteityp = kart NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
END.

PROCEDURE disp-noshowC2-b:
IF fdate NE ? AND tdate NE ? THEN 
      DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.resnr EQ res-number 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                          
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr  NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK  
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr  NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.cancelled GE fdate 
                   AND res-line.cancelled LE tdate 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.CANCELLED BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
      ELSE DO: 
        IF res-number GT 0 THEN     /*FDL April 18, 2024 => Ticket FEE854 | BDD22F*/
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.resnr EQ res-number
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate
                    AND history.resnr EQ res-number NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr                         
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE IF SUBSTR(gname,1,1) = "*" AND SUBSTR(gname,length(gname),1) = "*" THEN 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name MATCHES(gname) 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name MATCHES(gname) 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
        ELSE 
        DO:
            IF res-status = 1 THEN DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND (res-line.betrieb-gastpay NE 3 AND res-line.betrieb-gastpay NE 99) 
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname 
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
            ELSE DO:
                FOR EACH res-line WHERE resstatus = 9 
                   AND res-line.betrieb-gastpay = 3
                   AND res-line.active-flag = 2 
                   AND res-line.name GE gname AND res-line.name LE tname 
                   AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                   FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK    
                    BY res-line.name:
    
                    RUN assign-it.
                END.

                FOR EACH history WHERE history.bemerk MATCHES "*reactive by*"
                    AND history.ankunft GE fdate
                    AND history.ankunft LE tdate NO-LOCK,
                    FIRST res-line WHERE res-line.resnr = history.resnr
                        AND res-line.reslinnr = history.reslinnr 
                        AND res-line.name GE gname AND res-line.name LE tname  
                        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
                    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
                    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
                    FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK 
                    BY history.ankunft BY history.gastinfo:
                    FIND FIRST res-cancelled-list WHERE res-cancelled-list.resnr = history.resnr
                        AND res-cancelled-list.reslinnr = history.reslinnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE res-cancelled-list THEN
                        RUN assign-it-reactive.
                END.
            END.
        END.
      END. 
END.

PROCEDURE assign-it:
    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    DEFINE VARIABLE str   AS CHAR    NO-UNDO.
    DEFINE VARIABLE found-mainguest AS LOGICAL.
    
    DEFINE BUFFER buff-rline FOR res-line.

    /*FDL Jan 02, 2023 => Ticket 239B05 - If cancel rsv rmsharer doesn't have the cancel rsv main guest 
                        then cancel rsv rmsharer include calculate total room dan night*/
    FOR EACH buff-rline WHERE buff-rline.resnr EQ res-line.resnr
        AND buff-rline.betrieb-gastpay EQ 1
        AND buff-rline.l-zuordnung[3] EQ 0
        AND buff-rline.resstatus EQ res-line.resstatus NO-LOCK:

        found-mainguest = YES.
        LEAVE.
    END.

    IF found-mainguest THEN
    DO:
        IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1
            OR res-line.betrieb-gastpay = 11
            OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
        THEN.
        ELSE    
        DO:
            ASSIGN
                tot-rm = tot-rm + res-line.zimmeranz
                tot-nite = tot-nite + (res-line.abreise - res-line.ankunft) * res-line.zimmeranz.
        END.        
    END.        
    ELSE
    DO:
        ASSIGN
            tot-rm = tot-rm + res-line.zimmeranz
            tot-nite = tot-nite + (res-line.abreise - res-line.ankunft) * res-line.zimmeranz.
    END.
    ASSIGN
        tot-pax = tot-pax + res-line.erwachs * res-line.zimmeranz
        tot-ch1 = tot-ch1 + res-line.kind1 * res-line.zimmeranz
        tot-com = tot-com + res-line.gratis * res-line.zimmeranz. 


    CREATE res-cancelled-list.
    ASSIGN 
        res-cancelled-list.resnr             = res-line.resnr 
        res-cancelled-list.reslinnr          = res-line.reslinnr
        res-cancelled-list.gastnr            = res-line.gastnr
        res-cancelled-list.rsv-gastnr        = reservation.gastnr
        res-cancelled-list.zinr              = res-line.zinr 
        res-cancelled-list.name              = res-line.name 
        res-cancelled-list.rsv-name          = reservation.name 
        res-cancelled-list.ankunft           = res-line.ankunft 
        res-cancelled-list.bemerk            = res-line.bemerk
        res-cancelled-list.rsv-bemerk        = reservation.bemerk
        res-cancelled-list.anztage           = res-line.anztage 
        res-cancelled-list.abreise           = res-line.abreise 
        res-cancelled-list.zimmeranz         = res-line.zimmeranz 
        res-cancelled-list.kurzbez           = zimkateg.kurzbez
        res-cancelled-list.erwachs           = res-line.erwachs 
        res-cancelled-list.kind1             = res-line.kind1
        res-cancelled-list.gratis            = res-line.gratis 
        res-cancelled-list.arrangement       = res-line.arrangement 
        res-cancelled-list.zipreis           = res-line.zipreis
        res-cancelled-list.betrieb-gastpay   = res-line.betrieb-gastpay
        res-cancelled-list.cancelled         = res-line.cancelled
        res-cancelled-list.cancelled-id      = res-line.cancelled-id
        res-cancelled-list.resdat            = reservation.resdat
        res-cancelled-list.vesrdepot2        = reservation.vesrdepot2 
        res-cancelled-list.address           = guest.adresse1
        res-cancelled-list.city              = guest.wohnort + " " + guest.plz
        res-cancelled-list.res-resnr         = reservation.resnr
        res-cancelled-list.groupname         = reservation.groupname
        res-cancelled-list.vesrdepot         = reservation.vesrdepot
        res-cancelled-list.firma             = guest.name + ", " + guest.anredefirma.

    /*ITA 25Sept 2017*/
    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN res-cancelled-list.segment = ENTRY(1, segment.bezeich, "$$0").
    ASSIGN res-cancelled-list.usr-id = reservation.useridanlage.  

    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN 
        DO:
          res-cancelled-list.rate-code  = SUBSTR(str,7).
          LEAVE.
        END.
    END.

    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
         AND reslin-queasy.resnr = res-line.resnr 
         AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN
         ASSIGN res-cancelled-list.sp-req = reslin-queasy.char3 + "," + res-cancelled-list.sp-req.

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
      IF AVAILABLE segment THEN ASSIGN res-cancelled-list.vip = segment.bezeich.
    END.
    ASSIGN res-cancelled-list.nat = guest.nation1.  
    /*end*/
END.


PROCEDURE assign-it-reactive:
    DEFINE VARIABLE night AS INT.
    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    DEFINE VARIABLE str   AS CHAR    NO-UNDO.
    DEFINE VARIABLE found-mainguest AS LOGICAL.
    
    DEFINE BUFFER buff-rline FOR res-line.

    /*FDL Jan 02, 2023 => Ticket 239B05 - If cancel rsv rmsharer doesn't have the cancel rsv main guest 
                        then cancel rsv rmsharer include calculate total room dan night*/
    FOR EACH buff-rline WHERE buff-rline.resnr EQ res-line.resnr
        AND buff-rline.betrieb-gastpay EQ 1
        AND buff-rline.l-zuordnung[3] EQ 0
        AND buff-rline.resstatus EQ res-line.resstatus NO-LOCK:

        found-mainguest = YES.
        LEAVE.
    END.

    IF res-line.abreise = res-line.ankunft THEN night = 1.
    ELSE night = res-line.abreise - res-line.ankunft.

    IF found-mainguest THEN
    DO:
        IF res-line.zimmerfix OR res-line.l-zuordnung[3] = 1
            OR res-line.betrieb-gastpay = 11
            OR (res-line.kontakt-nr NE 0 AND (res-line.kontakt-nr NE res-line.reslinnr))
        THEN.
        ELSE    
        DO:
            ASSIGN
                tot-rm-reactive = tot-rm-reactive + res-line.zimmeranz
                tot-nite-reactive = tot-nite-reactive + night * res-line.zimmeranz.
        END.        
    END.        
    ELSE
    DO:
        ASSIGN
            tot-rm-reactive = tot-rm-reactive + res-line.zimmeranz
            tot-nite-reactive = tot-nite-reactive + night * res-line.zimmeranz.
    END.    
    ASSIGN
        tot-pax-reactive = tot-pax-reactive + res-line.erwachs * res-line.zimmeranz
        tot-ch1-reactive = tot-ch1-reactive + res-line.kind1 * res-line.zimmeranz
        tot-com-reactive = tot-com-reactive + res-line.gratis * res-line.zimmeranz.

    CREATE res-cancelled-list.
    ASSIGN 
        res-cancelled-list.resnr             = res-line.resnr 
        res-cancelled-list.columnr           = res-line.storno-nr
        res-cancelled-list.reslinnr          = res-line.reslinnr
        res-cancelled-list.gastnr            = res-line.gastnr
        res-cancelled-list.rsv-gastnr        = reservation.gastnr
        res-cancelled-list.zinr              = res-line.zinr 
        res-cancelled-list.name              = res-line.name 
        res-cancelled-list.rsv-name          = reservation.name 
        res-cancelled-list.ankunft           = res-line.ankunft 
        res-cancelled-list.bemerk            = res-line.bemerk
        res-cancelled-list.rsv-bemerk        = reservation.bemerk
        res-cancelled-list.anztage           = res-line.anztage 
        res-cancelled-list.abreise           = res-line.abreise 
        res-cancelled-list.zimmeranz         = res-line.zimmeranz 
        res-cancelled-list.kurzbez           = zimkateg.kurzbez
        res-cancelled-list.erwachs           = res-line.erwachs 
        res-cancelled-list.kind1             = res-line.kind1
        res-cancelled-list.gratis            = res-line.gratis 
        res-cancelled-list.arrangement       = res-line.arrangement 
        res-cancelled-list.zipreis           = res-line.zipreis
        res-cancelled-list.betrieb-gastpay   = res-line.betrieb-gastpay
        res-cancelled-list.cancelled         = res-line.cancelled
        res-cancelled-list.cancelled-id      = res-line.cancelled-id
        res-cancelled-list.resdat            = reservation.resdat
        res-cancelled-list.vesrdepot2        = reservation.vesrdepot2 
        res-cancelled-list.address           = guest.adresse1
        res-cancelled-list.city              = guest.wohnort + " " + guest.plz
        res-cancelled-list.res-resnr         = reservation.resnr
        res-cancelled-list.groupname         = reservation.groupname
        res-cancelled-list.flag              = 1
        res-cancelled-list.vesrdepot         = reservation.vesrdepot
        res-cancelled-list.firma             = guest.name + ", " + guest.anredefirma.

        /*ITA 25Sept 2017*/
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN res-cancelled-list.segment = ENTRY(1, segment.bezeich, "$$0").
        ASSIGN res-cancelled-list.usr-id = reservation.useridanlage.  
    
        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              res-cancelled-list.rate-code  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
    
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN res-cancelled-list.sp-req = reslin-queasy.char3 + "," + res-cancelled-list.sp-req.
    
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
          IF AVAILABLE segment THEN ASSIGN res-cancelled-list.vip = segment.bezeich.
        END.
        ASSIGN res-cancelled-list.nat = guest.nation1.  
        /*end*/
END.
