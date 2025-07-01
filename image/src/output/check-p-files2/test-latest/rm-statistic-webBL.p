DEFINE TEMP-TABLE rm-statistic-list
  FIELD grpflag     AS LOGICAL     
  FIELD flag        AS CHARACTER FORMAT "x(10)"
  FIELD segm        AS CHARACTER FORMAT "x(3)"
  FIELD bezeich     AS CHARACTER FORMAT "x(32)"
  FIELD dgroom      AS CHARACTER FORMAT "x(6)"
  FIELD proz1       AS CHARACTER FORMAT "x(6)"
  FIELD mgroom      AS CHARACTER FORMAT "x(6)"
  FIELD proz2       AS CHARACTER FORMAT "x(6)"
  FIELD ygroom      AS CHARACTER FORMAT "x(6)"
  FIELD proz3       AS CHARACTER FORMAT "x(6)"
  FIELD dgpax       AS CHARACTER FORMAT "x(6)"
  FIELD mgpax       AS CHARACTER FORMAT "x(6)"
  FIELD ygpax       AS CHARACTER FORMAT "x(6)"
  FIELD dgrate      AS CHARACTER FORMAT "x(19)"
  FIELD mgrate      AS CHARACTER FORMAT "x(19)"
  FIELD ygrate      AS CHARACTER FORMAT "x(19)"
  FIELD dgrev       AS CHARACTER FORMAT "x(19)"
  FIELD mgrev       AS CHARACTER FORMAT "x(19)"
  FIELD ygrev       AS CHARACTER FORMAT "x(19)"
.

DEFINE TEMP-TABLE rm-statistic-list1
  FIELD grpflag     AS LOGICAL     
  FIELD flag        AS CHARACTER FORMAT "x(10)"
  FIELD segm        AS CHARACTER FORMAT "x(3)" 
  FIELD bezeich     AS CHARACTER FORMAT "x(32)"
  FIELD droom       AS CHARACTER FORMAT "x(6)"               
  FIELD proz1       AS CHARACTER FORMAT "x(6)" 
  FIELD mroom       AS CHARACTER FORMAT "x(6)" 
  FIELD proz2       AS CHARACTER FORMAT "x(6)" 
  FIELD yroom       AS CHARACTER FORMAT "x(6)" 
  FIELD proz3       AS CHARACTER FORMAT "x(6)" 
  FIELD dpax        AS CHARACTER FORMAT "x(6)"                
  FIELD mpax        AS CHARACTER FORMAT "x(6)" 
  FIELD ypax        AS CHARACTER FORMAT "x(6)" 
  FIELD drate       AS CHARACTER FORMAT "x(19)"
  FIELD mrate       AS CHARACTER FORMAT "x(19)"
  FIELD yrate       AS CHARACTER FORMAT "x(19)"
  FIELD drev        AS CHARACTER FORMAT "x(19)"
  FIELD mrev        AS CHARACTER FORMAT "x(19)"
  FIELD yrev        AS CHARACTER FORMAT "x(19)"
.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER call-from        AS INTEGER.
DEFINE INPUT PARAMETER txt-file         AS CHAR.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER grp-flag         AS LOGICAL.
DEFINE INPUT PARAMETER show-ytd         AS LOGICAL.
DEFINE INPUT PARAMETER show-other       AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR rm-statistic-list.
DEFINE OUTPUT PARAMETER TABLE FOR rm-statistic-list1.

DEFINE VARIABLE LnLDelimeter            AS CHAR.

DEFINE TEMP-TABLE cl-list 
  FIELD grpflag    AS LOGICAL INITIAL NO 
  FIELD flag       AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD segm       AS INTEGER FORMAT ">>>" INITIAL 0 
  FIELD bezeich    AS CHAR FORMAT "x(16)" 
  FIELD droom      AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD tot-droom  AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD proz1      AS DECIMAL FORMAT ">>9.99" 
  FIELD mroom      AS INTEGER FORMAT ">,>>9" INITIAL 0 
  FIELD proz2      AS DECIMAL FORMAT ">>9.99" 
  FIELD yroom      AS INTEGER FORMAT ">>>,>>9" INITIAL 0
  FIELD proz3      AS DECIMAL FORMAT ">>9.99" 
  FIELD dpax       AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD tot-dpax   AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD mpax       AS INTEGER FORMAT ">,>>9" INITIAL 0 
  FIELD ypax       AS INTEGER FORMAT ">>>,>>9" INITIAL 0 
  FIELD drate      AS DECIMAL FORMAT ">>>,>>>,>>9.99" 
  FIELD mrate      AS DECIMAL FORMAT ">>>,>>>,>>9.99" 
  FIELD yrate      AS DECIMAL FORMAT ">>>,>>>,>>9.99" 
  FIELD drev       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD mrev       AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
  FIELD yrev       AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
  FIELD orev       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD flag-comp  AS LOGICAL INIT NO
  FIELD flag-temp  AS LOGICAL INIT NO
  FIELD segm-grup  AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE other-list
    FIELD flag       AS CHAR 
    FIELD segm       AS INTEGER FORMAT ">>>" INITIAL 0
    FIELD bezeich    AS CHAR FORMAT "x(16)"
    FIELD orev       AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD morev      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    FIELD yorev      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"
    .

DEFINE TEMP-TABLE s-list        /*utk compliment*/
  FIELD nr          AS INTEGER 
  FIELD bezeich     AS CHAR 
  FIELD droom       AS INTEGER 
  FIELD mroom       AS INTEGER 
  FIELD yroom       AS INTEGER
  FIELD dpax        AS INTEGER 
  FIELD mpax        AS INTEGER
  FIELD ypax        AS INTEGER
  . 

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

DEFINE VARIABLE droom AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE proz1 AS DECIMAL FORMAT ">>9.9". 
DEFINE VARIABLE mroom AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE proz2 AS INTEGER FORMAT ">>9.9". 
DEFINE VARIABLE yroom AS INTEGER FORMAT ">>>,>>9". 
DEFINE VARIABLE proz3 AS INTEGER FORMAT ">>9.9". 
DEFINE VARIABLE dpax  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mpax  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ypax  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE drate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE mrate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE yrate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE drev  AS DECIMAL FORMAT ">>,>>>,>>9.99". 
DEFINE VARIABLE mrev  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE yrev  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE lodg  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE olodg AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
 
DEFINE VARIABLE dgroom AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE gproz1 AS DECIMAL FORMAT ">>9.9". 
DEFINE VARIABLE mgroom AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE gproz2 AS INTEGER FORMAT ">>9.9". 
DEFINE VARIABLE ygroom AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE gproz3 AS INTEGER FORMAT ">>9.9". 
DEFINE VARIABLE dgpax  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mgpax  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ygpax  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE dgrate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE mgrate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE ygrate AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE dgrev  AS DECIMAL FORMAT ">>,>>>,>>9.99". 
DEFINE VARIABLE mgrev  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE ygrev  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 


DEFINE VARIABLE dgroom1 AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mgroom1 AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ygroom1 AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE dgpax1  AS INTEGER FORMAT ">>9". 
DEFINE VARIABLE mgpax1  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE ygpax1  AS INTEGER FORMAT ">,>>9". 
DEFINE VARIABLE dgrate1 AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE mgrate1 AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE ygrate1 AS DECIMAL FORMAT ">,>>>,>>9.99". 
DEFINE VARIABLE dgrev1  AS DECIMAL FORMAT ">>,>>>,>>9.99". 
DEFINE VARIABLE mgrev1  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE ygrev1  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 


DEFINE VARIABLE ttrev  AS DECIMAL FORMAT ">>,>>>,>>9.99". 
DEFINE VARIABLE ttmrev AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE ttyrev AS DECIMAL FORMAT ">>>,>>>,>>9.99". 

DEFINE VARIABLE from-date AS DATE NO-UNDO.

DEFINE BUFFER r-list   FOR rm-statistic-list. 
DEFINE BUFFER r-list1  FOR rm-statistic-list1.
DEFINE VARIABLE period-str  AS CHAR    NO-UNDO. 
DEFINE VARIABLE comp-room   AS CHAR    NO-UNDO. 
DEFINE VARIABLE curr-grup   AS INTEGER NO-UNDO.

DEFINE VARIABLE tot-droom AS INTEGER . 
DEFINE VARIABLE tot-proz1 AS DECIMAL . /*ragung from int change to decimal*/
DEFINE VARIABLE tot-mroom AS INTEGER . 
DEFINE VARIABLE tot-proz2 AS DECIMAL . /*ragung from int change to decimal*/
DEFINE VARIABLE tot-yroom AS INTEGER . 
DEFINE VARIABLE tot-proz3 AS INTEGER . 
DEFINE VARIABLE tot-dpax  AS INTEGER . 
DEFINE VARIABLE tot-mpax  AS INTEGER . 
DEFINE VARIABLE tot-ypax  AS INTEGER . 
DEFINE VARIABLE tot-drate AS DECIMAL . 
DEFINE VARIABLE tot-mrate AS DECIMAL . 
DEFINE VARIABLE tot-yrate AS DECIMAL . 
DEFINE VARIABLE tot-drev  AS DECIMAL . 
DEFINE VARIABLE tot-mrev  AS DECIMAL .
DEFINE VARIABLE tot-yrev  AS DECIMAL . 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rm-statistic-web". 

comp-room = translateExtended ("Compliment Rooms" , lvCAREA, ""). 
 
/****************************MAIN LOGIC**************************/
IF show-ytd THEN 
    RUN create-umsatz2. 
ELSE
    RUN create-umsatz.
/****************************PROCEDURE***************************/
PROCEDURE create-other:
    DEFINE VARIABLE black-list AS INTEGER. 
    FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
    black-list = htparam.finteger. 

    FOR EACH other-list:
        DELETE other-list.
    END.

    FOR EACH zinrstat WHERE zinrstat.datum GE from-date 
        AND zinrstat.datum LE to-date AND zinrstat.zinr = "SEGM" NO-LOCK, 
        FIRST segment WHERE segment.segmentcode = zinrstat.betriebsnr 
        AND segment.segmentcode NE black-list AND segment.segmentgrup LE 99 
        NO-LOCK BY segment.segmentgrup BY segment.segmentcode:
        FIND FIRST other-list WHERE other-list.segm = segment.segmentcode
           NO-ERROR.
        IF NOT AVAILABLE other-list THEN
        DO:
            CREATE other-list.
            ASSIGN 
                other-list.segm = segment.segmentcode.
        END.
        IF zinrstat.datum = to-date THEN
            other-list.orev = zinrstat.logisumsatz.
        IF MONTH(zinrstat.datum) = MONTH(to-date) THEN
            other-list.morev = other-list.morev + zinrstat.logisumsatz.
        IF show-ytd THEN
            other-list.yorev  = other-list.yorev + zinrstat.logisumsatz.
    END.
END PROCEDURE.

PROCEDURE create-umsatz2:
    DEFINE VARIABLE black-list AS INTEGER. 
    DEFINE VARIABLE fl-comp AS LOGICAL INIT NO.
    DEFINE VAR i AS INT INIT 0.
    DEFINE VARIABLE curr-grp AS INTEGER INITIAL -1. 
    DEFINE VARIABLE curr-segm AS INTEGER INITIAL 0. 
    DEFINE VARIABLE aa AS INTEGER INITIAL 0. 
    DEFINE VARIABLE xx AS INTEGER INITIAL 0. 
    DEFINE VARIABLE tot-slist-dpax AS DECIMAL INITIAL 0. 

    FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
    black-list = htparam.finteger. 

    FOR EACH rm-statistic-list: 
        DELETE rm-statistic-list. 
    END. 

    FOR EACH rm-statistic-list1:
        DELETE rm-statistic-list1.
    END.

    FOR EACH cl-list: 
      DELETE cl-list. 
    END. 

    FOR EACH s-list: 
      DELETE s-list. 
    END. 

    ASSIGN droom    = 0
           mroom    = 0 
           yroom    = 0 
           dpax     = 0 
           mpax     = 0 
           ypax     = 0 
           drate    = 0 
           mrate    = 0 
           yrate    = 0 
           drev     = 0 
           mrev     = 0 
           yrev     = 0 
           dgroom   = 0 
           mgroom   = 0 
           ygroom   = 0 
           dgpax    = 0 
           mgpax    = 0 
           ygpax    = 0 
           dgrate   = 0 
           mgrate   = 0 
           ygrate   = 0 
           dgrev    = 0 
           mgrev    = 0 
           ygrev    = 0 
           dgroom1  = 0 
           mgroom1  = 0 
           ygroom1  = 0 
           dgpax1   = 0 
           mgpax1   = 0 
           ygpax1   = 0 
           dgrate1  = 0 
           mgrate1  = 0 
           ygrate1  = 0 
           dgrev1   = 0 
           mgrev1   = 0 
           ygrev1   = 0
           tot-droom = 0 
           tot-proz1 = 0
           tot-mroom = 0 
           tot-proz2 = 0 
           tot-yroom = 0 
           tot-proz3 = 0 
           tot-dpax  = 0 
           tot-mpax  = 0 
           tot-ypax  = 0 
           tot-drate = 0 
           tot-mrate = 0  
           tot-yrate = 0  
           tot-drev  = 0  
           tot-mrev  = 0 
           tot-yrev  = 0. 

    DEFINE VAR flag-temp AS LOGICAL INIT NO.

    from-date = DATE(1, 1, year(to-date)). 
    IF show-other THEN RUN create-other.

    FOR EACH genstat WHERE 
        genstat.datum GE from-date 
        AND genstat.datum LE to-date
        AND genstat.segmentcode NE 0
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES 
        NO-LOCK USE-INDEX gastnrmember_ix, 
        FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
        AND segment.segmentcode NE black-list /* AND segment.segmentgrup LE 99 */
        BY genstat.segmentcode:

        IF genstat.zipreis EQ 0 AND genstat.resstatus EQ 6 AND genstat.gratis NE 0 THEN fl-comp = YES.    /*compliment*/
        ELSE fl-comp = NO.
        
        DO:
            FIND FIRST cl-list WHERE cl-list.segm EQ genstat.segmentcode
                AND cl-list.flag-comp EQ fl-comp AND NOT cl-list.grpflag NO-ERROR.
            IF NOT AVAILABLE cl-list THEN
            DO:
                CREATE cl-list.
                ASSIGN cl-list.segm      = genstat.segmentcode          /*SNo*/
                       cl-list.bezeich   = segment.bezeich            /*Guest Segment*/
                       cl-list.flag-comp = fl-comp
                       cl-list.segm-grup = segment.segmentgrup.
    
                IF genstat.zipreis EQ 0 AND genstat.resstatus NE 13 AND genstat.resstatus EQ 6 
                    AND genstat.gratis NE 0 THEN     /*compliment*/
                DO:
                    IF genstat.datum = to-date THEN
                    DO:
                        ASSIGN cl-list.droom = 1                                   /*#Rm*/
                               cl-list.dpax = cl-list.dpax + genstat.gratis
                               droom = droom + 1. /*MT 060912 */.
                    END.
                    IF MONTH(genstat.datum) = MONTH(to-date) THEN
                    DO:
                        ASSIGN cl-list.mroom = 1        /*Pax*/
                               cl-list.mpax = cl-list.mpax + genstat.gratis
                               mroom = mroom + 1. /*MT 060912 */
                    END.
    
                    ASSIGN cl-list.yroom = cl-list.yroom + 1
                           cl-list.ypax = cl-list.ypax + genstat.gratis
                           yroom = yroom + 1. /*MT 060912 */
                END.
                ELSE IF genstat.resstatus NE 13 /* AND genstat.gratis EQ 0 */ THEN                /*paying awal*/
                DO:
                    IF genstat.datum = to-date THEN
                    DO: 
                        ASSIGN cl-list.drev = genstat.logis                    /*Room-Revenue*/
                               cl-list.droom = cl-list.droom + 1                                   /*#Rm*/
                               cl-list.dpax = cl-list.dpax + genstat.erwachs 
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3        /*Pax*/
                               dgroom = dgroom + 1        /*total #Rm*/
                               dgpax = dgpax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.kind3
                               dgrev = dgrev + genstat.logis          /*Total Room-Revenue*/
                               cl-list.drate = cl-list.drate + (cl-list.drev / cl-list.droom)
                               dgrate = dgrev / dgroom
                               droom = droom + 1. /*MT 060912 */
                    END.
                    IF MONTH(genstat.datum) = MONTH(to-date) THEN
                    DO:
                        ASSIGN cl-list.mrev = genstat.logis
                               cl-list.mroom = cl-list.mroom + 1             /*MTD pertama*/
                               cl-list.mpax = cl-list.mpax + genstat.erwachs 
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3
                               mgroom = mgroom + 1      /*total MTD pertama*/
                               mgpax = mgpax + genstat.erwachs + genstat.kind1 
                                     + genstat.kind2 + genstat.kind3
                               mgrev = mgrev + genstat.logis
                               cl-list.mrate = cl-list.mrate + (cl-list.mrev / cl-list.mroom)
                               mgrate = mgrev / mgroom
                               mroom = mroom + 1. /*MT 060912 */
                    END.
                    ASSIGN cl-list.yrev = genstat.logis
                           cl-list.yroom = cl-list.yroom + 1             /*YTD pertama*/
                           cl-list.ypax = cl-list.ypax + genstat.erwachs 
                                        + genstat.kind1 + genstat.kind2 + genstat.kind3
                           ygroom = ygroom + 1      /*total YTD pertama*/
                           ygpax = ygpax + genstat.erwachs + genstat.kind1 
                                 + genstat.kind2 + genstat.kind3
                           ygrev = ygrev + genstat.logis
                           cl-list.yrate = cl-list.yrate + (cl-list.yrev / cl-list.yroom)
                           ygrate = ygrev / ygroom
                           yroom = yroom + 1. /*MT 060912 */
                END.
            END.
            ELSE        /*cl-list available*/
            DO:
                IF genstat.zipreis EQ 0 AND genstat.resstatus NE 13 AND genstat.resstatus EQ 6
                    AND genstat.gratis NE 0 THEN     /*compliment*/
                DO:
                    IF genstat.datum = to-date THEN 
                    DO:
                        UPDATE cl-list.droom = cl-list.droom + 1
                               cl-list.dpax = cl-list.dpax +  genstat.gratis
                               droom = droom + 1. /*MT 060912 */
                    END.
    
                    IF MONTH(genstat.datum) = MONTH(to-date) THEN
                    DO:
                        UPDATE cl-list.mroom = cl-list.mroom + 1
                               cl-list.mpax = cl-list.mpax +  genstat.gratis
                               mroom = mroom + 1. /*MT 060912 */
                    END.
    
                    UPDATE cl-list.yroom = cl-list.yroom + 1 
                           cl-list.ypax = cl-list.ypax + genstat.gratis
                           yroom = yroom + 1. /*MT 060912 */
                END.
                ELSE IF genstat.resstatus NE 13 /* AND genstat.gratis EQ 0 */ THEN
                DO:
                    IF genstat.datum = to-date THEN
                    DO: 
                            ASSIGN cl-list.drev = cl-list.drev + genstat.logis                    /*Room-Revenue*/
                                   cl-list.droom = cl-list.droom + 1                                   /*#Rm*/
                                   cl-list.dpax = cl-list.dpax + genstat.erwachs 
                                                + genstat.kind1 + genstat.kind2 + genstat.kind3    /*Pax*/
                                   dgroom = dgroom + 1        /*total #Rm*/
                                   dgpax = dgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   dgrev = dgrev + genstat.logis          /*Total Room-Revenue*/
                                   cl-list.drate = cl-list.drev / cl-list.droom
                                   dgrate = dgrev / dgroom
                                   droom = droom + 1. /*MT 060912 */
                        END.
                       
                        IF MONTH(genstat.datum) = MONTH(to-date) THEN
                        DO:
                            ASSIGN cl-list.mrev = cl-list.mrev + genstat.logis
                                   cl-list.mroom =  cl-list.mroom + 1             /*MTD pertama*/
                                   cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.kind1 
                                                + genstat.kind2 + genstat.kind3
                                   mgroom = mgroom + 1      /*total MTD pertama*/
                                   mgpax = mgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   mgrev = mgrev + genstat.logis
                                   cl-list.mrate = cl-list.mrev / cl-list.mroom
                                   mgrate = mgrev / mgroom
                                   mroom = mroom + 1. /*MT 060912 */
                        END.
    
    
                        ASSIGN cl-list.yroom = cl-list.yroom + 1
                               ygroom = ygroom + 1
                               cl-list.yrev = cl-list.yrev + genstat.logis
                               ygrev = ygrev + genstat.logis 
                               cl-list.yrate = cl-list.yrev / cl-list.yroom
                               ygrate = ygrev / ygroom
                               cl-list.ypax = cl-list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                               ygpax = ygpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                               yroom = yroom + 1. /*MT 060912 */
                END.
            END.
        END.
     END.
    

    FOR EACH cl-list WHERE NOT cl-list.flag-comp: 
    
    IF cl-list.droom EQ 0 THEN cl-list.dpax = 0. 
    IF cl-list.mroom EQ 0 THEN cl-list.mpax = 0. 
    IF cl-list.yroom EQ 0 THEN cl-list.ypax = 0. 
    IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
    IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom. 
    IF droom NE 0 THEN cl-list.proz1 = 100.0 * cl-list.droom / droom. 
    IF mroom NE 0 THEN cl-list.proz2 = 100.0 * cl-list.mroom / mroom.
    IF yroom NE 0 THEN cl-list.proz3 = 100.0 * cl-list.yroom / yroom.


    /*     IF cl-list.dpax NE 0 THEN cl-list.proz2 = 100.0 * cl-list.dpax / dgpax.
 ragung comment   IF mroom NE 0 THEN cl-list.proz2 = 100.0 * cl-list.mroom / mroom.  */
    IF droom NE 0 THEN drate = drev / droom. 
    IF mroom NE 0 THEN mrate = mrev / mroom. 

    
    IF show-ytd THEN
    DO:
        IF cl-list.yroom NE 0 THEN cl-list.yrate = cl-list.yrev / cl-list.yroom. 
        IF yroom NE 0 THEN cl-list.proz3 = 100.0 * cl-list.yroom / yroom. 
        IF yroom NE 0 THEN yrate = yrev / yroom. 
    END.

        IF grp-flag AND NOT cl-list.grpflag THEN DO:
            IF cl-list.segm-grup NE curr-grup AND curr-grup NE 0 THEN DO:
                /*CREATE rm-statistic-list1.*/
    
                CREATE rm-statistic-list1.
                ASSIGN
                    rm-statistic-list1.segm    = ""
                    rm-statistic-list1.bezeich = "T O T A L"
                    rm-statistic-list1.droom   = STRING(tot-droom, ">>,>>9")                 
                    rm-statistic-list1.proz1   = STRING(tot-proz1, ">>9.99")              
                    rm-statistic-list1.mroom   = STRING(tot-mroom, ">>,>>9")               
                    rm-statistic-list1.proz2   = STRING(tot-proz2, ">>9.99")              
                    rm-statistic-list1.yroom   = STRING(tot-yroom, ">>,>>9")              
                    rm-statistic-list1.proz3   = STRING(tot-proz3, ">>9.99")              
                    rm-statistic-list1.dpax    = STRING(tot-dpax, ">>,>>9")                  
                    rm-statistic-list1.mpax    = STRING(tot-mpax, ">>,>>9")               
                    rm-statistic-list1.ypax    = STRING(tot-ypax, ">>,>>9")               
                    rm-statistic-list1.drate   = STRING(tot-drate, "->>>,>>>,>>>,>>9.99")     
                    rm-statistic-list1.mrate   = STRING(tot-mrate, "->>>,>>>,>>>,>>9.99")     
                    rm-statistic-list1.yrate   = STRING(tot-yrate, "->>>,>>>,>>>,>>9.99")     
                    rm-statistic-list1.drev    = STRING(tot-drev, "->>>,>>>,>>>,>>9.99")   
                    rm-statistic-list1.mrev    = STRING(tot-mrev, "->>>,>>>,>>>,>>9.99")  
                    rm-statistic-list1.yrev    = STRING(tot-yrev, "->>>,>>>,>>>,>>9.99")
                .                
    
                CREATE rm-statistic-list1.
    
                ASSIGN tot-droom = 0 
                       tot-proz1 = 0
                       tot-mroom = 0 
                       tot-proz2 = 0 
                       tot-yroom = 0 
                       tot-proz3 = 0 
                       tot-dpax  = 0 
                       tot-mpax  = 0 
                       tot-ypax  = 0 
                       tot-drate = 0 
                       tot-mrate = 0  
                       tot-yrate = 0  
                       tot-drev  = 0  
                       tot-mrev  = 0 
                       tot-yrev  = 0
                       tot-droom = tot-droom + cl-list.droom 
                       tot-proz1 = tot-proz1 + cl-list.proz1
                       tot-mroom = tot-mroom + cl-list.mroom 
                       tot-proz2 = tot-proz2 + cl-list.proz2
                       tot-yroom = tot-yroom + cl-list.yroom 
                       tot-proz3 = tot-proz3 + cl-list.proz3
                       tot-dpax  = tot-dpax  + cl-list.dpax 
                       tot-mpax  = tot-mpax  + cl-list.mpax 
                       tot-ypax  = tot-ypax  + cl-list.ypax
                       tot-drate = tot-drate + cl-list.drate 
                       tot-mrate = tot-mrate + cl-list.mrate
                       tot-yrate = tot-yrate + cl-list.yrate  
                       tot-drev  = tot-drev  + cl-list.drev  
                       tot-mrev  = tot-mrev  + cl-list.mrev
                       tot-yrev  = tot-yrev  + cl-list.yrev.
            END.
            ELSE DO:
                ASSIGN tot-droom = tot-droom + cl-list.droom 
                       tot-proz1 = tot-proz1 + cl-list.proz1
                       tot-mroom = tot-mroom + cl-list.mroom 
                       tot-proz2 = tot-proz2 + cl-list.proz2
                       tot-yroom = tot-yroom + cl-list.yroom 
                       tot-proz3 = tot-proz3 + cl-list.proz3
                       tot-dpax  = tot-dpax  + cl-list.dpax 
                       tot-mpax  = tot-mpax  + cl-list.mpax 
                       tot-ypax  = tot-ypax  + cl-list.ypax
                       tot-drate = tot-drate + cl-list.drate 
                       tot-mrate = tot-mrate + cl-list.mrate
                       tot-yrate = tot-yrate + cl-list.yrate  
                       tot-drev  = tot-drev  + cl-list.drev  
                       tot-mrev  = tot-mrev  + cl-list.mrev
                       tot-yrev  = tot-yrev  + cl-list.yrev.
    
            END.
            ASSIGN curr-grup = cl-list.segm-grup.
        END.        

        CREATE rm-statistic-list1.
        IF long-digit THEN 
        DO:
            ASSIGN
                rm-statistic-list1.segm    = STRING(cl-list.segm, ">>>")                                      
                rm-statistic-list1.bezeich = cl-list.bezeich                          
                rm-statistic-list1.droom   = STRING(cl-list.droom, ">>,>>9")             
                rm-statistic-list1.proz1   = STRING(cl-list.proz1, ">>9.99")             
                rm-statistic-list1.mroom   = STRING(cl-list.mroom, ">>,>>9")             
                rm-statistic-list1.proz2   = STRING(cl-list.proz2, ">>9.99")             
                rm-statistic-list1.yroom   = STRING(cl-list.yroom, ">>,>>9")             
                rm-statistic-list1.proz3   = STRING(cl-list.proz3, ">>9.99")             
                rm-statistic-list1.dpax    = STRING(cl-list.dpax, ">>,>>9")              
                rm-statistic-list1.mpax    = STRING(cl-list.mpax, ">>,>>9")              
                rm-statistic-list1.ypax    = STRING(cl-list.ypax, ">>,>>9")              
                rm-statistic-list1.drate   = STRING(cl-list.drate, "->>,>>>,>>>,>>>,>>9")
                rm-statistic-list1.mrate   = STRING(cl-list.mrate, "->>,>>>,>>>,>>>,>>9")
                rm-statistic-list1.yrate   = STRING(cl-list.yrate, "->>,>>>,>>>,>>>,>>9")
                rm-statistic-list1.drev    = STRING(cl-list.drev, "->>,>>>,>>>,>>>,>>9") 
                rm-statistic-list1.mrev    = STRING(cl-list.mrev, "->>,>>>,>>>,>>>,>>9") 
                rm-statistic-list1.yrev    = STRING(cl-list.yrev, "->>,>>>,>>>,>>>,>>9") 
            .
        END.
        ELSE
        DO:
            ASSIGN
                rm-statistic-list1.segm    = STRING(cl-list.segm, ">>>")                                      
                rm-statistic-list1.bezeich = cl-list.bezeich                          
                rm-statistic-list1.droom   = STRING(cl-list.droom, ">>,>>9")             
                rm-statistic-list1.proz1   = STRING(cl-list.proz1, ">>9.99")             
                rm-statistic-list1.mroom   = STRING(cl-list.mroom, ">>,>>9")             
                rm-statistic-list1.proz2   = STRING(cl-list.proz2, ">>9.99")             
                rm-statistic-list1.yroom   = STRING(cl-list.yroom, ">>,>>9")             
                rm-statistic-list1.proz3   = STRING(cl-list.proz3, ">>9.99")             
                rm-statistic-list1.dpax    = STRING(cl-list.dpax, ">>,>>9")              
                rm-statistic-list1.mpax    = STRING(cl-list.mpax, ">>,>>9")              
                rm-statistic-list1.ypax    = STRING(cl-list.ypax, ">>,>>9")              
                rm-statistic-list1.drate   = STRING(cl-list.drate, "->>>,>>>,>>>,>>9.99")
                rm-statistic-list1.mrate   = STRING(cl-list.mrate, "->>>,>>>,>>>,>>9.99")
                rm-statistic-list1.yrate   = STRING(cl-list.yrate, "->>>,>>>,>>>,>>9.99")
                rm-statistic-list1.drev    = STRING(cl-list.drev, "->>>,>>>,>>>,>>9.99") 
                rm-statistic-list1.mrev    = STRING(cl-list.mrev, "->>>,>>>,>>>,>>9.99") 
                rm-statistic-list1.yrev    = STRING(cl-list.yrev, "->>>,>>>,>>>,>>9.99") 
            .
        END.        

        /*IF grp-flag AND NOT cl-list.grpflag THEN
        DO: 
            create output-list1. 
            output-list1.str1 = "   ". 
            DO i = 1 TO 102: 
              output-list1.str1 = output-list1.str1 + "----". 
            END.

                CREATE output-list1.
                ASSIGN
                output-list1.str1 = STRING("", "x(3)") 
                      + STRING("T O T A L", "x(16)") 
                      + STRING(cl-list.droom, ">>9") 
                      + STRING(cl-list.proz1, ">>9.99") 
                      + STRING(cl-list.mroom, ">,>>9") 
                      + STRING(cl-list.proz2, ">>9.99") 
                      + STRING(cl-list.yroom, ">>,>>9") 
                      + STRING(cl-list.proz3, ">>9.99") 
                      + STRING(cl-list.dpax, ">>9") 
                      + STRING(cl-list.mpax, ">>,>>9") 
                      + STRING(cl-list.ypax, ">>,>>9") 
                      + STRING(cl-list.drate, "->>>,>>>,>>9.99") 
                      + STRING(cl-list.mrate, "->>>,>>>,>>9.99") 
                      + STRING(cl-list.yrate, "->>>,>>>,>>9.99") 
                      + STRING(cl-list.drev, "->>,>>>,>>>,>>9.99") 
                      + STRING(cl-list.mrev, "->>>,>>>,>>>,>>9.99")
                      + STRING(cl-list.yrev, "->>>,>>>,>>>,>>9.99"). 
                CREATE output-list1.
        END.*/

        IF show-other THEN
        DO:
            FIND FIRST other-list WHERE other-list.segm = cl-list.segm NO-LOCK NO-ERROR.
            IF AVAILABLE other-list THEN
            DO:
                ASSIGN
                    ttrev  = cl-list.drev + other-list.orev
                    ttmrev = cl-list.mrev + other-list.morev
                    ttyrev = cl-list.yrev + other-list.yorev.

                CREATE rm-statistic-list1.                
                IF long-digit THEN
                DO:
                    ASSIGN 
                        rm-statistic-list1.flag     = "Orev"
                        rm-statistic-list1.bezeich  = translateExtended("Other Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(other-list.orev, "->>,>>>,>>>,>>>,>>9")  
                        rm-statistic-list1.mrev     = STRING(other-list.morev, "->>,>>>,>>>,>>>,>>9")
                        rm-statistic-list1.yrev     = STRING(other-list.yorev, "->>,>>>,>>>,>>>,>>9")
                    .
                END.                                            
                ELSE
                DO:
                    ASSIGN 
                        rm-statistic-list1.flag     = "Orev"
                        rm-statistic-list1.bezeich  = translateExtended("Other Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(other-list.orev, "->>>,>>>,>>>,>>9.99")  
                        rm-statistic-list1.mrev     = STRING(other-list.morev, "->>>,>>>,>>>,>>9.99")
                        rm-statistic-list1.yrev     = STRING(other-list.yorev, "->>>,>>>,>>>,>>9.99")
                    .
                END.
                                 
                CREATE rm-statistic-list1.
                IF long-digit THEN
                DO:
                    ASSIGN
                        rm-statistic-list1.flag     = "Trev"
                        rm-statistic-list1.bezeich  = translateExtended("Total Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(ttrev, "->>,>>>,>>>,>>>,>>9")  
                        rm-statistic-list1.mrev     = STRING(ttmrev, "->>,>>>,>>>,>>>,>>9")
                        rm-statistic-list1.yrev     = STRING(ttyrev, "->>,>>>,>>>,>>>,>>9")
                    .
                END.
                ELSE
                DO:
                    ASSIGN 
                        rm-statistic-list1.flag     = "Trev"
                        rm-statistic-list1.bezeich  = translateExtended("Total Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(ttrev, "->>>,>>>,>>>,>>9.99")  
                        rm-statistic-list1.mrev     = STRING(ttmrev, "->>>,>>>,>>>,>>9.99")
                        rm-statistic-list1.yrev     = STRING(ttyrev, "->>>,>>>,>>>,>>9.99")
                    .
                END.                   
                CREATE rm-statistic-list1.
            END.
        END.
  END. 


  IF grp-flag THEN 
  DO:    
    CREATE rm-statistic-list1.
    ASSIGN
        rm-statistic-list1.segm    = ""                                      
        rm-statistic-list1.bezeich = "T O T A L"                             
        rm-statistic-list1.droom   = STRING(tot-droom, ">>,>>9")             
        rm-statistic-list1.proz1   = STRING(tot-proz1, ">>9.99")             
        rm-statistic-list1.mroom   = STRING(tot-mroom, ">>,>>9")             
        rm-statistic-list1.proz2   = STRING(tot-proz2, ">>9.99")             
        rm-statistic-list1.yroom   = STRING(tot-yroom, ">>,>>9")             
        rm-statistic-list1.proz3   = STRING(tot-proz3, ">>9.99")             
        rm-statistic-list1.dpax    = STRING(tot-dpax, ">>,>>9")              
        rm-statistic-list1.mpax    = STRING(tot-mpax, ">>,>>9")              
        rm-statistic-list1.ypax    = STRING(tot-ypax, ">>,>>9")              
        rm-statistic-list1.drate   = STRING(tot-drate, "->>>,>>>,>>>,>>9.99")
        rm-statistic-list1.mrate   = STRING(tot-mrate, "->>>,>>>,>>>,>>9.99")
        rm-statistic-list1.yrate   = STRING(tot-yrate, "->>>,>>>,>>>,>>9.99")
        rm-statistic-list1.drev    = STRING(tot-drev, "->>>,>>>,>>>,>>9.99") 
        rm-statistic-list1.mrev    = STRING(tot-mrev, "->>>,>>>,>>>,>>9.99") 
        rm-statistic-list1.yrev    = STRING(tot-yrev, "->>>,>>>,>>>,>>9.99") 
    .    

    CREATE rm-statistic-list1.
  END.
  
  IF NOT show-ytd THEN
  DO:     
      CREATE rm-statistic-list.
      IF long-digit THEN 
      DO:
          ASSIGN
              rm-statistic-list.segm      = ""
              rm-statistic-list.bezeich   = translateExtended("Total Revenue Room", lvCAREA, "")
              rm-statistic-list.dgroom    = STRING(dgroom, ">>,>>9")  
              rm-statistic-list.proz1     = STRING(100, ">>9.99")  
              rm-statistic-list.mgroom    = STRING(mgroom, ">>,>>9")
              rm-statistic-list.proz2     = STRING(100, ">>9.99")  
              rm-statistic-list.dgpax     = STRING(dgpax, ">>,>>9")                
              rm-statistic-list.mgpax     = STRING(mgpax, ">>,>>9")             
              rm-statistic-list.dgrate    = STRING(dgrate, "->>,>>>,>>>,>>>,>>9")   
              rm-statistic-list.mgrate    = STRING(mgrate, "->>,>>>,>>>,>>>,>>9")   
              rm-statistic-list.dgrev     = STRING(dgrev, "->>,>>>,>>>,>>>,>>9") 
              rm-statistic-list.mgrev     = STRING(mgrev, "->>,>>>,>>>,>>>,>>9")
          .
      END.
      ELSE
      DO:
          ASSIGN
              rm-statistic-list.segm      = ""
              rm-statistic-list.bezeich   = translateExtended("Total Revenue Room", lvCAREA, "")
              rm-statistic-list.dgroom    = STRING(dgroom, ">>,>>9")  
              rm-statistic-list.proz1     = STRING(100, ">>9.99")  
              rm-statistic-list.mgroom    = STRING(mgroom, ">>,>>9")
              rm-statistic-list.proz2     = STRING(100, ">>9.99")  
              rm-statistic-list.dgpax     = STRING(dgpax, ">>,>>9")                
              rm-statistic-list.mgpax     = STRING(mgpax, ">>,>>9")             
              rm-statistic-list.dgrate    = STRING(dgrate, "->>>,>>>,>>>,>>9.99")   
              rm-statistic-list.mgrate    = STRING(mgrate, "->>>,>>>,>>>,>>9.99")   
              rm-statistic-list.dgrev     = STRING(dgrev, "->>>,>>>,>>>,>>9.99") 
              rm-statistic-list.mgrev     = STRING(mgrev, "->>>,>>>,>>>,>>9.99")
          .  
      END.      
  END.
  ELSE
  DO:
      CREATE rm-statistic-list1. 
      
      CREATE rm-statistic-list1.
      IF long-digit THEN
      DO:
          ASSIGN
              rm-statistic-list1.segm      = ""                                                  
              rm-statistic-list1.bezeich   = translateExtended("Total Revenue Room", lvCAREA, "")
              rm-statistic-list1.droom     = STRING(dgroom, ">>,>>9")                            
              rm-statistic-list1.proz1     = STRING(100, ">>9.99")                               
              rm-statistic-list1.mroom     = STRING(mgroom, ">>,>>9")                            
              rm-statistic-list1.proz2     = STRING(100, ">>9.99")
              rm-statistic-list1.yroom     = STRING(ygroom, ">>,>>9")                            
              rm-statistic-list1.proz3     = STRING(100, ">>9.99")
              rm-statistic-list1.dpax      = STRING(dgpax, ">>,>>9")                             
              rm-statistic-list1.mpax      = STRING(mgpax, ">>,>>9") 
              rm-statistic-list1.ypax      = STRING(ygpax, ">>>,>>9") /* Malik 194324 : ">>,>>9" -> ">>>,>>9" */
              rm-statistic-list1.drate     = STRING(dgrate, "->>,>>>,>>>,>>>,>>9")               
              rm-statistic-list1.mrate     = STRING(mgrate, "->>,>>>,>>>,>>>,>>9")
              rm-statistic-list1.yrate     = STRING(ygrate, "->>,>>>,>>>,>>>,>>9")
              rm-statistic-list1.drev      = STRING(dgrev, "->>,>>>,>>>,>>>,>>9")                
              rm-statistic-list1.mrev      = STRING(mgrev, "->>,>>>,>>>,>>>,>>9")                
              rm-statistic-list1.yrev      = STRING(ygrev, "->>,>>>,>>>,>>>,>>9")
          .
      END.
      ELSE
      DO:
          ASSIGN
              rm-statistic-list1.segm      = ""                                                  
              rm-statistic-list1.bezeich   = translateExtended("Total Revenue Room", lvCAREA, "")
              rm-statistic-list1.droom     = STRING(dgroom, ">>,>>9")                            
              rm-statistic-list1.proz1     = STRING(100, ">>9.99")                               
              rm-statistic-list1.mroom     = STRING(mgroom, ">>,>>9")                            
              rm-statistic-list1.proz2     = STRING(100, ">>9.99")
              rm-statistic-list1.yroom     = STRING(ygroom, ">>,>>9")                            
              rm-statistic-list1.proz3     = STRING(100, ">>9.99")
              rm-statistic-list1.dpax      = STRING(dgpax, ">>,>>9")                             
              rm-statistic-list1.mpax      = STRING(mgpax, ">>,>>9") 
              rm-statistic-list1.ypax      = STRING(ygpax, ">>>,>>9") /* Malik 194324 : ">>,>>9" -> ">>>,>>9" */
              rm-statistic-list1.drate     = STRING(dgrate, "->>>,>>>,>>>,>>9.99")               
              rm-statistic-list1.mrate     = STRING(mgrate, "->>>,>>>,>>>,>>9.99")
              rm-statistic-list1.yrate     = STRING(ygrate, "->>>,>>>,>>>,>>9.99")
              rm-statistic-list1.drev      = STRING(dgrev, "->>>,>>>,>>>,>>9.99")                
              rm-statistic-list1.mrev      = STRING(mgrev, "->>>,>>>,>>>,>>9.99")                
              rm-statistic-list1.yrev      = STRING(ygrev, "->>>,>>>,>>>,>>9.99")
          .
      END.      
  END.


  FIND FIRST cl-list WHERE cl-list.flag-comp NO-ERROR.
  IF AVAILABLE cl-list THEN
  DO:
      CREATE rm-statistic-list1. 
      CREATE rm-statistic-list1. 
      CREATE rm-statistic-list1. 
      rm-statistic-list1.bezeich = translateExtended("Compliment Rooms", lvCAREA, ""). 
         
      FOR EACH cl-list WHERE cl-list.flag-comp:
          CREATE rm-statistic-list1. 
          /*output-list1.segNo = cl-list.segm.*/
          ASSIGN
              rm-statistic-list1.segm      = STRING(cl-list.segm,">>9")                                                  
              rm-statistic-list1.bezeich   = cl-list.bezeich
              rm-statistic-list1.droom     = STRING(cl-list.droom, ">>,>>9")                               
              rm-statistic-list1.proz1     = ""                                         
              rm-statistic-list1.mroom     = STRING(cl-list.mroom, ">>,>>9")                             
              rm-statistic-list1.proz2     = ""                                         
              rm-statistic-list1.yroom     = STRING(cl-list.yroom, ">>,>>9")                            
              rm-statistic-list1.proz3     = ""                                         
              rm-statistic-list1.dpax      = STRING(cl-list.dpax, ">>,>>9")                                
              rm-statistic-list1.mpax      = STRING(cl-list.mpax, ">>,>>9")                             
              rm-statistic-list1.ypax      = STRING(cl-list.ypax, ">>,>>9").                            
          .            
      END.
  END.
END PROCEDURE.

PROCEDURE create-umsatz:
    DEFINE VARIABLE black-list AS INTEGER. 
    DEFINE VARIABLE fl-comp AS LOGICAL INIT NO.
    DEFINE VARIABLE dgroom AS INT INIT 0.
    DEFINE VAR i AS INT INIT 0.

    FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
    black-list = htparam.finteger. 

    FOR EACH rm-statistic-list: 
      DELETE rm-statistic-list. 
    END. 

    FOR EACH rm-statistic-list1:
      DELETE rm-statistic-list1.
    END.

    FOR EACH cl-list: 
      DELETE cl-list. 
    END. 

    FOR EACH s-list: 
      DELETE s-list. 
    END. 

    ASSIGN droom    = 0
           mroom    = 0 
           yroom    = 0 
           dpax     = 0 
           mpax     = 0 
           ypax     = 0 
           drate    = 0 
           mrate    = 0 
           yrate    = 0 
           drev     = 0 
           mrev     = 0 
           yrev     = 0 
           dgroom   = 0 
           mgroom   = 0 
           ygroom   = 0 
           dgpax    = 0 
           mgpax    = 0 
           ygpax    = 0 
           dgrate   = 0 
           mgrate   = 0 
           ygrate   = 0 
           dgrev    = 0 
           mgrev    = 0 
           ygrev    = 0
           tot-droom = 0 
           tot-proz1 = 0
           tot-mroom = 0 
           tot-proz2 = 0 
           tot-yroom = 0 
           tot-proz3 = 0 
           tot-dpax  = 0 
           tot-mpax  = 0 
           tot-ypax  = 0 
           tot-drate = 0 
           tot-mrate = 0  
           tot-yrate = 0  
           tot-drev  = 0  
           tot-mrev  = 0 
           tot-yrev  = 0. 

    DEFINE VAR flag-temp AS LOGICAL INIT NO.
   
    from-date = DATE(month(to-date), 1, year(to-date)). 

    IF show-other THEN RUN create-other.

    FOR EACH genstat WHERE 
        genstat.datum GE from-date 
        AND genstat.datum LE to-date 
        AND genstat.segmentcode NE 0
        AND genstat.nationnr NE 0
        NO-LOCK USE-INDEX gastnrmember_ix, 
        FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode
        AND segment.segmentcode NE black-list AND segment.segmentgrup LE 99:
        IF genstat.zipreis EQ 0 AND genstat.resstatus EQ 6 AND genstat.gratis NE 0 THEN 
            fl-comp = YES.    /*compliment*/
        ELSE fl-comp = NO.
        
        DO:
            FIND FIRST cl-list WHERE cl-list.segm EQ genstat.segmentcode
                AND cl-list.flag-comp EQ fl-comp NO-ERROR.
            IF NOT AVAILABLE cl-list THEN
            DO:
                CREATE cl-list.
                ASSIGN cl-list.segm      = genstat.segmentcode          /*SNo*/
                       cl-list.bezeich   = segment.bezeich            /*Guest Segment*/
                       cl-list.flag-comp = fl-comp
                       cl-list.segm-grup = segment.segmentgrup.
    
                IF genstat.zipreis EQ 0 AND genstat.resstatus EQ 6 
                    AND genstat.gratis NE 0 THEN     /*compliment*/
                DO:
                    IF genstat.datum = to-date THEN
                    DO:
                        ASSIGN cl-list.droom = 1                                   /*#Rm*/
                               cl-list.dpax = cl-list.dpax + genstat.gratis
                               /*dgroom = dgroom + 1.*/
                               droom = droom + 1. /*MT 060912 */
                    END.
                    IF MONTH(genstat.datum) = MONTH(to-date) THEN
                    DO:
                        ASSIGN cl-list.mroom = 1        /*Pax*/
                               cl-list.mpax = cl-list.mpax + genstat.gratis
                               mroom = mroom + 1. /*MT 060912 */
                                    /*mgroom = mgroom + 1.*/
                    END.
                END.
                ELSE IF genstat.resstatus NE 13 THEN                /*paying awal*/
                DO:
                    IF genstat.datum = to-date THEN
                    DO: 
                        ASSIGN cl-list.drev = genstat.logis                    /*Room-Revenue*/
                               cl-list.droom = cl-list.droom + 1                                   /*#Rm*/
                               cl-list.dpax = cl-list.dpax + genstat.erwachs 
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3        /*Pax*/
                               dgroom = dgroom + 1        /*total #Rm*/
                               dgpax = dgpax + genstat.erwachs 
                                     + genstat.kind1 + genstat.kind2 + genstat.kind3
                               dgrev = dgrev + genstat.logis          /*Total Room-Revenue*/
                               cl-list.drate = cl-list.drate + (cl-list.drev / cl-list.droom)
                               dgrate = dgrev / dgroom
                               droom = droom + 1. /*MT 060912 */
                    END.
                    IF MONTH(genstat.datum) = MONTH(to-date) THEN
                    DO:
                        ASSIGN cl-list.mrev = genstat.logis
                               cl-list.mroom = cl-list.mroom + 1             /*MTD pertama*/
                               cl-list.mpax = cl-list.mpax + genstat.erwachs 
                                            + genstat.kind1 + genstat.kind2 + genstat.kind3
                               mgroom = mgroom + 1      /*total MTD pertama*/
                               mgpax = mgpax + genstat.erwachs + genstat.kind1 
                                     + genstat.kind2 + genstat.kind3
                               mgrev = mgrev + genstat.logis
                               cl-list.mrate = cl-list.mrate + (cl-list.mrev / cl-list.mroom)
                               mgrate = mgrev / mgroom
                               mroom = mroom + 1. /*MT 060912 */
                    END.
                END.
            END.
            ELSE
            DO:
                IF genstat.zipreis EQ 0 AND genstat.resstatus EQ 6
                    AND genstat.gratis NE 0 THEN     /*compliment*/
                DO:
                    IF genstat.datum = to-date THEN 
                    DO:
                        UPDATE cl-list.droom = cl-list.droom + 1
                               cl-list.dpax = cl-list.dpax +  genstat.gratis
                               droom = droom + 1. /*MT 060912 */
                    END.
    
                    IF MONTH(genstat.datum) = MONTH(to-date) THEN
                    DO:
                        UPDATE cl-list.mroom = cl-list.mroom + 1
                               cl-list.mpax = cl-list.mpax +  genstat.gratis
                               mroom = mroom + 1. /*MT 060912 */
                    END.
                END.
                ELSE IF genstat.resstatus NE 13 THEN
                DO:
                    IF genstat.datum = to-date THEN
                    DO: 
                            ASSIGN cl-list.drev = cl-list.drev + genstat.logis                    /*Room-Revenue*/
                                   cl-list.droom = cl-list.droom + 1                                   /*#Rm*/
                                   cl-list.dpax = cl-list.dpax + genstat.erwachs 
                                                + genstat.kind1 + genstat.kind2 + genstat.kind3        /*Pax*/
                                   dgroom = dgroom + 1        /*total #Rm*/
                                   dgpax = dgpax + genstat.erwachs 
                                         + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   dgrev = dgrev + genstat.logis          /*Total Room-Revenue*/
                                   cl-list.drate = cl-list.drev / cl-list.droom
                                   dgrate = dgrev / dgroom
                                   droom = droom + 1. /*MT 060912 */
                        END.
                       
                        IF MONTH(genstat.datum) = MONTH(to-date) THEN
                        DO:
                            ASSIGN cl-list.mroom =  cl-list.mroom + 1             /*MTD pertama*/
                                   cl-list.mpax = cl-list.mpax + genstat.erwachs + genstat.kind1 
                                                + genstat.kind2 + genstat.kind3
                                   cl-list.mrev = cl-list.mrev + genstat.logis
                                   mgroom = mgroom + 1      /*total MTD pertama*/
                                   mgpax = mgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                                   mgrev = mgrev + genstat.logis
                                   cl-list.mrate = cl-list.mrev / cl-list.mroom
                                   mgrate = mgrev / mgroom
                                   mroom = mroom + 1. /*MT 060912 */
                        END.
                END.
            END.

        END.
    END.
   
  FOR EACH cl-list WHERE NOT flag-comp BY cl-list.segm-grup : 

    IF cl-list.droom EQ 0 THEN cl-list.dpax = 0. 
    IF cl-list.mroom EQ 0 THEN cl-list.mpax = 0. 
    IF cl-list.yroom EQ 0 THEN cl-list.ypax = 0. 
    IF cl-list.droom NE 0 THEN cl-list.drate = cl-list.drev / cl-list.droom. 
    IF cl-list.mroom NE 0 THEN cl-list.mrate = cl-list.mrev / cl-list.mroom.
    IF droom NE 0 THEN cl-list.proz1 = 100.0 * cl-list.droom / dgroom. 
    IF mroom NE 0 THEN cl-list.proz2 = 100.0 * cl-list.mroom / mgroom.

    /*     IF cl-list.dpax NE 0 THEN cl-list.proz2 = 100.0 * cl-list.dpax / dgpax.
 ragung comment IF mroom NE 0 THEN cl-list.proz2 = 100.0 * cl-list.mroom / mroom.  */
    IF droom NE 0 THEN drate = drev / droom. 
    IF mroom NE 0 THEN mrate = mrev / mroom.
    

    IF NOT show-ytd THEN
    DO: 
        IF grp-flag AND NOT cl-list.grpflag THEN DO:    
            IF cl-list.segm-grup NE curr-grup AND curr-grup NE 0 THEN DO:
                /*CREATE rm-statistic-list.*/

                CREATE rm-statistic-list.
                ASSIGN
                    rm-statistic-list.segm      = ""
                    rm-statistic-list.bezeich   = translateExtended("T O T A L", lvCAREA, "")
                    rm-statistic-list.dgroom    = STRING(tot-droom, ">>,>>9")               
                    rm-statistic-list.proz1     = STRING(tot-proz1, ">>9.99")            
                    rm-statistic-list.mgroom    = STRING(tot-mroom, ">>,>>9")             
                    rm-statistic-list.proz2     = STRING(tot-proz2, ">>9.99")            
                    rm-statistic-list.dgpax     = STRING(tot-dpax, ">>,>>9")                
                    rm-statistic-list.mgpax     = STRING(tot-mpax, ">>,>>9")             
                    rm-statistic-list.dgrate    = STRING(tot-drate, "->>>,>>>,>>>,>>9.99")   
                    rm-statistic-list.mgrate    = STRING(tot-mrate, "->>>,>>>,>>>,>>9.99")   
                    rm-statistic-list.dgrev     = STRING(tot-drev, "->>>,>>>,>>>,>>9.99") 
                    rm-statistic-list.mgrev     = STRING(tot-mrev, "->>>,>>>,>>>,>>9.99")
                .                

                CREATE rm-statistic-list.

                ASSIGN tot-droom = 0 
                       tot-proz1 = 0
                       tot-mroom = 0 
                       tot-proz2 = 0 
                       tot-yroom = 0 
                       tot-proz3 = 0 
                       tot-dpax  = 0 
                       tot-mpax  = 0 
                       tot-ypax  = 0 
                       tot-drate = 0 
                       tot-mrate = 0  
                       tot-yrate = 0  
                       tot-drev  = 0  
                       tot-mrev  = 0 
                       tot-yrev  = 0
                       tot-droom = tot-droom + cl-list.droom 
                       tot-proz1 = tot-proz1 + cl-list.proz1
                       tot-mroom = tot-mroom + cl-list.mroom 
                       tot-proz2 = tot-proz2 + cl-list.proz2
                       tot-yroom = tot-yroom + cl-list.yroom 
                       tot-proz3 = tot-proz3 + cl-list.proz3
                       tot-dpax  = tot-dpax  + cl-list.dpax 
                       tot-mpax  = tot-mpax  + cl-list.mpax 
                       tot-ypax  = tot-ypax  + cl-list.ypax
                       tot-drate = tot-drate + cl-list.drate 
                       tot-mrate = tot-mrate + cl-list.mrate
                       tot-yrate = tot-yrate + cl-list.yrate  
                       tot-drev  = tot-drev  + cl-list.drev  
                       tot-mrev  = tot-mrev  + cl-list.mrev
                       tot-yrev  = tot-yrev  + cl-list.yrev.
            END.
            ELSE DO:
                ASSIGN tot-droom = tot-droom + cl-list.droom 
                       tot-proz1 = tot-proz1 + cl-list.proz1
                       tot-mroom = tot-mroom + cl-list.mroom 
                       tot-proz2 = tot-proz2 + cl-list.proz2
                       tot-yroom = tot-yroom + cl-list.yroom 
                       tot-proz3 = tot-proz3 + cl-list.proz3
                       tot-dpax  = tot-dpax  + cl-list.dpax 
                       tot-mpax  = tot-mpax  + cl-list.mpax 
                       tot-ypax  = tot-ypax  + cl-list.ypax
                       tot-drate = tot-drate + cl-list.drate 
                       tot-mrate = tot-mrate + cl-list.mrate
                       tot-yrate = tot-yrate + cl-list.yrate  
                       tot-drev  = tot-drev  + cl-list.drev  
                       tot-mrev  = tot-mrev  + cl-list.mrev
                       tot-yrev  = tot-yrev  + cl-list.yrev.

            END.
            ASSIGN curr-grup = cl-list.segm-grup.
        END.
            
        CREATE rm-statistic-list.               
        IF long-digit THEN 
        DO:
            ASSIGN
                rm-statistic-list.segm      = STRING(cl-list.segm, ">>>")
                rm-statistic-list.bezeich   = cl-list.bezeich          
                rm-statistic-list.dgroom    = STRING(cl-list.droom, ">>,>>9")               
                rm-statistic-list.proz1     = STRING(cl-list.proz1, ">>9.99")            
                rm-statistic-list.mgroom    = STRING(cl-list.mroom, ">>,>>9")             
                rm-statistic-list.proz2     = STRING(cl-list.proz2, ">>9.99")            
                rm-statistic-list.dgpax     = STRING(cl-list.dpax, ">>,>>9")                
                rm-statistic-list.mgpax     = STRING(cl-list.mpax, ">>,>>9")             
                rm-statistic-list.dgrate    = STRING(cl-list.drate, "->>,>>>,>>>,>>>,>>9")   
                rm-statistic-list.mgrate    = STRING(cl-list.mrate, "->>,>>>,>>>,>>>,>>9")   
                rm-statistic-list.dgrev     = STRING(cl-list.drev, "->>,>>>,>>>,>>>,>>9") 
                rm-statistic-list.mgrev     = STRING(cl-list.mrev, "->>,>>>,>>>,>>>,>>9")
            .
        END.
        ELSE
        DO:
            ASSIGN
                rm-statistic-list.segm      = STRING(cl-list.segm, ">>>")
                rm-statistic-list.bezeich   = cl-list.bezeich          
                rm-statistic-list.dgroom    = STRING(cl-list.droom, ">>,>>9")               
                rm-statistic-list.proz1     = STRING(cl-list.proz1, ">>9.99")            
                rm-statistic-list.mgroom    = STRING(cl-list.mroom, ">>,>>9")             
                rm-statistic-list.proz2     = STRING(cl-list.proz2, ">>9.99")            
                rm-statistic-list.dgpax     = STRING(cl-list.dpax, ">>,>>9")                
                rm-statistic-list.mgpax     = STRING(cl-list.mpax, ">>,>>9")             
                rm-statistic-list.dgrate    = STRING(cl-list.drate, "->>>,>>>,>>>,>>9.99")   
                rm-statistic-list.mgrate    = STRING(cl-list.mrate, "->>>,>>>,>>>,>>9.99")   
                rm-statistic-list.dgrev     = STRING(cl-list.drev, "->>>,>>>,>>>,>>9.99") 
                rm-statistic-list.mgrev     = STRING(cl-list.mrev, "->>>,>>>,>>>,>>9.99")
            .
        END.            
        IF cl-list.grpflag THEN CREATE rm-statistic-list. 
    END.
    ELSE
    DO:
        IF grp-flag AND NOT cl-list.grpflag THEN
        DO: 
            IF cl-list.segm-grup NE curr-grup AND curr-grup NE 0 THEN DO:                
    
                CREATE rm-statistic-list.
                ASSIGN                        
                    rm-statistic-list.segm     = ""
                    rm-statistic-list.bezeich  = translateExtended("T O T A L", lvCAREA, "")
                    rm-statistic-list.dgroom   = STRING(tot-droom, ">>,>>9")               
                    rm-statistic-list.proz1    = STRING(tot-proz1, ">>9.99")            
                    rm-statistic-list.mgroom   = STRING(tot-mroom, ">>,>>9")             
                    rm-statistic-list.proz2    = STRING(tot-proz2, ">>9.99")            
                    rm-statistic-list.ygroom   = STRING(tot-yroom, ">>,>>9")            
                    rm-statistic-list.proz3    = STRING(tot-proz3, ">>9.99")            
                    rm-statistic-list.dgpax    = STRING(tot-dpax, ">>,>>9")                
                    rm-statistic-list.mgpax    = STRING(tot-mpax, ">>,>>9")             
                    rm-statistic-list.ygpax    = STRING(tot-ypax, ">>,>>9")             
                    rm-statistic-list.dgrate   = STRING(tot-drate, "->>>,>>>,>>>,>>9.99")   
                    rm-statistic-list.mgrate   = STRING(tot-mrate, "->>>,>>>,>>>,>>9.99")   
                    rm-statistic-list.ygrate   = STRING(tot-yrate, "->>>,>>>,>>>,>>9.99")   
                    rm-statistic-list.dgrev    = STRING(tot-drev, "->>>,>>>,>>>,>>9.99") 
                    rm-statistic-list.mgrev    = STRING(tot-mrev, "->>>,>>>,>>>,>>9.99")
                    rm-statistic-list.ygrev    = STRING(tot-yrev, "->>>,>>>,>>>,>>9.99")
                .                    
                CREATE rm-statistic-list.

                ASSIGN tot-droom = 0 
                       tot-proz1 = 0
                       tot-mroom = 0 
                       tot-proz2 = 0 
                       tot-yroom = 0 
                       tot-proz3 = 0 
                       tot-dpax  = 0 
                       tot-mpax  = 0 
                       tot-ypax  = 0 
                       tot-drate = 0 
                       tot-mrate = 0  
                       tot-yrate = 0  
                       tot-drev  = 0  
                       tot-mrev  = 0 
                       tot-yrev  = 0
                       tot-droom = tot-droom + cl-list.droom 
                       tot-proz1 = tot-proz1 + cl-list.proz1
                       tot-mroom = tot-mroom + cl-list.mroom 
                       tot-proz2 = tot-proz2 + cl-list.proz2
                       tot-yroom = tot-yroom + cl-list.yroom 
                       tot-proz3 = tot-proz3 + cl-list.proz3
                       tot-dpax  = tot-dpax  + cl-list.dpax 
                       tot-mpax  = tot-mpax  + cl-list.mpax 
                       tot-ypax  = tot-ypax  + cl-list.ypax
                       tot-drate = tot-drate + cl-list.drate 
                       tot-mrate = tot-mrate + cl-list.mrate
                       tot-yrate = tot-yrate + cl-list.yrate  
                       tot-drev  = tot-drev  + cl-list.drev  
                       tot-mrev  = tot-mrev  + cl-list.mrev
                       tot-yrev  = tot-yrev  + cl-list.yrev.
            END.
            ELSE DO:
                ASSIGN tot-droom = tot-droom + cl-list.droom 
                       tot-proz1 = tot-proz1 + cl-list.proz1
                       tot-mroom = tot-mroom + cl-list.mroom 
                       tot-proz2 = tot-proz2 + cl-list.proz2
                       tot-yroom = tot-yroom + cl-list.yroom 
                       tot-proz3 = tot-proz3 + cl-list.proz3
                       tot-dpax  = tot-dpax  + cl-list.dpax 
                       tot-mpax  = tot-mpax  + cl-list.mpax 
                       tot-ypax  = tot-ypax  + cl-list.ypax
                       tot-drate = tot-drate + cl-list.drate 
                       tot-mrate = tot-mrate + cl-list.mrate
                       tot-yrate = tot-yrate + cl-list.yrate  
                       tot-drev  = tot-drev  + cl-list.drev  
                       tot-mrev  = tot-mrev  + cl-list.mrev
                       tot-yrev  = tot-yrev  + cl-list.yrev.

            END.
            ASSIGN curr-grup = cl-list.segm-grup.
        END. 

        CREATE rm-statistic-list1.
        IF long-digit THEN 
        DO:
            ASSIGN
                rm-statistic-list1.segm    = STRING(cl-list.segm, ">>>")                 
                rm-statistic-list1.bezeich = cl-list.bezeich                             
                rm-statistic-list1.droom   = STRING(cl-list.droom, ">>,>>9")             
                rm-statistic-list1.proz1   = STRING(cl-list.proz1, ">>9.99")             
                rm-statistic-list1.mroom   = STRING(cl-list.mroom, ">>,>>9")             
                rm-statistic-list1.proz2   = STRING(cl-list.proz2, ">>9.99")             
                rm-statistic-list1.yroom   = STRING(cl-list.yroom, ">>,>>9")             
                rm-statistic-list1.proz3   = STRING(cl-list.proz3, ">>9.99")             
                rm-statistic-list1.dpax    = STRING(cl-list.dpax, ">>,>>9")              
                rm-statistic-list1.mpax    = STRING(cl-list.mpax, ">>,>>9")              
                rm-statistic-list1.ypax    = STRING(cl-list.ypax, ">>,>>9")              
                rm-statistic-list1.drate   = STRING(cl-list.drate, "->>,>>>,>>>,>>>,>>9")
                rm-statistic-list1.mrate   = STRING(cl-list.mrate, "->>,>>>,>>>,>>>,>>9")
                rm-statistic-list1.yrate   = STRING(cl-list.yrate, "->>,>>>,>>>,>>>,>>9")
                rm-statistic-list1.drev    = STRING(cl-list.drev, "->>,>>>,>>>,>>>,>>9") 
                rm-statistic-list1.mrev    = STRING(cl-list.mrev, "->>,>>>,>>>,>>>,>>9") 
                rm-statistic-list1.yrev    = STRING(cl-list.yrev, "->>,>>>,>>>,>>>,>>9") 
            .
        END.
        ELSE
        DO:
            ASSIGN
                rm-statistic-list1.segm    = STRING(cl-list.segm, ">>>")                 
                rm-statistic-list1.bezeich = cl-list.bezeich                             
                rm-statistic-list1.droom   = STRING(cl-list.droom, ">>,>>9")             
                rm-statistic-list1.proz1   = STRING(cl-list.proz1, ">>9.99")             
                rm-statistic-list1.mroom   = STRING(cl-list.mroom, ">>,>>9")             
                rm-statistic-list1.proz2   = STRING(cl-list.proz2, ">>9.99")             
                rm-statistic-list1.yroom   = STRING(cl-list.yroom, ">>,>>9")             
                rm-statistic-list1.proz3   = STRING(cl-list.proz3, ">>9.99")             
                rm-statistic-list1.dpax    = STRING(cl-list.dpax, ">>,>>9")              
                rm-statistic-list1.mpax    = STRING(cl-list.mpax, ">>,>>9")              
                rm-statistic-list1.ypax    = STRING(cl-list.ypax, ">>,>>9")              
                rm-statistic-list1.drate   = STRING(cl-list.drate, "->>>,>>>,>>>,>>9.99")
                rm-statistic-list1.mrate   = STRING(cl-list.mrate, "->>>,>>>,>>>,>>9.99")
                rm-statistic-list1.yrate   = STRING(cl-list.yrate, "->>>,>>>,>>>,>>9.99")
                rm-statistic-list1.drev    = STRING(cl-list.drev, "->>>,>>>,>>>,>>9.99") 
                rm-statistic-list1.mrev    = STRING(cl-list.mrev, "->>>,>>>,>>>,>>9.99") 
                rm-statistic-list1.yrev    = STRING(cl-list.yrev, "->>>,>>>,>>>,>>9.99") 
            .
        END.
        
        IF show-other THEN
        DO:
            FIND FIRST other-list WHERE other-list.segm = cl-list.segm NO-LOCK NO-ERROR.
            IF AVAILABLE other-list THEN
            DO:
                ASSIGN
                    ttrev  = cl-list.drev + other-list.orev
                    ttmrev = cl-list.mrev + other-list.morev
                    ttyrev = cl-list.yrev + other-list.yorev.

                CREATE rm-statistic-list1.                
                IF long-digit THEN
                DO:
                    ASSIGN 
                        rm-statistic-list1.flag     = "Orev"
                        rm-statistic-list1.bezeich  = translateExtended("Other Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(other-list.orev, "->>,>>>,>>>,>>>,>>9")  
                        rm-statistic-list1.mrev     = STRING(other-list.morev, "->>,>>>,>>>,>>>,>>9")
                        rm-statistic-list1.yrev     = STRING(other-list.yorev, "->>,>>>,>>>,>>>,>>9")
                    .
                END.                                            
                ELSE
                DO:
                    ASSIGN 
                        rm-statistic-list1.flag     = "Orev"
                        rm-statistic-list1.bezeich  = translateExtended("Other Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(other-list.orev, "->>>,>>>,>>>,>>9.99")  
                        rm-statistic-list1.mrev     = STRING(other-list.morev, "->>>,>>>,>>>,>>9.99")
                        rm-statistic-list1.yrev     = STRING(other-list.yorev, "->>>,>>>,>>>,>>9.99")
                    .
                END.
                                 
                CREATE rm-statistic-list1.
                IF long-digit THEN
                DO:
                    ASSIGN
                        rm-statistic-list1.flag     = "Trev"
                        rm-statistic-list1.bezeich  = translateExtended("Total Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(ttrev, "->>,>>>,>>>,>>>,>>9")  
                        rm-statistic-list1.mrev     = STRING(ttmrev, "->>,>>>,>>>,>>>,>>9")
                        rm-statistic-list1.yrev     = STRING(ttyrev, "->>,>>>,>>>,>>>,>>9")
                    .
                END.
                ELSE
                DO:
                    ASSIGN 
                        rm-statistic-list1.flag     = "Trev"
                        rm-statistic-list1.bezeich  = translateExtended("Total Revenue", lvCAREA, "")
                        rm-statistic-list1.drev     = STRING(ttrev, "->>>,>>>,>>>,>>9.99")  
                        rm-statistic-list1.mrev     = STRING(ttmrev, "->>>,>>>,>>>,>>9.99")
                        rm-statistic-list1.yrev     = STRING(ttyrev, "->>>,>>>,>>>,>>9.99")
                    .
                END.                
                CREATE rm-statistic-list1.
            END.
        END.
    END. 

  /* START RS 01/DEC/09  add variable tot-slist-dpax, it used to calculate complimentary rooms 
     then substract the dpax and dgpax with it,so the Total Rev-Room of PAX column have the right result
  
  FOR EACH s-list: 
    tot-slist-dpax = tot-slist-dpax + s-list.dpax.
    /*tot-slist-mpax = tot-slist-mpax + s-list.mpax.*/
  END. 
  dpax  = dpax - tot-slist-dpax .
  dgpax = dgpax - tot-slist-dpax .
    */
  /*mpax  = mpax - tot-slist-mpax .
  mgpax = mgpax - tot-slist-mpax .*/
  /* END RS 01/DEC/09 */

  END.

  IF grp-flag THEN 
  DO:        
      CREATE rm-statistic-list.
      IF NOT show-ytd THEN 
      DO:
          ASSIGN
              rm-statistic-list.segm      = ""
              rm-statistic-list.bezeich   = translateExtended("T O T A L", lvCAREA, "")
              rm-statistic-list.dgroom    = STRING(tot-droom, ">>,>>9")                
              rm-statistic-list.proz1     = STRING(tot-proz1, ">>9.99")                
              rm-statistic-list.mgroom    = STRING(tot-mroom, ">>,>>9")                
              rm-statistic-list.proz2     = STRING(tot-proz2, ">>9.99")                
              rm-statistic-list.dgpax     = STRING(tot-dpax, ">>,>>9")                 
              rm-statistic-list.mgpax     = STRING(tot-mpax, ">>,>>9")                 
              rm-statistic-list.dgrate    = STRING(tot-drate, "->>>,>>>,>>>,>>9.99")    
              rm-statistic-list.mgrate    = STRING(tot-mrate, "->>>,>>>,>>>,>>9.99")    
              rm-statistic-list.dgrev     = STRING(tot-drev, "->>>,>>>,>>>,>>9.99")    
              rm-statistic-list.mgrev     = STRING(tot-mrev, "->>>,>>>,>>>,>>9.99")    
          .              
          CREATE rm-statistic-list.
      END.
      ELSE IF show-ytd THEN 
      DO:
          ASSIGN                          
              rm-statistic-list.segm    = ""                                         
              rm-statistic-list.bezeich = translateExtended("T O T A L", lvCAREA, "")
              rm-statistic-list.dgroom  = STRING(tot-droom, ">>9")                
              rm-statistic-list.proz1   = STRING(tot-proz1, ">>9.99")             
              rm-statistic-list.mgroom  = STRING(tot-mroom, ">,>>9")              
              rm-statistic-list.proz2   = STRING(tot-proz2, ">>9.99")             
              rm-statistic-list.ygroom  = STRING(tot-yroom, ">>,>>9")             
              rm-statistic-list.proz3   = STRING(tot-proz3, ">>9.99")             
              rm-statistic-list.dgpax   = STRING(tot-dpax, ">>9")                 
              rm-statistic-list.mgpax   = STRING(tot-mpax, ">>,>>9")              
              rm-statistic-list.ygpax   = STRING(tot-ypax, ">>,>>9")              
              rm-statistic-list.dgrate  = STRING(tot-drate, "->>>,>>>,>>9.99")    
              rm-statistic-list.mgrate  = STRING(tot-mrate, "->>>,>>>,>>9.99")    
              rm-statistic-list.ygrate  = STRING(tot-yrate, "->>>,>>>,>>9.99")    
              rm-statistic-list.dgrev   = STRING(tot-drev, "->>,>>>,>>>,>>9.99")  
              rm-statistic-list.mgrev   = STRING(tot-mrev, "->>>,>>>,>>>,>>9.99") 
              rm-statistic-list.ygrev   = STRING(tot-yrev, "->>>,>>>,>>>,>>9.99").
          .         
          CREATE rm-statistic-list.
      END.
  END.

  IF NOT show-ytd THEN
  DO:
      CREATE rm-statistic-list. 
      
      CREATE rm-statistic-list.
      IF long-digit THEN 
      DO:
          ASSIGN
              rm-statistic-list.segm      = ""
              rm-statistic-list.bezeich   = translateExtended("Total Revenue Room", lvCAREA, "")
              rm-statistic-list.dgroom    = STRING(dgroom, ">>,>>9")               
              rm-statistic-list.proz1     = STRING(100, ">>9.99")               
              rm-statistic-list.mgroom    = STRING(mgroom, ">>,>>9")             
              rm-statistic-list.proz2     = STRING(100, ">>9.99")               
              rm-statistic-list.dgpax     = STRING(dgpax, ">>,>>9")                
              rm-statistic-list.mgpax     = STRING(mgpax, ">>,>>9")             
              rm-statistic-list.dgrate    = STRING(dgrate, "->>,>>>,>>>,>>>,>>9")   
              rm-statistic-list.mgrate    = STRING(mgrate, "->>,>>>,>>>,>>>,>>9")   
              rm-statistic-list.dgrev     = STRING(dgrev, "->>,>>>,>>>,>>>,>>9") 
              rm-statistic-list.mgrev     = STRING(mgrev, "->>,>>>,>>>,>>>,>>9")
          .
      END.
      ELSE
      DO:
          ASSIGN
              rm-statistic-list.segm      = ""
              rm-statistic-list.bezeich   = translateExtended("Total Revenue Room", lvCAREA, "")
              rm-statistic-list.dgroom    = STRING(dgroom, ">>,>>9")               
              rm-statistic-list.proz1     = STRING(100, ">>9.99")               
              rm-statistic-list.mgroom    = STRING(mgroom, ">>,>>9")             
              rm-statistic-list.proz2     = STRING(100, ">>9.99")               
              rm-statistic-list.dgpax     = STRING(dgpax, ">>,>>9")                
              rm-statistic-list.mgpax     = STRING(mgpax, ">>,>>9")             
              rm-statistic-list.dgrate    = STRING(dgrate, "->>>,>>>,>>>,>>9.99")   
              rm-statistic-list.mgrate    = STRING(mgrate, "->>>,>>>,>>>,>>9.99")   
              rm-statistic-list.dgrev     = STRING(dgrev, "->>>,>>>,>>>,>>9.99") 
              rm-statistic-list.mgrev     = STRING(mgrev, "->>>,>>>,>>>,>>9.99")
          .
      END.      
  END.

  FIND FIRST cl-list WHERE cl-list.flag-comp NO-ERROR.
  IF AVAILABLE cl-list THEN
  DO: 
      CREATE rm-statistic-list. 
      CREATE rm-statistic-list. 
      CREATE rm-statistic-list. 
      rm-statistic-list.bezeich = translateExtended("Compliment Rooms", lvCAREA, ""). 
  
      
      FOR EACH cl-list WHERE flag-comp BY cl-list.segm :
          CREATE rm-statistic-list. 
          /*output-list.segNo = cl-list.segm.*/
          ASSIGN
              rm-statistic-list.segm      = STRING(cl-list.segm,">>9")     
              rm-statistic-list.bezeich   = cl-list.bezeich                
              rm-statistic-list.dgroom    = STRING(cl-list.droom, ">>,>>9")
              rm-statistic-list.proz1     = ""                             
              rm-statistic-list.mgroom    = STRING(cl-list.mroom, ">>,>>9")
              rm-statistic-list.proz2     = ""                             
              rm-statistic-list.dgpax     = STRING(cl-list.dpax, ">>,>>9") 
              rm-statistic-list.mgpax     = STRING(cl-list.mpax, ">>,>>9")
          .                                           
      END.
  END.
END PROCEDURE.
