DEF TEMP-TABLE t-h-bill  LIKE h-bill  
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-tisch   LIKE tisch.

DEF TEMP-TABLE t-queasy33 LIKE queasy.
DEF TEMP-TABLE t-queasy31 LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resnr       AS INT.
DEF INPUT  PARAMETER reslinnr    AS INT.
/*FD Oct 18, 2022 => for Web*/
DEF INPUT  PARAMETER tischnr     AS INT.
DEF INPUT  PARAMETER curr-waiter AS INT.
DEF INPUT  PARAMETER tkellner-masterkey AS LOGICAL.
DEF INPUT  PARAMETER dept-no     AS INT.
DEF INPUT  PARAMETER TABLE FOR t-h-bill.
DEF INPUT  PARAMETER TABLE FOR t-tisch.

DEF OUTPUT PARAMETER rmno        AS CHAR.
DEF OUTPUT PARAMETER remark      AS CHAR.
DEF OUTPUT PARAMETER klimit      AS DECIMAL.
DEF OUTPUT PARAMETER ksaldo      AS DECIMAL.
DEF OUTPUT PARAMETER recid-bill  AS INT INIT 0.
DEF OUTPUT PARAMETER avail-bill  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER resline     AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER msg-str     AS CHAR INIT "".


{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-tbplan".

DEFINE VARIABLE p-1342 AS LOGICAL.
DEFINE VARIABLE table-ok AS LOGICAL INIT YES.

/*FD August 05, 2021 => Req Amaranta*/
DEFINE VARIABLE i AS INTEGER NO-UNDO.
DEFINE VARIABLE str AS CHARACTER NO-UNDO.
DEFINE VARIABLE child-age AS CHARACTER NO-UNDO.

DEFINE VARIABLE ci-date AS DATE NO-UNDO.

FIND FIRST vhp.htparam WHERE paramnr = 87 NO-LOCK.
ci-date = vhp.htparam.fdate.

FOR EACH queasy WHERE queasy.KEY EQ 33 AND queasy.number1 EQ dept-no
    AND queasy.date1 EQ ci-date AND queasy.logi3 EQ YES NO-LOCK:
    CREATE t-queasy33.
    BUFFER-COPY queasy TO t-queasy33.
END.

FOR EACH vhp.queasy WHERE vhp.queasy.key EQ 31 AND vhp.queasy.number1 EQ dept-no
    AND vhp.queasy.betriebsnr EQ 0 NO-LOCK BY vhp.queasy.number2:

    CREATE t-queasy31.
    BUFFER-COPY queasy TO t-queasy31.
    ASSIGN t-queasy31.rec-id = RECID(queasy).
END.

FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = resnr 
    AND vhp.res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.res-line THEN 
DO:
  resline = YES.
  RUN check-creditlimit. 
  rmno = vhp.res-line.zinr.
END.
ELSE
DO:
    /*FDL Sept 20, 2023 => Ticket 0C54BE*/
    FIND FIRST t-h-bill WHERE t-h-bill.tischnr EQ tischnr NO-LOCK NO-ERROR.
    IF AVAILABLE t-h-bill THEN
    DO:
        IF t-h-bill.resnr NE 0 AND t-h-bill.reslinnr EQ 0 THEN
        DO:
            FIND FIRST mc-guest WHERE mc-guest.gastnr EQ t-h-bill.resnr
                AND mc-guest.activeflag EQ YES NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN
            DO:
                ASSIGN remark = translateExtended ("Membership No:",lvCAREA,"") 
                    + " " + mc-guest.cardnum + CHR(10).
            END.
        END.
    END.
END.

/*FD Oct 18, 2022 => for Web*/
RUN htplogic.p (1342, OUTPUT p-1342).
FIND FIRST t-h-bill WHERE t-h-bill.tischnr EQ tischnr NO-LOCK NO-ERROR.
IF AVAILABLE t-h-bill THEN
DO:
    IF NOT p-1342 THEN /*FD Dec 17, 2021 => Yes for multi waiter's at same table*/
    DO:        
        IF NOT tkellner-masterkey THEN   
        DO:   
            IF AVAILABLE t-h-bill AND t-h-bill.kellner-nr NE curr-waiter THEN table-ok = NO.   
            ELSE
            DO:
                FIND FIRST t-tisch WHERE t-tisch.tischnr EQ tischnr NO-LOCK NO-ERROR.
                IF AVAILABLE t-tisch THEN
                DO:
                    IF t-tisch.kellner-nr NE 0 AND t-tisch.kellner-nr NE curr-waiter THEN table-ok = NO.
                END.                     
            END.                   
            IF NOT table-ok THEN   
            DO:   
                msg-str = translateExtended ("This table belongs to other waiter.",lvCAREA,"").
                RETURN.   
            END.   
        END.
    END.
END.

RUN getremark-rsv-table. /*FD Nov 04, 2022 => for Web*/

/************************************ PROCEDURE ************************************/
PROCEDURE check-creditlimit:
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 

  FIND FIRST vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
  FIND FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.res-line.gastnrpay NO-LOCK. 

  FIND FIRST vhp.mc-guest WHERE mc-guest.gastnr = vhp.guest.gastnr
      AND vhp.mc-guest.activeflag = YES NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.mc-guest THEN
  ASSIGN remark = translateExtended ("Membership No:",lvCAREA,"") 
      + " " + vhp.mc-guest.cardnum + CHR(10).

  IF vhp.guest.kreditlimit NE 0 THEN klimit = vhp.guest.kreditlimit. 
  ELSE 
  DO: 
    IF vhp.htparam.fdecimal NE 0 THEN klimit = vhp.htparam.fdecimal. 
    ELSE klimit = vhp.htparam.finteger. 
  END. 
  
  ksaldo = 0. 
  FIND FIRST vhp.bill WHERE vhp.bill.resnr = vhp.res-line.resnr 
    AND vhp.bill.reslinnr = vhp.res-line.reslinnr AND vhp.bill.flag = 0 
    AND vhp.bill.zinr = vhp.res-line.zinr NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.bill THEN 
  DO:
      recid-bill = RECID(vhp.bill).
      avail-bill = YES.
      ksaldo = vhp.bill.saldo. 
  END.

  /*
  remark = remark + STRING(vhp.res-line.ankunft) + " - " 
    + STRING(vhp.res-line.abreise) + CHR(10) 
    + "A " + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
    + "  Ch " + STRING(vhp.res-line.kind1) 
    + " - " + vhp.res-line.arrangement + CHR(10) 
    + vhp.res-line.bemerk. 
  */

  /*FD August 05, 2021 => Req Amaranta*/
  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    str = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(str,1,5) = "ChAge" THEN child-age = SUBSTR(str,6).
  END.
  
  IF child-age NE "" THEN
  DO:
    remark = remark + STRING(vhp.res-line.ankunft) + " - " 
      + STRING(vhp.res-line.abreise) + CHR(10) 
      + "A:" + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
      + " Ch:" + STRING(vhp.res-line.kind1) 
      + " " + "(" + child-age + ")"
      + " - " + vhp.res-line.arrangement + CHR(10) 
      + vhp.res-line.bemerk. 
  END.
  ELSE
  DO:
    remark = remark + STRING(vhp.res-line.ankunft) + " - " 
      + STRING(vhp.res-line.abreise) + CHR(10) 
      + "A:" + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
      + " Ch:" + STRING(vhp.res-line.kind1)       
      + " - " + vhp.res-line.arrangement + CHR(10) 
      + vhp.res-line.bemerk. 
  END.
END. 

PROCEDURE getremark-rsv-table:
    DEFINE VARIABLE hh1             AS CHAR    NO-UNDO.  
    DEFINE VARIABLE hh2             AS CHAR    NO-UNDO.  
    DEFINE VARIABLE hh3             AS CHAR    NO-UNDO.  
    DEFINE VARIABLE zeit            AS INTEGER NO-UNDO.  
    DEFINE VARIABLE table-occupied  AS LOGICAL NO-UNDO.


    FIND FIRST t-queasy31 WHERE t-queasy31.number2 EQ tischnr NO-ERROR.
    table-occupied = AVAILABLE t-queasy31 AND t-queasy31.date1 NE ?. 

    DO:   
        hh1 = STRING(TIME,"HH:MM").  
        hh1 = SUBSTR(hh1,1,2) + SUBSTR(hh1,4,2).  
        hh2 = STRING(INTEGER(SUBSTR(hh1,1,2)) + 2, "99") + SUBSTR(hh1,3,2).  
        hh3 = STRING(TIME - 1800,"HH:MM").  
        hh3 = SUBSTR(hh3,1,2) + SUBSTR(hh3,4,2).  

        FIND FIRST t-queasy33 WHERE t-queasy33.number2 EQ tischnr  
            AND hh1 LE t-queasy33.char1 AND hh2 GE t-queasy33.char1 NO-ERROR.  
        IF NOT AVAILABLE t-queasy33 AND NOT table-occupied THEN  
        DO:
            FIND FIRST t-queasy33 WHERE t-queasy33.number2 EQ tischnr  
                AND hh1 GE t-queasy33.char1 AND hh3 LE t-queasy33.char1 NO-ERROR.
        END.              

        IF AVAILABLE t-queasy33 THEN  
        DO:  
            zeit = INTEGER(SUBSTR(t-queasy33.char1,1,2)) * 3600 + INTEGER(SUBSTR(t-queasy33.char1,3,2)) * 60.  
            IF zeit GT TIME THEN  
            DO:
                remark = remark + ENTRY(1,t-queasy33.char2,"&&") + " - " + TRIM(SUBSTR(t-queasy33.char1,10)) + CHR(10)  
                    + STRING(SUBSTR(t-queasy33.char1,1,4),"99:99") + " - "  
                    + STRING(SUBSTR(t-queasy33.char1,5,4),"99:99") + CHR(10)  
                    + translateExtended("Pax:",lvCAREA,"") + " "   
                    + STRING(t-queasy33.number3) + CHR(10)  
                    + translateExtended("Remain Time:",lvCAREA,"") + " "   
                    + STRING(zeit - TIME,"HH:MM").
            END.              
            ELSE
            DO:
                remark = remark + ENTRY(1,t-queasy33.char2,"&&") + " - " + TRIM(SUBSTR(t-queasy33.char1,10)) + CHR(10)  
                    + STRING(SUBSTR(t-queasy33.char1,1,4),"99:99") + " - "  
                    + STRING(SUBSTR(t-queasy33.char1,5,4),"99:99") + CHR(10)  
                    + translateExtended("Pax:",lvCAREA,"") + " "   
                    + STRING(t-queasy33.number3) + CHR(10)  
                    + translateExtended("Current Time:",lvCAREA,"") + " "   
                    + STRING(TIME,"HH:MM").  
            END.            
            /* Dzikri 38254B - add remark and deposit from table reservation */
            IF TRIM(ENTRY(2,t-queasy33.char3,";")) NE "" THEN
            DO:
                remark = remark + CHR(10)  
                + translateExtended("Remark:",lvCAREA,"") + " " + TRIM(ENTRY(2,t-queasy33.char3,";")).
            END.
            IF t-queasy33.deci1 NE 0 THEN
            DO:
                remark = remark + CHR(10)
                + translateExtended("Deposit:",lvCAREA,"") + " " + TRIM(STRING(t-queasy33.deci1,"->>>,>>>,>>>,>>9.99")).
            END.
            /* Dzikri 38254B - END */
        END.  
    END.  
END PROCEDURE.
