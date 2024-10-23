/************TEMP-TABLE**********/

DEFINE TEMP-TABLE output-list
  FIELD NAME                AS CHARACTER 
  FIELD room                AS DECIMAL
  FIELD pax                 AS DECIMAL
  FIELD logis               AS DECIMAL
  FIELD proz                AS DECIMAL
  FIELD avrgrate            AS DECIMAL
  FIELD m-room              AS DECIMAL
  FIELD m-pax               AS DECIMAL
  FIELD m-logis             AS DECIMAL
  FIELD m-proz              AS DECIMAL
  FIELD m-avrgrate          AS DECIMAL
  FIELD y-room              AS DECIMAL
  FIELD y-pax               AS DECIMAL
  FIELD y-logis             AS DECIMAL
  FIELD y-proz              AS DECIMAL
  FIELD y-avrgrate          AS DECIMAL
  FIELD comp-room           AS DECIMAL
  FIELD comp-pax            AS DECIMAL
  FIELD comp-m-room         AS DECIMAL
  FIELD comp-m-pax          AS DECIMAL
  FIELD comp-y-room         AS DECIMAL
  FIELD comp-y-pax          AS DECIMAL
  FIELD exC-avrgrate        AS DECIMAL
  FIELD exC-m-avrgrate      AS DECIMAL
  FIELD exC-y-avrgrate      AS DECIMAL
  FIELD flag                AS INTEGER
  FIELD name2                AS CHAR   
  FIELD rmnite1             AS INTEGER
  FIELD rmrev1              AS DECIMAL
  FIELD rmnite              AS INTEGER
  FIELD rmrev               AS DECIMAL.  

DEFINE TEMP-TABLE to-list 
  FIELD gastnr          AS INTEGER 
  FIELD name            AS CHAR FORMAT "x(40)"  /*24*//*ger format name 8D1C55*/ 
  FIELD zinr            LIKE zimmer.zinr
                        
  FIELD room            AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD c-room          AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD pax             AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD logis           AS DECIMAL FORMAT "->>,>>>,>>9"     INITIAL 0  
  FIELD proz            AS DECIMAL FORMAT "->9.99"          INITIAL 0 
  FIELD avrgrate        AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD exC-avrgrate    AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD comp-room       AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD comp-pax        AS INTEGER FORMAT ">>9"             INITIAL 0 
 
  FIELD m-room          AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
  FIELD mc-room         AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD m-pax           AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
  FIELD m-logis         AS DECIMAL FORMAT ">,>>>,>>>,>>9"   INITIAL 0 
  FIELD m-proz          AS DECIMAL FORMAT "->9.99"          INITIAL 0 
  FIELD m-avrgrate      AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD exC-m-avrgrate  AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD comp-m-room     AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
  FIELD comp-m-pax      AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
 
  FIELD y-room          AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 
  FIELD yc-room         AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD y-pax           AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 
  FIELD y-logis         AS DECIMAL FORMAT "->,>>>,>>>,>>9"  INITIAL 0 
  FIELD y-proz          AS DECIMAL FORMAT "->9.99"          INITIAL 0 
  FIELD y-avrgrate      AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0
  FIELD exC-y-avrgrate  AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0
  FIELD comp-y-room     AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 
  FIELD comp-y-pax      AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 .
 
DEFINE TEMP-TABLE to-list1 
  FIELD gastnr          AS INTEGER 
  FIELD name            AS CHAR FORMAT "x(40)"  /*24*//*ger format name 8D1C55*/
 
  FIELD room            AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD c-room          AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD pax             AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD logis           AS DECIMAL FORMAT "->>,>>>,>>9"     INITIAL 0 
  FIELD proz            AS DECIMAL FORMAT "->9.99"          INITIAL 0 
  FIELD avrgrate        AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD exC-avrgrate     AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD comp-room       AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD comp-pax        AS INTEGER FORMAT ">>9"             INITIAL 0 
 
  FIELD m-room          AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
  FIELD mc-room         AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD m-pax           AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
  FIELD m-logis         AS DECIMAL FORMAT ">,>>>,>>>,>>9"   INITIAL 0 
  FIELD m-proz          AS DECIMAL FORMAT "->9.99"          INITIAL 0 
  FIELD m-avrgrate      AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0
  FIELD exC-m-avrgrate  AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD comp-m-room     AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
  FIELD comp-m-pax      AS INTEGER FORMAT ">>,>>9"          INITIAL 0 
 
  FIELD y-room          AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 
  FIELD yc-room         AS INTEGER FORMAT ">>9"             INITIAL 0 
  FIELD y-pax           AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 
  FIELD y-logis         AS DECIMAL FORMAT "->,>>>,>>>,>>9"  INITIAL 0 
  FIELD y-proz          AS DECIMAL FORMAT "->9.99"          INITIAL 0 
  FIELD y-avrgrate      AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0
  FIELD exC-y-avrgrate  AS DECIMAL FORMAT "->,>>>,>>9"      INITIAL 0 
  FIELD comp-y-room     AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 
  FIELD comp-y-pax      AS INTEGER FORMAT ">>>,>>9"         INITIAL 0 .

 /*SIS 22-01-13 --> mengubah format*/
 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER op-type          AS INTEGER.
/*0 create list, 1 design lnl, 2 print lnl, 3 print txt*/
DEFINE INPUT PARAMETER printer-nr       AS INTEGER.
DEFINE INPUT PARAMETER call-from        AS INTEGER.
DEFINE INPUT PARAMETER txt-file         AS CHAR.

DEFINE INPUT PARAMETER disptype         AS INTEGER.
DEFINE INPUT PARAMETER cardtype-1       AS INTEGER.
DEFINE INPUT PARAMETER currency-type    AS INTEGER.
DEFINE INPUT PARAMETER YTD-flag         AS INTEGER. /*1, YTD, 2 FDTD*/
DEFINE INPUT PARAMETER excl-comp        AS LOGICAL.
DEFINE INPUT PARAMETER last-sort        AS INTEGER.
DEFINE INPUT PARAMETER f-date           AS DATE.
DEFINE INPUT PARAMETER t-date           AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

/*1 Name, 2 MTD RmRev, 3 MTD RmNight, 4 YTD RmRev, 5 YTD RmNight*/
/*
DEFINE NEW shared VARIABLE LnLDelimeter AS CHAR.
LnLdelimeter = CHR(2).

DEFINE NEW SHARED TEMP-TABLE lnl-table 
  FIELD nr   AS INTEGER
  FIELD lcol AS CHAR 
INDEX nr_idx nr.
DEFINE NEW SHARED VARIABLE user-init AS CHAR INITIAL "99".
DEFINE NEW SHARED VARIABLE product-name AS CHAR.

DEFINE variable op-type          AS INTEGER INITIAL 0.
/*0 create list, 1 design lnl, 2 print lnl, 3 print txt*/
DEFINE variable printer-nr       AS INTEGER.
DEFINE variable call-from        AS INTEGER INITIAL 1.
DEFINE variable txt-file         AS CHAR INITIAL "C:\vhp\Output FIle.txt".

DEFINE variable disptype         AS INTEGER INITIAL 2.
DEFINE variable cardtype         AS INTEGER INITIAL 2.
DEFINE variable currency-type    AS INTEGER INITIAL 2.
DEFINE variable YTD-flag         AS INTEGER INITIAL 1. /*1, YTD, 2 FDTD*/
DEFINE variable excl-comp        AS LOGICAL INITIAL NO.
DEFINE variable last-sort        AS INTEGER INITIAL 1.
DEFINE variable f-date           AS DATE INITIAL 02/01/11.
DEFINE variable t-date           AS DATE INITIAL 02/27/11.
DEFINE variable to-date          AS DATE INITIAL 09/05/11.

RUN add-persist-procedure. 
PROCEDURE add-persist-procedure: 
    DEFINE VARIABLE lvHS AS HANDLE              NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE lFound AS LOGICAL INIT FALSE    NO-UNDO. 
 
    DO lvI = 1 TO NUM-ENTRIES(SESSION:SUPER-PROCEDURES): 
        lvHS = WIDGET-HANDLE(ENTRY(lvI, SESSION:SUPER-PROCEDURES)). 
        IF VALID-HANDLE(lvHS) THEN DO: 
            IF lvHS:NAME BEGINS "supertrans" THEN 
                lFound = TRUE. 
        END. 
    END. 
 
    IF NOT lFound THEN DO: 
        RUN supertrans.p PERSISTENT SET lvHS. 
        SESSION:ADD-SUPER-PROCEDURE(lvHS). 
    END. 
END. 
*/ 
/*
DEFINE VARIABLE disptype AS INTEGER INITIAL 1 
       VIEW-AS RADIO-SET TOOLTIP "Output Sources" 
       VERTICAL RADIO-BUTTONS "&Guest Type", 1, "&Nationality", 2, 
       "&Source of Booking", 3, "Guest &Resident", 4, 
       "Domestic Market", 5 SIZE 20 BY 3.4. 
DEFINE VARIABLE cardtype AS INTEGER INITIAL 2 
       VIEW-AS RADIO-SET TOOLTIP "Type of Guest File" 
       VERTICAL RADIO-BUTTONS "&Individual", 0, "&Company", 1, 
       "&Travel Agent", 2, "&ALL", 3  SIZE 20 BY 2.9. 
DEFINE VARIABLE currency-type AS INTEGER INITIAL 1 
       VIEW-AS RADIO-SET TOOLTIP "Selected Currency" 
       VERTICAL RADIO-BUTTONS "&Local", 1, "&Foreign", 2 SIZE 15 BY 2.45. 

*/

/**********VARIABLES************/
{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rm-product". 

DEFINE VARIABLE cardtype        AS INTEGER NO-UNDO.
DEFINE VARIABLE ota-only        AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE foreign-nr      AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
 
DEFINE VARIABLE incl-comp       AS LOGICAL INITIAL YES.
 
DEFINE VARIABLE message-it      AS LOGICAL INITIAL YES. 
DEFINE VARIABLE ind             AS INTEGER. 
DEFINE VARIABLE room            AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE c-room          AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE pax             AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE logis           AS DECIMAL FORMAT "->>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE avrgrate        AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE exC-avrgrate    AS DECIMAL FORMAT "->,>>>,>>9". 

DEFINE VARIABLE comp-room       AS INTEGER FORMAT ">>9" INITIAL 0. 
DEFINE VARIABLE comp-pax        AS INTEGER FORMAT ">>9" INITIAL 0. 
 
DEFINE VARIABLE m-room          AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE mc-room         AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE m-pax           AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE m-logis         AS DECIMAL FORMAT ">,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE m-avrgrate      AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE exC-m-avrgrate  AS DECIMAL FORMAT "->,>>>,>>9". 

DEFINE VARIABLE comp-m-room     AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
DEFINE VARIABLE comp-m-pax      AS INTEGER FORMAT ">>,>>9" INITIAL 0. 
 
DEFINE VARIABLE y-room          AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE yc-room         AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-pax           AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-logis         AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE y-avrgrate      AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE exC-y-avrgrate  AS DECIMAL FORMAT "->,>>>,>>9". 
DEFINE VARIABLE comp-y-room     AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
DEFINE VARIABLE comp-y-pax      AS INTEGER FORMAT ">>>,>>9" INITIAL 0. 
 
DEFINE VARIABLE from-bez        AS CHAR FORMAT "x(22)". 
DEFINE VARIABLE to-bez          AS CHAR FORMAT "x(22)". 
 
DEFINE VARIABLE curr-select     AS CHAR INITIAL "". 
 
DEFINE STREAM s1. 

DEF VAR tot AS CHAR NO-UNDO. 
tot = translateExtended ("T o t a l", lvCAREA,""). 




/*******************MAIN LOGIC**************/
IF cardtype-1 GE 10 THEN
ASSIGN
    cardtype = cardtype-1 - 10
    ota-only = YES
.
ELSE cardtype = cardtype-1.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
END. 

CASE op-type:
    WHEN 0 THEN
    DO:
        IF disptype = 1 THEN 
        DO: 
            IF cardtype LT 3 THEN RUN create-umsatz1.   /*individu comp travel agent*/
            ELSE RUN create-umsatz11. /*aLL*/
        END. 
        ELSE IF disptype = 2 THEN RUN create-umsatz2. /*  BY nation */ 
        ELSE IF disptype = 3 THEN RUN create-umsatz3. 
        ELSE IF disptype = 4 THEN RUN create-umsatz4. 
        ELSE IF disptype = 5 THEN RUN create-umsatz5. 
    END.
    /*MT
    WHEN 1 THEN
    DO:
        RUN design-lnl.
    END.
    WHEN 2 THEN
    DO:
        RUN print-lnl.
    END.
    WHEN 3 THEN
    DO:
        RUN print-txt.
    END.
    */
END CASE.


/***************PROCEDURE*************/
DEFINE TEMP-TABLE tmp-room
    FIELD gastnr    AS INTEGER
    FIELD zinr      LIKE zimmer.zinr
    FIELD flag      AS INTEGER
    INDEX gstnr gastnr DESC zinr.      /*1 DATE    2 MONTH   3 YEAR*/
DEFINE TEMP-TABLE tmp-room1 LIKE tmp-room.

PROCEDURE create-umsatz1:
    DEFINE VARIABLE mm AS INTEGER. 
    DEFINE VARIABLE yy AS INTEGER. 
    DEFINE VARIABLE from-date AS DATE.
    DEFINE VARIABLE datum AS DATE.
    DEFINE VARIABLE curr-zinr LIKE zimmer.zinr INIT "".
    DEFINE VARIABLE prev-zinr LIKE zimmer.zinr INIT "".

    DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
    DEFINE VARIABLE curr-gastnr AS INT INIT 0.
    DEFINE VARIABLE prev-gastnr AS INT INIT 0.
    DEFINE VARIABLE beg-date    AS DATE NO-UNDO.

    incl-comp = NOT excl-comp. 
    ASSIGN
      room          = 0 
      c-room        = 0 
      comp-room     = 0 
      pax           = 0 
      logis         = 0
      m-room        = 0 
      mc-room       = 0 
      comp-m-room   = 0
      m-pax         = 0 
      m-logis       = 0 
      y-room        = 0 
      yc-room       = 0 
      comp-y-room   = 0 
      y-pax         = 0 
      y-logis       = 0. 

    IF ytd-flag = 2 THEN
    DO:        
      /*to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date).
      beg-date = DATE(MONTH(f-date),1,yy).

      IF f-date GT beg-date THEN ASSIGN beg-date = f-date.
      IF MONTH(to-date) GT MONTH(f-date) THEN ASSIGN beg-date = DATE(mm,1,yy).
      from-date = beg-date.*/

      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
    END. 
    ELSE 
    DO: 
      mm = month(to-date). 
      yy = year(to-date). 
      from-date = DATE(1,1,yy). 
    END. 

        
    FOR EACH output-list: 
      delete output-list. 
    END. 
    FOR EACH to-list: 
      delete to-list. 
    END. 
    FOR EACH tmp-room:
        DELETE tmp-room.
    END.
    FOR EACH tmp-room1:
        DELETE tmp-room1.
    END.
    
    /*MTIF incl-comp THEN*/
    FOR EACH genstat WHERE genstat.datum GE from-date
      AND genstat.datum LE to-date 
        /*AND genstat.karteityp = cardtype*/
      AND genstat.resstatus NE 13
        /*AND genstat.res-int[1] NE 13*/
      AND genstat.segmentcode NE 0 
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
      USE-INDEX gastnrmember_ix NO-LOCK,
      FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp = cardtype
      USE-INDEX gastnr_index NO-LOCK BY guest.NAME  BY guest.gastnr BY genstat.zinr :

      do-it = YES.
      IF guest.karteityp = 2 AND ota-only THEN
        do-it = guest.steuernr NE "".

      IF do-it THEN
      DO:
        datum = genstat.datum. 
        PROCESS EVENTS. 
        exchg-rate = 1. 

        IF currency-type = 2 THEN 
        DO: 
          IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
            AND exrate.datum = datum NO-LOCK NO-ERROR. 
          ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
          IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
        END. 
        
        prev-zinr = curr-zinr.
        curr-zinr = genstat.zinr.

        prev-gastnr = curr-gastnr.
        curr-gastnr = genstat.gastnr.
        FIND FIRST to-list WHERE to-list.gastnr EQ genstat.gastnr NO-ERROR.
        IF NOT AVAILABLE to-list THEN
        DO: 
            CREATE to-list.
            ASSIGN to-list.gastnr = genstat.gastnr
                        to-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                          + guest.anrede1 + guest.anredefirma.

                FIND FIRST bediener WHERE bediener.userinit = guest.phonetik3 NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN
                    to-list.NAME = to-list.NAME + "=" + bediener.username.


                IF genstat.datum EQ to-date THEN
                DO:
                    FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                        AND tmp-room.zinr EQ genstat.zinr 
                        AND tmp-room.flag = 1 NO-ERROR.
                    IF NOT AVAILABLE tmp-room THEN
                    DO:
                        to-list.room = to-list.room + 1.
                        room = room + 1.

                        CREATE tmp-room.
                        ASSIGN tmp-room.gastnr = genstat.gastnr
                                    tmp-room.zinr = genstat.zinr
                                    tmp-room.flag = 1.
                    END.
                    to-list.pax = to-list.pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    logis = logis + genstat.logis / exchg-rate.
                END.
                IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                DO:
                    to-list.m-room = to-list.m-room + 1.
                    m-room = m-room + 1.
                    to-list.m-pax = to-list.m-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
                    m-pax = m-pax + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    m-logis = m-logis + genstat.logis / exchg-rate.
                END.

                IF ytd-flag = 1 OR ytd-flag = 2 THEN
                DO:
                    to-list.y-room = to-list.y-room + 1.
                    y-room = y-room + 1.
                   
                    to-list.y-pax = to-list.y-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
                    y-pax = y-pax + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    y-logis = y-logis + genstat.logis / exchg-rate.
                END.
        END.
        ELSE
        DO:
                IF genstat.datum EQ to-date THEN
                DO:  
                    FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                        AND tmp-room.zinr EQ genstat.zinr 
                        AND tmp-room.flag = 1 NO-ERROR.
                    IF NOT AVAILABLE tmp-room THEN
                    DO:
                        to-list.room = to-list.room + 1.
                        room = room + 1.

                        CREATE tmp-room.
                        ASSIGN tmp-room.gastnr = genstat.gastnr
                                    tmp-room.zinr = genstat.zinr
                                    tmp-room.flag = 1.
                    END.
                    to-list.pax = to-list.pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    logis = logis + genstat.logis / exchg-rate.      
                END.
                IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                DO:
                    to-list.m-room = to-list.m-room + 1.
                    m-room = m-room + 1.
                    to-list.m-pax = to-list.m-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
                    m-pax = m-pax + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    m-logis = m-logis + genstat.logis / exchg-rate.
                END.

                IF ytd-flag = 1 OR ytd-flag = 2  THEN
                DO:
                    to-list.y-room = to-list.y-room + 1.
                    y-room = y-room + 1.

                    to-list.y-pax = to-list.y-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
                    y-pax = y-pax + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    y-logis = y-logis + genstat.logis / exchg-rate.
                END.
        END.
      END.
    END.
    
    /*MTELSE    */
    FOR EACH genstat WHERE genstat.datum GE from-date
      AND genstat.datum LE to-date 
        /*AND genstat.karteityp = cardtype*/
      AND genstat.gratis EQ 0
      AND genstat.resstatus NE 13
        /*AND genstat.res-int[1] NE 13*/
      AND genstat.segmentcode NE 0   
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
      USE-INDEX gastnrmember_ix NO-LOCK,
      FIRST guest WHERE guest.gastnr = genstat.gastnr AND guest.karteityp = cardtype
      USE-INDEX gastnr_index NO-LOCK BY guest.NAME BY guest.gastnr
      BY genstat.zinr :

      do-it = YES.
      IF guest.karteityp = 2 AND ota-only THEN
        do-it = guest.steuernr NE "".

      IF do-it THEN
      DO:
        datum = genstat.datum. 
        PROCESS EVENTS. 
        exchg-rate = 1. 

        IF currency-type = 2 THEN 
        DO: 
          IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
            AND exrate.datum = datum NO-LOCK NO-ERROR. 
          ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
          IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
        END. 
        
        prev-zinr = curr-zinr.
        curr-zinr = genstat.zinr.

        prev-gastnr = curr-gastnr.
        curr-gastnr = genstat.gastnr.
        FIND FIRST to-list WHERE to-list.gastnr EQ genstat.gastnr NO-ERROR.
        IF NOT AVAILABLE to-list THEN       /*awal*/
        DO: 
            CREATE to-list.
            ASSIGN to-list.gastnr = genstat.gastnr
                        to-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                          + guest.anrede1 + guest.anredefirma.
                
                FIND FIRST bediener WHERE bediener.userinit = guest.phonetik3 NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN
                    to-list.NAME = to-list.NAME + "=" + bediener.username.

                IF genstat.datum EQ to-date THEN
                DO:
                    FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                        AND tmp-room1.zinr EQ genstat.zinr 
                        AND tmp-room1.flag = 1 NO-ERROR.
                    IF NOT AVAILABLE tmp-room1 THEN
                    DO:
                        to-list.comp-room = to-list.comp-room + 1.
                        comp-room = comp-room + 1.

                        CREATE tmp-room1.
                        ASSIGN tmp-room1.gastnr = genstat.gastnr
                                    tmp-room1.zinr = genstat.zinr
                                    tmp-room1.flag = 1.
                    END.
                    to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2.
                    /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/
                    comp-pax = comp-pax + genstat.erwachs + genstat.kind1 + genstat.kind2.
                    /*MTlogis = logis + genstat.logis / exchg-rate.*/
                END.

                IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                DO: 
                    to-list.comp-m-room = to-list.comp-m-room + 1.
                    comp-m-room = comp-m-room + 1.
                    to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2.
                    /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/
                    comp-m-pax = comp-m-pax + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2.
                    /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                END.

                 IF ytd-flag = 1 OR ytd-flag = 2  THEN
                 DO:
                    to-list.comp-y-room = to-list.comp-y-room + 1.
                    comp-y-room = comp-y-room + 1.

                    to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs + genstat.kind1 + genstat.kind2.
                    comp-y-pax = comp-y-pax + genstat.erwachs + genstat.kind1 + genstat.kind2.
                    /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
                    y-logis = y-logis + genstat.logis / exchg-rate.*/
                END.
        END.
        ELSE
        DO:
                IF genstat.datum EQ to-date THEN
                DO: 
                    FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                        AND tmp-room1.zinr EQ genstat.zinr 
                        AND tmp-room1.flag = 1 NO-ERROR.
                    IF NOT AVAILABLE tmp-room1 THEN
                    DO:
                        to-list.comp-room = to-list.comp-room + 1.
                        comp-room = comp-room + 1.

                        CREATE tmp-room1.
                        ASSIGN tmp-room1.gastnr = genstat.gastnr
                                    tmp-room1.zinr = genstat.zinr
                                    tmp-room1.flag = 1.
                    END.
                    to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2.
                    /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/
                    comp-pax = comp-pax + genstat.erwachs + genstat.kind1 + genstat.kind2.
                    /*MTlogis = logis + genstat.logis / exchg-rate.*/
                END.
                IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                DO:
                    to-list.comp-m-room = to-list.comp-m-room + 1.
                    comp-m-room = comp-m-room + 1.

                    to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                      + genstat.kind1 + genstat.kind2.
                    /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/
                    comp-m-pax = comp-m-pax + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2.
                    /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                END.

                IF ytd-flag = 1 OR ytd-flag = 2  THEN
                DO:
                    to-list.comp-y-room = to-list.comp-y-room + 1.
                    comp-y-room = comp-y-room + 1.

                    to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs + genstat.kind1 + genstat.kind2.
                    comp-y-pax = comp-y-pax + genstat.erwachs + genstat.kind1 + genstat.kind2.
                    /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
                    y-logis = y-logis + genstat.logis / exchg-rate.*/
                END.
        END.
      END.
    END.
    FOR EACH to-list: 
    IF (to-list.room - to-list.c-room) NE 0 THEN
        to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
    IF to-list.comp-room NE 0  THEN 
        to-list.exC-avrgrate = to-list.logis / to-list.comp-room.

    IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
      to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room).
    IF to-list.comp-m-room NE 0  THEN 
        to-list.exC-m-avrgrate = to-list.m-logis / to-list.comp-m-room.

    IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
      to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room).
    IF to-list.comp-y-room NE 0  THEN 
        to-list.exC-y-avrgrate = to-list.y-logis / to-list.comp-y-room.

    IF logis NE 0 THEN 
      to-list.proz = to-list.logis / logis * 100. 
    IF m-logis NE 0 THEN 
      to-list.m-proz = to-list.m-logis / m-logis * 100. 
    IF y-logis NE 0 THEN 
      to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END. 

    FOR EACH to-list NO-LOCK BY to-list.name: 
        create output-list.
        ASSIGN
            output-list.NAME            = to-list.name
            output-list.room            = to-list.room
            output-list.pax             = to-list.pax
            output-list.logis           = to-list.logis
            output-list.proz            = to-list.proz
            output-list.avrgrate        = to-list.avrgrate
            output-list.m-room          = to-list.m-room      
            output-list.m-pax           = to-list.m-pax       
            output-list.m-logis         = to-list.m-logis     
            output-list.m-proz          = to-list.m-proz      
            output-list.m-avrgrate      = to-list.m-avrgrate  
            output-list.y-room          = to-list.y-room      
            output-list.y-pax           = to-list.y-pax       
            output-list.y-logis         = to-list.y-logis     
            output-list.y-proz          = to-list.y-proz      
            output-list.y-avrgrate      = to-list.y-avrgrate  
            output-list.comp-room       = to-list.comp-room   
            output-list.comp-pax        = to-list.comp-pax    
            output-list.comp-m-room     = to-list.comp-m-room 
            output-list.comp-m-pax      = to-list.comp-m-pax  
            output-list.comp-y-room     = to-list.comp-y-room 
            output-list.comp-y-pax      = to-list.comp-y-pax  
            output-list.exC-avrgrate    = to-list.exC-avrgrate  
            output-list.exC-m-avrgrate  = to-list.exC-m-avrgrate
            output-list.exC-y-avrgrate  = to-list.exC-y-avrgrate
            output-list.name2           = to-list.name
            output-list.rmnite1         = to-list.y-room 
            output-list.rmrev1          = to-list.y-logis  
            output-list.rmnite          = to-list.m-room
            output-list.rmrev           = to-list.m-logis. 
    END.

  create output-list. 
  output-list.flag = 1. 
  DO ind = 1 TO 280: 
    output-list.name = output-list.name + "-". 
  END. 
  create output-list. 
  output-list.flag = 2. 
   /*avrgrate = 0. */
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
  IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room. 
  /*m-avrgrate = 0. */
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room).
  IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
  /*y-avrgrate = 0. */
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 
  IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room. 

  ASSIGN
    output-list.NAME            = "T o t a l"
    output-list.room            = room         
    output-list.pax             = pax          
    output-list.logis           = logis        
    output-list.proz            = 100          
    output-list.avrgrate        = avrgrate     
    output-list.m-room          = m-room       
    output-list.m-pax           = m-pax        
    output-list.m-logis         = m-logis     
    output-list.m-proz          = 100          
    output-list.m-avrgrate      = m-avrgrate   
    output-list.y-room          = y-room       
    output-list.y-pax           = y-pax        
    output-list.y-logis         = y-logis     
    output-list.y-proz          = 100          
    output-list.y-avrgrate      = y-avrgrate   
    output-list.comp-room       = comp-room    
    output-list.comp-pax        = comp-pax     
    output-list.comp-m-room     = comp-m-room 
    output-list.comp-m-pax      = comp-m-pax   
    output-list.comp-y-room     = comp-y-room 
    output-list.comp-y-pax      = comp-y-pax  
    output-list.exC-avrgrate    = exC-avrgrate 
    output-list.exC-m-avrgrate  = exC-m-avrgrate
    output-list.exC-y-avrgrate  = exC-y-avrgrate.

END PROCEDURE.


PROCEDURE create-umsatz11:          /*ALL bener*/
    DEFINE VARIABLE mm AS INTEGER. 
    DEFINE VARIABLE yy AS INTEGER. 
    DEFINE VARIABLE from-date AS DATE. 
    DEFINE VARIABLE datum AS DATE. 
    DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 1. 
    DEFINE VARIABLE do-it AS LOGICAL. 
    DEFINE VARIABLE beg-date    AS DATE NO-UNDO.

    incl-comp = NOT excl-comp. 

    room = 0. 
    c-room = 0. 
    pax = 0. 
    logis = 0. 
    m-room = 0. 
    mc-room = 0. 
    m-pax = 0. 
    m-logis = 0. 
    y-room = 0. 
    yc-room = 0. 
    y-pax = 0. 
    y-logis = 0. 

    comp-pax = 0. 
    comp-room = 0. 
    comp-y-room = 0. 
    comp-y-pax = 0. 
    comp-m-room = 0. 
    comp-m-pax = 0. 

    IF ytd-flag = 2 THEN
    DO:        
      /*to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date).
      beg-date = DATE(MONTH(f-date),1,yy).

      IF f-date GT beg-date THEN ASSIGN beg-date = f-date.
      IF MONTH(to-date) GT MONTH(f-date) THEN ASSIGN beg-date = DATE(mm,1,yy).
      from-date = beg-date.*/

      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
    END. 
    ELSE 
    DO: 
      mm = month(to-date). 
      yy = year(to-date). 
      from-date = DATE(1,1,yy). 
    END. 

    FOR EACH output-list: 
      delete output-list. 
    END. 
    FOR EACH to-list: 
      delete to-list. 
    END. 
    FOR EACH tmp-room:
        DELETE tmp-room.
    END.
    FOR EACH tmp-room1:
        DELETE tmp-room1.
    END.
    
    /*MTIF incl-comp THEN*/
    DO:
        FOR EACH genstat WHERE
           genstat.datum GE from-date AND genstat.datum LE to-date
           AND genstat.resstatus NE 13 AND genstat.segmentcode NE 0
           /*AND genstat.res-int[1] NE 13*/
           AND genstat.nationnr NE 0
           AND genstat.segmentcode NE 0
           AND genstat.nationnr NE 0
           AND genstat.zinr NE ""
           AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
           USE-INDEX nat_ix NO-LOCK:
           
           FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
           IF AVAILABLE guest THEN
           DO:
               datum = genstat.datum. 
               PROCESS EVENTS. 
               exchg-rate = 1.

               IF currency-type = 2 THEN 
               DO: 
                 IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
                   AND exrate.datum = datum NO-LOCK NO-ERROR. 
                 ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
                 IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
               END.

               FIND FIRST to-list WHERE to-list.gastnr EQ genstat.gastnr NO-ERROR.
               IF NOT AVAILABLE to-list THEN
               DO:
                   CREATE to-list.
                   ASSIGN to-list.gastnr = genstat.gastnr
                               to-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                            + guest.anrede1 + guest.anredefirma. 

                   FIND FIRST bediener WHERE bediener.userinit = guest.phonetik3 NO-LOCK NO-ERROR.
                   IF AVAILABLE bediener THEN
                       to-list.NAME = to-list.NAME + "=" + bediener.username.

                   IF genstat.datum EQ to-date THEN
                   DO: 
                       FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                           AND tmp-room.zinr EQ genstat.zinr 
                           AND tmp-room.flag = 1 NO-ERROR.
                       IF NOT AVAILABLE tmp-room THEN
                       DO:
                           to-list.room = to-list.room + 1.
                           room = room + 1.

                           CREATE tmp-room.
                           ASSIGN tmp-room.gastnr = genstat.gastnr
                                       tmp-room.zinr = genstat.zinr
                                       tmp-room.flag = 1.
                       END.
                       to-list.pax = to-list.pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       to-list.logis = to-list.logis + genstat.logis / exchg-rate.

                       pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       logis = logis + genstat.logis / exchg-rate.
                   END.

                   IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                   DO:
                       to-list.m-room = to-list.m-room + 1.
                       m-room = m-room + 1.


                       to-list.m-pax = to-list.m-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

                       m-pax = m-pax + genstat.erwachs + genstat.kind1 
                             + genstat.kind2 + genstat.gratis.
                       m-logis = m-logis + genstat.logis / exchg-rate.
                   END.

                   to-list.y-room = to-list.y-room + 1.
                   to-list.y-pax = to-list.y-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.gratis.
                   to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.

                   y-room = y-room + 1.
                   y-pax = y-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                   y-logis = y-logis + genstat.logis / exchg-rate.
               END.
               ELSE
               DO:
                   IF genstat.datum EQ to-date THEN
                   DO:
                       FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                           AND tmp-room.zinr EQ genstat.zinr 
                           AND tmp-room.flag = 1 NO-ERROR.
                       IF NOT AVAILABLE tmp-room THEN
                       DO:
                           to-list.room = to-list.room + 1.
                           room = room + 1.

                           CREATE tmp-room.
                           ASSIGN tmp-room.gastnr = genstat.gastnr
                                       tmp-room.zinr = genstat.zinr
                                       tmp-room.flag = 1.
                       END.
                       to-list.pax = to-list.pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                       pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       logis = logis + genstat.logis / exchg-rate.
                   END.
                   IF MONTH(genstat.datum) EQ mm THEN
                   DO:
                       to-list.m-room = to-list.m-room + 1.
                       m-room = m-room + 1.

                       to-list.m-pax = to-list.m-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
                       m-pax = m-pax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       m-logis = m-logis + genstat.logis / exchg-rate.
                   END.

                   to-list.y-room = to-list.y-room + 1.
                   to-list.y-pax = to-list.y-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.gratis.
                   to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.

                   y-room = y-room + 1.
                   y-pax = y-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                   y-logis = y-logis + genstat.logis / exchg-rate.
               END.
           END.
           ELSE
           DO:
               FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-ERROR.
               IF AVAILABLE guest THEN
               DO:
                   FIND FIRST to-list WHERE to-list.gastnr EQ genstat.gastnr NO-ERROR.
                   IF NOT AVAILABLE to-list THEN
                   DO:
                       CREATE to-list.
                       ASSIGN to-list.gastnr = genstat.gastnr
                                   to-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                                + guest.anrede1 + guest.anredefirma. 

                       FIND FIRST bediener WHERE bediener.userinit = guest.phonetik3 NO-LOCK NO-ERROR.
                       IF AVAILABLE bediener THEN
                            to-list.NAME = to-list.NAME + "=" + bediener.username.

                       IF genstat.datum EQ to-date THEN
                       DO:
                           FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                               AND tmp-room.zinr EQ genstat.zinr 
                               AND tmp-room.flag = 1 NO-ERROR.
                           IF NOT AVAILABLE tmp-room THEN
                           DO:
                               to-list.room = to-list.room + 1.
                               room = room + 1.

                               CREATE tmp-room.
                               ASSIGN tmp-room.gastnr = genstat.gastnr
                                           tmp-room.zinr = genstat.zinr
                                           tmp-room.flag = 1.
                           END.
                           to-list.pax = to-list.pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           to-list.logis = to-list.logis + genstat.logis / exchg-rate.

                           pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           logis = logis + genstat.logis / exchg-rate.
                       END.

                       IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                       DO:
                           to-list.m-room = to-list.m-room + 1.
                           m-room = m-room + 1.


                           to-list.m-pax = to-list.m-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

                           m-pax = m-pax + genstat.erwachs + genstat.kind1 
                                 + genstat.kind2 + genstat.gratis.
                           m-logis = m-logis + genstat.logis / exchg-rate.
                       END.

                       to-list.y-room = to-list.y-room + 1.
                       to-list.y-pax = to-list.y-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.

                       y-room = y-room + 1.
                       y-pax = y-pax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       y-logis = y-logis + genstat.logis / exchg-rate.
                   END.
                   ELSE
                   DO:
                       IF genstat.datum EQ to-date THEN
                       DO:
                           FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                               AND tmp-room.zinr EQ genstat.zinr 
                               AND tmp-room.flag = 1 NO-ERROR.
                           IF NOT AVAILABLE tmp-room THEN
                           DO:
                               to-list.room = to-list.room + 1.
                               room = room + 1.

                               CREATE tmp-room.
                               ASSIGN tmp-room.gastnr = genstat.gastnr
                                           tmp-room.zinr = genstat.zinr
                                           tmp-room.flag = 1.
                           END.
                           to-list.pax = to-list.pax + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                           pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           logis = logis + genstat.logis / exchg-rate.
                       END.
                       IF MONTH(genstat.datum) EQ mm THEN
                       DO:
                           to-list.m-room = to-list.m-room + 1.
                           m-room = m-room + 1.

                           to-list.m-pax = to-list.m-pax + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
                           m-pax = m-pax + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
                           m-logis = m-logis + genstat.logis / exchg-rate.
                       END.

                       to-list.y-room = to-list.y-room + 1.
                       to-list.y-pax = to-list.y-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.

                       y-room = y-room + 1.
                       y-pax = y-pax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                       y-logis = y-logis + genstat.logis / exchg-rate.
                   END.
               END.
           END.
        END.
    END.
    /*MTELSE*/
    DO:
      FOR EACH genstat WHERE 
          genstat.datum GE from-date AND genstat.datum LE to-date
          AND genstat.resstatus NE 13
          /*AND genstat.res-int[1] NE 13 */
          AND genstat.gratis EQ 0
          AND genstat.nationnr NE 0
          AND genstat.segmentcode NE 0
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
          USE-INDEX nat_ix NO-LOCK: 
           FIND FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
           IF AVAILABLE guest THEN
           DO:
               datum = genstat.datum. 
               PROCESS EVENTS. 
               exchg-rate = 1.

               IF currency-type = 2 THEN 
               DO: 
                 IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
                   AND exrate.datum = datum NO-LOCK NO-ERROR. 
                 ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
                 IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
               END.

               FIND FIRST to-list WHERE to-list.gastnr EQ genstat.gastnr NO-ERROR.
               IF NOT AVAILABLE to-list THEN
               DO:
                   CREATE to-list.
                   ASSIGN to-list.gastnr = genstat.gastnr
                               to-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                            + guest.anrede1 + guest.anredefirma. 

                   FIND FIRST bediener WHERE bediener.userinit = guest.phonetik3 NO-LOCK NO-ERROR.
                   IF AVAILABLE bediener THEN
                     to-list.NAME = to-list.NAME + "=" + bediener.username.

                   IF genstat.datum EQ to-date THEN
                   DO:
                       FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                           AND tmp-room1.zinr EQ genstat.zinr 
                           AND tmp-room1.flag = 1 NO-ERROR.
                       IF NOT AVAILABLE tmp-room1 THEN
                       DO:
                           to-list.comp-room = to-list.comp-room + 1.
                           comp-room = comp-room + 1.

                           CREATE tmp-room1.
                           ASSIGN tmp-room1.gastnr = genstat.gastnr
                                       tmp-room1.zinr = genstat.zinr
                                       tmp-room1.flag = 1.
                       END.
                       to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/

                       comp-pax = comp-pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTlogis = logis + genstat.logis / exchg-rate.*/
                   END.

                   IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                   DO:
                       to-list.comp-m-room = to-list.comp-m-room + 1.
                       comp-m-room = comp-m-room + 1.


                       to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/

                       comp-m-pax = comp-m-pax + genstat.erwachs + genstat.kind1 
                             + genstat.kind2 + genstat.kind3.
                       /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                   END.

                   to-list.comp-y-room = to-list.comp-y-room + 1.
                   to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.kind3.
                   /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.*/

                   comp-y-room = comp-y-room + 1.
                   comp-y-pax = comp-y-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.kind3.
                   /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
               END.
               ELSE
               DO:
                   IF genstat.datum EQ to-date THEN
                   DO:
                       FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                           AND tmp-room1.zinr EQ genstat.zinr 
                           AND tmp-room1.flag = 1 NO-ERROR.
                       IF NOT AVAILABLE tmp-room1 THEN
                       DO:
                           to-list.comp-room = to-list.comp-room + 1.
                           comp-room = comp-room + 1.

                           CREATE tmp-room1.
                           ASSIGN tmp-room1.gastnr = genstat.gastnr
                                       tmp-room1.zinr = genstat.zinr
                                       tmp-room1.flag = 1.
                       END.
                       to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/
                       comp-pax = comp-pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTlogis = logis + genstat.logis / exchg-rate.*/
                   END.
                   IF MONTH(genstat.datum) EQ mm THEN
                   DO:
                       to-list.comp-m-room = to-list.comp-m-room + 1.
                       comp-m-room = comp-m-room + 1.

                       to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/
                       comp-m-pax = comp-m-pax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                   END.

                   to-list.comp-y-room = to-list.comp-y-room + 1.
                   to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.kind3.
                   /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.*/

                   comp-y-room = comp-y-room + 1.
                   comp-y-pax = comp-y-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.kind3.
                   /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
               END.
           END.
           ELSE
           DO:
               FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-ERROR.
               IF AVAILABLE guest THEN
               DO:
                   FIND FIRST to-list WHERE to-list.gastnr EQ genstat.gastnr NO-ERROR.
                   IF NOT AVAILABLE to-list THEN
                   DO:
                       CREATE to-list.
                       ASSIGN to-list.gastnr = genstat.gastnr
                                   to-list.NAME = guest.name + ", " + guest.vorname1 + " " 
                                                + guest.anrede1 + guest.anredefirma. 

                       FIND FIRST bediener WHERE bediener.userinit = guest.phonetik3 NO-LOCK NO-ERROR.
                       IF AVAILABLE bediener THEN
                           to-list.NAME = to-list.NAME + "=" + bediener.username.

                       IF genstat.datum EQ to-date THEN
                       DO:
                           FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                               AND tmp-room1.zinr EQ genstat.zinr 
                               AND tmp-room1.flag = 1 NO-ERROR.
                           IF NOT AVAILABLE tmp-room1 THEN
                           DO:
                               to-list.comp-room = to-list.comp-room + 1.
                               comp-room = comp-room + 1.

                               CREATE tmp-room1.
                               ASSIGN tmp-room1.gastnr = genstat.gastnr
                                           tmp-room1.zinr = genstat.zinr
                                           tmp-room1.flag = 1.
                           END.
                           to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/

                           comp-pax = comp-pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTlogis = logis + genstat.logis / exchg-rate.*/
                       END.

                       IF MONTH(genstat.datum) EQ MONTH(to-date) THEN
                       DO:
                           to-list.comp-m-room = to-list.comp-m-room + 1.
                           comp-m-room = comp-m-room + 1.


                           to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/

                           comp-m-pax = comp-m-pax + genstat.erwachs + genstat.kind1 
                                 + genstat.kind2 + genstat.kind3.
                           /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                       END.

                       to-list.comp-y-room = to-list.comp-y-room + 1.
                       to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.*/

                       comp-y-room = comp-y-room + 1.
                       comp-y-pax = comp-y-pax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
                   END.
                   ELSE
                   DO:
                       IF genstat.datum EQ to-date THEN
                       DO:
                           FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                               AND tmp-room1.zinr EQ genstat.zinr 
                               AND tmp-room1.flag = 1 NO-ERROR.
                           IF NOT AVAILABLE tmp-room1 THEN
                           DO:
                               to-list.comp-room = to-list.comp-room + 1.
                               comp-room = comp-room + 1.

                               CREATE tmp-room1.
                               ASSIGN tmp-room1.gastnr = genstat.gastnr
                                           tmp-room1.zinr = genstat.zinr
                                           tmp-room1.flag = 1.
                           END.
                           to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/
                           comp-pax = comp-pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTlogis = logis + genstat.logis / exchg-rate.*/
                       END.
                       IF MONTH(genstat.datum) EQ mm THEN
                       DO:
                           to-list.comp-m-room = to-list.comp-m-room + 1.
                           comp-m-room = comp-m-room + 1.

                           to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/
                           comp-m-pax = comp-m-pax + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.kind3.
                           /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                       END.

                       to-list.comp-y-room = to-list.comp-y-room + 1.
                       to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.*/

                       comp-y-room = comp-y-room + 1.
                       comp-y-pax = comp-y-pax + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.kind3.
                       /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
                   END.
               END.
           END.
        END.
    END.

    FOR EACH to-list: 
    IF (to-list.room - to-list.c-room) NE 0 THEN
        to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
    IF to-list.comp-room NE 0 THEN
        to-list.exC-avrgrate = to-list.logis / to-list.comp-room. 

    IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
      to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room). 
    IF to-list.comp-m-room NE 0 THEN
        to-list.exC-m-avrgrate = to-list.m-logis / to-list.comp-m-room.

    IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
      to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room). 
    IF to-list.comp-y-room NE 0 THEN
        to-list.exC-y-avrgrate = to-list.y-logis / to-list.comp-y-room. 

    IF logis NE 0 THEN 
      to-list.proz = to-list.logis / logis * 100. 
    IF m-logis NE 0 THEN 
      to-list.m-proz = to-list.m-logis / m-logis * 100. 
    IF y-logis NE 0 THEN 
      to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END. 
    FOR EACH to-list NO-LOCK BY to-list.name: 
        /*M DISP STRING(to-list.name, "x(24)") STRING(to-list.comp-room, ">>9")
            STRING(to-list.comp-pax, ">>9"). */
        create output-list.
        ASSIGN
            output-list.NAME            = to-list.NAME         
            output-list.room            = to-list.room         
            output-list.pax             = to-list.pax          
            output-list.logis           = to-list.logis        
            output-list.proz            = to-list.proz         
            output-list.avrgrate        = to-list.avrgrate    
            output-list.m-room          = to-list.m-room       
            output-list.m-pax           = to-list.m-pax        
            output-list.m-logis         = to-list.m-logis      
            output-list.m-proz          = to-list.m-proz       
            output-list.m-avrgrate      = to-list.m-avrgrate   
            output-list.y-room          = to-list.y-room       
            output-list.y-pax           = to-list.y-pax        
            output-list.y-logis         = to-list.y-logis      
            output-list.y-proz          = to-list.y-proz       
            output-list.y-avrgrate      = to-list.y-avrgrate   
            output-list.comp-room       = to-list.comp-room    
            output-list.comp-pax        = to-list.comp-pax     
            output-list.comp-m-room     = to-list.comp-m-room  
            output-list.comp-m-pax      = to-list.comp-m-pax   
            output-list.comp-y-room     = to-list.comp-y-room  
            output-list.comp-y-pax      = to-list.comp-y-pax   
            output-list.exC-avrgrate    = to-list.exC-avrgrate 
            output-list.exC-m-avrgrate  = to-list.exC-m-avrgrate
            output-list.exC-y-avrgrate  = to-list.exC-y-avrgrate
            output-list.name2           = to-list.name     
            output-list.rmnite1         = to-list.y-room 
            output-list.rmrev1          = to-list.y-logis
            output-list.rmnite          = to-list.m-room 
            output-list.rmrev           = to-list.m-logis. 
    END.

  create output-list. 
  output-list.flag = 1. 
  DO ind = 1 TO 280: 
    output-list.name = output-list.name + "-". 
  END. 
  create output-list. 
  output-list.flag = 2. 
  
  /*avrgrate = 0. */
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
  IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room. 
  /*m-avrgrate = 0. */
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
  /*y-avrgrate = 0. */
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 
  IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room.
  
  ASSIGN
    output-list.NAME            = "T o t a l"
    output-list.room            = room         
    output-list.pax             = pax         
    output-list.logis           = logis       
    output-list.proz            = 100          
    output-list.avrgrate        = avrgrate     
    output-list.m-room          = m-room       
    output-list.m-pax           = m-pax        
    output-list.m-logis         = m-logis      
    output-list.m-proz          = 100          
    output-list.m-avrgrate      = m-avrgrate   
    output-list.y-room          = y-room       
    output-list.y-pax           = y-pax        
    output-list.y-logis         = y-logis      
    output-list.y-proz          = 100          
    output-list.y-avrgrate      = y-avrgrate   
    output-list.comp-room       = comp-room    
    output-list.comp-pax        = comp-pax     
    output-list.comp-m-room     = comp-m-room  
    output-list.comp-m-pax      = comp-m-pax  
    output-list.comp-y-room     = comp-y-room 
    output-list.comp-y-pax      = comp-y-pax 
    output-list.exC-avrgrate    = exC-avrgrate 
    output-list.exC-m-avrgrate  = exC-m-avrgrate
    output-list.exC-y-avrgrate  = exC-y-avrgrate. 
END PROCEDURE. 


PROCEDURE create-umsatz2: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE from-date AS DATE. 
DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE beg-date    AS DATE NO-UNDO.

  incl-comp = NOT excl-comp.
 
  room = 0. 
  c-room = 0. 
  pax = 0. 
  logis = 0. 
  m-room = 0. 
  mc-room = 0. 
  m-pax = 0. 
  m-logis = 0. 
  y-room = 0. 
  yc-room = 0. 
  y-pax = 0. 
  y-logis = 0. 
 
  /*IF MENU-ITEM mi-ftd:CHECKED IN MENU mbar = YES THEN */
  IF ytd-flag = 2 THEN
  DO:      
    /*to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date).
      beg-date = DATE(MONTH(f-date),1,yy).

      IF f-date GT beg-date THEN ASSIGN beg-date = f-date.
      IF MONTH(to-date) GT MONTH(f-date) THEN ASSIGN beg-date = DATE(mm,1,yy).
      from-date = beg-date.*/

      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
  END. 
  ELSE 
  DO: 
    mm = month(to-date). 
    yy = year(to-date). 
    from-date = DATE(1,1,yy). 
  END. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH to-list: 
    delete to-list. 
  END. 
  FOR EACH to-list1: 
    delete to-list1. 
  END. 
 

  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich: 
    PROCESS EVENTS.
    CREATE to-list. 
    to-list.gastnr = nation.nationnr. 

    IF nation.bezeich MATCHES "*;*" THEN ASSIGN to-list.name = ENTRY(1,nation.bezeich,";").
    ELSE ASSIGN to-list.name = nation.bezeich. 

    FIND FIRST to-list1 WHERE to-list1.gastnr = nation.untergruppe 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE to-list1 THEN 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 6 
        AND queasy.number1 = nation.untergruppe 
        AND queasy.number2 = 0 AND queasy.deci2 = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE queasy THEN 
      DO: 
        CREATE to-list1. 
        to-list1.gastnr = queasy.number1.
        to-list1.name = queasy.char1. 
      END. 
    END.

   /*MTIF incl-comp THEN*/
   DO:
       FOR EACH genstat WHERE
           genstat.datum GE from-date AND genstat.datum LE to-date
           AND genstat.resstatus NE 13 AND genstat.segmentcode NE 0
           /*AND genstat.res-int[1] NE 13*/
           AND genstat.nationnr NE 0
           AND genstat.segmentcode NE 0
           AND genstat.nationnr EQ nation.nationnr
           AND genstat.zinr NE ""
           AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
           USE-INDEX nat_ix NO-LOCK: 
           
           /*M Sept 6th 11 = fix wrong exrate calculation  */
           datum = genstat.datum. 
           PROCESS EVENTS. 
           exchg-rate = 1. 
           IF currency-type = 2 THEN 
           DO: 
             IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
               AND exrate.datum = datum NO-LOCK NO-ERROR. 
             ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
             IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
           END. 
           
           IF genstat.datum EQ to-date THEN
           DO:
               FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
               IF NOT AVAILABLE tmp-room THEN
               DO:
                    to-list.room = to-list.room + 1.
                    room = room + 1.

                    IF AVAILABLE to-list1 THEN
                        to-list1.room  = to-list1.room  + 1.

                    CREATE tmp-room.
                    ASSIGN tmp-room.gastnr = genstat.gastnr
                           tmp-room.zinr = genstat.zinr
                           tmp-room.flag = 1.
               END.

               to-list.pax   = to-list.pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 
                                             + genstat.gratis.
               to-list.logis = to-list.logis + genstat.logis / exchg-rate. 
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.pax   = to-list1.pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2 
                                                   + genstat.gratis.
                   to-list1.logis = to-list1.logis + genstat.logis / exchg-rate. 
               END.
               
               pax   = pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2 
                             + genstat.gratis.
               logis = logis + genstat.logis / exchg-rate. 
           END.

           IF MONTH(genstat.datum) = MONTH(to-date) /*AND year(genstat.datum) = yy*/ THEN 
           DO: 
               to-list.m-room  = to-list.m-room  + 1.
               to-list.m-pax   = to-list.m-pax   + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2
                               + genstat.gratis.
               to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.m-room  = to-list1.m-room  + 1.
                   to-list1.m-pax   = to-list1.m-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2
                                    + genstat.gratis.
                   to-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.
               END.

               m-room  = m-room  + 1.
               m-pax   = m-pax   + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2
                                 + genstat.gratis.
               m-logis = m-logis + genstat.logis / exchg-rate.
           END.

           IF AVAILABLE to-list1 THEN
           DO:
               to-list1.y-room  = to-list1.y-room  + 1.
               to-list1.y-pax   = to-list1.y-pax   + to-list.pax + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2
                               + genstat.gratis.
               to-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. 
           END.
           to-list.y-room  = to-list.y-room  + 1.
           to-list.y-pax   = to-list.y-pax   + genstat.erwachs 
                           + genstat.kind1 + genstat.kind2
                           + genstat.gratis.
           to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. 

           y-room  = y-room  + 1.
           y-pax   = y-pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2
                             + genstat.gratis.
           y-logis = y-logis + genstat.logis / exchg-rate.
       END.
   END.
   /*MTELSE*/
   DO: 
       FOR EACH genstat WHERE 
           genstat.datum GE from-date AND genstat.datum LE to-date
           AND genstat.resstatus NE 13
           /*AND genstat.res-int[1] NE 13 */
           AND genstat.gratis EQ 0
           AND genstat.nationnr NE 0
           AND genstat.segmentcode NE 0
           AND genstat.nationnr EQ nation.nationnr
           AND genstat.zinr NE ""
           AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
           USE-INDEX nat_ix NO-LOCK: 
           
           /*M Sept 6th 11 = fix wrong exrate calculation  */
           datum = genstat.datum. 
           PROCESS EVENTS. 
           exchg-rate = 1. 
           IF currency-type = 2 THEN 
           DO: 
             IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
               AND exrate.datum = datum NO-LOCK NO-ERROR. 
             ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
             IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
           END. 
           
           IF genstat.datum EQ to-date THEN
           DO:
               FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                   AND tmp-room1.zinr EQ genstat.zinr 
                   AND tmp-room1.flag = 1 NO-ERROR.
               IF NOT AVAILABLE tmp-room1 THEN
               DO:
                        to-list.comp-room = to-list.comp-room + 1.
                        comp-room = comp-room + 1.

                        IF AVAILABLE to-list1 THEN
                            to-list1.comp-room  = to-list1.comp-room  + 1.

                        CREATE tmp-room1.
                        ASSIGN tmp-room1.gastnr = genstat.gastnr
                                    tmp-room1.zinr = genstat.zinr
                                    tmp-room1.flag = 1.
               END.
               
               to-list.comp-pax   = to-list.comp-pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 
                                             + genstat.kind3.
               /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate. */
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.comp-pax   = to-list1.comp-pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2 
                                                   + genstat.kind3.
                   /*MTto-list1.logis = to-list1.logis + genstat.logis / exchg-rate. */
               END.
               
               comp-pax   = comp-pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2 
                             + genstat.kind3.
               /*MTlogis = logis + genstat.logis / exchg-rate. */
           END.

           IF month(genstat.datum) = MONTH(to-date) /*AND year(genstat.datum) = yy*/ THEN 
           DO: 
               to-list.comp-m-room  = to-list.comp-m-room  + 1.
               to-list.comp-m-pax   = to-list.comp-m-pax   + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2.
               /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.comp-m-room  = to-list1.comp-m-room  + 1.
                   to-list1.comp-m-pax   = to-list1.comp-m-pax   + genstat.erwachs 
                                   + genstat.kind1 + genstat.kind2.
                   /*MTto-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.*/
               END.
               comp-m-room  = comp-m-room  + 1.
               comp-m-pax   = comp-m-pax   + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2.
               /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
           END.
           IF AVAILABLE to-list1 THEN
           DO:
               to-list1.comp-y-room  = to-list1.comp-y-room  + 1.
               to-list1.comp-y-pax   = to-list1.comp-y-pax  + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2.
               /*MTto-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. */
           END.
           to-list.comp-y-room  = to-list.comp-y-room  + 1.
           to-list.comp-y-pax   = to-list.comp-y-pax   + genstat.erwachs 
                           + genstat.kind1 + genstat.kind2.
           /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. */

           comp-y-room  = comp-y-room  + 1.
           comp-y-pax   = comp-y-pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2.
           /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
       END.
   END.
  END.

   /*MT
   IF incl-comp THEN
   DO:
       FOR EACH genstat WHERE
           genstat.datum GE from-date AND genstat.datum LE to-date
           AND genstat.resstatus NE 13 AND genstat.segmentcode NE 0
           /*AND genstat.res-int[1] NE 13*/
           AND genstat.nationnr NE 0
           AND genstat.segmentcode NE 0
           AND genstat.nationnr EQ nation.nationnr
           AND genstat.zinr NE ""
           USE-INDEX nat_ix NO-LOCK: 
           
           /*M Sept 6th 11 = fix wrong exrate calculation  */
           datum = genstat.datum. 
           PROCESS EVENTS. 
           exchg-rate = 1. 
           IF currency-type = 2 THEN 
           DO: 
             IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
               AND exrate.datum = datum NO-LOCK NO-ERROR. 
             ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
             IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
           END. 
           
           IF genstat.datum EQ to-date THEN
           DO:
               FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
               IF NOT AVAILABLE tmp-room THEN
               DO:
                    to-list.room = to-list.room + 1.
                    room = room + 1.

                    IF AVAILABLE to-list1 THEN
                        to-list1.room  = to-list1.room  + 1.

                    CREATE tmp-room.
                    ASSIGN tmp-room.gastnr = genstat.gastnr
                           tmp-room.zinr = genstat.zinr
                           tmp-room.flag = 1.
               END.

               to-list.pax   = to-list.pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 
                                             + genstat.gratis.
               to-list.logis = to-list.logis + genstat.logis / exchg-rate. 
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.pax   = to-list1.pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2 
                                                   + genstat.gratis.
                   to-list1.logis = to-list1.logis + genstat.logis / exchg-rate. 
               END.
               
               pax   = pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2 
                             + genstat.gratis.
               logis = logis + genstat.logis / exchg-rate. 
           END.

           IF MONTH(genstat.datum) = MONTH(to-date) /*AND year(genstat.datum) = yy*/ THEN 
           DO: 
               to-list.m-room  = to-list.m-room  + 1.
               to-list.m-pax   = to-list.m-pax   + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2
                               + genstat.gratis.
               to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.m-room  = to-list1.m-room  + 1.
                   to-list1.m-pax   = to-list1.m-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2
                                    + genstat.gratis.
                   to-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.
               END.

               m-room  = m-room  + 1.
               m-pax   = m-pax   + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2
                                 + genstat.gratis.
               m-logis = m-logis + genstat.logis / exchg-rate.
           END.

           IF AVAILABLE to-list1 THEN
           DO:
               to-list1.y-room  = to-list1.y-room  + 1.
               to-list1.y-pax   = to-list1.y-pax   + to-list.pax + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2
                               + genstat.gratis.
               to-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. 
           END.
           to-list.y-room  = to-list.y-room  + 1.
           to-list.y-pax   = to-list.y-pax   + genstat.erwachs 
                           + genstat.kind1 + genstat.kind2
                           + genstat.gratis.
           to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. 

           y-room  = y-room  + 1.
           y-pax   = y-pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2
                             + genstat.gratis.
           y-logis = y-logis + genstat.logis / exchg-rate.
       END.
   END.
   ELSE
   DO: 
       FOR EACH genstat WHERE 
           genstat.datum GE from-date AND genstat.datum LE to-date
           AND genstat.resstatus NE 13
           /*AND genstat.res-int[1] NE 13 */
           AND genstat.gratis EQ 0
           AND genstat.nationnr NE 0
           AND genstat.segmentcode NE 0
           AND genstat.nationnr EQ nation.nationnr
           AND genstat.zinr NE ""
           USE-INDEX nat_ix NO-LOCK: 
           
           /*M Sept 6th 11 = fix wrong exrate calculation  */
           datum = genstat.datum. 
           PROCESS EVENTS. 
           exchg-rate = 1. 
           IF currency-type = 2 THEN 
           DO: 
             IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
               AND exrate.datum = datum NO-LOCK NO-ERROR. 
             ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
             IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
           END. 
           
           IF genstat.datum EQ to-date THEN
           DO:
               FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
               IF NOT AVAILABLE tmp-room THEN
               DO:
                        to-list.room = to-list.room + 1.
                        room = room + 1.

                        IF AVAILABLE to-list1 THEN
                            to-list1.room  = to-list1.room  + 1.

                        CREATE tmp-room.
                        ASSIGN tmp-room.gastnr = genstat.gastnr
                                    tmp-room.zinr = genstat.zinr
                                    tmp-room.flag = 1.
               END.
               
               to-list.pax   = to-list.pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 
                                             + genstat.kind3.
               to-list.logis = to-list.logis + genstat.logis / exchg-rate. 
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.pax   = to-list1.pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2 
                                                   + genstat.kind3.
                   to-list1.logis = to-list1.logis + genstat.logis / exchg-rate. 
               END.
               
               pax   = pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2 
                             + genstat.kind3.
               logis = logis + genstat.logis / exchg-rate. 
           END.

           IF month(genstat.datum) = MONTH(to-date) /*AND year(genstat.datum) = yy*/ THEN 
           DO: 
               to-list.m-room  = to-list.m-room  + 1.
               to-list.m-pax   = to-list.m-pax   + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2.
               to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.m-room  = to-list1.m-room  + 1.
                   to-list1.m-pax   = to-list1.m-pax   + genstat.erwachs 
                                   + genstat.kind1 + genstat.kind2.
                   to-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.
               END.
               m-room  = m-room  + 1.
               m-pax   = m-pax   + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2.
               m-logis = m-logis + genstat.logis / exchg-rate.
           END.
           IF AVAILABLE to-list1 THEN
           DO:
               to-list1.y-room  = to-list1.y-room  + 1.
               to-list1.y-pax   = to-list1.y-pax  + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2.
               to-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. 
           END.
           to-list.y-room  = to-list.y-room  + 1.
           to-list.y-pax   = to-list.y-pax   + genstat.erwachs 
                           + genstat.kind1 + genstat.kind2.
           to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. 

           y-room  = y-room  + 1.
           y-pax   = y-pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2.
           y-logis = y-logis + genstat.logis / exchg-rate.
       END.
    END. 
  END.
  */

  FOR EACH to-list: 
    IF (to-list.room - to-list.c-room) NE 0 THEN 
      to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
    IF to-list.comp-room NE 0 THEN
      to-list.exC-avrgrate = to-list.logis / to-list.comp-room.
    IF logis NE 0 THEN to-list.proz = to-list.logis / logis * 100. 

    IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
      to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room). 
    IF to-list.comp-m-room NE 0 THEN
      to-list.exC-m-avrgrate = to-list.m-logis / to-list.comp-m-room. 
    IF m-logis NE 0 THEN to-list.m-proz = to-list.m-logis / m-logis * 100. 

    IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
      to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room).
    IF to-list.comp-y-room NE 0 THEN
      to-list.exC-y-avrgrate = to-list.y-logis / to-list.comp-y-room.
    IF y-logis NE 0 THEN to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END. 
 
  FOR EACH to-list1: 
    IF (to-list1.room - to-list1.c-room) NE 0 THEN 
      to-list1.avrgrate = to-list1.logis / (to-list1.room - to-list1.c-room). 
    IF to-list1.comp-room NE 0 THEN
        to-list1.exC-avrgrate = to-list1.logis / to-list1.comp-room. 
    IF logis NE 0 THEN 
      to-list1.proz = to-list1.logis / logis * 100.

    IF (to-list1.m-room - to-list1.mc-room) NE 0 THEN 
      to-list1.m-avrgrate = to-list1.m-logis / (to-list1.m-room - to-list1.mc-room). 
    IF to-list1.comp-m-room NE 0 THEN
      to-list1.exC-m-avrgrate = to-list1.m-logis / to-list1.comp-m-room. 
    IF m-logis NE 0 THEN 
      to-list1.m-proz = to-list1.m-logis / m-logis * 100.         

    IF (to-list1.y-room - to-list1.yc-room) NE 0 THEN 
      to-list1.y-avrgrate = to-list1.y-logis / (to-list1.y-room - to-list1.yc-room). 
    IF to-list1.comp-y-room NE 0 THEN
      to-list1.exC-y-avrgrate = to-list1.y-logis / to-list1.comp-y-room. 
    IF y-logis NE 0 THEN 
      to-list1.y-proz = to-list1.y-logis / y-logis * 100. 
  END. 
 
  FOR EACH to-list NO-LOCK WHERE to-list.y-room NE 0 BY to-list.name: 
    create output-list. 
    output-list.flag = 0. 
    output-list.rmnite = to-list.y-room. 
    output-list.rmrev = to-list.y-logis. 
    output-list.rmnite1 = to-list.m-room. 
    output-list.rmrev1 = to-list.m-logis. 

    ASSIGN                          
      output-list.NAME            = to-list.name         
      output-list.room            = to-list.room         
      output-list.pax             = to-list.pax          
      output-list.logis           = to-list.logis         
      output-list.proz            = to-list.proz         
      output-list.avrgrate        = to-list.avrgrate      
      output-list.m-room          = to-list.m-room       
      output-list.m-pax           = to-list.m-pax        
      output-list.m-logis         = to-list.m-logis        
      output-list.m-proz          = to-list.m-proz       
      output-list.m-avrgrate      = to-list.m-avrgrate    
      output-list.y-room          = to-list.y-room       
      output-list.y-pax           = to-list.y-pax        
      output-list.y-logis         = to-list.y-logis       
      output-list.y-proz          = to-list.y-proz       
      output-list.y-avrgrate      = to-list.y-avrgrate   
      output-list.comp-room       = to-list.comp-room    
      output-list.comp-pax        = to-list.comp-pax     
      output-list.comp-m-room     = to-list.comp-m-room  
      output-list.comp-m-pax      = to-list.comp-m-pax   
      output-list.comp-y-room     = to-list.comp-y-room  
      output-list.comp-y-pax      = to-list.comp-y-pax   
      output-list.exC-avrgrate    = to-list.exC-avrgrate 
      output-list.exC-m-avrgrate  = to-list.exC-m-avrgrate
      output-list.exC-y-avrgrate  = to-list.exC-y-avrgrate.
  END. 

  create output-list. 
  output-list.flag = 1. 
  DO ind = 1 TO 280: 
    output-list.name = output-list.name + "-". 
  END. 
  create output-list. 
  output-list.flag = 2. 
  avrgrate = 0. 
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
  exC-avrgrate = 0. 
  IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room.
  m-avrgrate = 0. 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room).
  exC-m-avrgrate = 0. 
  IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
  y-avrgrate = 0. 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room).
  exC-y-avrgrate = 0. 
  IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room.
 
  ASSIGN                          
    output-list.NAME            = "T o t a l" 
    output-list.room            = room        
    output-list.pax             = pax         
    output-list.logis           = logis       
    output-list.proz            = 100         
    output-list.avrgrate        = avrgrate    
    output-list.m-room          = m-room      
    output-list.m-pax           = m-pax       
    output-list.m-logis         = m-logis     
    output-list.m-proz          = 100
    output-list.m-avrgrate      = m-avrgrate  
    output-list.y-room          = y-room      
    output-list.y-pax           = y-pax       
    output-list.y-logis         = y-logis     
    output-list.y-proz          = 100         
    output-list.y-avrgrate      = y-avrgrate  
    output-list.comp-room       = comp-room   
    output-list.comp-pax        = comp-pax    
    output-list.comp-m-room     = comp-m-room 
    output-list.comp-m-pax      = comp-m-pax  
    output-list.comp-y-room     = comp-y-room 
    output-list.comp-y-pax      = comp-y-pax  
    output-list.exC-avrgrate    = exC-avrgrate
    output-list.exC-m-avrgrate  = exC-m-avrgrate    
    output-list.exC-y-avrgrate  = exC-y-avrgrate.      
 
  FIND FIRST to-list1 NO-LOCK NO-ERROR. 
  IF AVAILABLE to-list1 THEN 
  DO: 
    create output-list. 
    output-list.flag = 3. 
    create output-list. 
    output-list.flag = 4. 
    output-list.name = translateExtended ("*** STATISTIC BY REGION ***",lvCAREA,""). 
    FOR EACH to-list1 NO-LOCK BY to-list1.name: 
      create output-list. 
      output-list.flag = 5. 
      output-list.rmnite = to-list1.y-room. 
      output-list.rmrev = to-list1.y-logis. 
      output-list.rmnite1 = to-list1.m-room. 
      output-list.rmrev1 = to-list1.m-logis. 
      ASSIGN                          
        output-list.NAME            = to-list1.name
        output-list.room            = to-list1.room        
        output-list.pax             = to-list1.pax         
        output-list.logis           = to-list1.logis       
        output-list.proz            = to-list1.proz        
        output-list.avrgrate        = to-list1.avrgrate    
        output-list.m-room          = to-list1.m-room      
        output-list.m-pax           = to-list1.m-pax       
        output-list.m-logis         = to-list1.m-logis     
        output-list.m-proz          = to-list1.m-proz      
        output-list.m-avrgrate      = to-list1.m-avrgrate  
        output-list.y-room          = to-list1.y-room      
        output-list.y-pax           = to-list1.y-pax       
        output-list.y-logis         = to-list1.y-logis     
        output-list.y-proz          = to-list1.y-proz      
        output-list.y-avrgrate      = to-list1.y-avrgrate  
        output-list.comp-room       = to-list1.comp-room   
        output-list.comp-pax        = to-list1.comp-pax    
        output-list.comp-m-room     = to-list1.comp-m-room 
        output-list.comp-m-pax      = to-list1.comp-m-pax  
        output-list.comp-y-room     = to-list1.comp-y-room 
        output-list.comp-y-pax      = to-list1.comp-y-pax  
        output-list.exC-avrgrate    = to-list1.exC-avrgrate 
        output-list.exC-m-avrgrate  = to-list1.exC-m-avrgrate
        output-list.exC-y-avrgrate  = to-list1.exC-y-avrgrate.
    END. 

    create output-list. 
    output-list.flag = 6. 
    DO ind = 1 TO 280:  /*bef 180*/
      output-list.name = output-list.name + "-". 
    END. 
    create output-list. 
    output-list.flag = 7. 
    avrgrate = 0. 
    IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
    exC-avrgrate = 0. 
    IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room. 
    m-avrgrate = 0. 
    IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room).
    exC-m-avrgrate = 0. 
    IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
    y-avrgrate = 0. 
    IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room).
    exC-y-avrgrate = 0. 
    IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room. 
    ASSIGN                          
      output-list.NAME            = "T o t a l" 
      output-list.room            = room          
      output-list.pax             = pax           
      output-list.logis           = logis         
      output-list.proz            = 100           
      output-list.avrgrate        = avrgrate      
      output-list.m-room          = m-room        
      output-list.m-pax           = m-pax         
      output-list.m-logis         = m-logis       
      output-list.m-proz          = 100           
      output-list.m-avrgrate      = m-avrgrate    
      output-list.y-room          = y-room        
      output-list.y-pax           = y-pax         
      output-list.y-logis         = y-logis        
      output-list.y-proz          = 100           
      output-list.y-avrgrate      = y-avrgrate    
      output-list.comp-room       = comp-room     
      output-list.comp-pax        = comp-pax      
      output-list.comp-m-room     = comp-m-room   
      output-list.comp-m-pax      = comp-m-pax    
      output-list.comp-y-room     = comp-y-room   
      output-list.comp-y-pax      = comp-y-pax    
      output-list.exC-avrgrate    = exC-avrgrate  
      output-list.exC-m-avrgrate  = exC-m-avrgrate
      output-list.exC-y-avrgrate  = exC-y-avrgrate.  
  END. 
END PROCEDURE. 

PROCEDURE create-umsatz3: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE from-date AS DATE. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE curr-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE beg-date    AS DATE NO-UNDO.

/*DEFINE VARIABLE incl-comp AS LOGICAL INITIAL YES. */
  incl-comp = NOT excl-comp.
 
  room = 0. 
  c-room = 0. 
  pax = 0. 
  logis = 0. 
  m-room = 0. 
  mc-room = 0. 
  m-pax = 0. 
  m-logis = 0. 
  y-room = 0. 
  yc-room = 0. 
  y-pax = 0. 
  y-logis = 0.
 
  /*IF MENU-ITEM mi-ftd:CHECKED IN MENU mbar = YES THEN */
  IF ytd-flag = 2 THEN
  DO:      
    /*to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date).
      beg-date = DATE(MONTH(f-date),1,yy).

      IF f-date GT beg-date THEN ASSIGN beg-date = f-date.
      IF MONTH(to-date) GT MONTH(f-date) THEN ASSIGN beg-date = DATE(mm,1,yy).
      from-date = beg-date.*/

      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
  END. 
  ELSE 
  DO: 
    mm = month(to-date). 
    yy = year(to-date). 
    from-date = DATE(1,1,yy). 
  END. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH to-list: 
    delete to-list. 
  END.
  FOR EACH to-list1: 
    delete to-list1. 
  END. 

  FOR EACH sourccod NO-LOCK:
      PROCESS EVENTS.
        create to-list. 
        to-list.gastnr = sourccod.source-code. 
        to-list.name = sourccod.bezeich.
        
        FOR EACH genstat WHERE 
            genstat.datum GE from-date AND genstat.datum LE to-date
            AND genstat.resstatus NE 13 
            AND genstat.nationnr NE 0
            AND genstat.segmentcode NE 0
            /*AND genstat.res-int[1] NE 13*/
            AND genstat.source EQ sourccod.source-code 
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
            USE-INDEX segm_ix NO-LOCK:
            
            datum = genstat.datum.
            exchg-rate = 1. 
            IF currency-type = 2 THEN 
            DO: 
                IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
                AND exrate.datum = datum NO-LOCK NO-ERROR. 
                ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
                IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
            END. 

            
            IF genstat.datum EQ to-date THEN 
            DO: 
              /*MTIF incl-comp THEN */
              DO: 
                  FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
                  IF NOT AVAILABLE tmp-room THEN
                  DO:
                      to-list.room  = to-list.room  + 1.
                      room  = room  + 1.

                      IF AVAILABLE to-list1 THEN
                            to-list1.room  = to-list1.room  + 1.

                      CREATE tmp-room.
                      ASSIGN tmp-room.gastnr = genstat.gastnr
                             tmp-room.zinr = genstat.zinr
                             tmp-room.flag = 1.
                  END.
                  to-list.pax   = to-list.pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                  pax   = pax   + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  logis = logis + genstat.logis / exchg-rate.
              END. 
              /*MTELSE*/
              DO: 
                  IF genstat.gratis EQ 0 THEN
                  DO:
                      FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                       AND tmp-room1.zinr EQ genstat.zinr 
                       AND tmp-room1.flag = 1 NO-ERROR.
                      IF NOT AVAILABLE tmp-room1 THEN
                      DO:
                          to-list.comp-room  = to-list.comp-room  + 1.
                          comp-room  = comp-room  + 1.

                          IF AVAILABLE to-list1 THEN
                                to-list1.comp-room  = to-list1.comp-room  + 1.

                          CREATE tmp-room1.
                          ASSIGN tmp-room1.gastnr = genstat.gastnr
                                 tmp-room1.zinr = genstat.zinr
                                 tmp-room1.flag = 1.
                      END.
                      to-list.comp-pax   = to-list.comp-pax   + genstat.erwachs 
                                                + genstat.kind1 + genstat.kind2.
                      /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/
                      comp-pax   = comp-pax  + genstat.erwachs 
                                                + genstat.kind1 + genstat.kind2.
                      /*MTlogis = logis + genstat.logis / exchg-rate.*/
                  END.
              END. 
            END. 


            IF MONTH(genstat.datum) = mm /*AND year(genstat.datum) = yy*/ THEN 
            DO: 
              /*MTIF incl-comp THEN */
              DO: 
                to-list.m-room  = to-list.m-room  + 1.
                to-list.m-pax   = to-list.m-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
                m-room  = m-room  + 1.
                m-pax   = m-pax   + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
                m-logis = m-logis + genstat.logis / exchg-rate.
              END. 
              /*MTELSE*/
              DO: 
                  IF genstat.gratis EQ 0 THEN
                  DO:
                      to-list.comp-m-room  = to-list.comp-m-room  + 1.
                      to-list.comp-m-pax   = to-list.comp-m-pax + genstat.erwachs 
                                              + genstat.kind1 + genstat.kind2 + genstat.gratis.
                      /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/

                      comp-m-room  = comp-m-room  + 1. 
                      comp-m-pax   = comp-m-pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2.
                      /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
                  END.
              END.
            END. 

            /*MTIF incl-comp THEN */
            DO: 
              to-list.y-room  = to-list.y-room  + 1.
              to-list.y-pax   = to-list.y-pax + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
              to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
              y-room  = y-room  + 1.
              y-pax   = y-pax   + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
              y-logis = y-logis + genstat.logis / exchg-rate.
            END. 
            /*MTELSE */
            DO: 
                IF genstat.gratis EQ 0 THEN
                DO:
                    to-list.comp-y-room  = to-list.comp-y-room  + 1.
                    to-list.comp-y-pax   = to-list.comp-y-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.*/
                    comp-y-room  = comp-y-room  + 1.
                    comp-y-pax   = comp-y-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
                END.
            END. 
        END.
  END.

  /*MT  
  FOR EACH sourccod:
      PROCESS EVENTS.
        create to-list. 
        to-list.gastnr = sourccod.source-code. 
        to-list.name = sourccod.bezeich.
        
        FOR EACH genstat WHERE 
            genstat.datum GE from-date AND genstat.datum LE to-date
            AND genstat.resstatus NE 13 
            AND genstat.nationnr NE 0
            AND genstat.segmentcode NE 0
            /*AND genstat.res-int[1] NE 13*/
            AND genstat.source EQ sourccod.source-code 
            AND genstat.zinr NE ""
            USE-INDEX segm_ix NO-LOCK:
            
            datum = genstat.datum.
            exchg-rate = 1. 
            IF currency-type = 2 THEN 
            DO: 
                IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
                AND exrate.datum = datum NO-LOCK NO-ERROR. 
                ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
                IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
            END. 

            
            IF genstat.datum EQ to-date THEN 
            DO: 
              IF incl-comp THEN 
              DO: 
                  FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
                  IF NOT AVAILABLE tmp-room THEN
                  DO:
                      to-list.room  = to-list.room  + 1.
                      room  = room  + 1.

                      IF AVAILABLE to-list1 THEN
                            to-list1.room  = to-list1.room  + 1.

                      CREATE tmp-room.
                      ASSIGN tmp-room.gastnr = genstat.gastnr
                             tmp-room.zinr = genstat.zinr
                             tmp-room.flag = 1.
                  END.
                  to-list.pax   = to-list.pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                  pax   = pax   + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                  logis = logis + genstat.logis / exchg-rate.
              END. 
              ELSE DO: 
                  IF genstat.gratis EQ 0 THEN
                  DO:
                      FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                       AND tmp-room.zinr EQ genstat.zinr 
                       AND tmp-room.flag = 1 NO-ERROR.
                      IF NOT AVAILABLE tmp-room THEN
                      DO:
                          to-list.room  = to-list.room  + 1.
                          room  = room  + 1.

                          IF AVAILABLE to-list1 THEN
                                to-list1.room  = to-list1.room  + 1.

                          CREATE tmp-room.
                          ASSIGN tmp-room.gastnr = genstat.gastnr
                                 tmp-room.zinr = genstat.zinr
                                 tmp-room.flag = 1.
                      END.
                      to-list.pax   = to-list.pax   + genstat.erwachs 
                                                + genstat.kind1 + genstat.kind2.
                      to-list.logis = to-list.logis + genstat.logis / exchg-rate.
                      pax   = pax  + genstat.erwachs 
                                                + genstat.kind1 + genstat.kind2.
                      logis = logis + genstat.logis / exchg-rate.
                  END.
              END. 
            END. 


            IF MONTH(genstat.datum) = mm /*AND year(genstat.datum) = yy*/ THEN 
            DO: 
              IF incl-comp THEN 
              DO: 
                to-list.m-room  = to-list.m-room  + 1.
                to-list.m-pax   = to-list.m-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2 + genstat.gratis.
                to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.
                m-room  = m-room  + 1.
                m-pax   = m-pax   + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
                m-logis = m-logis + genstat.logis / exchg-rate.
              END. 
              ELSE DO: 
                  IF genstat.gratis EQ 0 THEN
                  DO:
                      to-list.m-room  = to-list.m-room  + 1.
                      to-list.m-pax   = to-list.m-pax + genstat.erwachs 
                                              + genstat.kind1 + genstat.kind2 + genstat.gratis.
                      to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

                      m-room  = m-room  + 1. 
                      m-pax   = m-pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2.
                      m-logis = m-logis + genstat.logis / exchg-rate.
                  END.
              END.
            END. 

            IF incl-comp THEN 
            DO: 
              to-list.y-room  = to-list.y-room  + 1.
              to-list.y-pax   = to-list.y-pax + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
              to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
              y-room  = y-room  + 1.
              y-pax   = y-pax   + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
              y-logis = y-logis + genstat.logis / exchg-rate.
            END. 
            ELSE DO: 
                IF genstat.gratis EQ 0 THEN
                DO:
                    to-list.y-room  = to-list.y-room  + 1.
                    to-list.y-pax   = to-list.y-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.
                    y-room  = y-room  + 1.
                    y-pax   = y-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    y-logis = y-logis + genstat.logis / exchg-rate.
                END.
            END. 
        END.
  END.
  */

  FOR EACH to-list: 
    IF (to-list.room - to-list.c-room) NE 0 THEN 
      to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
    IF to-list.comp-room NE 0 THEN
      to-list.exC-avrgrate = to-list.logis / to-list.comp-room.

    IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
      to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room). 
    IF to-list.comp-m-room NE 0 THEN 
      to-list.exC-m-avrgrate = to-list.m-logis / to-list.comp-m-room. 

    IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
      to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room). 
    IF to-list.comp-y-room NE 0 THEN 
      to-list.exC-y-avrgrate = to-list.y-logis / to-list.comp-y-room. 

    IF logis NE 0 THEN 
      to-list.proz = to-list.logis / logis * 100. 
    IF m-logis NE 0 THEN 
      to-list.m-proz = to-list.m-logis / m-logis * 100. 
    IF y-logis NE 0 THEN 
      to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END. 
  
  FOR EACH to-list NO-LOCK BY to-list.name: 
    create output-list. 
    output-list.flag = 1. 
    output-list.name = STRING(to-list.name, "x(40)"). 
    output-list.rmnite = to-list.y-room. 
    output-list.rmrev = to-list.y-logis. 
    output-list.rmnite1 = to-list.m-room. 
    output-list.rmrev1 = to-list.m-logis. 
    ASSIGN                          
      output-list.NAME            = to-list.name         
      output-list.room            = to-list.room         
      output-list.pax             = to-list.pax          
      output-list.logis           = to-list.logis         
      output-list.proz            = to-list.proz         
      output-list.avrgrate        = to-list.avrgrate      
      output-list.m-room          = to-list.m-room       
      output-list.m-pax           = to-list.m-pax        
      output-list.m-logis         = to-list.m-logis        
      output-list.m-proz          = to-list.m-proz       
      output-list.m-avrgrate      = to-list.m-avrgrate    
      output-list.y-room          = to-list.y-room       
      output-list.y-pax           = to-list.y-pax        
      output-list.y-logis         = to-list.y-logis       
      output-list.y-proz          = to-list.y-proz       
      output-list.y-avrgrate      = to-list.y-avrgrate   
      output-list.comp-room       = to-list.comp-room    
      output-list.comp-pax        = to-list.comp-pax     
      output-list.comp-m-room     = to-list.comp-m-room  
      output-list.comp-m-pax      = to-list.comp-m-pax   
      output-list.comp-y-room     = to-list.comp-y-room  
      output-list.comp-y-pax      = to-list.comp-y-pax   
      output-list.exC-avrgrate    = to-list.exC-avrgrate 
      output-list.exC-m-avrgrate  = to-list.exC-m-avrgrate
      output-list.exC-y-avrgrate  = to-list.exC-y-avrgrate.
  END. 
  create output-list. 
  output-list.flag = 2. 
  DO ind = 1 TO 280: /*bef 180*/
    output-list.name = output-list.name + "-". 
  END. 
  create output-list. 
  output-list.flag = 3. 
  avrgrate = 0. 
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
  exC-avrgrate = 0. 
  IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room. 
  m-avrgrate = 0. 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  exC-m-avrgrate = 0. 
  IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
  y-avrgrate = 0. 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 
  exC-y-avrgrate = 0. 
  IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room. 
 
  ASSIGN                          
    output-list.NAME            = "T o t a l"
    output-list.room            = room         
    output-list.pax             = pax          
    output-list.logis           = logis         
    output-list.proz            = 100          
    output-list.avrgrate        = avrgrate      
    output-list.m-room          = m-room       
    output-list.m-pax           = m-pax        
    output-list.m-logis         = m-logis       
    output-list.m-proz          = 100          
    output-list.m-avrgrate      = m-avrgrate    
    output-list.y-room          = y-room       
    output-list.y-pax           = y-pax        
    output-list.y-logis         = y-logis     
    output-list.y-proz          = 100          
    output-list.y-avrgrate      = y-avrgrate   
    output-list.comp-room       = comp-room    
    output-list.comp-pax        = comp-pax     
    output-list.comp-m-room     = comp-m-room  
    output-list.comp-m-pax      = comp-m-pax   
    output-list.comp-y-room     = comp-y-room  
    output-list.comp-y-pax      = comp-y-pax   
    output-list.exC-avrgrate    = exC-avrgrate 
    output-list.exC-m-avrgrate  = exC-m-avrgrate
    output-list.exC-y-avrgrate  = exC-y-avrgrate.
END PROCEDURE. 
 

PROCEDURE create-umsatz4: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE from-date AS DATE. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE beg-date    AS DATE NO-UNDO.

/*DEFINE VARIABLE incl-comp AS LOGICAL INITIAL YES. */
  incl-comp = NOT excl-comp.
 
  room = 0. 
  c-room= 0. 
  pax = 0. 
  logis = 0. 
  m-room = 0. 
  mc-room = 0. 
  m-pax = 0. 
  m-logis = 0. 
  y-room = 0. 
  yc-room = 0. 
  y-pax = 0. 
  y-logis = 0. 
 
  /*IF MENU-ITEM mi-ftd:CHECKED IN MENU mbar = YES THEN */
  IF ytd-flag = 2 THEN
  DO:      
   /*to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date).
      beg-date = DATE(MONTH(f-date),1,yy).

      IF f-date GT beg-date THEN ASSIGN beg-date = f-date.
      IF MONTH(to-date) GT MONTH(f-date) THEN ASSIGN beg-date = DATE(mm,1,yy).
      from-date = beg-date.*/

      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
  END. 
  ELSE 
  DO: 
    mm = month(to-date). 
    yy = year(to-date). 
    from-date = DATE(1,1,yy). 
  END. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH to-list: 
    delete to-list. 
  END. 
  FOR EACH to-list1: 
    delete to-list1. 
  END. 

  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich: 
      create to-list. 
      to-list.gastnr = nation.nationnr. 
      IF nation.bezeich MATCHES "*;*" THEN ASSIGN to-list.name = ENTRY(1,nation.bezeich,";").
      ELSE ASSIGN to-list.name = nation.bezeich. 
      FIND FIRST to-list1 WHERE to-list1.gastnr = nation.untergruppe 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE to-list1 THEN 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 6 
          AND queasy.number1 = nation.untergruppe 
          AND queasy.number2 = 0 AND queasy.deci2 = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          create to-list1. 
          to-list1.gastnr = queasy.number1. 
          to-list1.name = queasy.char1. 
        END. 
      END. 
    
      FOR EACH genstat WHERE /*genstat.datum EQ datum*/
          genstat.datum GE from-date AND genstat.datum LE to-date
          AND genstat.resstatus NE 13 AND genstat.segmentcode NE 0
          /*AND genstat.res-int[1] NE 13*/
          AND genstat.resident NE 0     /*FT*/
          AND genstat.segmentcode NE 0  
          AND genstat.resident EQ nation.nationnr /*FT*/
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
          USE-INDEX nat_ix NO-LOCK: 
          
          /*M Sept 6th 11 = fix wrong exrate calculation  */
          datum = genstat.datum. 
          PROCESS EVENTS. 
          exchg-rate = 1. 
          IF currency-type = 2 THEN 
          DO: 
            IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
              AND exrate.datum = datum NO-LOCK NO-ERROR. 
            ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
            IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
          END. 

        IF genstat.datum = to-date THEN 
        DO: 
          /*MTIF incl-comp THEN */
          DO:
              FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
               IF NOT AVAILABLE tmp-room THEN
               DO:
                   to-list.room = to-list.room + 1.
                   room = room + 1.

                   IF AVAILABLE to-list1 THEN
                       to-list1.room  = to-list1.room  + 1.

                   CREATE tmp-room.
                   ASSIGN tmp-room.gastnr = genstat.gastnr
                               tmp-room.zinr = genstat.zinr
                               tmp-room.flag = 1.
               END.

               to-list.pax   = to-list.pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 
                                             + genstat.gratis.
               to-list.logis = to-list.logis + genstat.logis / exchg-rate. 
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.pax   = to-list1.pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2 
                                                   + genstat.gratis.
                   to-list1.logis = to-list1.logis + genstat.logis / exchg-rate. 
               END.

               pax   = pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2 
                             + genstat.gratis.
               logis = logis + genstat.logis / exchg-rate. 
          END. 
          /*MTELSE*/
          DO:
              IF genstat.gratis EQ 0 THEN
              DO:
                  FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                         AND tmp-room1.zinr EQ genstat.zinr 
                         AND tmp-room1.flag = 1 NO-ERROR.
                     IF NOT AVAILABLE tmp-room1 THEN
                     DO:
                              to-list.comp-room = to-list.comp-room + 1.
                              comp-room = comp-room + 1.

                              IF AVAILABLE to-list1 THEN
                                  to-list1.comp-room  = to-list1.comp-room  + 1.

                              CREATE tmp-room1.
                              ASSIGN tmp-room1.gastnr = genstat.gastnr
                                          tmp-room1.zinr = genstat.zinr
                                          tmp-room1.flag = 1.
                     END.

                     to-list.comp-pax   = to-list.comp-pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2.
                     /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate. */
                     IF AVAILABLE to-list1 THEN
                     DO:
                         to-list1.comp-pax   = to-list1.comp-pax   + genstat.erwachs 
                                                         + genstat.kind1 + genstat.kind2.
                         /*MTto-list1.logis = to-list1.logis + genstat.logis / exchg-rate. */
                     END.

                     comp-pax   = comp-pax   + genstat.erwachs 
                                   + genstat.kind1 + genstat.kind2.
                     /*MTlogis = logis + genstat.logis / exchg-rate. */
              END.
          END. 
        END. 
        IF month(genstat.datum) = mm /*AND year(genstat.datum) = yy*/ THEN 
        DO: 
          /*MTIF incl-comp THEN */
          DO: 
              to-list.m-room  = to-list.m-room  + 1.
               to-list.m-pax   = to-list.m-pax   + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2
                               + genstat.gratis.
               to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.m-room  = to-list1.m-room  + 1.
                   to-list1.m-pax   = to-list1.m-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2
                                    + genstat.gratis.
                   to-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.
               END.

               m-room  = m-room  + 1.
               m-pax   = m-pax   + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2
                                 + genstat.gratis.
               m-logis = m-logis + genstat.logis / exchg-rate.
          END. 
          /*MTELSE */
          DO: 
              IF genstat.gratis EQ 0 THEN
              DO:
                  to-list.comp-m-room  = to-list.comp-m-room  + 1.
                  to-list.comp-m-pax   = to-list.comp-m-pax   + genstat.erwachs 
                                  + genstat.kind1 + genstat.kind2.
                  /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/

                  IF AVAILABLE to-list1 THEN
                  DO:
                      to-list1.comp-m-room  = to-list1.comp-m-room  + 1.
                      to-list1.comp-m-pax   = to-list1.comp-m-pax   + genstat.erwachs 
                                       + genstat.kind1 + genstat.kind2.
                      /*MTto-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.*/
                  END.

                  comp-m-room  = comp-m-room  + 1.
                  comp-m-pax   = comp-m-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2.
                  /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
              END.
          END. 
        END. 

        /*MTIF incl-comp THEN*/
        DO:
            IF AVAILABLE to-list1 THEN
            DO:
                to-list1.y-room  = to-list1.y-room  + 1.
                to-list1.y-pax   = to-list1.y-pax   + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2
                                + genstat.gratis.
                to-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. 
            END.
            to-list.y-room  = to-list.y-room  + 1.
            to-list.y-pax   = to-list.y-pax  + genstat.erwachs 
                            + genstat.kind1 + genstat.kind2
                            + genstat.gratis.
            to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. 

            y-room  = y-room  + 1.
            y-pax   = y-pax   + genstat.erwachs 
                              + genstat.kind1 + genstat.kind2
                              + genstat.gratis.
            y-logis = y-logis + genstat.logis / exchg-rate.
        END.
        /*MTELSE*/
        DO:
            IF genstat.gratis EQ 0 THEN
            DO:
                IF AVAILABLE to-list1 THEN
                DO:
                    to-list1.comp-y-room  = to-list1.comp-y-room  + 1.
                    to-list1.comp-y-pax   = to-list1.comp-y-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2.
                    /*MTto-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. */
                END.
                to-list.comp-y-room  = to-list.comp-y-room  + 1.
                to-list.comp-y-pax   = to-list.comp-y-pax  + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2.
                /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. */

                comp-y-room  = comp-y-room  + 1.
                comp-y-pax   = comp-y-pax   + genstat.erwachs 
                                  + genstat.kind1 + genstat.kind2.
                /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
            END.
        END.
      END. 
  END. 
 
  /*MT
  FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.bezeich: 
    PROCESS EVENTS. 
    create to-list. 
    to-list.gastnr = nation.nationnr. 
    to-list.name = nation.bezeich. 
    FIND FIRST to-list1 WHERE to-list1.gastnr = nation.untergruppe 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE to-list1 THEN 
    DO: 
      FIND FIRST queasy WHERE queasy.key = 6 
        AND queasy.number1 = nation.untergruppe 
        AND queasy.number2 = 0 AND queasy.deci2 = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE queasy THEN 
      DO: 
        create to-list1. 
        to-list1.gastnr = queasy.number1. 
        to-list1.name = queasy.char1. 
      END. 
    END. 
 
    
      FOR EACH genstat WHERE /*genstat.datum EQ datum*/
           genstat.datum GE from-date AND genstat.datum LE to-date
           AND genstat.resstatus NE 13 AND genstat.segmentcode NE 0
           /*AND genstat.res-int[1] NE 13*/
           AND genstat.nationnr EQ nation.nationnr
           AND genstat.zinr NE ""
           USE-INDEX nat_ix NO-LOCK: 
          
          /*M Sept 6th 11 = fix wrong exrate calculation  */
          datum = genstat.datum. 
          PROCESS EVENTS. 
          exchg-rate = 1. 
          IF currency-type = 2 THEN 
          DO: 
            IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
              AND exrate.datum = datum NO-LOCK NO-ERROR. 
            ELSE FIND FIRST exrate WHERE exrate.datum = datum NO-LOCK NO-ERROR. 
            IF AVAILABLE exrate THEN exchg-rate = exrate.betrag. 
          END. 

        IF genstat.datum = to-date THEN 
        DO: 
          IF incl-comp THEN 
          DO:
              FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                   AND tmp-room.zinr EQ genstat.zinr 
                   AND tmp-room.flag = 1 NO-ERROR.
               IF NOT AVAILABLE tmp-room THEN
               DO:
                        to-list.room = to-list.room + 1.
                        room = room + 1.

                        IF AVAILABLE to-list1 THEN
                            to-list1.room  = to-list1.room  + 1.

                        CREATE tmp-room.
                        ASSIGN tmp-room.gastnr = genstat.gastnr
                                    tmp-room.zinr = genstat.zinr
                                    tmp-room.flag = 1.
               END.

               to-list.pax   = to-list.pax   + genstat.erwachs 
                                             + genstat.kind1 + genstat.kind2 
                                             + genstat.gratis.
               to-list.logis = to-list.logis + genstat.logis / exchg-rate. 
               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.pax   = to-list1.pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2 
                                                   + genstat.gratis.
                   to-list1.logis = to-list1.logis + genstat.logis / exchg-rate. 
               END.

               pax   = pax   + genstat.erwachs 
                             + genstat.kind1 + genstat.kind2 
                             + genstat.gratis.
               logis = logis + genstat.logis / exchg-rate. 
          END. 
          ELSE DO:
              IF genstat.gratis EQ 0 THEN
              DO:
                  FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                         AND tmp-room.zinr EQ genstat.zinr 
                         AND tmp-room.flag = 1 NO-ERROR.
                     IF NOT AVAILABLE tmp-room THEN
                     DO:
                              to-list.room = to-list.room + 1.
                              room = room + 1.

                              IF AVAILABLE to-list1 THEN
                                  to-list1.room  = to-list1.room  + 1.

                              CREATE tmp-room.
                              ASSIGN tmp-room.gastnr = genstat.gastnr
                                          tmp-room.zinr = genstat.zinr
                                          tmp-room.flag = 1.
                     END.

                     to-list.pax   = to-list.pax   + genstat.erwachs 
                                                   + genstat.kind1 + genstat.kind2.
                     to-list.logis = to-list.logis + genstat.logis / exchg-rate. 
                     IF AVAILABLE to-list1 THEN
                     DO:
                         to-list1.pax   = to-list1.pax   + genstat.erwachs 
                                                         + genstat.kind1 + genstat.kind2.
                         to-list1.logis = to-list1.logis + genstat.logis / exchg-rate. 
                     END.

                     pax   = pax   + genstat.erwachs 
                                   + genstat.kind1 + genstat.kind2.
                     logis = logis + genstat.logis / exchg-rate. 
              END.
          END. 
        END. 
        IF month(genstat.datum) = mm /*AND year(genstat.datum) = yy*/ THEN 
        DO: 
          IF incl-comp THEN 
          DO: 
              to-list.m-room  = to-list.m-room  + 1.
               to-list.m-pax   = to-list.m-pax   + genstat.erwachs 
                               + genstat.kind1 + genstat.kind2
                               + genstat.gratis.
               to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

               IF AVAILABLE to-list1 THEN
               DO:
                   to-list1.m-room  = to-list1.m-room  + 1.
                   to-list1.m-pax   = to-list1.m-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2
                                    + genstat.gratis.
                   to-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.
               END.

               m-room  = m-room  + 1.
               m-pax   = m-pax   + genstat.erwachs 
                                 + genstat.kind1 + genstat.kind2
                                 + genstat.gratis.
               m-logis = m-logis + genstat.logis / exchg-rate.
          END. 
          ELSE 
          DO: 
              IF genstat.gratis EQ 0 THEN
              DO:
                  to-list.m-room  = to-list.m-room  + 1.
                  to-list.m-pax   = to-list.m-pax   + genstat.erwachs 
                                  + genstat.kind1 + genstat.kind2.
                  to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

                  IF AVAILABLE to-list1 THEN
                  DO:
                      to-list1.m-room  = to-list1.m-room  + 1.
                      to-list1.m-pax   = to-list1.m-pax   + genstat.erwachs 
                                       + genstat.kind1 + genstat.kind2.
                      to-list1.m-logis = to-list1.m-logis + genstat.logis / exchg-rate.
                  END.

                  m-room  = m-room  + 1.
                  m-pax   = m-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2.
                  m-logis = m-logis + genstat.logis / exchg-rate.
              END.
          END. 
        END. 

        IF incl-comp THEN
        DO:
            IF AVAILABLE to-list1 THEN
            DO:
                to-list1.y-room  = to-list1.y-room  + 1.
                to-list1.y-pax   = to-list1.y-pax   + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2
                                + genstat.gratis.
                to-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. 
            END.
            to-list.y-room  = to-list.y-room  + 1.
            to-list.y-pax   = to-list.y-pax  + genstat.erwachs 
                            + genstat.kind1 + genstat.kind2
                            + genstat.gratis.
            to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. 

            y-room  = y-room  + 1.
            y-pax   = y-pax   + genstat.erwachs 
                              + genstat.kind1 + genstat.kind2
                              + genstat.gratis.
            y-logis = y-logis + genstat.logis / exchg-rate.
        END.
        ELSE
        DO:
            IF genstat.gratis EQ 0 THEN
            DO:
                IF AVAILABLE to-list1 THEN
                DO:
                    to-list1.y-room  = to-list1.y-room  + 1.
                    to-list1.y-pax   = to-list1.y-pax   + genstat.erwachs 
                                    + genstat.kind1 + genstat.kind2.
                    to-list1.y-logis = to-list1.y-logis + genstat.logis / exchg-rate. 
                END.
                to-list.y-room  = to-list.y-room  + 1.
                to-list.y-pax   = to-list.y-pax  + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2.
                to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate. 

                y-room  = y-room  + 1.
                y-pax   = y-pax   + genstat.erwachs 
                                  + genstat.kind1 + genstat.kind2.
                y-logis = y-logis + genstat.logis / exchg-rate.
            END.
        END.
      END. 
  END. 
  */
 
  FOR EACH to-list: 
    IF (to-list.room - to-list.c-room) NE 0 THEN 
      to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
     IF to-list.comp-room NE 0 THEN 
      to-list.exC-avrgrate = to-list.logis / to-list.comp-room. 

    IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
      to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room). 
    IF to-list.comp-m-room NE 0 THEN 
      to-list.exC-m-avrgrate = to-list.m-logis / to-list.comp-m-room. 

    IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
      to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room). 
    IF to-list.comp-y-room NE 0 THEN 
      to-list.exC-y-avrgrate = to-list.y-logis / to-list.comp-y-room. 

    IF logis NE 0 THEN 
      to-list.proz = to-list.logis / logis * 100. 
    IF m-logis NE 0 THEN 
      to-list.m-proz = to-list.m-logis / m-logis * 100. 
    IF y-logis NE 0 THEN 
      to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END. 
 
  FOR EACH to-list1: 
    IF (to-list1.room - to-list1.c-room) NE 0 THEN 
      to-list1.avrgrate = to-list1.logis / (to-list1.room - to-list1.c-room). 
    IF to-list1.comp-room NE 0 THEN 
      to-list1.exC-avrgrate = to-list1.logis / to-list1.comp-room. 
    IF logis NE 0 THEN 
      to-list1.proz = to-list1.logis / logis * 100. 

    IF (to-list1.m-room - to-list1.mc-room) NE 0 THEN 
      to-list1.m-avrgrate = to-list1.m-logis / (to-list1.m-room - to-list1.mc-room). 
    IF to-list1.comp-m-room NE 0 THEN 
      to-list1.exC-m-avrgrate = to-list1.m-logis / to-list1.comp-m-room. 
    IF m-logis NE 0 THEN 
      to-list1.m-proz = to-list1.m-logis / m-logis * 100. 

    IF (to-list1.y-room - to-list1.yc-room) NE 0 THEN 
      to-list1.y-avrgrate = to-list1.y-logis / (to-list1.y-room - to-list1.yc-room). 
    IF to-list1.comp-y-room NE 0 THEN 
      to-list1.exC-y-avrgrate = to-list1.y-logis / to-list1.comp-y-room.    
    IF y-logis NE 0 THEN 
      to-list1.y-proz = to-list1.y-logis / y-logis * 100. 
  END. 
 
  FOR EACH to-list WHERE to-list.y-room NE 0 NO-LOCK BY to-list.name: 
    create output-list. 
    output-list.flag = 1. 
    output-list.rmnite = to-list.y-room. 
    output-list.rmrev = to-list.y-logis. 
    output-list.rmnite1 = to-list.m-room. 
    output-list.rmrev1 = to-list.m-logis. 
    ASSIGN                          
      output-list.NAME            = to-list.NAME         
      output-list.room            = to-list.room         
      output-list.pax             = to-list.pax          
      output-list.logis           = to-list.logis        
      output-list.proz            = to-list.proz         
      output-list.avrgrate        = to-list.avrgrate      
      output-list.m-room          = to-list.m-room       
      output-list.m-pax           = to-list.m-pax        
      output-list.m-logis         = to-list.m-logis        
      output-list.m-proz          = to-list.m-proz       
      output-list.m-avrgrate      = to-list.m-avrgrate    
      output-list.y-room          = to-list.y-room       
      output-list.y-pax           = to-list.y-pax        
      output-list.y-logis         = to-list.y-logis       
      output-list.y-proz          = to-list.y-proz       
      output-list.y-avrgrate      = to-list.y-avrgrate   
      output-list.comp-room       = to-list.comp-room    
      output-list.comp-pax        = to-list.comp-pax     
      output-list.comp-m-room     = to-list.comp-m-room  
      output-list.comp-m-pax      = to-list.comp-m-pax   
      output-list.comp-y-room     = to-list.comp-y-room  
      output-list.comp-y-pax      = to-list.comp-y-pax   
      output-list.exC-avrgrate    = to-list.exC-avrgrate 
      output-list.exC-m-avrgrate  = to-list.exC-m-avrgrate
      output-list.exC-y-avrgrate  = to-list.exC-y-avrgrate.
  END. 
  create output-list. 
  output-list.flag = 2. 
  DO ind = 1 TO 280: /*bef 180*/
    output-list.name = output-list.name + "-". 
  END. 
  create output-list. 
  output-list.flag = 3. 
  avrgrate = 0. 
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room).
  exC-avrgrate = 0. 
  IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room.

  m-avrgrate = 0. 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  exC-m-avrgrate = 0. 
  IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 

  y-avrgrate = 0. 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room).
  exC-y-avrgrate = 0. 
  IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room.
 
  ASSIGN                          
    output-list.NAME            = "T o t a l"
    output-list.room            = room        
    output-list.pax             = pax         
    output-list.logis           = logis       
    output-list.proz            = 100         
    output-list.avrgrate        = avrgrate    
    output-list.m-room          = m-room      
    output-list.m-pax           = m-pax       
    output-list.m-logis         = m-logis     
    output-list.m-proz          = 100         
    output-list.m-avrgrate      = m-avrgrate  
    output-list.y-room          = y-room      
    output-list.y-pax           = y-pax       
    output-list.y-logis         = y-logis     
    output-list.y-proz          = 100         
    output-list.y-avrgrate      = y-avrgrate  
    output-list.comp-room       = comp-room   
    output-list.comp-pax        = comp-pax    
    output-list.comp-m-room     = comp-m-room 
    output-list.comp-m-pax      = comp-m-pax  
    output-list.comp-y-room     = comp-y-room 
    output-list.comp-y-pax      = comp-y-pax  
    output-list.exC-avrgrate    = exC-avrgrate
    output-list.exC-m-avrgrate  = exC-m-avrgrate
    output-list.exC-y-avrgrate  = exC-y-avrgrate.

  FIND FIRST to-list1 NO-LOCK NO-ERROR. 
  IF AVAILABLE to-list1 THEN 
  DO: 
    create output-list. 
    output-list.flag = 4. 
    create output-list. 
    output-list.flag = 5. 
    output-list.name = translateExtended ("*** STATISTIC BY REGION ***",lvCAREA,""). 
    FOR EACH to-list1 NO-LOCK BY to-list1.name: 
      create output-list. 
      output-list.flag = 6. 
      output-list.rmnite = to-list1.y-room. 
      output-list.rmrev = to-list1.y-logis. 
      output-list.rmnite1 = to-list1.m-room. 
      output-list.rmrev1 = to-list1.m-logis. 
      
      ASSIGN                          
        output-list.NAME            = to-list1.name
        output-list.room            = to-list1.room           
        output-list.pax             = to-list1.pax            
        output-list.logis           = to-list1.logis          
        output-list.proz            = to-list1.proz           
        output-list.avrgrate        = to-list1.avrgrate       
        output-list.m-room          = to-list1.m-room         
        output-list.m-pax           = to-list1.m-pax          
        output-list.m-logis         = to-list1.m-logis        
        output-list.m-proz          = to-list1.m-proz         
        output-list.m-avrgrate      = to-list1.m-avrgrate     
        output-list.y-room          = to-list1.y-room         
        output-list.y-pax           = to-list1.y-pax          
        output-list.y-logis         = to-list1.y-logis        
        output-list.y-proz          = to-list1.y-proz         
        output-list.y-avrgrate      = to-list1.y-avrgrate     
        output-list.comp-room       = to-list1.comp-room      
        output-list.comp-pax        = to-list1.comp-pax       
        output-list.comp-m-room     = to-list1.comp-m-room    
        output-list.comp-m-pax      = to-list1.comp-m-pax     
        output-list.comp-y-room     = to-list1.comp-y-room    
        output-list.comp-y-pax      = to-list1.comp-y-pax     
        output-list.exC-avrgrate    = to-list1.exC-avrgrate   
        output-list.exC-m-avrgrate  = to-list1.exC-m-avrgrate 
        output-list.exC-y-avrgrate  = to-list1.exC-y-avrgrate. 
    END. 

    create output-list. 
    output-list.flag = 7. 
    DO ind = 1 TO 280: /*bef 180*/
      output-list.name = output-list.name + "-". 
    END. 
    create output-list. 
    output-list.flag = 8. 
    avrgrate = 0. 
    IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
    exC-avrgrate = 0. 
    IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room. 
    m-avrgrate = 0. 
    IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
    exC-m-avrgrate = 0. 
    IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
    y-avrgrate = 0. 
    IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room).
    exC-y-avrgrate = 0. 
    IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room.
 
    ASSIGN                          
      output-list.NAME            = "T o t a l"
      output-list.room            = room         
      output-list.pax             = pax          
      output-list.logis           = logis        
      output-list.proz            = 100          
      output-list.avrgrate        = avrgrate     
      output-list.m-room          = m-room       
      output-list.m-pax           = m-pax        
      output-list.m-logis         = m-logis      
      output-list.m-proz          = 100          
      output-list.m-avrgrate      = m-avrgrate   
      output-list.y-room          = y-room       
      output-list.y-pax           = y-pax        
      output-list.y-logis         = y-logis       
      output-list.y-proz          = 100          
      output-list.y-avrgrate      = y-avrgrate   
      output-list.comp-room       = comp-room    
      output-list.comp-pax        = comp-pax     
      output-list.comp-m-room     = comp-m-room  
      output-list.comp-m-pax      = comp-m-pax   
      output-list.comp-y-room     = comp-y-room  
      output-list.comp-y-pax      = comp-y-pax   
      output-list.exC-avrgrate    = exC-avrgrate 
      output-list.exC-m-avrgrate  = exC-m-avrgrate
      output-list.exC-y-avrgrate  = exC-y-avrgrate.
  END. 
END. 

PROCEDURE create-umsatz5: 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE from-date AS DATE. 
DEFINE VARIABLE datum AS DATE. 
DEFINE BUFFER buf-nation FOR nation.
DEFINE VARIABLE beg-date    AS DATE NO-UNDO.

  ASSIGN
      incl-comp = NOT excl-comp
      room = 0
      c-room = 0
      pax = 0
      logis = 0
      m-room = 0
      mc-room = 0
      m-pax = 0
      m-logis = 0
      y-room = 0
      yc-room = 0
      y-pax = 0
      y-logis = 0.
  
  IF ytd-flag = 2 THEN
  DO:        
      /*to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date).
      beg-date = DATE(MONTH(f-date),1,yy).

      IF f-date GT beg-date THEN ASSIGN beg-date = f-date.
      IF MONTH(to-date) GT MONTH(f-date) THEN ASSIGN beg-date = DATE(mm,1,yy).
      from-date = beg-date.*/

      from-date = f-date. 
      to-date = t-date. 
      mm = month(to-date). 
      yy = year(to-date). 
  END. 
  ELSE 
  DO: 
      mm = month(to-date). 
      yy = year(to-date). 
      from-date = DATE(1,1,yy). 
  END. 
 
  FOR EACH output-list:
      delete output-list. 
  END. 
  FOR EACH to-list:
      delete to-list. 
  END. 

  FOR EACH nation WHERE nation.natcode > 0 NO-LOCK:
      FIND FIRST to-list WHERE 
          to-list.gastnr EQ nation.nationnr NO-ERROR.
      IF NOT AVAILABLE to-list THEN
      DO: 
          CREATE to-list.
          ASSIGN to-list.gastnr = nation.nationnr
                 to-list.NAME = nation.bezeich.
      END.

      FOR EACH genstat WHERE
          genstat.datum GE from-date AND genstat.datum LE to-date
          AND genstat.resstatus NE 13 
          /*AND genstat.res-int[1] NE 13*/
          AND genstat.segmentcode NE 0
          AND genstat.nationnr NE 0
          AND genstat.domestic EQ nation.nationnr
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
          USE-INDEX date_ix NO-LOCK,
          FIRST guest WHERE guest.gastnr EQ genstat.gastnrmember:

          IF genstat.datum EQ to-date THEN
          DO:
              FIND FIRST tmp-room WHERE tmp-room.gastnr EQ genstat.gastnr
                  AND tmp-room.zinr EQ genstat.zinr 
                  AND tmp-room.flag = 1 NO-ERROR.
              IF NOT AVAILABLE tmp-room THEN
              DO:
                  to-list.room = to-list.room + 1.
                  room = room + 1.

                  CREATE tmp-room.
                  ASSIGN tmp-room.gastnr = genstat.gastnr
                         tmp-room.zinr = genstat.zinr
                         tmp-room.flag = 1.
              END.
              to-list.pax = to-list.pax + genstat.erwachs 
                            + genstat.kind1 + genstat.kind2 
                            + genstat.gratis.
              to-list.logis = to-list.logis + genstat.logis / exchg-rate.

              pax = pax + genstat.erwachs + genstat.kind1 
                    + genstat.kind2 + genstat.gratis.
              logis = logis + genstat.logis / exchg-rate.

              IF genstat.gratis EQ 0 THEN
              DO:
                  FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                      AND tmp-room1.zinr EQ genstat.zinr 
                      AND tmp-room1.flag = 1 NO-ERROR.
                  IF NOT AVAILABLE tmp-room1 THEN
                  DO:
                      to-list.comp-room = to-list.comp-room + 1.
                      comp-room = comp-room + 1.

                      CREATE tmp-room1.
                      ASSIGN tmp-room1.gastnr = genstat.gastnr
                             tmp-room1.zinr = genstat.zinr
                             tmp-room1.flag = 1.
                  END.
                  to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2.
                  /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/

                  comp-pax = comp-pax + genstat.erwachs + genstat.kind1 
                        + genstat.kind2.
                  /*MTlogis = logis + genstat.logis / exchg-rate.*/
              END.
          END.

          IF MONTH(genstat.datum) = MONTH(to-date) /*AND year(genstat.datum) = yy*/ THEN 
          DO:
              to-list.m-room = to-list.m-room + 1.
              m-room = m-room + 1.

              to-list.m-pax = to-list.m-pax + genstat.erwachs 
                            + genstat.kind1 + genstat.kind2 + genstat.gratis.
              to-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.

              m-pax = m-pax + genstat.erwachs + genstat.kind1 
                    + genstat.kind2 + genstat.gratis.
              m-logis = m-logis + genstat.logis / exchg-rate.

              IF genstat.gratis EQ 0 THEN
              DO:
                  to-list.comp-m-room = to-list.comp-m-room + 1.
                  comp-m-room = comp-m-room + 1.


                  to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                                + genstat.kind1 + genstat.kind2.
                  /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/

                  comp-m-pax = comp-m-pax + genstat.erwachs + genstat.kind1 
                        + genstat.kind2.
                  /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
              END.
          END.

          to-list.y-room = to-list.y-room + 1.
          to-list.y-pax = to-list.y-pax + genstat.erwachs 
                        + genstat.kind1 + genstat.kind2 + genstat.gratis.
          to-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.

          y-room = y-room + 1.
          y-pax = y-pax + genstat.erwachs 
                + genstat.kind1 + genstat.kind2 + genstat.gratis.
          y-logis = y-logis + genstat.logis / exchg-rate.
          IF genstat.gratis EQ 0 THEN
          DO:
              to-list.comp-y-room = to-list.comp-y-room + 1.
              to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs 
                            + genstat.kind1 + genstat.kind2.
              comp-y-room = comp-y-room + 1.
              comp-y-pax = comp-y-pax + genstat.erwachs 
                    + genstat.kind1 + genstat.kind2.
          END.
      END.
  END.

  /***
  FOR EACH nation WHERE nation.natcode > 0:
      FIND FIRST to-list WHERE 
          to-list.gastnr EQ nation.nationnr NO-ERROR.
      IF NOT AVAILABLE to-list THEN
      DO: 
          CREATE to-list.
          ASSIGN to-list.gastnr = nation.nationnr
                 to-list.NAME = nation.bezeich.
      END.

      FOR EACH genstat WHERE
          genstat.datum GE from-date AND genstat.datum LE to-date
          AND genstat.resstatus NE 13 
          /*AND genstat.res-int[1] NE 13*/
          AND genstat.segmentcode NE 0
          AND genstat.nationnr NE 0
          AND genstat.gratis EQ 0
          AND genstat.domestic EQ nation.nationnr
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] /*MU 27032012 sleeping = yes */
          USE-INDEX date_ix,
          FIRST guest WHERE guest.gastnr EQ genstat.gastnrmember :

              IF genstat.datum EQ to-date THEN
              DO:
                FIND FIRST tmp-room1 WHERE tmp-room1.gastnr EQ genstat.gastnr
                    AND tmp-room1.zinr EQ genstat.zinr 
                    AND tmp-room1.flag = 1 NO-ERROR.
                IF NOT AVAILABLE tmp-room1 THEN
                DO:
                    to-list.comp-room = to-list.comp-room + 1.
                    comp-room = comp-room + 1.

                    CREATE tmp-room1.
                    ASSIGN tmp-room1.gastnr = genstat.gastnr
                           tmp-room1.zinr = genstat.zinr
                           tmp-room1.flag = 1.
                END.
                to-list.comp-pax = to-list.comp-pax + genstat.erwachs 
                              + genstat.kind1 + genstat.kind2.
                /*MTto-list.logis = to-list.logis + genstat.logis / exchg-rate.*/

                comp-pax = comp-pax + genstat.erwachs + genstat.kind1 
                      + genstat.kind2.
                /*MTlogis = logis + genstat.logis / exchg-rate.*/
              END.

              IF MONTH(genstat.datum) = MONTH(to-date) /*AND year(genstat.datum) = yy*/ THEN 
              DO:
                to-list.comp-m-room = to-list.comp-m-room + 1.
                comp-m-room = comp-m-room + 1.


                to-list.comp-m-pax = to-list.comp-m-pax + genstat.erwachs 
                              + genstat.kind1 + genstat.kind2.
                /*MTto-list.m-logis = to-list.m-logis + genstat.logis / exchg-rate.*/

                comp-m-pax = comp-m-pax + genstat.erwachs + genstat.kind1 
                      + genstat.kind2.
                /*MTm-logis = m-logis + genstat.logis / exchg-rate.*/
              END.

              to-list.comp-y-room = to-list.comp-y-room + 1.
              to-list.comp-y-pax = to-list.comp-y-pax + genstat.erwachs 
                            + genstat.kind1 + genstat.kind2.
              /*MTto-list.y-logis = to-list.y-logis + genstat.logis / exchg-rate.*/

              comp-y-room = comp-y-room + 1.
              comp-y-pax = comp-y-pax + genstat.erwachs 
                    + genstat.kind1 + genstat.kind2.
              /*MTy-logis = y-logis + genstat.logis / exchg-rate.*/
      END.
  END.
  ***/

  FOR EACH to-list: 
      IF (to-list.room - to-list.c-room) NE 0 THEN 
        to-list.avrgrate = to-list.logis / (to-list.room - to-list.c-room). 
      IF to-list.comp-room NE 0 THEN 
        to-list.exC-avrgrate = to-list.logis / to-list.comp-room.
      IF logis NE 0 THEN 
        to-list.proz = to-list.logis / logis * 100. 

      IF (to-list.m-room - to-list.mc-room) NE 0 THEN 
        to-list.m-avrgrate = to-list.m-logis / (to-list.m-room - to-list.mc-room). 
      IF to-list.comp-m-room NE 0 THEN 
        to-list.exC-m-avrgrate = to-list.m-logis / to-list.comp-m-room. 
      IF m-logis NE 0 THEN 
        to-list.m-proz = to-list.m-logis / m-logis * 100.

      IF (to-list.y-room - to-list.yc-room) NE 0 THEN 
        to-list.y-avrgrate = to-list.y-logis / (to-list.y-room - to-list.yc-room). 
      IF to-list.comp-y-room NE 0 THEN 
        to-list.exC-y-avrgrate = to-list.y-logis / to-list.comp-y-room. 
      IF y-logis NE 0 THEN 
        to-list.y-proz = to-list.y-logis / y-logis * 100. 
  END. 
 
  FOR EACH to-list NO-LOCK WHERE to-list.y-room NE 0 
      BY to-list.name: 
      create output-list. 
      output-list.flag = 1. 
      output-list.rmnite = to-list.y-room. 
      output-list.rmrev = to-list.y-logis. 
      output-list.rmnite1 = to-list.m-room. 
      output-list.rmrev1 = to-list.m-logis. 
       
      ASSIGN                          
        output-list.NAME            = to-list.name        
        output-list.room            = to-list.room        
        output-list.pax             = to-list.pax         
        output-list.logis           = to-list.logis        
        output-list.proz            = to-list.proz        
        output-list.avrgrate        = to-list.avrgrate     
        output-list.m-room          = to-list.m-room      
        output-list.m-pax           = to-list.m-pax       
        output-list.m-logis         = to-list.m-logis       
        output-list.m-proz          = to-list.m-proz      
        output-list.m-avrgrate      = to-list.m-avrgrate   
        output-list.y-room          = to-list.y-room      
        output-list.y-pax           = to-list.y-pax       
        output-list.y-logis         = to-list.y-logis      
        output-list.y-proz          = to-list.y-proz      
        output-list.y-avrgrate      = to-list.y-avrgrate  
        output-list.comp-room       = to-list.comp-room   
        output-list.comp-pax        = to-list.comp-pax    
        output-list.comp-m-room     = to-list.comp-m-room 
        output-list.comp-m-pax      = to-list.comp-m-pax  
        output-list.comp-y-room     = to-list.comp-y-room 
        output-list.comp-y-pax      = to-list.comp-y-pax  
        output-list.exC-avrgrate    = to-list.exC-avrgrate
        output-list.exC-m-avrgrate  = to-list.exC-m-avrgrate
        output-list.exC-y-avrgrate  = to-list.exC-y-avrgrate.
  END. 

  create output-list. 
  output-list.flag = 2. 
  DO ind = 1 TO 280: /*bef 180*/
    output-list.name = output-list.name + "-". 
  END. 
  create output-list. 
  output-list.flag = 3. 
  avrgrate = 0. 
  IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room).
  exC-avrgrate = 0. 
  IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room.
  m-avrgrate = 0. 
  IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
  exC-m-avrgrate = 0. 
  IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
  y-avrgrate = 0. 
  IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room). 
  exC-y-avrgrate = 0. 
  IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room. 
 
  ASSIGN                          
    output-list.NAME            = "T o t a l" 
    output-list.room            = room         
    output-list.pax             = pax          
    output-list.logis           = logis        
    output-list.proz            = 100          
    output-list.avrgrate        = avrgrate     
    output-list.m-room          = m-room       
    output-list.m-pax           = m-pax        
    output-list.m-logis         = m-logis      
    output-list.m-proz          = 100          
    output-list.m-avrgrate      = m-avrgrate   
    output-list.y-room          = y-room       
    output-list.y-pax           = y-pax        
    output-list.y-logis         = y-logis      
    output-list.y-proz          = 100          
    output-list.y-avrgrate      = y-avrgrate   
    output-list.comp-room       = comp-room  
    output-list.comp-pax        = comp-pax   
    output-list.comp-m-room     = comp-m-room
    output-list.comp-m-pax      = comp-m-pax 
    output-list.comp-y-room     = comp-y-room
    output-list.comp-y-pax      = comp-y-pax 
    output-list.exC-avrgrate    = exC-avrgrate 
    output-list.exC-m-avrgrate  = exC-m-avrgrate
    output-list.exC-y-avrgrate  = exC-y-avrgrate.
 
  FIND FIRST to-list1 NO-LOCK NO-ERROR. 
  IF AVAILABLE to-list1 THEN 
  DO: 
    create output-list. 
    output-list.flag = 4. 
    create output-list. 
    output-list.flag = 5. 
    output-list.name = translateExtended ("*** STATISTIC BY REGION ***",lvCAREA,""). 
    FOR EACH to-list1 NO-LOCK BY to-list1.name: 
      create output-list. 
      output-list.flag = 6. 
      output-list.rmnite = to-list1.y-room. 
      output-list.rmrev = to-list1.y-logis. 
      output-list.rmnite1 = to-list1.m-room. 
      output-list.rmrev1 = to-list1.m-logis. 

        ASSIGN                          
          output-list.NAME            = to-list1.name           
          output-list.room            = to-list1.room           
          output-list.pax             = to-list1.pax            
          output-list.logis           = to-list1.logis          
          output-list.proz            = to-list1.proz           
          output-list.avrgrate        = to-list1.avrgrate       
          output-list.m-room          = to-list1.m-room         
          output-list.m-pax           = to-list1.m-pax          
          output-list.m-logis         = to-list1.m-logis         
          output-list.m-proz          = to-list1.m-proz         
          output-list.m-avrgrate      = to-list1.m-avrgrate     
          output-list.y-room          = to-list1.y-room         
          output-list.y-pax           = to-list1.y-pax          
          output-list.y-logis         = to-list1.y-logis        
          output-list.y-proz          = to-list1.y-proz         
          output-list.y-avrgrate      = to-list1.y-avrgrate     
          output-list.comp-room       = to-list1.comp-room      
          output-list.comp-pax        = to-list1.comp-pax       
          output-list.comp-m-room     = to-list1.comp-m-room    
          output-list.comp-m-pax      = to-list1.comp-m-pax     
          output-list.comp-y-room     = to-list1.comp-y-room    
          output-list.comp-y-pax      = to-list1.comp-y-pax     
          output-list.exC-avrgrate    = to-list1.exC-avrgrate   
          output-list.exC-m-avrgrate  = to-list1.exC-m-avrgrate 
          output-list.exC-y-avrgrate  = to-list1.exC-y-avrgrate. 
    END. 

    create output-list. 
    output-list.flag = 7. 
    DO ind = 1 TO 280: /*bef 180*/
      output-list.name = output-list.name + "-". 
    END. 
    create output-list. 
    output-list.flag = 8. 
    avrgrate = 0. 
    IF (room - c-room) NE 0 THEN avrgrate = logis / (room - c-room). 
    exC-avrgrate = 0. 
    IF comp-room NE 0 THEN exC-avrgrate = logis / comp-room. 
    m-avrgrate = 0. 
    IF (m-room - mc-room) NE 0 THEN m-avrgrate = m-logis / (m-room - mc-room). 
    exC-m-avrgrate = 0. 
    IF comp-m-room NE 0 THEN exC-m-avrgrate = m-logis / comp-m-room. 
    y-avrgrate = 0. 
    IF (y-room - yc-room) NE 0 THEN y-avrgrate = y-logis / (y-room - yc-room).
    exC-y-avrgrate = 0. 
    IF comp-y-room NE 0 THEN exC-y-avrgrate = y-logis / comp-y-room.
    IF price-decimal = 0 AND currency-type = 1 THEN 
    ASSIGN                          
      output-list.NAME            = "T o t a l"
      output-list.room            = room         
      output-list.pax             = pax          
      output-list.logis           = logis        
      output-list.proz            = 100          
      output-list.avrgrate        = avrgrate     
      output-list.m-room          = m-room       
      output-list.m-pax           = m-pax        
      output-list.m-logis         = m-logis      
      output-list.m-proz          = 100          
      output-list.m-avrgrate      = m-avrgrate   
      output-list.y-room          = y-room       
      output-list.y-pax           = y-pax        
      output-list.y-logis         = y-logis      
      output-list.y-proz          = 100          
      output-list.y-avrgrate      = y-avrgrate   
      output-list.comp-room       = comp-room    
      output-list.comp-pax        = comp-pax     
      output-list.comp-m-room     = comp-m-room  
      output-list.comp-m-pax      = comp-m-pax   
      output-list.comp-y-room     = comp-y-room  
      output-list.comp-y-pax      = comp-y-pax   
      output-list.exC-avrgrate    = exC-avrgrate 
      output-list.exC-m-avrgrate  = exC-m-avrgrate
      output-list.exC-y-avrgrate  = exC-y-avrgrate.
  END. 
END.
