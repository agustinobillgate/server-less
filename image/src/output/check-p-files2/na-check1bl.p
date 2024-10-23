
DEF INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER def-natcode    AS CHAR.

DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str2       AS CHAR.
DEF OUTPUT PARAMETER msg-str3       AS CHAR.
DEF OUTPUT PARAMETER w-flag         AS LOGICAL.
DEF OUTPUT PARAMETER names-ok       AS LOGICAL.
DEF OUTPUT PARAMETER its-ok         AS LOGICAL.
DEF OUTPUT PARAMETER htparam-recid  AS INTEGER INIT 0.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "na-start".

DEFINE VARIABLE localRegion-exist   AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE sharerOK            AS LOGICAL INITIAL YES  NO-UNDO.
DEFINE VARIABLE rmNo                AS CHAR NO-UNDO.
DEFINE VARIABLE cidate              AS DATE NO-UNDO.
DEFINE VARIABLE billdate            AS DATE NO-UNDO.

DEFINE VARIABLE frate               AS DECIMAL NO-UNDO INITIAL 1.
DEFINE VARIABLE lodg-betrag         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE argt-betrag         AS DECIMAL NO-UNDO. 
DEFINE VARIABLE ex-rate             AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat-art             AS DECIMAL NO-UNDO.
DEFINE VARIABLE service-art         AS DECIMAL NO-UNDO.
DEFINE VARIABLE vat2-art            AS DECIMAL NO-UNDO.
DEFINE VARIABLE fact-art            AS DECIMAL NO-UNDO.
DEFINE VARIABLE gross-argt          AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-argt            AS DECIMAL NO-UNDO.
DEFINE VARIABLE bfast-value         AS DECIMAL NO-UNDO.
DEFINE VARIABLE lunch-value         AS DECIMAL NO-UNDO.
DEFINE VARIABLE dinner-value        AS DECIMAL NO-UNDO.
DEFINE VARIABLE luncdin-value       AS DECIMAL NO-UNDO.
DEFINE VARIABLE other-value         AS DECIMAL NO-UNDO.
DEFINE VARIABLE bfast-art           AS INTEGER NO-UNDO. 
DEFINE VARIABLE lunch-art           AS INTEGER NO-UNDO. 
DEFINE VARIABLE dinner-art          AS INTEGER NO-UNDO. 
DEFINE VARIABLE lundin-art          AS INTEGER NO-UNDO. 
DEFINE VARIABLE segment-type        AS INTEGER NO-UNDO.
DEFINE VARIABLE passfirst           AS LOGICAL NO-UNDO. /*william*/
DEFINE VARIABLE tmpdate             AS DATE    NO-UNDO.

DEFINE BUFFER rbuff FOR res-line.

RUN htpdate.p(87, OUTPUT cidate).
RUN htpdate.p(110, OUTPUT billdate).

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
lunch-art = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
dinner-art = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
lundin-art = htparam.finteger. 

IF billdate NE cidate THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Wrong Check-in date or Billing date (must be equal).",lvCAREA,"").
  RETURN. 
END. 

IF billdate GE TODAY THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Night-Audit not possible (too early).",lvCAREA,"").
  RETURN NO-APPLY. 
END. 


/* SY 26/05/2015*/
FOR EACH res-line WHERE res-line.resstatus = 8 AND res-line.abreise = billdate 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK:
    FIND FIRST bill WHERE bill.resnr = res-line.resnr
        AND bill.parent-nr = res-line.reslinnr 
        AND bill.saldo NE 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:    
        msg-str = msg-str + CHR(2)
                + translateExtended ("Night-Audit not possible:",lvCAREA,"") 
                + CHR(10)
                + translateExtended ("Unbalanced bill of checked-out guest exists",lvCAREA,""). 
        RETURN. 
    END.
END.

FOR EACH res-line WHERE res-line.active-flag = 1 AND res-line.resstatus = 13 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK:
    FIND FIRST rbuff WHERE rbuff.active-flag = 1 AND rbuff.resstatus = 6
        AND rbuff.zinr = res-line.zinr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rbuff THEN
    DO:
        ASSIGN
          rmNo     = res-line.zinr
          sharerOK = NO
        .
        LEAVE.
    END.
END.


IF NOT sharerOK THEN
DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Room Sharer found with no main guest: RmNo",lvCAREA,"")
            + " " + rmNo.
    /*MTAPPLY "entry" TO btn-cancel. */
    RETURN NO-APPLY. 
END.

FOR EACH res-line WHERE res-line.active-flag = 1 
    AND res-line.resstatus NE 12
    AND res-line.l-zuordnung[3] = 0 NO-LOCK:
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK
        NO-ERROR.
    IF NOT AVAILABLE guest THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Guest record of inhouse guest not found: RmNo",lvCAREA,"")
                + " " + res-line.zinr
                + CHR(10)
                + translateExtended ("Night-Audit not possible.",lvCAREA,"").
       /*MTAPPLY "entry" TO btn-cancel.*/
       RETURN NO-APPLY. 
    END.
    FIND FIRST nation WHERE nation.kurzbez = guest.nation1
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE nation THEN
    DO:
       msg-str = msg-str + CHR(2)
               + translateExtended ("Nationality of inhouse guest not defined: RmNo",lvCAREA,"")
               + " " + res-line.zinr
               + CHR(10)
               + translateExtended ("Night-Audit not possible.",lvCAREA,"").
       /*MTAPPLY "entry" TO btn-cancel.*/
       RETURN NO-APPLY. 
    END.
END.

FIND FIRST res-line WHERE res-line.active-flag = 1
 AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
 AND res-line.abreise = billdate NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Today departing inhouse guest(s) found: RmNo",lvCAREA,"")
          + " " + res-line.zinr
          + CHR(10)
          + translateExtended ("Night-Audit not possible.",lvCAREA,"").
  /*MTAPPLY "entry" TO btn-cancel.*/
  RETURN NO-APPLY. 
END.

/*  09/07/2006
    FIND FIRST htparam WHERE htparam.paramnr = 236 NO-LOCK. 
    IF NOT htparam.flogical THEN
*/


DO: 
  FIND FIRST h-bill WHERE h-bill.flag = 0 AND h-bill.rechnr GT 0 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE h-bill THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("N/A not possible as opened Restaurant bill(s) found :",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Department",lvCAREA,"") + " " + STRING(h-bill.departement) + " "
            + translateExtended ("BillNo",lvCAREA,"") + " " + STRING(h-bill.rechnr).
    /*MTAPPLY "entry" TO btn-cancel. */
    RETURN NO-APPLY. 
  END. 
END. 

FIND FIRST nation WHERE nation.natcode GT 0 NO-LOCK NO-ERROR.
localRegion-exist = AVAILABLE nation.

/***********************************************************************/

/* Test, IF all currency codes used BY res-line are well defined */ 
FOR EACH res-line WHERE res-line.active-flag = 1 
    AND res-line.resstatus NE 12 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE waehrung THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Currency not found for the following reservation :",lvCAREA,"")
              + CHR(10)
              + translateExtended ("ResNo :",lvCAREA,"") + " " + STRING(res-line.resnr) + " - " + res-line.zinr
              + " " + res-line.name.
      w-flag = YES. 
    END. 
    ELSE 
    DO: 
      IF waehrung.ankauf = 0 OR waehrung.einheit = 0 THEN 
      DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Currency Rate incorrect for the following reservation :",lvCAREA,"")
                + CHR(10)
                + translateExtended ("Code :",lvCAREA,"") + " " + waehrung.wabkurz + " - " + res-line.zinr
                + " " + res-line.name.
        w-flag = YES. 
      END. 
    END.
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guest THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Guest record not found for following reservation :",lvCAREA,"")
                + CHR(10)
                + res-line.zinr + " " + res-line.name.
        w-flag = YES. 
        LEAVE.
    END.
    ELSE
    DO:
        FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE nation THEN
        DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Nation code not correctly defined for following reservation :",lvCAREA,"")
                    + CHR(10)
                    + res-line.zinr + " " + res-line.name.
            w-flag = YES. 
            LEAVE.
        END.
        FIND FIRST nation WHERE nation.kurzbez = guest.land NO-LOCK NO-ERROR.
        IF NOT AVAILABLE nation THEN
        DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Country code not correctly defined for following reservation :",lvCAREA,"")
                    + CHR(10)
                    + res-line.zinr + " " + res-line.name.
            w-flag = YES. 
            LEAVE.
        END.
        IF localRegion-exist AND (guest.land EQ def-natcode) THEN
        DO:
            FIND FIRST nation WHERE nation.kurzbez = guest.nation2 
                AND nation.natcode GT 0 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE nation THEN
            DO:
                msg-str = msg-str + CHR(2)
                        + translateExtended ("Local Region code not correctly defined for following reservation :",lvCAREA,"")
                        + CHR(10)
                        + res-line.zinr + " " + res-line.name.
                w-flag = YES. 
                LEAVE.
            END.
        END.

        /*FDL Feb 02, 2023 - Ticket 43AC00*/
        IF guest.land EQ "UNK" THEN
        DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Country code UNK found for following reservation :",lvCAREA,"")
                    + CHR(10)
                    + res-line.zinr + " " + res-line.name
                    + CHR(10)
                    + "Please change another code".
            w-flag = YES. 
            LEAVE.
        END.
        ELSE IF guest.nation1 EQ "UNK" THEN
        DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("Nation code UNK found for following reservation :",lvCAREA,"")
                    + CHR(10)
                    + res-line.zinr + " " + res-line.name
                    + CHR(10)
                    + "Please change another code".
            w-flag = YES. 
            LEAVE.
        END.
    END.

    /*FDL April 25, 2023 => Ticket 183883*/
    IF res-line.zipreis NE 0 THEN 
    DO:
        IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
        ELSE 
        DO: 
            FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ res-line.betriebsnr NO-LOCK NO-ERROR. 
            IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
        END. 

        lodg-betrag = 0.
        lodg-betrag = res-line.zipreis * frate.

        FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK. 

        FOR EACH argt-line WHERE argt-line.argtnr EQ arrangement.argtnr 
            AND NOT argt-line.kind2 AND argt-line.kind1,
            FIRST artikel WHERE artikel.artnr EQ argt-line.argt-artnr 
              AND artikel.departement EQ argt-line.departement NO-LOCK:
            RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
              OUTPUT argt-betrag, OUTPUT ex-rate). 

            /*RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
                billdate, OUTPUT service-art, OUTPUT vat-art, 
                OUTPUT vat2-art, OUTPUT fact-art).


            ASSIGN
                argt-betrag = argt-betrag * ex-rate
                gross-argt = gross-argt + argt-betrag            
                argt-betrag = argt-betrag / fact-art  
                net-argt = net-argt + argt-betrag
            .*/

            /*res-deci : [2] = bfast; [3] = lunch; [4] = dinner; [5] = misc*/
            IF artikel.zwkum EQ bfast-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                lodg-betrag = lodg-betrag - argt-betrag.  
            END.            
            ELSE IF artikel.zwkum EQ lunch-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                lodg-betrag = lodg-betrag - argt-betrag. 
            END.            
            ELSE IF artikel.zwkum EQ dinner-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                lodg-betrag = lodg-betrag - argt-betrag. 
            END.            
            ELSE IF artikel.zwkum EQ lundin-art AND (artikel.umsatzart EQ 3 OR artikel.umsatzart GE 5) THEN 
            DO:
                lodg-betrag = lodg-betrag - argt-betrag. 
            END.            
            ELSE 
            DO:
                lodg-betrag = lodg-betrag - argt-betrag. 
            END.                               
        END.

        IF lodg-betrag LT 0 THEN
        DO:
            msg-str = msg-str + CHR(2)
                + translateExtended ("Minus lodging found with reservation : ",lvCAREA,"")
                + STRING(res-line.resnr) + "/" + STRING(res-line.reslinnr, "999")
                .

            w-flag = YES. 
            LEAVE.
        END.
    END.
    /*End FDL*/
    /*overlapping fixed rate validation*/
    passfirst = YES.                                                                     /*william start*/
    FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
        AND reslin-queasy.resnr = res-line.resnr
        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK BY reslin-queasy.date1:
        IF passfirst = NO THEN
        DO:
            IF tmpdate GE reslin-queasy.date1 THEN
            DO:
                msg-str = msg-str + CHR(2)
                + translateExtended ("overlapping fixed rate",lvCAREA,"") + chr(10)
                + translateExtended ("please check fixed rate in reservation: ",lvCAREA,"")
                + STRING(reslin-queasy.resnr)
                .

                w-flag = YES. 
                LEAVE.
            END.         
        END.
       /* IF reslin-queasy.date1 NE reslin-queasy.date2 THEN
        DO:
            msg-str = msg-str + CHR(2)
            + translateExtended ("overlapping fixed rate",lvCAREA,"") + chr(10)
            + translateExtended ("please check fixed rate in reservation: ",lvCAREA,"")
            + STRING(reslin-queasy.resnr)
            .

            w-flag = YES. 
            LEAVE.
        END.*/
        passfirst = NO.
        tmpdate = reslin-queasy.date2.
    END.
    IF w-flag THEN LEAVE.                                                              /*william end*/
END.

IF w-flag = YES THEN 
DO: 
  /*MTAPPLY "entry" TO btn-cancel. */
  RETURN NO-APPLY. 
END. 


RUN check-na-program-names (OUTPUT names-ok).
IF NOT names-ok THEN
DO:
  /*MTAPPLY "entry" TO btn-cancel.*/
  RETURN NO-APPLY. 
END.


FIND FIRST bill WHERE bill.flag = 1 
  AND (bill.saldo GE 0.1 OR bill.saldo LE -0.1) NO-LOCK NO-ERROR. 
IF AVAILABLE bill THEN 
DO: 
  msg-str2 = msg-str2 + CHR(2) + "&W"
           + translateExtended ("Closed bill with a non zero balance found: BillNo =",lvCAREA,"") + " "
           + TRIM(STRING(bill.rechnr,">>>,>>>,>>9"))
           + " - " + STRING(bill.saldo).
END.


FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
IF NOT htparam.flogical THEN 
DO: 
  DEF VAR na-date AS DATE.
  DEF VAR na-time AS INT.
  DEF VAR na-name AS CHAR.
  FIND FIRST htparam WHERE paramnr = 102 NO-LOCK.
  na-date = htparam.fdate.
  FIND FIRST htparam WHERE paramnr = 103 NO-LOCK.
  na-time = htparam.finteger.
  FIND FIRST htparam WHERE paramnr = 253 NO-LOCK.
  na-name = htparam.fchar.
  IF na-date = today THEN
  DO:
    msg-str3 = msg-str3 + CHR(2) + "&W"
             + translateExtended ("The last night audit was running TODAY",lvCAREA,"")
             + CHR(10)
             + STRING(na-date) + " " + translateExtended ("at",lvCAREA,"") + " " + STRING(na-time, "HH:MM")
             + "  " + translateExtended ("by",lvCAREA,"") + " " + na-name.
  END.
  its-ok = YES.

  /*MT
  IF its-ok THEN 
  DO: 
    answer = NO. 
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Do you really want to run the night audit program NOW ?",lvCAREA,"") 
      VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
    IF answer THEN 
    DO: 
      DO TRANSACTION: 
        FIND CURRENT htparam EXCLUSIVE-LOCK. 
        htparam.flogical = YES. 
        RUN na-prog. 
        FIND FIRST htparam WHERE paramnr = 253 EXCLUSIVE-LOCK. 
        htparam.fchar = bediener.username. 
        htparam.fdate = today. 
        htparam.finteger = time. 
        htparam.flogical = NO. 
        FIND CURRENT htparam NO-LOCK. 
        FIND FIRST htparam WHERE paramnr = 102 EXCLUSIVE-LOCK. 
        htparam.fdate = today. 
        FIND CURRENT htparam NO-LOCK. 
        FIND FIRST htparam WHERE paramnr = 103 EXCLUSIVE-LOCK. 
        htparam.finteger = time. 
        FIND CURRENT htparam NO-LOCK. 
        mess-str = "Night Audit finished.". 
        DISP mess-str WITH FRAME frame1. 
      END. 
      FIND FIRST htparam WHERE htparam.paramnr = 99 NO-LOCK. 
      printer-nr = htparam.finteger. 
      RUN select-printer.p(INPUT-OUTPUT printer-nr). 
      IF printer-nr NE 0 THEN 
      DO: 
        mess-str = "Printing Night Audit Reports, please wait ...". 
        DISP mess-str WITH FRAME frame1. 
        CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait"). 
        PROCESS EVENTS. 
        RUN print-na.p (INPUT printer-nr). 
        CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow"). 
        mess-str = "Printing finished.". 
        DISP mess-str WITH FRAME frame1. 
      END. 
    END. 
  END.
END. */
END. 
ELSE 
DO: 
  msg-str3 = msg-str3 + CHR(2)
           + translateExtended ("Night audit flag is active!",lvCAREA,"").
END. 

IF its-ok THEN
DO:
    FIND CURRENT htparam.
    htparam-recid = RECID(htparam).
END.


PROCEDURE check-na-program-names:
DEF OUTPUT PARAMETER names-ok AS LOGICAL INIT YES NO-UNDO.
DEF VAR progname  AS CHAR    NO-UNDO.
DEF VAR not-found AS LOGICAL NO-UNDO.

  FOR EACH nightaudit WHERE nightaudit.selektion NO-LOCK
      BY (1 - nightaudit.hogarest) BY nightaudit.reihenfolge
      
      : 
      progname = nightaudit.programm.
      RUN ass-progname(nightaudit.abschlussart,INPUT-OUTPUT progname).

      not-found = SEARCH(LC(progname)) = ?.
      IF not-found THEN
      ASSIGN
        progname  = REPLACE(progname, ".p", ".r")
        progname  = REPLACE(progname, ".w", ".r")
        not-found = (SEARCH(LC(progname)) = ?)
      .
      IF not-found THEN
      DO:
        IF progname MATCHES "nt-tauziarpt.r"
            OR progname MATCHES "nt-exportgcf.r" 
            OR progname MATCHES "nt-exportghs.r"
			/*NC - #CE960D 01/08/24*/
			OR progname MATCHES "nt-exportghs2.r"
            OR progname MATCHES "nt-salesboard.r"
            OR progname MATCHES "nt-dashboardohm-daily.r"
            OR progname MATCHES "nt-dashboard-daily.r" 
            /*FDL Oct 27, 2023 => Ticket 302FE1*/
            OR progname MATCHES "nt-exportguestsense.r"
            OR progname MATCHES "nt-exportghs-phm.r"
            OR progname MATCHES "nt-guestlist-csv.r"
            THEN.
        ELSE
        DO:
            msg-str = msg-str + CHR(2)
                    + translateExtended ("N/A Program does not exist:",lvCAREA,"")
                    + " " + nightaudit.program.
            names-ok = NO.
            RETURN.
        END.
      END.
  END.
END.


PROCEDURE ass-progname:
DEF INPUT PARAMETER abschlussart AS INT.
DEF INPUT-OUTPUT PARAMETER progname AS CHAR.
DEF VAR a AS INT.
  IF progname MATCHES ("*bl.p*") THEN .
  ELSE 
  DO:
      IF INT(abschlussart) = 1 THEN.
      ELSE 
      DO:
        a = R-INDEX (progname, ".p").
        progname = SUBSTR(LC(progname), 1, a - 1) + "bl.p".
        /*RUN VALUE(SUBSTR(LC(progname), 1, a - 1) + "bl.p") ON hServer.*/
      END.
  END.
END.
