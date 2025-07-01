
DEFINE TEMP-TABLE output-list 
  FIELD personal        AS LOGICAL INITIAL NO
  FIELD reihenfolge     AS INTEGER INITIAL 0
  FIELD SELECTED        AS LOGICAL INITIAL NO 
  FIELD cleanflag       AS LOGICAL INITIAL NO 
  FIELD odd-even        AS INTEGER INITIAL 0 
  FIELD flag            AS INTEGER INITIAL 1 
  FIELD zinr            LIKE zimmer.zinr            LABEL "RmNo" 
  FIELD rstat           AS CHAR FORMAT "x(20)"      LABEL "Room Status" 
  FIELD rstat1          AS CHAR FORMAT "x(2)" 
  FIELD departed        AS CHAR FORMAT "x(1)" INITIAL " " 
  FIELD gstat           AS CHAR FORMAT "x(12)"      LABEL "Guest" 
  FIELD floor           AS INTEGER FORMAT ">9"      LABEL "FL" 
  FIELD code            AS CHAR 
  FIELD inactive        AS CHAR FORMAT "x(1)"       LABEL "I" 
  FIELD ldry            AS CHAR FORMAT "x(2)"       LABEL "LD" 
  FIELD towel           AS CHAR FORMAT "x(2)"       LABEL "TW" 
  FIELD kbezeich        AS CHAR FORMAT "x(12)"      LABEL "Description" 
  FIELD arrival         AS LOGICAL INITIAL NO 
  FIELD ankunft         AS DATE                     LABEL "Arrival" 
  FIELD abreise         AS DATE                     LABEL "Departure" 
  FIELD nation          AS CHAR FORMAT "x(3)"       LABEL "Nation" 
  FIELD zistatus        AS INTEGER 
  FIELD gname           AS CHAR FORMAT "x(32)"      LABEL "Main GuestName" 
  FIELD resname         AS CHAR FORMAT "x(48)"      LABEL "Reserve Name" 
  FIELD bemerk          AS CHAR FORMAT "x(50)"      LABEL "Reservation Comments"
  FIELD rsv-flag        AS LOGICAL INITIAL NO
  FIELD co-time         AS CHAR FORMAT "x(8)"       LABEL "DepTime"
  FIELD vip             AS CHAR FORMAT "x(7)"       LABEL "VIP". 


DEFINE INPUT PARAMETER  pvILanguage     AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-zimaid".

DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(20)" NO-UNDO. 
  stat-list[1]  = translateExtended ("Vacant Clean Checked", lvCAREA,""). 
  stat-list[2]  = translateExtended ("Vac. Clean Unchecked", lvCAREA,""). 
  stat-list[3]  = translateExtended ("Vacant Dirty", lvCAREA,""). 
  stat-list[4]  = translateExtended ("Expected Departure", lvCAREA,""). 
  stat-list[5]  = translateExtended ("Occupied Dirty", lvCAREA,""). 
  stat-list[6]  = translateExtended ("Occupied Cleaned", lvCAREA,""). 
  stat-list[7]  = translateExtended ("Out-of-Order", lvCAREA,""). 
  stat-list[8]  = translateExtended ("Off-Market", lvCAREA,""). 
  stat-list[9]  = translateExtended ("Do not Disturb", lvCAREA,""). 
  stat-list[10] = translateExtended ("Out of Service", lvCAREA,""). 


DEFINE VARIABLE stat-list1 AS CHAR EXTENT 11 FORMAT "x(2)" 
  INITIAL [ "VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "DD", "OS", "EA" ]. 

DEFINE VARIABLE vip-nr  AS INTEGER EXTENT 10 NO-UNDO. 

RUN fill-vipnr.
RUN fill-list.

DEF VAR resbemerk AS CHAR.
FOR EACH output-list:
    /*MASDOD 08092023 Fixing HK Room Attendant Report Data not display all*/
    resbemerk = "".
    resbemerk = output-list.bemerk.
    resbemerk = REPLACE(resbemerk,CHR(10),"").
    resbemerk = REPLACE(resbemerk,CHR(13),"").
    resbemerk = REPLACE(resbemerk,"~n","").
    resbemerk = REPLACE(resbemerk,"\n","").
    resbemerk = REPLACE(resbemerk,"~r","").
    resbemerk = REPLACE(resbemerk,"~r~n","").
    resbemerk = REPLACE(resbemerk,CHR(10) + CHR(13),"").

    IF LENGTH(resbemerk) LT 3 THEN resbemerk = REPLACE(resbemerk,CHR(32),"").
    IF LENGTH(resbemerk) EQ ? THEN resbemerk = "".

    output-list.bemerk = TRIM(resbemerk).
    resbemerk = "".
END.

PROCEDURE fill-vipnr: 
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
END. 

PROCEDURE fill-list: 
DEFINE VARIABLE i           AS INTEGER NO-UNDO. 
DEFINE VARIABLE anz         AS INTEGER NO-UNDO. 
DEFINE VARIABLE ci-date     AS DATE    NO-UNDO. 
DEFINE VARIABLE off-market  AS LOGICAL NO-UNDO. 
DEFINE VARIABLE ldry        AS INTEGER NO-UNDO. 
DEFINE VARIABLE towel       AS INTEGER NO-UNDO. 
DEFINE VARIABLE c-vip       AS CHAR    NO-UNDO.

  FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
  ci-date = htparam.fdate. 
  FIND FIRST htparam WHERE paramnr = 159 NO-LOCK. 
  ldry = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 218 NO-LOCK. 
  towel = htparam.finteger. 
 
  FOR EACH zimmer WHERE ((zistatus GE 0 AND zistatus LE 6) OR zistatus = 8) NO-LOCK BY zimmer.zinr: 
    off-market = NO. 
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr AND outorder.betriebsnr = 2 AND outorder.gespstart LE ci-date AND outorder.gespende GE ci-date NO-LOCK NO-ERROR. 
    IF AVAILABLE outorder THEN off-market = YES. 
 
    CREATE output-list. 
    ASSIGN
      output-list.reihenfolge   = zimmer.reihenfolge
      output-list.personal      = zimmer.personal
      output-list.floor         = zimmer.etage 
      output-list.zinr          = zimmer.zinr  
      output-list.zistatus      = zimmer.zistatus 
      output-list.kbezeich      = zimmer.kbezeich 
      output-list.code          = zimmer.CODE.

    IF output-list.reihenfolge = 0 THEN
        output-list.reihenfolge = 1.

    IF SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "1" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "3" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "5" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "7" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "9" THEN 
        output-list.odd-even = 1. 
    ELSE IF SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "0" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "2" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "4" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "6" OR 
        SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "8" THEN 
        output-list.odd-even = 2. 
 
    IF off-market THEN 
    ASSIGN
      output-list.zistatus = 7
      output-list.rstat = stat-list[8]
      output-list.rstat1 = stat-list1[8] 
    . 
    ELSE 
    ASSIGN
      output-list.rstat = stat-list[zimmer.zistatus + 1]
      output-list.rstat1 = stat-list1[zimmer.zistatus + 1] 
    . 
 
    IF output-list.zistatus = 6 THEN 
    DO: 
      FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE outorder THEN output-list.gname = outorder.gespgrund.
      IF AVAILABLE outorder AND (outorder.betriebsnr = 3 OR outorder.betriebsnr = 4) THEN 
      ASSIGN
          output-list.zistatus = 9
          output-list.rstat    = stat-list[10] 
          output-list.rstat1   = stat-list1[10] 
      . 
    END. 
 
    IF NOT zimmer.sleeping THEN output-list.inactive = "I". 
    IF zimmer.zistatus EQ 0 THEN 
    ASSIGN
      output-list.cleanflag = YES 
      output-list.flag = 0 
    . 
    IF (zimmer.zistatus GE 3 AND zimmer.zistatus LE 5) OR zimmer.zistatus = 8 THEN DO: 
      FIND FIRST res-line WHERE res-line.resstatus = 6 
        AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
        ASSIGN output-list.resnam = guest.NAME
            output-list.co-time = STRING(res-line.abreisezeit, "HH:MM:SS").

        /*ITA 060717 --> for special request*/
         FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
         IF AVAILABLE reslin-queasy THEN
             ASSIGN output-list.code = output-list.CODE + "," + reslin-queasy.char3.
        /*end*/
         /*masdod 051224 validate code value ticket #700033*/ /*FDL Ticket 23A90B - Add LENGTH(output-list.code) GT 0*/         
         IF LENGTH(output-list.code) GT 0 AND SUBSTRING(output-list.code,LENGTH(output-list.code),1) EQ "," THEN
         DO:
             output-list.CODE = SUBSTRING(output-list.code,1,LENGTH(output-list.code) - 1).
         END.

        IF ldry NE 0 AND ci-date GT res-line.ankunft THEN 
        DO: 
          IF (ci-date - res-line.ankunft) MODULO ldry = 0 THEN 
            output-list.ldry = "LD". 
        END. 
        IF towel NE 0 AND ci-date GT res-line.ankunft THEN 
        DO: 
          IF (ci-date - res-line.ankunft) MODULO towel = 0 THEN 
            output-list.towel = "TW". 
        END. 
        FIND FIRST output-list WHERE output-list.zinr = res-line.zinr 
            NO-ERROR. 
        IF AVAILABLE output-list THEN 
        DO: 
          ASSIGN
            output-list.bemerk = res-line.bemerk
            output-list.flag = 1 
          .
          DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
            IF guest.vorname1 NE "" THEN
              output-list.resname = guest.NAME + ", " + guest.vorname1.
            ELSE ASSIGN output-list.resnam = guest.NAME.
          END.

          IF output-list.gname = "" THEN 
          DO: 
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
            RUN check-vip-guest(OUTPUT c-vip).
            output-list.gname = guest.name + ", " + guest.vorname1 
              + " " + guest.anrede1. 
            output-list.nation = guest.nation1. 
            IF c-vip NE "" THEN ASSIGN output-list.vip = c-vip.
          END. 
          output-list.ankunft = res-line.ankunft. 
          output-list.abreise = res-line.abreise. 
          IF res-line.ankunft = res-line.abreise THEN 
          DO: 
            anz = res-line.erwachs + res-line.gratis. 
            IF anz LE 2 THEN 
            DO i = 1 TO anz: 
              output-list.gstat = output-list.gstat + "U". 
            END. 
            ELSE output-list.gstat = STRING(anz) + "U". 
            
            anz = res-line.kind1 + res-line.l-zuordnung[4]. 
            IF anz LE 2 THEN 
            DO i = 1 TO anz: 
              output-list.gstat = output-list.gstat + "u". 
            END. 
            ELSE output-list.gstat = output-list.gstat 
                + STRING(anz) + "u". 

            DO i = 1 TO res-line.kind2: 
              output-list.gstat = output-list.gstat + "C". 
            END. 

          END. 

          ELSE IF res-line.abreise = ci-date THEN 
          DO: 
            ASSIGN
              output-list.zistatus = 3
              output-list.rstat    = stat-list[4] 
              output-list.rstat1   = stat-list1[4] 
            . 
            anz = res-line.erwachs + res-line.gratis. 
            IF anz LE 2 THEN 
            DO i = 1 TO anz: 
              output-list.gstat = output-list.gstat + "D". 
            END. 
            ELSE output-list.gstat = STRING(anz) + "D". 
            
            anz = res-line.kind1 + res-line.l-zuordnung[4]. 
            IF anz LE 2 THEN 
            DO i = 1 TO anz: 
              output-list.gstat = output-list.gstat + "d". 
            END. 
            ELSE output-list.gstat = output-list.gstat 
                + STRING(anz) + "d". 

            DO i = 1 TO res-line.kind2: 
              output-list.gstat = output-list.gstat + "C". 
            END. 
          END. 
          ELSE 
          DO: 
            anz = res-line.erwachs + res-line.gratis. 
            IF anz LE 2 THEN 
            DO i = 1 TO anz: 
              output-list.gstat = output-list.gstat + "R". 
            END. 
            ELSE output-list.gstat = STRING(anz) + "R".

            anz = res-line.kind1 + res-line.l-zuordnung[4]. 
            IF anz LE 2 THEN 
            DO i = 1 TO anz: 
              output-list.gstat = output-list.gstat + "r". 
            END. 
            ELSE output-list.gstat = output-list.gstat + STRING(anz) + "r". 

            DO i = 1 TO res-line.kind2: 
              output-list.gstat = output-list.gstat + "C". 
            END. 
          
          END. 
        END. 
      END. 
    END. 
    ELSE IF zimmer.zistatus LE 2 THEN 
    DO: 
      IF zimmer.zistatus = 2 THEN 
      DO: 
        IF ldry NE 0 THEN output-list.ldry = "LD". 
        IF towel NE 0 THEN output-list.towel = "TW". 
        FIND FIRST res-line WHERE resstatus EQ 8 AND active-flag = 2 
          AND res-line.abreise = ci-date AND res-line.zinr = zimmer.zinr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE res-line THEN 
        DO: 
/*        output-list.rstat = output-list.rstat + " *". */ 
          output-list.gstat = output-list.gstat + "*". 
/*        output-list.departed = "*".  */ 
        END. 
      END. 
 
      FIND FIRST res-line WHERE (resstatus LE 2 OR resstatus = 5) 
        AND active-flag = 0 
        AND res-line.ankunft = ci-date AND res-line.zinr = zimmer.zinr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        FIND FIRST output-list WHERE output-list.zinr = res-line.zinr 
            NO-ERROR. 
        IF AVAILABLE output-list THEN 
        DO: 
          output-list.bemerk = res-line.bemerk. 
          output-list.flag = 1. 
          DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
            IF guest.vorname1 NE "" THEN
              output-list.resname = guest.NAME + ", " + guest.vorname1.
            ELSE ASSIGN output-list.resnam = guest.NAME.
          END.
          IF output-list.gname = "" THEN 
          DO: 
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
            RUN check-vip-guest(OUTPUT c-vip).
            output-list.gname = guest.name + ", " + guest.vorname1 
              + " " + guest.anrede1. 
            output-list.nation = guest.nation1. 
            IF c-vip NE "" THEN ASSIGN output-list.vip = c-vip.
          END. 
          ASSIGN
            output-list.ankunft = res-line.ankunft
            output-list.abreise = res-line.abreise
            output-list.arrival = YES
            anz = res-line.erwachs + res-line.gratis
          .
          IF anz LE 2 THEN 
          DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "A". 
          END. 
          ELSE output-list.gstat = output-list.gstat 
              + STRING(anz) + "A". 
          
          anz = res-line.kind1 + res-line.l-zuordnung[4].
          IF anz LE 2 THEN 
          DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "a". 
          END. 
          ELSE output-list.gstat = output-list.gstat + STRING(anz) + "a". 

          DO i = 1 TO res-line.kind2: 
            output-list.gstat = output-list.gstat + "C". 
          END.

          /*ITA 060717 --> for special request*/
         FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
         IF AVAILABLE reslin-queasy THEN
             ASSIGN output-list.code = output-list.CODE + "," + reslin-queasy.char3.
        /*end*/
         /*masdod 051224 validate code value ticket #700033*/ /*FDL Ticket 23A90B - Add LENGTH(output-list.code) GT 0*/
         IF LENGTH(output-list.code) GT 0 AND SUBSTRING(output-list.code,LENGTH(output-list.code),1) EQ "," THEN
         DO:
             output-list.CODE = SUBSTRING(output-list.code,1,LENGTH(output-list.code) - 1).
         END.

        END. 
      END. 
    END. 
    
    IF output-list.zistatus EQ 3 THEN 
    DO: 
      FIND FIRST res-line WHERE (resstatus LE 2 OR resstatus = 5) 
        AND active-flag = 0 
        AND res-line.ankunft = ci-date AND res-line.zinr = zimmer.zinr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        CREATE output-list. 
        ASSIGN
          output-list.reihenfolge   = 0
          output-list.personal      = zimmer.personal
          output-list.floor         = zimmer.etage 
          output-list.zinr          = zimmer.zinr 
          output-list.zistatus      = zimmer.zistatus 
          output-list.kbezeich      = zimmer.kbezeich 
          output-list.code          = zimmer.CODE
        .
        DO: 
          IF SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "1" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "3" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "5" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "7" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "9" THEN 
             output-list.odd-even = 1. 
          ELSE IF SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "0" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "2" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "4" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "6" OR 
             SUBSTR(zimmer.zinr,LENGTH(zimmer.zinr),1) = "8" THEN 
             output-list.odd-even = 2. 
 
          ASSIGN
            output-list.bemerk = res-line.bemerk
            output-list.flag = 1 
            output-list.rsv-flag = YES
          .
          FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK. 
          IF guest.vorname1 NE "" THEN
            output-list.resname = guest.NAME + ", " + guest.vorname1.
          ELSE ASSIGN output-list.resnam = guest.NAME.

          FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
          RUN check-vip-guest(OUTPUT c-vip).
          ASSIGN
            output-list.gname = guest.name + ", " + guest.vorname1 
              + " " + guest.anrede1
            output-list.nation = guest.nation1 
            output-list.ankunft = res-line.ankunft
            output-list.abreise = res-line.abreise 
            output-list.arrival = YES   
            anz = res-line.erwachs + res-line.gratis.
          IF c-vip NE "" THEN ASSIGN output-list.vip = c-vip.
          IF anz LE 2 THEN 
          DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "A". 
          END. 
          ELSE output-list.gstat = output-list.gstat 
              + STRING(anz) + "A". 

          anz = res-line.kind1 + res-line.l-zuordnung[4].
          IF anz LE 2 THEN 
          DO i = 1 TO anz: 
            output-list.gstat = output-list.gstat + "a". 
          END. 
          ELSE output-list.gstat = output-list.gstat 
              + STRING(anz) + "a". 

          DO i = 1 TO res-line.kind2: 
            output-list.gstat = output-list.gstat + "C". 
          END. 

              /*ITA 060717 --> for special request*/
             FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
                 AND reslin-queasy.resnr = res-line.resnr 
                 AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
             IF AVAILABLE reslin-queasy THEN
                 ASSIGN output-list.code = output-list.CODE + "," + reslin-queasy.char3.
            /*end*/
             /*masdod 051224 validate code value ticket #700033*/ /*FDL Ticket 23A90B - Add LENGTH(output-list.code) GT 0*/
             IF LENGTH(output-list.code) GT 0 AND SUBSTRING(output-list.code,LENGTH(output-list.code),1) EQ "," THEN
             DO:
                 output-list.CODE = SUBSTRING(output-list.code,1,LENGTH(output-list.code) - 1).
             END.
        
        END. 
      END. 
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

