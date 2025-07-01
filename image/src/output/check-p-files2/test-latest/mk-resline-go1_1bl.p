DEF TEMP-TABLE curr-resline LIKE res-line.

DEF TEMP-TABLE t-resline    LIKE res-line.
DEF TEMP-TABLE member-list
    FIELD reslinnr AS INTEGER
.
DEF TEMP-TABLE zwunsch-rline
    FIELD s-label   AS CHAR
    FIELD s-value1  AS CHAR
    FIELD s-value2  AS CHAR
    FIELD used      AS LOGICAL INIT NO
.
DEF TEMP-TABLE zwunsch-rmember
    FIELD s-label   AS CHAR
    FIELD s-value2  AS CHAR
.

DEFINE TEMP-TABLE update-fixrate
    FIELD date1 AS DATE
    FIELD date2 AS DATE
    FIELD argt  AS CHAR
.

DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER user-init   AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER specRequest AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER c-apply     AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER incl-gname  AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER incl-ginhouse  AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR curr-resline.
DEF OUTPUT PARAMETER msg-str     AS CHAR    NO-UNDO INIT "".

DEF VARIABLE do-it               AS LOGICAL NO-UNDO.
DEF VARIABLE allFlag             AS LOGICAL NO-UNDO.
DEF VARIABLE curr-i              AS INTEGER NO-UNDO.
DEF VARIABLE ct                  AS CHAR    NO-UNDO.
DEF VARIABLE zikatstr            AS CHAR    NO-UNDO.
DEF VARIABLE curr-msg            AS CHAR    NO-UNDO.
DEF VARIABLE init-time           AS INTEGER NO-UNDO.
DEF VARIABLE init-date           AS DATE    NO-UNDO.
DEF VARIABLE ankunft1            AS DATE    NO-UNDO.
DEF VARIABLE abreise1            AS DATE    NO-UNDO.

DEF VARIABLE i                   AS INTEGER NO-UNDO.
DEF VARIABLE str                 AS CHAR    NO-UNDO.
DEF VARIABLE m-flight            AS CHAR    NO-UNDO.

DEF VARIABLE overbook    AS LOGICAL NO-UNDO INITIAL NO. 
DEF VARIABLE overmax     AS LOGICAL NO-UNDO INITIAL NO. 
DEF VARIABLE overanz     AS INTEGER NO-UNDO INITIAL 0. 
DEF VARIABLE overdate    AS DATE    NO-UNDO. 
DEF VARIABLE incl-allot  AS LOGICAL NO-UNDO INITIAL NO. 
DEF VARIABLE rmcat-ovb   AS INTEGER NO-UNDO.

DEF BUFFER rline        FOR res-line.
DEF BUFFER rmember      FOR res-line.
DEF BUFFER rbuff        FOR res-line.
DEF BUFFER raccomp      FOR res-line.
DEF BUFFER spreqBuff    FOR reslin-queasy.
DEF BUFFER resline      FOR res-line.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

CREATE t-resline.

FIND FIRST curr-resline.
FIND FIRST res-line WHERE res-line.resnr = curr-resline.resnr
    AND res-line.reslinnr = curr-resline.reslinnr NO-LOCK.

IF specRequest THEN FIND FIRST spreqBuff WHERE 
    spreqBuff.KEY      = "specialRequest" AND 
    spreqBuff.resnr    = curr-resline.resnr AND 
    spreqBuff.reslinnr = curr-resline.reslinnr NO-LOCK NO-ERROR.

DO i = 1 TO NUM-ENTRIES(curr-resline.zimmer-wunsch,";") - 1:
    CREATE zwunsch-rline.
    str = ENTRY(i, curr-resline.zimmer-wunsch, ";").
    IF SUBSTR(str,1,7) = "voucher" THEN 
    ASSIGN zwunsch-rline.s-label  = "voucher"
           zwunsch-rline.s-value1 = SUBSTR(str,8).   
    ELSE IF SUBSTR(str,1,5) = "ChAge"  THEN 
    ASSIGN zwunsch-rline.s-label  = "chAge"
           zwunsch-rline.s-value1 = SUBSTR(str,6).   
    ELSE IF SUBSTR(str,1,10) = "$OrigCode$" THEN 
    ASSIGN zwunsch-rline.s-label  = "$OrigCode$"
           zwunsch-rline.s-value1 = SUBSTR(str,11).   
    ELSE IF SUBSTR(str,1,6) = "$CODE$" THEN 
    ASSIGN zwunsch-rline.s-label  = "$CODE$"
           zwunsch-rline.s-value1 = SUBSTR(str,7).   
    ELSE IF SUBSTR(str,1,5) = "DATE,"  THEN 
    ASSIGN zwunsch-rline.s-label  = "DATE,"
           zwunsch-rline.s-value1 = SUBSTR(str,6).   
    ELSE IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
    ASSIGN zwunsch-rline.s-label  = "SEGM_PUR"
           zwunsch-rline.s-value1 = SUBSTR(str,9).
    ELSE IF SUBSTR(str,1,6) = "ebdisc"  THEN 
    ASSIGN zwunsch-rline.s-label  = "ebdisc"
           zwunsch-rline.s-value1 = "Y".
    ELSE IF SUBSTR(str,1,6) = "kbdisc"  THEN 
    ASSIGN zwunsch-rline.s-label  = "kbdisc"
           zwunsch-rline.s-value1 = "Y".
    ELSE IF SUBSTR(str,1,10) = "restricted"  THEN 
    ASSIGN zwunsch-rline.s-label  = "restricted"
           zwunsch-rline.s-value1 = "Y".
    ELSE IF SUBSTR(str,1,6) = "pickup"  THEN 
    ASSIGN zwunsch-rline.s-label  = "pickup"
           zwunsch-rline.s-value1 = "Y".
    ELSE IF SUBSTR(str,1,14) = "drop-passanger"  THEN 
    ASSIGN zwunsch-rline.s-label  = "drop-passanger"
           zwunsch-rline.s-value1 = "Y".   
    ELSE IF str MATCHES "*WCI-req*" THEN
    ASSIGN zwunsch-rline.s-label  = "WCI-req"
           zwunsch-rline.s-value1 = ENTRY(2, str, "=").
END.
DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    CREATE zwunsch-rline.
    str = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(str,1,7) = "voucher" THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "voucher"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "voucher"
             zwunsch-rline.s-value2 = SUBSTR(str,8).
    END.
    ELSE IF SUBSTR(str,1,5) = "ChAge"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "ChAge"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "ChAge"
             zwunsch-rline.s-value2 = SUBSTR(str,6).
    END.
    ELSE IF SUBSTR(str,1,10) = "$OrigCode$" THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "voucher"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "$OrigCode$"
             zwunsch-rline.s-value2 = SUBSTR(str,11).
    END.
    ELSE IF SUBSTR(str,1,6) = "$CODE$" THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "&CODE$"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "$CODE$"
             zwunsch-rline.s-value2 = SUBSTR(str,7).
    END.
    ELSE IF SUBSTR(str,1,5) = "DATE,"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "DATE,"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "DATE,"
             zwunsch-rline.s-value2 = SUBSTR(str,6).
    END.
    ELSE IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "SEGM_PUR"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "SEGM_PUR"
             zwunsch-rline.s-value2 = SUBSTR(str,9).
    END.
    ELSE IF SUBSTR(str,1,6) = "ebdisc"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "ebdisc"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "ebdisc"
             zwunsch-rline.s-value2 = "Y".
    END.
    ELSE IF SUBSTR(str,1,6) = "kbdisc"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "kbdisx"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "kbdisc"
             zwunsch-rline.s-value2 = "Y".
    END.
    ELSE IF SUBSTR(str,1,10) = "restricted"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "restricted"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "restricted"
             zwunsch-rline.s-value2 = "Y".
    END.
    ELSE IF SUBSTR(str,1,6) = "pickup"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "pickup"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "pickup"
             zwunsch-rline.s-value2 = "Y".
    END.
    ELSE IF SUBSTR(str,1,14) = "drop-passanger"  THEN 
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "drop-passanger"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "drop-passanger"
             zwunsch-rline.s-value2 = "Y".
    END.
    ELSE IF str MATCHES "*WCI-req*" THEN
    DO:
      FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label = "WCI-req"
          NO-ERROR.
      IF NOT AVAILABLE zwunsch-rline THEN CREATE zwunsch-rline.
      ASSIGN zwunsch-rline.s-label  = "WCI-req"
             zwunsch-rline.s-value2 = ENTRY(2, str, "=").
    END.
END.

FOR EACH zwunsch-rline WHERE zwunsch-rline.s-value1 
    = zwunsch-rline.s-value2:
    DELETE zwunsch-rline.
END.

allFlag = (c-apply = "ALL").
IF NOT allFlag THEN
DO curr-i = 1 TO NUM-ENTRIES(c-apply, ","):
    ct = TRIM(ENTRY(curr-i, c-apply, ",")).
    IF ct NE "" THEN
    DO:
        CREATE member-list.
        ASSIGN member-list.reslinnr = INTEGER(ct).
    END.
END.

/*ITA 200217*/
FIND FIRST resline WHERE resline.resnr = curr-resline.resnr
    AND resline.active-flag = 1
    AND resline.reslinnr NE curr-resline.reslinnr
    AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE resline:

    IF allFlag THEN do-it = YES.
    ELSE
    DO:
        FIND FIRST member-list WHERE member-list.reslinnr = resline.reslinnr NO-ERROR.
        do-it = AVAILABLE member-list.
    END.

    IF do-it THEN 
    DO TRANSACTION:
        FIND FIRST rbuff WHERE RECID(rbuff) = RECID(resline) EXCLUSIVE-LOCK.
        IF curr-resline.bemerk NE res-line.bemerk THEN
            rbuff.bemerk = res-line.bemerk.

        IF incl-ginhouse THEN DO:
            rbuff.arrangement = res-line.arrangement.

            IF incl-gname THEN ASSIGN rbuff.gastnrmember = res-line.gastnrmember.

            IF resline.resstatus NE 11 AND resline.resstatus NE 13 THEN
                RUN check-fixrates-changes.
        END.

        FIND FIRST rbuff NO-LOCK.
        RELEASE rbuff.
    END.


    FIND NEXT resline WHERE resline.resnr = curr-resline.resnr
        AND resline.active-flag = 1
        AND resline.reslinnr NE curr-resline.reslinnr
        AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
END.
/*end ITA*/


FIND FIRST rmember WHERE rmember.resnr = curr-resline.resnr
    AND rmember.active-flag = 0 
    /*AND rmember.reslinnr NE 12*/
    AND rmember.reslinnr NE curr-resline.reslinnr 
    AND rmember.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE rmember:

    IF allFlag THEN do-it = YES.
    ELSE
    DO:
        FIND FIRST member-list WHERE 
            member-list.reslinnr = rmember.reslinnr NO-ERROR.
        do-it = AVAILABLE member-list.
    END.

    IF do-it THEN
    DO:
       RUN check-timebl.p (1, rmember.resnr, rmember.reslinnr, 
           "res-line", ?, ?, OUTPUT do-it, OUTPUT init-time, 
           OUTPUT init-date).
       IF NOT do-it THEN msg-str = msg-str + "#" + STRING(rmember.reslinnr,"99") + " "
           + rmember.NAME + CHR(10)
           + translateExtended("Reservation being modified by other user.",lvCAREA,"")
           + CHR(10) + CHR(10).
    END.

    IF do-it THEN
    DO TRANSACTION:
        BUFFER-COPY rmember TO t-resline.
        FIND FIRST rbuff WHERE RECID(rbuff) = RECID(rmember)
            EXCLUSIVE-LOCK.

        m-flight = "".
        IF SUBSTR(curr-resline.flight-nr,1,6) NE 
           SUBSTR(res-line.flight-nr,1,6) THEN
           m-flight = SUBSTR(res-line.flight-nr,1,6).
        ELSE m-flight = SUBSTR(rmember.flight-nr,1,6).
        IF SUBSTR(curr-resline.flight-nr,7,5) NE 
           SUBSTR(res-line.flight-nr,7,5) THEN
           m-flight = m-flight + SUBSTR(res-line.flight-nr,7,5).
        ELSE m-flight = m-flight + SUBSTR(rmember.flight-nr,7,5).
        IF SUBSTR(curr-resline.flight-nr,12,6) NE 
           SUBSTR(res-line.flight-nr,12,6) THEN
           m-flight = m-flight + SUBSTR(res-line.flight-nr,12,6).
        ELSE m-flight = m-flight + SUBSTR(rmember.flight-nr,12,6).
        IF SUBSTR(curr-resline.flight-nr,18,5) NE 
           SUBSTR(res-line.flight-nr,18,5) THEN
           m-flight = m-flight + SUBSTR(res-line.flight-nr,18,5).
        ELSE m-flight = m-flight + SUBSTR(rmember.flight-nr,18,5).

        ASSIGN rmember.flight-nr = m-flight.

        IF curr-resline.CODE NE res-line.CODE THEN
            rbuff.CODE = res-line.CODE.
        IF curr-resline.l-zuordnung[1] NE res-line.l-zuordnung[1] 
            AND curr-resline.zikatnr = rmember.zikatnr THEN
            rbuff.l-zuordnung[1] = res-line.l-zuordnung[1].
        IF curr-resline.gastnrpay NE res-line.gastnrpay THEN
            rbuff.gastnrpay = res-line.gastnrpay.
        IF curr-resline.arrangement NE res-line.arrangement THEN
            rbuff.arrangement = res-line.arrangement.
        IF curr-resline.kontignr NE res-line.kontignr THEN
            rbuff.kontignr = res-line.kontignr.
        IF curr-resline.betriebsnr NE res-line.betriebsnr THEN
            rbuff.betriebsnr = res-line.betriebsnr.
        IF curr-resline.reserve-int NE res-line.reserve-int THEN
            rbuff.reserve-int = res-line.reserve-int.
        IF curr-resline.bemerk NE res-line.bemerk THEN
            rbuff.bemerk = res-line.bemerk.
        IF curr-resline.erwachs NE res-line.erwachs 
            AND res-line.erwachs GT 0 
            AND rmember.resstatus NE 11 THEN
            rbuff.erwachs = res-line.erwachs.
        IF curr-resline.resstatus NE res-line.resstatus 
            AND (curr-resline.resstatus LE 2 OR curr-resline.resstatus = 5)
            AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN
            rbuff.resstatus = res-line.resstatus.

        /*ITA 06/02/24 */
        IF incl-gname /*AND curr-resline.gastnrmember NE rmember.gastnrmember*/ THEN
            rbuff.gastnrmember = res-line.gastnrmember.
        
        IF (curr-resline.ankunft NE res-line.ankunft) OR
           (curr-resline.abreise NE res-line.abreise) OR
            (curr-resline.zikatnr NE res-line.zikatnr) THEN
        DO:
          ankunft1 = rmember.ankunft.
          IF curr-resline.ankunft NE res-line.ankunft THEN
              ankunft1 = res-line.ankunft.
          abreise1 = rmember.abreise.
          IF curr-resline.abreise NE res-line.abreise THEN
              abreise1 = res-line.abreise.
          do-it = abreise1 GE ankunft1.
          IF NOT do-it THEN msg-str = msg-str + "#" + STRING(rmember.reslinnr) + " "
              + rmember.NAME + CHR(10)
              + translateExtended("Wrong check-in/check-out date",lvCAREA,"")
              + ": " + STRING(ankunft1) + "/" + STRING(abreise1)
              + CHR(10) + CHR(10).
          IF do-it AND rmember.zinr NE "" THEN
          DO:
            FIND FIRST outorder WHERE outorder.zinr = rmember.zinr
                AND NOT outorder.gespstart GE abreise1
                AND NOT outorder.gespende LT ankunft1 NO-LOCK NO-ERROR.
            do-it = NOT AVAILABLE outorder.
            IF NOT do-it THEN msg-str = msg-str + "#" + STRING(rmember.reslinnr) + " "
                + rmember.NAME + CHR(10)
                + translateExtended("O-O-O found RmNo",lvCAREA,"")
                + " " + rmember.zinr
                + ": " + STRING(outorder.gespstart) 
                + "/"  + STRING(outorder.gespende)
                + CHR(10) + CHR(10).
            ELSE
            DO:
              FIND FIRST rline WHERE rline.zinr = rmember.zinr
                AND (rline.resstatus LE 2 OR rline.resstatus = 5)
                AND RECID(rline) NE RECID(rmember)
                AND NOT rline.ankunft GE abreise1
                AND NOT rline.abreise LE ankunft1 NO-LOCK NO-ERROR.
              do-it = NOT AVAILABLE rline.
              IF NOT do-it THEN msg-str = msg-str + "#" + STRING(rmember.reslinnr) + " "
                 + rmember.NAME + CHR(10)
                 + translateExtended("Overlapping with other reservation - RmNo",lvCAREA,"")
                 + " " + rmember.zinr
                 + ": " + STRING(rline.ankunft) 
                 + "/"  + STRING(rline.abreise)
                 + CHR(10) + CHR(10).
            END.
          END.
          IF do-it THEN
          DO:
            IF curr-resline.zikatnr NE res-line.zikatnr 
              AND curr-resline.zikatnr = rmember.zikatnr THEN
            FIND FIRST zimkateg WHERE zimkateg.zikatnr 
              = res-line.zikatnr NO-LOCK.
            ELSE    
            FIND FIRST zimkateg WHERE zimkateg.zikatnr 
              = rmember.zikatnr NO-LOCK.
            zikatstr = zimkateg.kurzbez.
            RUN res-overbookbl.p (pvILanguage, "modify", rmember.resnr,
              rmember.reslinnr, res-line.ankunft, res-line.abreise, 
              1, zikatstr, ?, YES, OUTPUT overbook, OUTPUT overmax, 
              OUTPUT overanz, OUTPUT overdate, OUTPUT incl-allot, 
              OUTPUT curr-msg, OUTPUT rmcat-ovb). 
            do-it = NOT overbook.
            IF NOT do-it THEN msg-str = msg-str + "#" + STRING(rmember.reslinnr) + " "
              + rmember.NAME + CHR(10)
              + translateExtended("Overbooking found on",lvCAREA,"")
              + " " + STRING(overdate)
              + CHR(10) + CHR(10).
          END.
          IF do-it THEN
          DO:
              IF curr-resline.ankunft NE res-line.ankunft THEN
              ASSIGN
                  rbuff.ankunft = res-line.ankunft
                  rbuff.anztage = rbuff.abreise - rbuff.ankunft
              .
              IF curr-resline.abreise NE res-line.abreise THEN
              ASSIGN
                  rbuff.abreise = res-line.abreise
                  rbuff.anztage = rbuff.abreise - rbuff.ankunft
              .
              IF curr-resline.zikatnr NE res-line.zikatnr 
                  AND curr-resline.zikatnr = rmember.zikatnr THEN
              ASSIGN
                  rbuff.zikatnr = res-line.zikatnr
                  rbuff.setup   = res-line.setup
                  rbuff.zinr    = ""
              .
              FOR EACH raccomp WHERE raccomp.resnr = rmember.resnr
                  AND raccomp.resstatus = 11
                  AND raccomp.kontakt-nr = rmember.reslinnr
                  AND raccomp.l-zuordnung[3] = 1:
                  ASSIGN
                      raccomp.ankunft = rbuff.ankunft
                      raccomp.abreise = rbuff.abreise
                      raccomp.zikatnr = rbuff.zikatnr
                      raccomp.zinr    = rbuff.zinr
                  .
              END.
          END.
        END.
        
        IF do-it AND curr-resline.zipreis NE res-line.zipreis
            AND rmember.resstatus NE 11 
            AND rmember.resstatus NE 13 THEN rbuff.zipreis = res-line.zipreis.
        
        IF do-it AND specRequest AND AVAILABLE spreqBuff THEN 
            RUN update-special-request.

        IF do-it THEN
        DO i = 1 TO NUM-ENTRIES(rmember.zimmer-wunsch,";") - 1:
            CREATE zwunsch-rmember.
            str = ENTRY(i, rmember.zimmer-wunsch, ";").
            IF SUBSTR(str,1,7) = "voucher" THEN 
            ASSIGN zwunsch-rmember.s-label  = "voucher"
                   zwunsch-rmember.s-value2 = SUBSTR(str,8).
            ELSE IF SUBSTR(str,1,5) = "ChAge"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "chAge"
                   zwunsch-rmember.s-value2 = SUBSTR(str,6).
            ELSE IF SUBSTR(str,1,10) = "$OrigCode$" THEN 
            ASSIGN zwunsch-rmember.s-label  = "$OrigCode$"
                   zwunsch-rmember.s-value2 = SUBSTR(str,11).
            ELSE IF SUBSTR(str,1,6) = "$CODE$" THEN 
            ASSIGN zwunsch-rmember.s-label  = "$CODE$"
                   zwunsch-rmember.s-value2 = SUBSTR(str,7).
            ELSE IF SUBSTR(str,1,5) = "DATE,"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "DATE,"
                   zwunsch-rmember.s-value2 = SUBSTR(str,6).
            ELSE IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
            ASSIGN zwunsch-rmember.s-label  = "SEGM_PUR"
                   zwunsch-rmember.s-value2 = SUBSTR(str,9).
            ELSE IF SUBSTR(str,1,6) = "ebdisc"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "ebdisc"
                   zwunsch-rmember.s-value2 = "Y".
            ELSE IF SUBSTR(str,1,6) = "kbdisc"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "kbdisc"
                   zwunsch-rmember.s-value2 = "Y".
            ELSE IF SUBSTR(str,1,10) = "restricted"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "restricted"
                   zwunsch-rmember.s-value2 = "Y".
            ELSE IF SUBSTR(str,1,6) = "pickup"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "pickup"
                   zwunsch-rmember.s-value2 = "Y".
            ELSE IF SUBSTR(str,1,14) = "drop-passanger"  THEN 
            ASSIGN zwunsch-rmember.s-label  = "drop-passanger"
                   zwunsch-rmember.s-value2 = "Y".
            ELSE IF str MATCHES "*WCI-req*" THEN
            ASSIGN zwunsch-rmember.s-label  = "WCI-req"
                   zwunsch-rmember.s-value2 = ENTRY(2, str, "=").
        END.
        
        FOR EACH zwunsch-rmember:
            FIND FIRST zwunsch-rline WHERE zwunsch-rline.s-label =
                zwunsch-rmember.s-label NO-ERROR.
            IF AVAILABLE zwunsch-rline THEN 
            ASSIGN zwunsch-rmember.s-value2 = zwunsch-rline.s-value2
                   zwunsch-rline.used       = YES.
        END.
        FOR EACH zwunsch-rline WHERE NOT zwunsch-rline.used:
            CREATE zwunsch-rmember.
            BUFFER-COPY zwunsch-rline TO zwunsch-rmember.
        END.
        FOR EACH zwunsch-rline WHERE zwunsch-rline.used:
            zwunsch-rline.used = NO.
        END.

        ASSIGN ct = "".
        FOR EACH zwunsch-rmember:
            IF zwunsch-rmember.s-value2 NE "" THEN
            DO: 
                IF zwunsch-rmember.s-value2 = "Y" THEN
                ct = ct + zwunsch-rmember.s-label + ";".
                ELSE
                ct = ct + zwunsch-rmember.s-label 
                   + zwunsch-rmember.s-value2 + ";".
            END.
            DELETE zwunsch-rmember.
        END.
        ASSIGN rbuff.zimmer-wunsch = ct.
                
        IF rmember.resstatus NE 11 AND rmember.resstatus NE 13 THEN
            RUN check-fixrates-changes.

        FIND CURRENT rbuff NO-LOCK.
        RUN res-changes.
        RUN check-timebl.p(2, rmember.resnr, rmember.reslinnr, 
        "res-line", init-time, init-date, OUTPUT do-it, 
        OUTPUT init-time, OUTPUT init-date).
    END.
    FIND NEXT rmember WHERE rmember.resnr = curr-resline.resnr
        AND rmember.active-flag = 0 
        /*AND rmember.reslinnr NE 12*/
        AND rmember.reslinnr NE curr-resline.reslinnr 
        AND rmember.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
END.

PROCEDURE check-fixrates-changes:
DEF BUFFER rqsy FOR reslin-queasy.
DEF VARIABLE curr-date   AS DATE    NO-UNDO.
DEF VARIABLE start-date  AS DATE    NO-UNDO.
DEF VARIABLE start-time  AS INTEGER NO-UNDO.
DEF VARIABLE do-it       AS LOGICAL NO-UNDO.
DEF VARIABLE chgFlag     AS LOGICAL NO-UNDO.
DEF VARIABLE chg-mode    AS CHAR    NO-UNDO.
DEF VARIABLE curr-argt   AS CHAR    NO-UNDO.
    
    /*FIND FIRST reslin-queasy WHERE 
        reslin-queasy.KEY      = "fixrate-trace-record" AND
        reslin-queasy.resnr    = curr-resline.resnr AND
        reslin-queasy.reslinnr = curr-resline.reslinnr 
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE reslin-queasy THEN RETURN.*/

    FOR EACH update-fixrate:
        DELETE update-fixrate.
    END.
    
    FIND FIRST reslin-queasy WHERE 
        reslin-queasy.KEY      = "fixrate-trace-record" AND
        reslin-queasy.resnr    = curr-resline.resnr AND
        reslin-queasy.reslinnr = curr-resline.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN 
        ASSIGN
            start-date = reslin-queasy.date1
            start-time = reslin-queasy.number1
            
        .

    
    FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
        AND reslin-queasy.resnr    = curr-resline.resnr
        AND reslin-queasy.reslinnr = curr-resline.reslinnr
        NO-LOCK BY reslin-queasy.date1:
        IF reslin-queasy.date1 LT reslin-queasy.date2 THEN
        DO:
          DO curr-date = reslin-queasy.date1 + 1 TO reslin-queasy.date2:
            CREATE rqsy.
            BUFFER-COPY reslin-queasy EXCEPT date1 date2 TO rqsy.
            ASSIGN rqsy.date1 = curr-date
                   rqsy.date2 = curr-date
            .
            FIND CURRENT rqsy NO-LOCK.
          END.
          FIND FIRST rqsy WHERE RECID(rqsy) = RECID(reslin-queasy) 
            EXCLUSIVE-LOCK.
          ASSIGN rqsy.date2 = rqsy.date1.

          FIND FIRST update-fixrate WHERE update-fixrate.date1 = rqsy.date1
              AND update-fixrate.date2 = rqsy.date2 NO-LOCK NO-ERROR.
          IF NOT AVAILABLE update-fixrate THEN DO:
              CREATE update-fixrate.
              ASSIGN update-fixrate.date1 = rqsy.date1
                     update-fixrate.date2 = rqsy.date2
                     update-fixrate.argt  = rqsy.char1
               .
          END.

          FIND CURRENT rqsy NO-LOCK.
          RELEASE rqsy.
        END.
    END.

    FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
        AND reslin-queasy.resnr    = rmember.resnr
        AND reslin-queasy.reslinnr = rmember.reslinnr
        NO-LOCK BY reslin-queasy.date1:
        IF reslin-queasy.date1 LT reslin-queasy.date2 THEN
        DO:
          DO curr-date = reslin-queasy.date1 + 1 TO reslin-queasy.date2:
            CREATE rqsy.
            BUFFER-COPY reslin-queasy EXCEPT date1 date2 TO rqsy.
            ASSIGN rqsy.date1 = curr-date
                   rqsy.date2 = curr-date
            .

            FIND FIRST update-fixrate WHERE update-fixrate.date1 = rqsy.date1
                  AND update-fixrate.date2 = rqsy.date2 NO-LOCK NO-ERROR.
            IF AVAILABLE update-fixrate THEN ASSIGN rqsy.char1 = update-fixrate.argt.

            FIND CURRENT rqsy NO-LOCK.
          END.

          FIND FIRST rqsy WHERE RECID(rqsy) = RECID(reslin-queasy) 
            EXCLUSIVE-LOCK.
          ASSIGN rqsy.date2 = rqsy.date1.          

          FIND CURRENT rqsy NO-LOCK.
          RELEASE rqsy.
        END.
    END.

    FOR EACH reslin-queasy WHERE reslin-queasy.KEY = "arrangement"
      AND reslin-queasy.resnr    = curr-resline.resnr
      AND reslin-queasy.reslinnr = curr-resline.reslinnr
      NO-LOCK BY reslin-queasy.date1:
      do-it = (start-date LT reslin-queasy.date3) OR
             ((start-date EQ reslin-queasy.date3) AND
              (start-time LE reslin-queasy.number2)).
      
      IF do-it THEN
      DO:
        chg-mode = "CHG".
        FIND FIRST rqsy WHERE rqsy.KEY = "arrangement"
            AND rqsy.resnr    = rmember.resnr
            AND rqsy.reslinnr = rmember.reslinnr
            AND rqsy.date1    = reslin-queasy.date1
            NO-LOCK NO-ERROR.
        chgFlag = NOT AVAILABLE rqsy OR
            (AVAILABLE rqsy AND reslin-queasy.deci1 NE rqsy.deci1).
        IF chgFlag THEN
        DO:
          IF NOT AVAILABLE rqsy THEN 
          DO:    
            CREATE rqsy.
            ASSIGN
              rqsy.resnr    = rmember.resnr
              rqsy.reslinnr = rmember.reslinnr
              chg-mode      = "ADD"
            .
          END.
          ELSE FIND CURRENT rqsy EXCLUSIVE-LOCK.
          RUN fixrate-changes(chg-mode, reslin-queasy.date1,
              rqsy.deci1, reslin-queasy.deci1).          
          BUFFER-COPY reslin-queasy EXCEPT resnr reslinnr TO rqsy.
          FIND CURRENT rqsy NO-LOCK.
        END.
      END.
    END.
END.

PROCEDURE fixrate-changes:
DEF INPUT PARAMETER chg-mode  AS CHAR    NO-UNDO.
DEF INPUT PARAMETER curr-date AS DATE    NO-UNDO.
DEF INPUT PARAMETER old-rate  AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER new-rate  AS DECIMAL NO-UNDO.

DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 

DEF BUFFER rqy FOR reslin-queasy.

    IF rmember.changed NE ? THEN
    ASSIGN
        cid   = rmember.changed-id 
        cdate = STRING(rmember.changed)
    .

    IF chg-mode = "CHG" THEN
    DO:
        CREATE rqy.
        ASSIGN
          rqy.key         = "ResChanges"
          rqy.resnr       = rmember.resnr
          rqy.reslinnr    = rmember.reslinnr
          rqy.date2       = TODAY
          rqy.number2     = TIME 
        .  
        rqy.char3 = STRING(rmember.ankunft) + ";" 
                + STRING(rmember.ankunft) + ";" 
                + STRING(rmember.abreise) + ";" 
                + STRING(rmember.abreise) + ";" 
                + STRING(rmember.zimmeranz) + ";" 
                + STRING(rmember.zimmeranz) + ";" 
                + STRING(rmember.erwachs) + ";" 
                + STRING(rmember.erwachs) + ";" 
                + STRING(rmember.kind1) + ";" 
                + STRING(rmember.kind1) + ";" 
                + STRING(rmember.gratis) + ";" 
                + STRING(rmember.gratis) + ";" 
                + STRING(rmember.zikatnr) + ";" 
                + STRING(rmember.zikatnr) + ";" 
                + STRING(rmember.zinr) + ";" 
                + STRING(rmember.zinr) + ";"
                + STRING(rmember.arrangement) + ";" 
                + STRING(rmember.arrangement) + ";"
                + STRING(rmember.zipreis) + ";" 
                + STRING(rmember.zipreis) + ";"
                + STRING(cid) + ";" 
                + STRING(user-init) + ";" 
                + STRING(cdate, "x(8)") + ";" 
                + STRING(TODAY) + ";" 
                + STRING("CHG Fixrate FR:") + ";" 
                + STRING(curr-date) 
                + "-" + STRING(old-rate) + ";"
                + STRING("YES", "x(3)") + ";" 
                + STRING("YES", "x(3)") + ";" 
        .
        FIND CURRENT rqy NO-LOCK.
        RELEASE rqy. 
    END.

    CREATE rqy.
    ASSIGN
      rqy.key         = "ResChanges"
      rqy.resnr       = rmember.resnr
      rqy.reslinnr    = rmember.reslinnr
      rqy.date2       = TODAY
      rqy.number2     = TIME 
    .  
    rqy.char3 = STRING(rmember.ankunft) + ";" 
            + STRING(rmember.ankunft) + ";" 
            + STRING(rmember.abreise) + ";" 
            + STRING(rmember.abreise) + ";" 
            + STRING(rmember.zimmeranz) + ";" 
            + STRING(rmember.zimmeranz) + ";" 
            + STRING(rmember.erwachs) + ";" 
            + STRING(rmember.erwachs) + ";" 
            + STRING(rmember.kind1) + ";" 
            + STRING(rmember.kind1) + ";" 
            + STRING(rmember.gratis) + ";" 
            + STRING(rmember.gratis) + ";" 
            + STRING(rmember.zikatnr) + ";" 
            + STRING(rmember.zikatnr) + ";" 
            + STRING(rmember.zinr) + ";" 
            + STRING(rmember.zinr) + ";"
            + STRING(rmember.arrangement) + ";" 
            + STRING(rmember.arrangement) + ";"
            + STRING(rmember.zipreis) + ";" 
            + STRING(rmember.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + chg-mode + " " + STRING("Fixrate TO:") + ";" 
            + STRING(curr-date) 
            + "-" + STRING(new-rate) + ";"
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 
END.

PROCEDURE res-changes: 
DEFINE BUFFER guest1 FOR guest. 
DEFINE VARIABLE cid     AS CHAR     NO-UNDO FORMAT "x(2)" INITIAL "  ". 
DEFINE VARIABLE cdate   AS CHAR     NO-UNDO FORMAT "x(8)" INITIAL "        ". 
DEF VAR heute           AS DATE     NO-UNDO. 
DEF VAR zeit            AS INTEGER  NO-UNDO. 
 
    heute = TODAY. 
    zeit = TIME. 
    IF TRIM(t-resline.changed-id) NE "" THEN 
    DO: 
      cid = t-resline.changed-id. 
      cdate = STRING(t-resline.changed). 
    END. 
    ELSE IF LENGTH(t-resline.reserve-char) GE 14 THEN    /* created BY */ 
      cid = SUBSTR(t-resline.reserve-char,14). 
 
    CREATE reslin-queasy.
    ASSIGN
      reslin-queasy.key = "ResChanges"
      reslin-queasy.resnr = rbuff.resnr
      reslin-queasy.reslinnr = rbuff.reslinnr
      reslin-queasy.date2 = heute
      reslin-queasy.number2 = zeit. 
    .  
    reslin-queasy.char3 = STRING(t-resline.ankunft) + ";" 
                        + STRING(rbuff.ankunft) + ";" 
                        + STRING(t-resline.abreise) + ";" 
                        + STRING(rbuff.abreise) + ";" 
                        + STRING(t-resline.zimmeranz) + ";" 
                        + STRING(rbuff.zimmeranz) + ";" 
                        + STRING(t-resline.erwachs) + ";" 
                        + STRING(rbuff.erwachs) + ";" 
                        + STRING(t-resline.kind1) + ";" 
                        + STRING(rbuff.kind1) + ";" 
                        + STRING(t-resline.gratis) + ";" 
                        + STRING(rbuff.gratis) + ";" 
                        + STRING(t-resline.zikatnr) + ";" 
                        + STRING(rbuff.zikatnr) + ";" 
                        + STRING(t-resline.zinr) + ";" 
                        + STRING(rbuff.zinr) + ";". 

    IF rbuff.reserve-int = t-resline.reserve-int THEN 
    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(t-resline.arrangement) + ";" 
                        + STRING(rbuff.arrangement) + ";". 
    ELSE 
    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(t-resline.arrangement) + ";" 
                        + STRING(t-resline.reserve-int) + ";".

    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(t-resline.zipreis) + ";" 
                        + STRING(rbuff.zipreis) + ";"
                        + STRING(cid) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(cdate, "x(8)") + ";" 
                        + STRING(heute) + ";" 
                        + STRING(t-resline.NAME) + ";" 
                        + STRING(t-resline.bemerk) + ";". 
    IF rbuff.was-status = 0 THEN 
      reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";". 
    ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";". 
    reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";". 
  
    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
 
    IF t-resline.bemerk NE rbuff.bemerk THEN
    DO: 
        CREATE res-history. 
        ASSIGN 
            res-history.nr = bediener.nr 
            res-history.resnr = t-resline.resnr 
            res-history.reslinnr = t-resline.reslinnr 
            res-history.datum = heute 
            res-history.zeit = zeit 
            res-history.aenderung = t-resline.bemerk 
            res-history.action = "Remark". 
 
        res-history.aenderung = t-resline.bemerk + CHR(10) + CHR(10) 
            + "*** Changed to:" + CHR(10) + CHR(10) 
            + rbuff.bemerk. 
        IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history. 
    END. 
END. 



PROCEDURE update-special-request:
DEF BUFFER rqsy FOR reslin-queasy.
    FIND FIRST rqsy WHERE rqsy.KEY = "specialRequest"
        AND rqsy.resnr = rmember.resnr
        AND rqsy.reslinnr = rmember.reslinnr EXCLUSIVE-LOCK
        NO-ERROR.
    IF NOT AVAILABLE rqsy THEN
    DO:
        CREATE rqsy.
        ASSIGN
            rqsy.KEY      = "specialRequest"
            rqsy.resnr    = rmember.resnr
            rqsy.reslinnr = rmember.reslinnr
        .
    END.
    ASSIGN rqsy.char3 = spreqBuff.char3.
    FIND CURRENT rqsy NO-LOCK.
    RELEASE rqsy.
END.
