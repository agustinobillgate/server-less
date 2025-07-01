
/*MI 12/05/14 -> update pada waiter2 dengan field kcredit-nr dan departement*/

DEFINE TEMP-TABLE t-zwkum LIKE zwkum.

DEF INPUT PARAMETER r-kellner AS INT.
DEF INPUT PARAMETER dept2 AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER crart2 AS INT.

DEF BUFFER toart1 FOR artikel. 
DEF BUFFER toart2 FOR artikel.
DEF BUFFER waiter1 FOR kellne1.
DEF BUFFER waiter2 FOR kellner. 
DEF BUFFER b-zwkum FOR zwkum.

DEFINE VARIABLE to-deptname AS CHARACTER.
DEFINE VARIABLE from-deptname AS CHARACTER.
DEFINE VARIABLE str-desc AS CHARACTER.
DEFINE VARIABLE subgrp-number AS INT.


FIND FIRST hoteldpt WHERE hoteldpt.num EQ dept2 NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN to-deptname = hoteldpt.depart.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN from-deptname = hoteldpt.depart.

FIND FIRST kellner WHERE RECID(kellner) = r-kellner. /*Alder - Serverless - Issue 851*/
IF AVAILABLE kellner THEN
DO:
    FIND FIRST toart2 WHERE toart2.artnr = kellner.kumsatz-nr 
        AND toart2.departement = dept2 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE toart2 THEN 
    DO: 
        FIND FIRST toart1 WHERE toart1.artnr = kellner.kumsatz-nr 
            AND toart1.departement = dept NO-LOCK NO-ERROR. 
        IF AVAILABLE toart1 THEN
        DO:
            CREATE toart2.
            BUFFER-COPY toart1 EXCEPT departement TO toart2. 
            ASSIGN toart2.departement = dept2. 
    
            /*FDL Jan 02, 2025: CDC936*/
            IF NUM-ENTRIES(toart1.bezeich," ") GT 2 THEN
            DO:
                IF ENTRY(1,toart1.bezeich," ") EQ "T/O" THEN
                DO:           
                    IF ENTRY(3,toart1.bezeich," ") NE "" THEN str-desc = "T/O " + to-deptname + " " + ENTRY(3,toart1.bezeich," ").
                    ELSE str-desc = "T/O " + to-deptname + " 1".                
                    toart2.bezeich = str-desc.
                END.   
            END.
            
            FIND FIRST zwkum WHERE zwkum.zknr EQ toart1.zwkum
                AND zwkum.departement EQ dept2 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE zwkum THEN
            DO:
                FOR EACH b-zwkum WHERE b-zwkum.departement EQ dept2 NO-LOCK BY b-zwkum.zknr DESC:
                    CREATE t-zwkum.
                    BUFFER-COPY b-zwkum EXCEPT b-zwkum.zknr TO t-zwkum.
                    t-zwkum.zknr = toart1.zwkum. 
                    t-zwkum.bezeich = str-desc.
                    LEAVE.
                END.      
                CREATE zwkum.
                BUFFER-COPY t-zwkum TO zwkum.            
            END.
            str-desc = "".
        END.     
    END. 
    
    FIND FIRST toart2 WHERE toart2.artnr = kellner.kzahl-nr 
        AND toart2.departement = dept2 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE toart2 THEN 
    DO: 
        /*CREATE toart2.*/
        FIND FIRST toart1 WHERE toart1.artnr = kellner.kzahl-nr 
            AND toart1.departement = dept NO-LOCK NO-ERROR. 
        IF AVAILABLE toart1 THEN
        DO:
            CREATE toart2.
            BUFFER-COPY toart1 EXCEPT departement TO toart2. 
            ASSIGN toart2.departement = dept2. 
    
            /*FDL Jan 02, 2025: CDC936*/
            IF NUM-ENTRIES(toart1.bezeich," ") GT 2 THEN
            DO:
                IF ENTRY(1,toart1.bezeich," ") EQ "T/O" THEN
                DO:           
                    IF ENTRY(3,toart1.bezeich," ") NE "" THEN str-desc = "T/O " + to-deptname + " " + ENTRY(3,toart1.bezeich," ").
                    ELSE str-desc = "T/O " + to-deptname + " 1".                
                    toart2.bezeich = str-desc.
                END.   
            END.
            
            FIND FIRST zwkum WHERE zwkum.zknr EQ toart1.zwkum
                AND zwkum.departement EQ dept2 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE zwkum THEN
            DO:
                FOR EACH b-zwkum WHERE b-zwkum.departement EQ dept2 NO-LOCK BY b-zwkum.zknr DESC:
                    CREATE t-zwkum.
                    BUFFER-COPY b-zwkum EXCEPT b-zwkum.zknr TO t-zwkum.
                    t-zwkum.zknr = toart1.zwkum. 
                    t-zwkum.bezeich = str-desc.
                    LEAVE.
                END.      
                CREATE zwkum.
                BUFFER-COPY t-zwkum TO zwkum.            
            END.
            str-desc = "".
        END.    
    END. 
    
    /*MI 12/05/14*/
    FIND FIRST waiter2 WHERE waiter2.departement = dept2 AND 
        waiter2.kumsatz-nr = kellner.kumsatz-nr NO-LOCK NO-ERROR.
    IF AVAILABLE waiter2 THEN 
    DO: 
        FIND CURRENT waiter2 EXCLUSIVE-LOCK.
        BUFFER-COPY kellner EXCEPT kcredit-nr departement TO waiter2. 
        ASSIGN 
            waiter2.kcredit-nr = crart2 
            waiter2.departement = dept2. 
    END.
    ELSE 
    DO: 
        FIND FIRST kellner WHERE RECID(kellner) = r-kellner NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 851*/
        IF AVAILABLE kellner THEN
        DO:
            CREATE waiter2.
            BUFFER-COPY kellner EXCEPT kcredit-nr departement TO waiter2. 
            ASSIGN 
                waiter2.kcredit-nr = crart2 
                waiter2.departement = dept2.
        END.
    END.
    FIND CURRENT waiter2 NO-LOCK. 
    RELEASE waiter2. 
    
    FIND FIRST waiter1 WHERE waiter1.kellner-nr = kellner.kellner-nr 
        AND waiter1.departement = dept2 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE waiter1 THEN 
    DO: 
        CREATE waiter1. 
        BUFFER-COPY kellner EXCEPT departement TO waiter1. 
        ASSIGN waiter1.departement = dept2. 
        RELEASE waiter1.
    END. 
END.
