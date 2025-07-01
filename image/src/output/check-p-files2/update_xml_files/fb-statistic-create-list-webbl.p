DEFINE TEMP-TABLE cl-list
    FIELD dept      AS INTEGER
    FIELD deptname  AS CHAR
    FIELD typ       AS INTEGER
    FIELD descrip   AS CHAR
    FIELD grev      AS DECIMAL  FORMAT "->>,>>>,>>9.99" INITIAL 0
    FIELD gpax      AS INTEGER  FORMAT "->>9"           INITIAL 0
    FIELD gproz     AS DECIMAL  FORMAT ">>9.99"         INITIAL 0
    FIELD gcost     AS DECIMAL  FORMAT "->>,>>>,>>9.99" INITIAL 0
    FIELD gavg      AS DECIMAL  FORMAT "->>,>>>,>>9.99" INITIAL 0
    FIELD wrev      AS DECIMAL  FORMAT "->>,>>>,>>9.99" INITIAL 0
    FIELD wpax      AS INTEGER  FORMAT "->>>9"           INITIAL 0
    FIELD wproz     AS DECIMAL  FORMAT ">>9.99"         INITIAL 0
    FIELD wcost     AS DECIMAL  FORMAT "->>,>>>,>>9.99" INITIAL 0
    FIELD wavg      AS DECIMAL  FORMAT "->>,>>>,>>9.99" INITIAL 0
    FIELD totpax    AS INTEGER  FORMAT "->>>9"            INITIAL 0
    FIELD totrev    AS DECIMAL  FORMAT "->>>,>>>,>>9.99" INITIAL 0
    FIELD totcost   AS DECIMAL  FORMAT "->>>,>>>,>>9.99" INITIAL 0
    .

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER fdept          AS INT.
DEF INPUT  PARAMETER tdept          AS INT.
DEF INPUT  PARAMETER fdate          AS DATE.
DEF INPUT  PARAMETER tdate          AS DATE.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER TABLE FOR cl-list.

/*
DEF VAR pvILanguage    AS INTEGER NO-UNDO INIT 1.
DEF VAR fdept          AS INT INIT 1.
DEF VAR tdept          AS INT INIT 1. 
DEF VAR fdate          AS DATE INIT 10/01/18.
DEF VAR tdate          AS DATE INIT 12/31/18 .
DEF VAR price-decimal  AS INT INIT 2.
*/

DEFINE VARIABLE tgrev    AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE twrev    AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE tgpax    AS INTEGER INITIAL 0.
DEFINE VARIABLE tgcost   AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE twpax    AS INTEGER INITIAL 0.
DEFINE VARIABLE twcost   AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE ttotpax    AS INTEGER INITIAL 0 FORMAT "->>>9".
DEFINE VARIABLE ttotrev    AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE ttotcost   AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.

DEFINE VARIABLE tot-gpax   AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-grev   AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE tot-gcost  AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE tot-wpax   AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-wrev   AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE tot-wcost  AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE tot-tpax   AS INTEGER INITIAL 0.
DEFINE VARIABLE tot-trev   AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.
DEFINE VARIABLE tot-tcost  AS DECIMAL FORMAT "->>>,>>>,>>9.99"  INITIAL 0.

RUN create-list.
/*
FOR EACH cl-list:
    DISP cl-list.gpax cl-list.wpax.
END.
*/
PROCEDURE create-list:
    DEF BUFFER stat FOR fbstat.
    FOR EACH cl-list:
        DELETE cl-list.
    END.

    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 AND hoteldpt.num GE fdept
    AND hoteldpt.num LE tdept NO-LOCK BY hoteldpt.num:

        ASSIGN
            tot-gpax = 0
            tot-grev = 0
            tot-gcost = 0
            tot-wpax = 0
            tot-wrev = 0
            tot-wcost = 0
            tot-tpax = 0
            tot-trev = 0
            tot-tcost = 0.

        FIND FIRST stat WHERE stat.departement = hoteldpt.num 
            AND stat.datum GE fdate AND stat.datum LE tdate
            NO-LOCK NO-ERROR.
        IF AVAILABLE stat THEN
        DO:
            CREATE cl-list.
            ASSIGN
                cl-list.descrip = STRING(hoteldpt.num) + " - " + 
                               hoteldpt.depart.
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 1
                cl-list.descrip = "Breakfast"
                .
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 1
                cl-list.descrip = "Lunch"
                .
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 1
                cl-list.descrip = "Dinner"
                .
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 1
                cl-list.descrip = "Supper"
                .        

            CREATE cl-list.
            cl-list.descrip = "-----".
            CREATE cl-list.
            ASSIGN
                cl-list.descrip = "FOOD TOTAL"
                cl-list.dept = hoteldpt.num
                cl-list.typ = 1.
            CREATE cl-list.
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 2
                cl-list.descrip = "Breakfast".
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 2
                cl-list.descrip = "Lunch"
                .
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 2
                cl-list.descrip = "Dinner".
    
            CREATE cl-list.
            ASSIGN cl-list.dept = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 2
                cl-list.descrip = "Supper".

            CREATE cl-list.
            cl-list.descrip = "-----".
            CREATE cl-list.
            ASSIGN
                cl-list.descrip = "BEV TOTAL"
                cl-list.dept = hoteldpt.num
                cl-list.typ = 2.
            CREATE cl-list.
    
            CREATE cl-list.
            ASSIGN
                cl-list.dept    = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 3
                cl-list.descrip = "Breakfast".
    
            CREATE cl-list.
            ASSIGN
                cl-list.dept    = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 3
                cl-list.descrip = "Lunch".
            
            CREATE cl-list.
            ASSIGN
                cl-list.dept    = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 3
                cl-list.descrip = "Dinner".
    
            CREATE cl-list.
            ASSIGN
                cl-list.dept    = hoteldpt.num
                cl-list.deptname = hoteldpt.depart
                cl-list.typ     = 3
                cl-list.descrip = "Supper".

            CREATE cl-list.
            cl-list.descrip = "-----".
            CREATE cl-list.
            ASSIGN
                cl-list.descrip = "OTHER TOTAL"
                cl-list.dept = hoteldpt.num
                cl-list.typ = 3.
            CREATE cl-list.

            CREATE cl-list.
            ASSIGN
                cl-list.descrip = "TOTAL"
                cl-list.dept = hoteldpt.num
                cl-list.typ = 4.
            CREATE cl-list.
        END.

        FOR EACH fbstat WHERE fbstat.datum GE fdate AND fbstat.datum
            LE tdate AND fbstat.departement = hoteldpt.num
            NO-LOCK:
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 1 AND cl-list.descrip = "Breakfast" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.food-grev[1]
                    cl-list.gpax    = cl-list.gpax  + fbstat.food-gpax[1]
                    cl-list.gcost   = cl-list.gcost + fbstat.food-gcost[1]
                    cl-list.wrev    = cl-list.wrev  + fbstat.food-wrev[1]
                    cl-list.wpax    = cl-list.wpax  + fbstat.food-wpax[1]
                    cl-list.wcost   = cl-list.wcost + fbstat.food-wcost[1]
                    cl-list.totrev  = cl-list.totrev + fbstat.food-grev[1] + fbstat.food-wrev[1]
                    cl-list.totpax  = cl-list.totpax + fbstat.food-gpax[1] + fbstat.food-wpax[1]
                    cl-list.totcost  = cl-list.totcost + fbstat.food-gcost[1] + fbstat.food-wcost[1].

                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.                                                  

            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 1 AND cl-list.descrip = "Lunch" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.food-grev[2]
                    cl-list.gpax    = cl-list.gpax  + fbstat.food-gpax[2]
                    cl-list.gcost   = cl-list.gcost + fbstat.food-gcost[2]
                    cl-list.wrev    = cl-list.wrev  + fbstat.food-wrev[2]
                    cl-list.wpax    = cl-list.wpax  + fbstat.food-wpax[2]
                    cl-list.wcost   = cl-list.wcost + fbstat.food-wcost[2]
                    cl-list.totrev  = cl-list.totrev + fbstat.food-grev[2] + fbstat.food-wrev[2]
                    cl-list.totpax  = cl-list.totpax + fbstat.food-gpax[2] + fbstat.food-wpax[2]
                    cl-list.totcost  = cl-list.totcost + fbstat.food-gcost[2] + fbstat.food-wcost[2].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
            
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 1 AND cl-list.descrip = "Dinner" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.food-grev[3]
                    cl-list.gpax    = cl-list.gpax  + fbstat.food-gpax[3]
                    cl-list.gcost   = cl-list.gcost + fbstat.food-gcost[3]
                    cl-list.wrev    = cl-list.wrev  + fbstat.food-wrev[3]
                    cl-list.wpax    = cl-list.wpax  + fbstat.food-wpax[3]
                    cl-list.wcost   = cl-list.wcost + fbstat.food-wcost[3]
                    cl-list.totrev  = cl-list.totrev + fbstat.food-grev[3] + fbstat.food-wrev[3]
                    cl-list.totpax  = cl-list.totpax + fbstat.food-gpax[3] + fbstat.food-wpax[3]
                    cl-list.totcost  = cl-list.totcost + fbstat.food-gcost[3] + fbstat.food-wcost[3].
                    
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
            
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 1 AND cl-list.descrip = "Supper" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.food-grev[4]
                    cl-list.gpax    = cl-list.gpax  + fbstat.food-gpax[4]
                    cl-list.gcost   = cl-list.gcost + fbstat.food-gcost[4]
                    cl-list.wrev    = cl-list.wrev  + fbstat.food-wrev[4]
                    cl-list.wpax    = cl-list.wpax  + fbstat.food-wpax[4]
                    cl-list.wcost   = cl-list.wcost + fbstat.food-wcost[4]
                    cl-list.totrev  = cl-list.totrev + fbstat.food-grev[4] + fbstat.food-wrev[4]
                    cl-list.totpax  = cl-list.totpax + fbstat.food-gpax[4] + fbstat.food-wpax[4]
                    cl-list.totcost  = cl-list.totcost + fbstat.food-gcost[4] + fbstat.food-wcost[4].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wavg NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wrev    = cl-list.wrev / cl-list.wpax.
            END.
                        
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 2 AND cl-list.descrip = "Breakfast" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.bev-grev[1]
                    cl-list.gpax    = cl-list.gpax  + fbstat.bev-gpax[1]
                    cl-list.gcost   = cl-list.gcost + fbstat.bev-gcost[1] 
                    cl-list.wrev    = cl-list.wrev  + fbstat.bev-wrev[1]
                    cl-list.wpax    = cl-list.wpax  + fbstat.bev-wpax[1]
                    cl-list.wcost   = cl-list.wcost + fbstat.bev-wcost[1]
                    cl-list.totrev  = cl-list.totrev + fbstat.bev-grev[1] + fbstat.bev-wrev[1]
                    cl-list.totpax  = cl-list.totpax + fbstat.bev-gpax[1] + fbstat.bev-wpax[1]
                    cl-list.totcost  = cl-list.totcost + fbstat.bev-gcost[1] + fbstat.bev-wcost[1].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
                        
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 2 AND cl-list.descrip = "Lunch" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.bev-grev[2]
                    cl-list.gpax    = cl-list.gpax  + fbstat.bev-gpax[2]
                    cl-list.gcost   = cl-list.gcost + fbstat.bev-gcost[2]
                    cl-list.wrev    = cl-list.wrev  + fbstat.bev-wrev[2]
                    cl-list.wpax    = cl-list.wpax  + fbstat.bev-wpax[2]
                    cl-list.wcost   = cl-list.wcost + fbstat.bev-wcost[2]
                    cl-list.totrev  = cl-list.totrev + fbstat.bev-grev[2] + fbstat.bev-wrev[2]
                    cl-list.totpax  = cl-list.totpax + fbstat.bev-gpax[2] + fbstat.bev-wpax[2]
                    cl-list.totcost  = cl-list.totcost + fbstat.bev-gcost[2] + fbstat.bev-wcost[2].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
                        
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 2 AND cl-list.descrip = "Dinner" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                     cl-list.grev    = cl-list.grev  + fbstat.bev-grev[3]
                     cl-list.gpax    = cl-list.gpax  + fbstat.bev-gpax[3]
                     cl-list.gcost   = cl-list.gcost + fbstat.bev-gcost[3]
                     cl-list.wrev    = cl-list.wrev  + fbstat.bev-wrev[3]
                     cl-list.wpax    = cl-list.wpax  + fbstat.bev-wpax[3]
                     cl-list.wcost   = cl-list.wcost + fbstat.bev-wcost[3]
                     cl-list.totrev  = cl-list.totrev + fbstat.bev-grev[3] + fbstat.bev-wrev[3]
                     cl-list.totpax  = cl-list.totpax + fbstat.bev-gpax[3] + fbstat.bev-wpax[3]
                     cl-list.totcost  = cl-list.totcost + fbstat.bev-gcost[3] + fbstat.bev-wcost[3].
                 IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                     cl-list.gavg    = cl-list.grev / cl-list.gpax.
                 IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                     cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
                        
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 2 AND cl-list.descrip = "Supper" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.bev-grev[4]
                    cl-list.gpax    = cl-list.gpax  + fbstat.bev-gpax[4]
                    cl-list.gcost   = cl-list.gcost + fbstat.bev-gcost[4]
                    cl-list.wrev    = cl-list.wrev  + fbstat.bev-wrev[4]
                    cl-list.wpax    = cl-list.wpax  + fbstat.bev-wpax[4]
                    cl-list.wcost   = cl-list.wcost + fbstat.bev-wcost[4]
                    cl-list.totrev  = cl-list.totrev + fbstat.bev-grev[4] + fbstat.bev-wrev[4]
                    cl-list.totpax  = cl-list.totpax + fbstat.bev-gpax[4] + fbstat.bev-wpax[4]
                    cl-list.totcost  = cl-list.totcost + fbstat.bev-gcost[4] + fbstat.bev-wcost[4].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
                        
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 3 AND cl-list.descrip = "Breakfast" NO-LOCK NO-ERROR.
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.other-grev[1]
                    cl-list.gpax    = cl-list.gpax  + fbstat.other-gpax[1]
                    cl-list.gcost   = cl-list.gcost + fbstat.other-gcost[1]
                    cl-list.wrev    = cl-list.wrev  + fbstat.other-wrev[1]
                    cl-list.wpax    = cl-list.wpax  + fbstat.other-wpax[1]
                    cl-list.wcost   = cl-list.wcost + fbstat.other-wcost[1]
                    cl-list.totrev  = cl-list.totrev + fbstat.other-grev[1] + fbstat.other-wrev[1]
                    cl-list.totpax  = cl-list.totpax + fbstat.other-gpax[1] + fbstat.other-wpax[1]
                    cl-list.totcost  = cl-list.totcost + fbstat.other-gcost[1] + fbstat.other-wcost[1].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.                                                  

            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 3 AND cl-list.descrip = "Lunch" NO-LOCK NO-ERROR.
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.other-grev[2]
                    cl-list.gpax    = cl-list.gpax  + fbstat.other-gpax[2]
                    cl-list.gcost   = cl-list.gcost + fbstat.other-gcost[2]
                    cl-list.wrev    = cl-list.wrev  + fbstat.other-wrev[2]
                    cl-list.wpax    = cl-list.wpax  + fbstat.other-wpax[2]
                    cl-list.wcost   = cl-list.wcost + fbstat.other-wcost[2]
                    cl-list.totrev  = cl-list.totrev + fbstat.other-grev[2] + fbstat.other-wrev[2]
                    cl-list.totpax  = cl-list.totpax + fbstat.other-gpax[2] + fbstat.other-wpax[2]
                    cl-list.totcost  = cl-list.totcost + fbstat.other-gcost[2] + fbstat.other-wcost[2].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
               
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 3 AND cl-list.descrip = "Dinner" NO-LOCK NO-ERROR.
            DO:
                ASSIGN 
                     cl-list.grev    = cl-list.grev  + fbstat.other-grev[3]
                     cl-list.gpax    = cl-list.gpax  + fbstat.other-gpax[3]
                     cl-list.gcost   = cl-list.gcost + fbstat.other-gcost[3]
                     cl-list.wrev    = cl-list.wrev  + fbstat.other-wrev[3]
                     cl-list.wpax    = cl-list.wpax  + fbstat.other-wpax[3]
                     cl-list.wcost   = cl-list.wcost + fbstat.other-wcost[3]
                     cl-list.totrev  = cl-list.totrev + fbstat.other-grev[3] + fbstat.other-wrev[3]
                     cl-list.totpax  = cl-list.totpax + fbstat.other-gpax[3] + fbstat.other-wpax[3]
                     cl-list.totcost  = cl-list.totcost + fbstat.other-gcost[3] + fbstat.other-wcost[3].
                 IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                     cl-list.gavg    = cl-list.grev / cl-list.gpax.
                 IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                     cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.
                   
            FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num
                AND cl-list.typ = 3 AND cl-list.descrip = "Supper" NO-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                ASSIGN 
                    cl-list.grev    = cl-list.grev  + fbstat.other-grev[4]
                    cl-list.gpax    = cl-list.gpax  + fbstat.other-gpax[4]
                    cl-list.gcost   = cl-list.gcost + fbstat.other-gcost[4]
                    cl-list.wrev    = cl-list.wrev  + fbstat.other-wrev[4]
                    cl-list.wpax    = cl-list.wpax  + fbstat.other-wpax[4]
                    cl-list.wcost   = cl-list.wcost + fbstat.other-wcost[4]
                    cl-list.totrev  = cl-list.totrev + fbstat.other-grev[4] + fbstat.other-wrev[4]
                    cl-list.totpax  = cl-list.totpax + fbstat.other-gpax[4] + fbstat.other-wpax[4]
                    cl-list.totcost  = cl-list.totcost + fbstat.other-gcost[4] + fbstat.other-wcost[4].
                IF cl-list.grev NE 0 AND cl-list.gpax NE 0 THEN
                    cl-list.gavg    = cl-list.grev / cl-list.gpax.
                IF cl-list.wrev NE 0 AND cl-list.wpax NE 0 THEN
                    cl-list.wavg    = cl-list.wrev / cl-list.wpax.
            END.                                                  
        END. /*end fbstat*/

        ASSIGN
            tgpax = 0
            tgrev = 0
            tgcost = 0
            twpax = 0
            twrev = 0
            twcost = 0
            ttotpax = 0
            ttotrev = 0
            ttotcost = 0.
        FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.typ = 1 NO-LOCK:
            ASSIGN
                tgpax = tgpax + cl-list.gpax
                tgrev = tgrev + cl-list.grev 
                tgcost = tgcost + cl-list.gcost
                twpax = twpax + cl-list.wpax
                twrev = twrev + cl-list.wrev
                twcost = twcost + cl-list.wcost
                ttotpax = ttotpax + cl-list.totpax
                ttotrev = ttotrev + cl-list.totrev
                ttotcost = ttotcost + cl-list.totcost.
        END.

        FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num AND
            cl-list.typ = 1 :
            IF cl-list.grev NE 0 AND tgrev NE 0 THEN
                cl-list.gproz = cl-list.grev / tgrev * 100.
            IF cl-list.wrev NE 0 AND twrev NE 0 THEN
                cl-list.wproz = cl-list.wrev / twrev * 100.
        END.

        FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.typ = 1 AND cl-list.descrip = "FOOD TOTAL" NO-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            ASSIGN
                cl-list.gpax = tgpax
                cl-list.grev = tgrev
                cl-list.gcost = tgcost
                cl-list.gproz = 100
                cl-list.wpax = twpax
                cl-list.wrev = twrev
                cl-list.wcost = twcost
                cl-list.wproz = 100
                cl-list.totpax = ttotpax
                cl-list.totrev = ttotrev
                cl-list.totcost = ttotcost.
            IF tgpax NE 0 THEN
                cl-list.gavg = tgrev / tgpax.
            IF twpax NE 0 THEN
                cl-list.wavg = twrev / twpax.
        END.
        
        ASSIGN
            tot-gpax = tot-gpax + tgpax
            tot-grev = tot-grev + tgrev
            tot-gcost = tot-gcost + tgcost
            tot-wpax = tot-wpax + twpax
            tot-wrev = tot-wrev + twrev
            tot-wcost = tot-wcost + twcost
            tot-tpax = tot-tpax + ttotpax
            tot-trev = tot-trev + ttotrev
            tot-tcost = tot-tcost + ttotcost.

        ASSIGN
            tgpax = 0
            tgrev = 0
            tgcost = 0
            twpax = 0
            twrev = 0
            twcost = 0
            ttotpax = 0
            ttotrev = 0
            ttotcost = 0.
        FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.typ = 2 NO-LOCK:
            ASSIGN
                tgpax = tgpax + cl-list.gpax
                tgrev = tgrev + cl-list.grev 
                tgcost = tgcost + cl-list.gcost
                twpax = twpax + cl-list.wpax
                twrev = twrev + cl-list.wrev
                twcost = twcost + cl-list.wcost
                ttotpax = ttotpax + cl-list.totpax
                ttotrev = ttotrev + cl-list.totrev
                ttotcost = ttotcost + cl-list.totcost.
        END.

        FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num AND
            cl-list.typ = 2:
            IF cl-list.grev NE 0 AND tgrev NE 0 THEN
                cl-list.gproz = cl-list.grev / tgrev * 100.
            IF cl-list.wrev NE 0 AND twrev NE 0 THEN
                cl-list.wproz = cl-list.wrev / twrev * 100.
        END.
        
        FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.typ = 2 AND cl-list.descrip = "BEV TOTAL" NO-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            ASSIGN
                cl-list.gpax = tgpax
                cl-list.grev = tgrev
                cl-list.gcost = tgcost
                cl-list.gproz = 100
                cl-list.wpax = twpax
                cl-list.wrev = twrev
                cl-list.wcost = twcost
                cl-list.wproz = 100
                cl-list.totpax = ttotpax
                cl-list.totrev = ttotrev
                cl-list.totcost = ttotcost.
            IF tgpax NE 0 THEN
                cl-list.gavg = tgrev / tgpax.
            IF twpax NE 0 THEN
                cl-list.wavg = twrev / twpax.
        END.
                    
        ASSIGN
            tot-gpax = tot-gpax + tgpax
            tot-grev = tot-grev + tgrev
            tot-gcost = tot-gcost + tgcost
            tot-wpax = tot-wpax + twpax
            tot-wrev = tot-wrev + twrev
            tot-wcost = tot-wcost + twcost
            tot-tpax = tot-tpax + ttotpax
            tot-trev = tot-trev + ttotrev
            tot-tcost = tot-tcost + ttotcost.
        
        ASSIGN
            tgpax = 0
            tgrev = 0
            tgcost = 0
            twpax = 0
            twrev = 0
            twcost = 0
            ttotpax = 0
            ttotrev = 0
            ttotcost = 0.
        
        FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.typ = 3 NO-LOCK:
            ASSIGN
                tgpax = tgpax + cl-list.gpax
                tgrev = tgrev + cl-list.grev 
                tgcost = tgcost + cl-list.gcost
                twpax = twpax + cl-list.wpax
                twrev = twrev + cl-list.wrev
                twcost = twcost + cl-list.wcost
                ttotpax = ttotpax + cl-list.totpax
                ttotrev = ttotrev + cl-list.totrev
                ttotcost = ttotcost + cl-list.totcost.
        END.

        FOR EACH cl-list WHERE cl-list.dept = hoteldpt.num AND
            cl-list.typ = 3 :
            IF cl-list.grev NE 0 AND tgrev NE 0 THEN
                cl-list.gproz = cl-list.grev / tgrev * 100.
            IF cl-list.wrev NE 0 AND twrev NE 0 THEN
                cl-list.wproz = cl-list.wrev / twrev * 100.
        END.
        
        FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.typ = 3 AND cl-list.descrip = "OTHER TOTAL" NO-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            ASSIGN
                cl-list.gpax = tgpax
                cl-list.grev = tgrev
                cl-list.gcost = tgcost
                cl-list.gproz = 100
                cl-list.wpax = twpax
                cl-list.wrev = twrev
                cl-list.wcost = twcost
                cl-list.wproz = 100
                cl-list.totpax = ttotpax
                cl-list.totrev = ttotrev
                cl-list.totcost = ttotcost.
            IF tgpax NE 0 THEN
                cl-list.gavg = tgrev / tgpax.
            IF twpax NE 0 THEN
                cl-list.wavg = twrev / twpax.
        END.
                  
        ASSIGN
            tot-gpax = tot-gpax + tgpax
            tot-grev = tot-grev + tgrev
            tot-gcost = tot-gcost + tgcost
            tot-wpax = tot-wpax + twpax
            tot-wrev = tot-wrev + twrev
            tot-wcost = tot-wcost + twcost
            tot-tpax = tot-tpax + ttotpax
            tot-trev = tot-trev + ttotrev
            tot-tcost = tot-tcost + ttotcost.

        FIND FIRST cl-list WHERE cl-list.dept = hoteldpt.num 
            AND cl-list.descrip = "TOTAL" NO-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            ASSIGN
                cl-list.gpax = tot-gpax
                cl-list.grev = tot-grev
                cl-list.gcost = tot-gcost
                cl-list.gproz = 100
                cl-list.wpax = tot-wpax
                cl-list.wrev = tot-wrev
                cl-list.wcost = tot-wcost
                cl-list.wproz = 100
                cl-list.totpax = tot-tpax
                cl-list.totrev = tot-trev
                cl-list.totcost = tot-tcost.
            IF tot-gpax NE 0 THEN
                cl-list.gavg = tot-grev / tot-gpax.
            IF twpax NE 0 THEN
                cl-list.wavg = tot-wrev / tot-wpax.
        END.
            

    END. 
END.

