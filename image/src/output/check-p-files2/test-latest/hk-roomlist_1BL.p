DEFINE TEMP-TABLE output-list
  FIELD location        AS CHAR
  FIELD active-flag     AS INTEGER INITIAL 99
  FIELD resnr           AS INTEGER INITIAL 0
  FIELD reslinnr        AS INTEGER INITIAL 0
  FIELD service-flag    AS LOGICAL INITIAL NO 
  FIELD flag            AS INTEGER INITIAL 0 
  FIELD ankunft         AS DATE 
  FIELD abreise         AS DATE 
  FIELD zinr            LIKE zimmer.zinr            LABEL "RmNo" INITIAL "" 
  FIELD rstat           AS CHAR FORMAT "x(23)"      LABEL "Room Status" 
  FIELD gstat           AS CHAR FORMAT "x(12)"      LABEL "Guest" 
  FIELD floor           AS INTEGER FORMAT " >> "    LABEL "Floor" 
  FIELD inactive        AS CHAR FORMAT "x(3)"       LABEL "   " 
  FIELD kbezeich        AS CHAR FORMAT "x(5)"       LABEL "Cat." 
  FIELD arrival         AS LOGICAL INITIAL NO 
  FIELD inhouse         AS LOGICAL INITIAL NO 
  FIELD zistatus        AS INTEGER 
  FIELD gastnrmember    AS INTEGER INITIAL 0 
  FIELD gname           AS CHAR FORMAT "x(32)"      LABEL "Main GuestName" 
  FIELD company         AS CHAR FORMAT "x(24)"      LABEL "Reserve Name" 
  FIELD arrtime         AS CHAR FORMAT "x(5)"       LABEL "ArrTime" 
  FIELD deptime         AS CHAR FORMAT "x(5)"       LABEL "DepTime" 
  FIELD etd             AS CHAR FORMAT "x(5)"       LABEL "ETD" 
  FIELD bemerk          AS CHAR FORMAT "x(32)"      LABEL "Reservation Comments"
  FIELD cashBasis       AS LOGICAL INITIAL NO
  FIELD vip             AS CHAR FORMAT "x(1)"       LABEL "VIP"
  FIELD spreq           AS CHAR FORMAT "x(32)"      LABEL "SpecialRequest"
  FIELD norms           AS INTEGER
  FIELD pax             AS INTEGER
  FIELD rmrate          AS DECIMAL
  FIELD argt            AS CHAR
  FIELD usr-id          AS CHAR
  FIELD nat             AS CHAR FORMAT "x(3)". 

DEF TEMP-TABLE t-history
    FIELD ankunft    LIKE history.ankunft
    FIELD abreise    LIKE history.abreise
    FIELD zinr       LIKE history.zinr
    FIELD zi-wechsel LIKE history.zi-wechsel
    FIELD bemerk     LIKE history.bemerk
    FIELD gastnr     LIKE history.gastnr.

DEFINE INPUT  PARAMETER  casetype    AS INTEGER.
DEFINE INPUT  PARAMETER  pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER  curr-date   AS DATE.
DEFINE INPUT  PARAMETER  prog-name   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER  def-cotime  AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER  pr-opt-str  AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER  ci-date     AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-history.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-roomlist".

DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(23)" NO-UNDO. 
stat-list[1] = translateExtended ("Vacant Clean Checked", lvCAREA,""). 
stat-list[2] = translateExtended ("Vacant Clean Unchecked", lvCAREA,""). 
stat-list[3] = translateExtended ("Vacant Dirty", lvCAREA,""). 
stat-list[4] = translateExtended ("Expected Departure", lvCAREA,""). 
stat-list[5] = translateExtended ("Occupied Dirty", lvCAREA,""). 
stat-list[6] = translateExtended ("Occupied Cleaned", lvCAREA,""). 
stat-list[7] = translateExtended ("Out-of-Order", lvCAREA,""). 
stat-list[8] = translateExtended ("Off-Market", lvCAREA,""). 
stat-list[9] = translateExtended ("Do not Disturb", lvCAREA,""). 
stat-list[10] = translateExtended ("Out-of-Service",lvCAREA,""). 

DEFINE VARIABLE vip-nr  AS INTEGER EXTENT 10 NO-UNDO. 
DEFINE VARIABLE resbemerk   AS CHAR NO-UNDO.
DEFINE VARIABLE his-bemerk  AS CHAR  NO-UNDO.
DEFINE VARIABLE count-i     AS INTEGER.

DEFINE BUFFER gast FOR guest. 

RUN htpdate.p (87, OUTPUT ci-date).
RUN htpchar.p (925, OUTPUT def-cotime).

FIND FIRST queasy WHERE queasy.KEY = 140 
  AND queasy.char1 = prog-name NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN pr-opt-str = queasy.char3.

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

IF casetype = 1 THEN
    RUN fill-list.
ELSE RUN fill-arrival.


FOR EACH output-list:

    /*FDL March 05, 2023 => Ticket 4C8057*/
    resbemerk = output-list.bemerk.
    resbemerk = REPLACE(resbemerk,CHR(10),"").
    resbemerk = REPLACE(resbemerk,CHR(13),"").
    resbemerk = REPLACE(resbemerk,"~n","").
    resbemerk = REPLACE(resbemerk,"\n","").
    resbemerk = REPLACE(resbemerk,"~r","").
    resbemerk = REPLACE(resbemerk,"~r~n","").
    resbemerk = REPLACE(resbemerk,"&nbsp;"," ").
    resbemerk = REPLACE(resbemerk,"</p>","</p></p>").
    resbemerk = REPLACE(resbemerk,"</p>",CHR(13)).
    resbemerk = REPLACE(resbemerk,"<BR>",CHR(13)).
    resbemerk = REPLACE(resbemerk,CHR(10) + CHR(13),"").
    resbemerk = REPLACE(resbemerk,CHR(2),"").
    resbemerk = REPLACE(resbemerk,CHR(3),"").
    resbemerk = REPLACE(resbemerk,CHR(4),"").    

    IF LENGTH(resbemerk) LT 3 THEN resbemerk = REPLACE(resbemerk,CHR(32),"").
    IF LENGTH(resbemerk) LT 3 THEN resbemerk = "".
    IF LENGTH(resbemerk) EQ ? THEN resbemerk = "".

    DO count-i = 1 TO 31:
        IF resbemerk MATCHES CHR(count-i) THEN resbemerk = REPLACE(resbemerk,CHR(count-i),"").
    END.
    DO count-i = 127 TO 255:
        IF resbemerk MATCHES CHR(count-i) THEN resbemerk = REPLACE(resbemerk,CHR(count-i),"").
    END.

    output-list.bemerk = resbemerk.
    resbemerk = "".

    FOR EACH history WHERE history.gastnr = output-list.gastnrmember 
        AND history.abreise LE TODAY USE-INDEX hist_index NO-LOCK:
        CREATE t-history.
        ASSIGN
            t-history.ankunft    = history.ankunft
            t-history.abreise    = history.abreise
            t-history.zinr       = history.zinr
            t-history.zi-wechsel = history.zi-wechsel
            /*t-history.bemerk     = history.bemerk*/
            t-history.gastnr     = history.gastnr.
        
        /*FDL March 05, 2023 => Ticket 4C8057*/
        his-bemerk = history.bemerk.        
        his-bemerk = REPLACE(his-bemerk,CHR(10),"").
        his-bemerk = REPLACE(his-bemerk,CHR(13),"").
        his-bemerk = REPLACE(his-bemerk,"~n","").
        his-bemerk = REPLACE(his-bemerk,"\n","").
        his-bemerk = REPLACE(his-bemerk,"~r","").
        his-bemerk = REPLACE(his-bemerk,"~r~n","").
        his-bemerk = REPLACE(his-bemerk,"&nbsp;"," ").
        his-bemerk = REPLACE(his-bemerk,"</p>","</p></p>").
        his-bemerk = REPLACE(his-bemerk,"</p>",CHR(13)).
        his-bemerk = REPLACE(his-bemerk,"<BR>",CHR(13)).
        his-bemerk = REPLACE(his-bemerk,CHR(10) + CHR(13),"").
        his-bemerk = REPLACE(his-bemerk,CHR(2),"").
        his-bemerk = REPLACE(his-bemerk,CHR(3),"").
        his-bemerk = REPLACE(his-bemerk,CHR(4),"").
    
        IF LENGTH(his-bemerk) LT 3 THEN his-bemerk = REPLACE(his-bemerk,CHR(32),"").
        IF LENGTH(his-bemerk) LT 3 THEN his-bemerk = "".
        IF LENGTH(his-bemerk) EQ ? THEN his-bemerk = "".

        t-history.bemerk = his-bemerk.
        his-bemerk = "".
    END.
END.

/********************************************************************************/
PROCEDURE fill-list:
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE anz AS INTEGER. 
  DEFINE VARIABLE off-market AS LOGICAL. 
  
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH zimmer NO-LOCK BY (zimmer.zinr): 
    off-market = NO. 
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
      AND outorder.betriebsnr = 2 
      AND outorder.gespstart LE ci-date AND outorder.gespende GE ci-date 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE outorder THEN off-market = YES. 
    
    CREATE output-list. 
    ASSIGN
      output-list.location  = zimmer.CODE
      output-list.floor     = zimmer.etage
      output-list.zinr      = zimmer.zinr
      output-list.kbezeich  = zimmer.kbezeich
      output-list.zistatus  = zimmer.zistatus
    . 
    
    IF NOT zimmer.sleeping THEN output-list.inactive = "  I". 
    IF off-market THEN 
    DO: 
      output-list.rstat = stat-list[8]. 
      output-list.zistatus = 7. 
    END. 
    ELSE output-list.rstat = stat-list[zimmer.zistatus + 1]. 
 
    IF output-list.zistatus = 6 THEN /* Malik Serverless : output-list.zistat -> output-list.zistatus */
    DO: 
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder AND outorder.betriebsnr GT 2 THEN 
        DO: 
          output-list.service-flag = YES. 
          output-list.rstat = stat-list[10]. 
          output-list.zistatus = 9. 
        END. 
    END. 
    
    IF (zimmer.zistatus GE 3 AND zimmer.zistatus LE 5) OR zimmer.zistatus = 8 
    THEN 
    DO: 
      FIND FIRST res-line WHERE res-line.resstatus = 6 
        AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
        FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK. 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
        FIND FIRST output-list WHERE output-list.zinr = res-line.zinr. 
        IF guest.karteityp = 0 THEN output-list.gastnrmember = res-line.gastnrmember. 
 
        ASSIGN
          output-list.inhouse      = YES
          output-list.resnr        = res-line.resnr
          output-list.reslinnr     = res-line.reslinnr
          output-list.active-flag  = res-line.active-flag
          output-list.ankunft      = res-line.ankunft 
          output-list.abreise      = res-line.abreise 
          anz = res-line.erwachs + res-line.gratis 
          output-list.bemerk       =  /*reservation.bemerk*/  res-line.bemerk
          output-list.norms        = res-line.zimmeranz   /*wen*/
          output-list.pax          = res-line.erwachs
          output-list.rmrate       = res-line.zipreis
          output-list.argt         = res-line.arrangement
          output-list.usr-id       = reservation.useridanlage
.

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
        RUN check-vip-guest(OUTPUT output-list.vip).
        
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN output-list.spreq = reslin-queasy.char3 + "," + output-list.spreq.
        /*end*/
 
        FIND FIRST queasy WHERE queasy.KEY = 24 AND queasy.char1 = res-line.zinr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          output-list.bemerk = OUTPUT-list.bemerk + CHR(10) + CHR(10) + 
              translateExtended ("Guest Preference:",lvCAREA,"") + CHR(10). 
          FOR EACH queasy WHERE queasy.KEY = 24 AND queasy.char1 = res-line.zinr 
            NO-LOCK BY queasy.date1: 
            output-list.bemerk = output-list.bemerk + queasy.char3 + CHR(10). 
          END. 
        END. 
        IF res-line.ankzeit NE 0 THEN 
          output-list.arrtime = STRING(res-line.ankzeit,"HH:MM"). 
 
        IF res-line.abreisezeit NE 0 THEN 
          output-list.deptime = STRING(res-line.abreisezeit,"HH:MM"). 
 
        IF SUBSTR(res-line.flight-nr,18,4) NE "0000" 
          AND SUBSTR(res-line.flight-nr,18,4) NE "    " THEN 
          output-list.etd = SUBSTR(res-line.flight-nr, 18, 2) 
            + ":" + SUBSTR(res-line.flight-nr, 20, 2). 
 
        IF output-list.gname = "" THEN 
        DO: 
          output-list.gname = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1. 
          output-list.company = gast.NAME. 
          output-list.nat = guest.nation1.   /*wen*/
        END. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
          IF anz LE 2 THEN DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "U". 
          END. 
          ELSE output-list.gstat = output-list.gstat + STRING(anz) + "U". 
          DO i = 1 TO res-line.kind1: 
            output-list.gstat = output-list.gstat + "u". 
          END. 
          DO i = 1 TO res-line.kind2: 
            output-list.gstat = output-list.gstat + "C". 
          END. 
        END. 
        ELSE IF res-line.abreise = today THEN 
        DO: 
          IF anz LE 2 THEN DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "D". 
          END. 
          ELSE output-list.gstat = output-list.gstat + STRING(anz) + "D". 
          DO i = 1 TO res-line.kind1: 
            output-list.gstat = output-list.gstat + "d". 
          END. 
          DO i = 1 TO res-line.kind2: 
            output-list.gstat = output-list.gstat + "C". 
          END. 
        END. 
        ELSE 
        DO: 
          IF anz LE 2 THEN DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "R". 
          END. 
          ELSE output-list.gstat = output-list.gstat + STRING(anz) + "R". 
          DO i = 1 TO res-line.kind1: 
            output-list.gstat = output-list.gstat + "r". 
          END. 
          DO i = 1 TO res-line.kind2: 
            output-list.gstat = output-list.gstat + "C". 
          END. 
        END. 
      END. 
 
      IF zimmer.zistatus = 3 THEN 
      DO: 
        FIND FIRST res-line WHERE res-line.active-flag = 0 
          AND (res-line.resstatus LE 2 OR res-line.resstatus = 5)
          AND res-line.ankunft = ci-date 
          AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
        IF AVAILABLE res-line THEN 
        DO: 
          FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
          FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK. 
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
 
          CREATE output-list. 
          ASSIGN
            output-list.resnr        = res-line.resnr
            output-list.reslinnr     = res-line.reslinnr
            output-list.ankunft      = res-line.ankunft
            output-list.abreise      = res-line.abreise 
            output-list.active-flag  = res-line.active-flag
            output-list.norms        = res-line.zimmeranz   /*wen*/
            output-list.pax          = res-line.erwachs
            output-list.rmrate       = res-line.zipreis
            output-list.argt         = res-line.arrangement.

              /*ITA 130717 --> Add Request Patra*/
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
            RUN check-vip-guest(OUTPUT output-list.vip).
            
            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
                 AND reslin-queasy.resnr = res-line.resnr 
                 AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
                 ASSIGN output-list.spreq = reslin-queasy.char3 + "," + output-list.spreq.
            /*end*/

          IF guest.karteityp = 0 THEN 
              output-list.gastnrmember = res-line.gastnrmember. 
          ASSIGN 
            output-list.location = zimmer.CODE
            output-list.floor    = zimmer.etage 
            output-list.zinr     = zimmer.zinr 
            output-list.kbezeich = zimmer.kbezeich 
            output-list.zistatus = zimmer.zistatus. 
          IF NOT zimmer.sleeping THEN output-list.inactive = "  I". 
          IF off-market THEN 
          DO: 
            output-list.rstat = stat-list[8]. 
            output-list.zistatus = 7. 
          END. 
          ELSE output-list.rstat = stat-list[zimmer.zistatus + 1]. 
          output-list.bemerk = /*reservation.bemerk*/  res-line.bemerk. 
          IF output-list.gname = "" THEN 
          DO: 
            output-list.gname = guest.name + ", " + guest.vorname1 
              + " " + guest.anrede1. 
            output-list.company = gast.NAME. 
            output-list.nat = guest.nation1.   /*wen*/
          END. 
          output-list.arrival = YES. 
          
          anz = res-line.erwachs + res-line.gratis. 
          IF anz LE 2 THEN DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "A". 
          END. 
          ELSE output-list.gstat = output-list.gstat + STRING(anz) + "A". 

          anz = res-line.kind1 + res-line.l-zuordnung[4].
          IF anz LE 2 THEN DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "a". 
          END. 
          ELSE output-list.gstat = output-list.gstat + STRING(anz) + "a".
          
          DO i = 1 TO res-line.kind2: 
            output-list.gstat = output-list.gstat + "C". 
          END. 
 
          IF SUBSTR(res-line.flight-nr,7,4) NE "0000" 
            AND SUBSTR(res-line.flight-nr,7,4) NE "    " THEN 
            output-list.arrtime = SUBSTR(res-line.flight-nr, 7, 2) 
              + ":" + SUBSTR(res-line.flight-nr,9,2). 
 
        END. 
      END. 
 
    END. 
    ELSE IF zimmer.zistatus LE 2 THEN 
    DO: 
      IF zimmer.zistatus = 2 THEN 
      DO: 
        FIND FIRST res-line WHERE res-line.resstatus EQ 8 AND 
          res-line.active-flag = 2 
          AND res-line.abreise = ci-date AND res-line.zinr = zimmer.zinr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE res-line THEN 
        DO: 
            ASSIGN
                output-list.arrtime = STRING(res-line.ankzeit, "HH:MM")
                output-list.deptime = STRING(res-line.abreisezeit, "HH:MM").
          FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
          FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK. 
          FIND FIRST output-list WHERE output-list.zinr = res-line.zinr 
            NO-ERROR. 
          IF AVAILABLE output-list THEN 
          DO: 
            IF guest.karteityp = 0 THEN 
                output-list.gastnrmember = res-line.gastnrmember. 
            output-list.rstat = output-list.rstat  + " *". 
          END. 
        END. 
      END. 
      FIND FIRST res-line WHERE (resstatus LE 2 OR resstatus = 5)
        AND res-line.active-flag = 0 
        AND res-line.ankunft = ci-date AND res-line.zinr = zimmer.zinr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
        FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK.
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
        FIND FIRST output-list WHERE output-list.zinr = res-line.zinr. 
        IF guest.karteityp = 0 THEN output-list.gastnrmember = res-line.gastnrmember. 
        output-list.bemerk = /*reservation.bemerk */ res-line.bemerk. 
        IF output-list.gname = "" THEN 
        DO: 
          /*ITA 130717 --> Add Request Patra*/
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
            RUN check-vip-guest(OUTPUT output-list.vip).
            
            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
                 AND reslin-queasy.resnr = res-line.resnr 
                 AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
                 ASSIGN output-list.spreq = reslin-queasy.char3 + "," + output-list.spreq.
            /*end*/

          output-list.gname = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1. 
          output-list.company = gast.NAME. 
          output-list.nat = guest.nation1 .  /*wen*/
        END. 
        ASSIGN
          output-list.ankunft = res-line.ankunft
          output-list.abreise = res-line.abreise
          output-list.arrival = YES. 
        
        anz = res-line.erwachs + res-line.gratis. 
        IF anz LE 2 THEN DO i = 1 TO anz: 
          output-list.gstat = output-list.gstat + "A". 
        END. 
        ELSE output-list.gstat = output-list.gstat + STRING(anz) + "A". 

        anz = res-line.kind1 + res-line.l-zuordnung[4].
        IF anz LE 2 THEN DO i = 1 TO anz: 
          output-list.gstat = output-list.gstat + "a". 
        END. 
        ELSE output-list.gstat = output-list.gstat + STRING(anz) + "a".

        DO i = 1 TO res-line.kind2: 
          output-list.gstat = output-list.gstat + "C". 
        END. 
 
        IF res-line.ankzeit NE 0 THEN 
          output-list.arrtime = STRING(res-line.ankzeit, "HH:MM").
        ELSE IF SUBSTR(res-line.flight-nr,7,4) NE "0000" 
          AND SUBSTR(res-line.flight-nr,7,4) NE "    " THEN 
          output-list.arrtime = SUBSTR(res-line.flight-nr, 7, 2) 
          + ":" + SUBSTR(res-line.flight-nr,9,2). 
        
      END. 
    END. 
  END. 
  
  FOR EACH res-line WHERE res-line.active-flag = 0 
    AND (res-line.resstatus LE 2 OR res-line.resstatus = 5)
    AND res-line.zinr = "" AND res-line.ankunft = ci-date 
    NO-LOCK BY res-line.zikatnr BY res-line.name: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
    FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK. 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
 
    CREATE output-list. 
    ASSIGN
        output-list.resnr        = res-line.resnr
        output-list.reslinnr     = res-line.reslinnr
        output-list.active-flag  = res-line.active-flag
        output-list.ankunft      = res-line.ankunft
        output-list.abreise      = res-line.abreise
        output-list.norms        = res-line.zimmeranz   /*wen*/
        output-list.pax          = res-line.erwachs
        output-list.rmrate       = res-line.zipreis
        output-list.argt         = res-line.arrangement
    . 
 
    IF guest.karteityp = 0 THEN output-list.gastnrmember = res-line.gastnrmember. 
    output-list.flag = 1. 
    output-list.kbezeich = zimkateg.kurzbez. 
    output-list.zinr = "#" + TRIM(STRING(res-line.zimmeranz,">>9")). 
    output-list.bemerk = /*reservation.bemerk*/  res-line.bemerk. 
    output-list.gname = res-line.name. 
    output-list.company = gast.NAME. 
    output-list.arrival = YES. 

    /*ITA 130717 --> Add Request Patra*/
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
        RUN check-vip-guest(OUTPUT output-list.vip).
        
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN output-list.spreq = reslin-queasy.char3 + "," + output-list.spreq.
        /*end*/

    anz = res-line.erwachs + res-line.gratis. 
    IF anz LE 2 THEN DO i = 1 TO anz: 
      output-list.gstat = output-list.gstat + "A". 
    END. 
    ELSE output-list.gstat = output-list.gstat + STRING(anz) + "A". 

    anz = res-line.kind1 + res-line.l-zuordnung[4].
    IF anz LE 2 THEN DO i = 1 TO anz: 
      output-list.gstat = output-list.gstat + "a". 
    END. 
    ELSE output-list.gstat = output-list.gstat + STRING(anz) + "a".

    DO i = 1 TO res-line.kind2: 
      output-list.gstat = output-list.gstat + "C". 
    END. 
 
    IF SUBSTR(res-line.flight-nr,7,4) NE "0000" 
      AND SUBSTR(res-line.flight-nr,7,4) NE "    " THEN 
      output-list.arrtime = SUBSTR(res-line.flight-nr, 7, 2) 
        + ":" + SUBSTR(res-line.flight-nr,9,2). 
 
  END. 
  
  FOR EACH res-line WHERE res-line.active-flag = 2 
    AND res-line.resstatus = 8
    AND res-line.l-zuordnung[3] = 0
    AND res-line.abreise = ci-date 
    NO-LOCK BY res-line.zikatnr BY res-line.name: 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK.
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
    FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK. 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
 
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
      AND outorder.betriebsnr = 2 
      AND outorder.gespstart LE ci-date AND outorder.gespende GE ci-date 
      NO-LOCK NO-ERROR. 
    off-market = AVAILABLE outorder.

    CREATE output-list. 
    ASSIGN
        output-list.resnr       = res-line.resnr
        output-list.reslinnr    = res-line.reslinnr
        output-list.active-flag = res-line.active-flag
        output-list.ankunft     = res-line.ankunft
        output-list.abreise     = res-line.abreise
        output-list.arrtime     = STRING(res-line.ankzeit, "HH:MM")
        output-list.deptime     = STRING(res-line.abreisezeit, "HH:MM")
        output-list.flag        = 2
        output-list.kbezeich    = zimkateg.kurzbez
        output-list.zinr        = res-line.zinr
        output-list.location    = zimmer.CODE
        output-list.zistatus    = zimmer.zistatus
        output-list.bemerk      =  /*reservation.bemerk*/  res-line.bemerk 
        output-list.gname       = res-line.NAME
        output-list.company     = gast.NAME
        output-list.arrival     = NO    
        output-list.norms        = res-line.zimmeranz   /*wen*/
        output-list.pax          = res-line.erwachs
        output-list.rmrate       = res-line.zipreis
        output-list.argt         = res-line.arrangement
    . 

    /*ITA 130717 --> Add Request Patra*/
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
        RUN check-vip-guest(OUTPUT output-list.vip).
        
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN output-list.spreq = reslin-queasy.char3 + "," + output-list.spreq.
        /*end*/

    IF guest.karteityp = 0 THEN output-list.gastnrmember = res-line.gastnrmember. 
    
    anz = res-line.erwachs + res-line.gratis. 
    IF anz LE 2 THEN DO i = 1 TO anz: 
      output-list.gstat = output-list.gstat + "*". 
    END. 
    ELSE output-list.gstat = output-list.gstat + STRING(anz) + "*". 

    anz = res-line.kind1 + res-line.l-zuordnung[4].
    IF anz LE 2 THEN DO i = 1 TO anz: 
      output-list.gstat = output-list.gstat + "o". 
    END. 
    ELSE output-list.gstat = output-list.gstat + STRING(anz) + "o".

    DO i = 1 TO res-line.kind2: 
      output-list.gstat = output-list.gstat + "C". 
    END. 
 
    IF off-market THEN 
    DO: 
      output-list.rstat = stat-list[8]. 
      output-list.zistatus = 7. 
    END. 
    ELSE output-list.rstat = stat-list[zimmer.zistatus + 1]. 
    
         IF SUBSTR(res-line.flight-nr,7,4) NE "0000" 
      AND SUBSTR(res-line.flight-nr,7,4) NE "    " THEN 
      output-list.arrtime = SUBSTR(res-line.flight-nr, 7, 2) 
        + ":" + SUBSTR(res-line.flight-nr,9,2). 
 
  END. 

  FOR EACH output-list WHERE output-list.gastnrmember GT 0 NO-LOCK: 
    FIND FIRST guest WHERE guest.gastnr = output-list.gastnrmember NO-LOCK. 
    IF guest.bemerk NE "" THEN output-list.bemerk = guest.bemerk + CHR(10) 
        + output-list.bemerk. 
  END. 

  RUN fill-cashBasis.
END. 


PROCEDURE fill-arrival: 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE anz AS INTEGER. 
  DEFINE VARIABLE off-market AS LOGICAL. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH res-line WHERE res-line.active-flag = 0 
    AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) 
    AND res-line.ankunft = curr-date 
    NO-LOCK BY res-line.zikatnr BY res-line.name: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
    FIND FIRST gast WHERE gast.gastnr = res-line.gastnr NO-LOCK. 
 
    CREATE output-list. 
    ASSIGN
        output-list.resnr        = res-line.resnr
        output-list.reslinnr     = res-line.reslinnr
        output-list.active-flag  = res-line.active-flag
        output-list.ankunft      = res-line.ankunft
        output-list.abreise      = res-line.abreise
        output-list.norms        = res-line.zimmeranz   /*wen*/
        output-list.pax          = res-line.erwachs
        output-list.rmrate       = res-line.zipreis
        output-list.argt         = res-line.arrangement
    . 
 
    IF guest.karteityp = 0 THEN output-list.gastnrmember = res-line.gastnrmember. 
    IF res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      ASSIGN
        output-list.location = zimmer.CODE
        output-list.floor = zimmer.etage
        output-list.zinr = zimmer.zinr
        output-list.kbezeich = zimmer.kbezeich 
        output-list.zistatus = zimmer.zistatus
      . 
      IF NOT zimmer.sleeping THEN output-list.inactive = "  I". 
      IF off-market THEN 
      DO: 
        output-list.rstat = stat-list[8]. 
        output-list.zistatus = 7. 
      END. 
      ELSE output-list.rstat = stat-list[zimmer.zistatus + 1]. 
    END. 
    ELSE 
    DO: 
      output-list.flag = 1. 
      output-list.kbezeich = zimkateg.kurzbez. 
      output-list.zinr = "#" + TRIM(STRING(res-line.zimmeranz,">>9")). 
    END. 
    output-list.bemerk = /*reservation.bemerk*/  res-line.bemerk. 
    output-list.gname = res-line.name. 
    output-list.company = gast.NAME. 
    output-list.arrival = YES. 

    /*ITA 130717 --> Add Request Patra*/
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
        RUN check-vip-guest(OUTPUT output-list.vip).
        
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN output-list.spreq = reslin-queasy.char3 + "," + output-list.spreq.
        /*end*/
    
    anz = res-line.erwachs + res-line.gratis. 
    IF anz LE 2 THEN DO i = 1 TO anz: 
      output-list.gstat = output-list.gstat + "A". 
    END. 
    ELSE output-list.gstat = output-list.gstat + STRING(anz) + "A". 
    
    anz = res-line.kind1 + res-line.l-zuordnung[4].
    IF anz LE 2 THEN DO i = 1 TO anz: 
      output-list.gstat = output-list.gstat + "a". 
    END. 
    ELSE output-list.gstat = output-list.gstat + STRING(anz) + "a".

    DO i = 1 TO res-line.kind2: 
      output-list.gstat = output-list.gstat + "C". 
    END. 
 
    IF SUBSTR(res-line.flight-nr,7,4) NE "0000" 
      AND SUBSTR(res-line.flight-nr,7,4) NE "    " THEN 
      output-list.arrtime = SUBSTR(res-line.flight-nr, 7, 2) 
        + ":" + SUBSTR(res-line.flight-nr,9,2). 
 
  END. 
  RUN fill-cashBasis.
END. 


PROCEDURE fill-cashBasis:
DEF BUFFER rline FOR res-line.
  FOR EACH output-list WHERE output-list.resnr GT 0:
      FIND FIRST rline WHERE rline.resnr = output-list.resnr
          AND rline.reslinnr = output-list.reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE rline AND INTEGER(rline.CODE) NE 0 THEN
      DO:
        FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 AND vhp.queasy.number1 = 
          INTEGER(rline.code) NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN 
          output-list.cashBasis = YES.
      END.
  END.
END.


PROCEDURE check-vip-guest:
DEF OUTPUT PARAMETER c-vip AS CHAR NO-UNDO INIT "".
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
      FIND FIRST segment WHERE 
          segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE segment THEN ASSIGN 
          c-vip = segment.bezeich + " ".
    END.
END.

