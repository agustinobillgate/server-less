

DEFINE TEMP-TABLE tprop
    FIELD nr AS INTEGER
    FIELD nm AS CHAR.

DEFINE TEMP-TABLE tbrowse
    FIELD desc1 AS CHAR FORMAT "x(80)"
    FIELD desc2 AS CHAR FORMAT "x(50)"
    FIELD reqno AS CHAR FORMAT "x(20)"
    FIELD opend AS CHAR FORMAT "x(20)"
    FIELD processd AS CHAR FORMAT "x(20)"
    FIELD doned AS CHAR FORMAT "x(20)"
    FIELD subtask AS CHAR FORMAT "x(30)"
    FIELD reqstat AS CHAR FORMAT "x(20)"
    FIELD tFlag   AS CHAR .

DEF INPUT PARAMETER room-nr AS CHAR.
DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF INPUT PARAMETER prop-nr AS INT.
DEF OUTPUT PARAMETER TABLE FOR tbrowse.
DEF OUTPUT PARAMETER TABLE FOR tprop.

DEF VAR tot AS INTEGER.
DEF VAR atotal AS INTEGER.
DEF VAR btotal AS INTEGER.
DEFINE VARIABLE int-str AS CHAR EXTENT 5 INITIAL
    ["New",  "Processed", "Done",  "Postponed", "Closed"].
DEF BUFFER tbuff FOR l-artikel.

RUN create-history.

PROCEDURE create-history:
    DEF VAR char1 AS CHAR.
    DEF VAR char2 AS CHAR.
    DEF VAR char3 AS CHAR.
    DEF VAR char4 AS CHAR.
    DEF VAR a AS CHAR.
    DEF VAR b AS CHAR.
    DEF VAR c AS CHAR.
    DEF VAR vendo-nm AS CHAR.
    DEF VAR itotal AS DECIMAL.

    DEF VAR nm-prop AS CHAR.

    char1 = " Art No.      Article                                  ".  

    char2 = "".

    FOR EACH tbrowse:
        DELETE tbrowse.
    END.

    FOR EACH tprop:
        DELETE tprop.
    END.

    CREATE tbrowse.
    ASSIGN tbrowse.desc1 = CHAR1
           tbrowse.desc2 = char2
           tbrowse.tflag = "0".

    CREATE tbrowse.
    ASSIGN tbrowse.desc1 = "================================================================================"
           tbrowse.desc2 = "=================================================="
           tbrowse.tflag = "0".

    atotal = 0.
    btotal = 0.

    FOR EACH eg-request WHERE  eg-request.zinr = room-nr AND eg-request.opened-date >= fdate AND eg-request.opened-date <= tdate OR 
        eg-request.propertynr = prop-nr AND eg-request.closed-date >= fdate AND eg-request.closed-date <= tdate OR 
        eg-request.propertynr = prop-nr AND eg-request.process-date >= fdate AND eg-request.process-date <= tdate 
        USE-INDEX prop_ix NO-LOCK:
        
        FIND FIRST tprop WHERE tprop.nr = eg-request.propertynr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tprop THEN
        DO:
            FIND FIRST eg-property WHERE eg-property.nr = eg-request.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-property THEN nm-prop = eg-property.bezeich.
            ELSE nm-prop = "".

            CREATE tprop.
            ASSIGN tprop.nr = eg-request.propertynr
                   tprop.nm = nm-prop.
            char1 =  STRING(eg-request.propertynr , "->>>>>>9") + "  " + string(nm-prop, "x(30)")  + "  ".                
            char2 = "   " .

            CREATE tbrowse.
            ASSIGN tbrowse.desc1 = CHAR1
                   tbrowse.desc2 = char2
                   tbrowse.tflag = "0".
            CREATE tbrowse.
            ASSIGN tbrowse.desc1 = "--------------------------------------------------------------------------------"
                   tbrowse.desc2 = "--------------------------------------------------"
                   tbrowse.tflag = "0".

        END.

        
        IF eg-request.opened-date = ? THEN  a = "    -     ".
        ELSE a = STRING(eg-request.opened-date ,"99/99/99").

        IF eg-request.closed-date = ? THEN  b = "   -     ".
        ELSE b = STRING(eg-request.closed-date ,"99/99/99").

        IF eg-request.done-date = ? THEN  c =   "    -    ".
        ELSE c = STRING(eg-request.done-date ,"99/99/99").

        FIND FIRST eg-subtask WHERE eg-subtask.sub-CODE = eg-request.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN char4 = STRING(eg-subtask.bezeich , "x(36)").
        ELSE    char4 = "".

        char1 = "          Req No.  Open       Process    Done       Task                          ".  
        char2 = "Status ".
        CREATE tbrowse.
        ASSIGN tbrowse.desc1 = CHAR1
               tbrowse.desc2 = char2
               tbrowse.tflag = "0".
    
        CREATE tbrowse.        
        ASSIGN tbrowse.desc1 = "         -----------------------------------------------------------------------"
               tbrowse.desc2 = "--------------------------------------------------"
               tbrowse.tflag = "0".
        ASSIGN tbrowse.desc1 = "         -----------------------------------------------------------------------" /*"--------------------------------------------------------------------------------"*/
               tbrowse.desc2 = "--------------------------------------------------"
               tbrowse.tflag = "0".

        char1 =  "         " + STRING(eg-request.reqnr , "->>>>>>9") + "  " + string(a, "x(9)")  + "  " 
            + string(b,"x(9)")  + "  "  + string(c,"x(9)")  + "  "  + string(char4, "x(20)") + "   ". 
        char2 = string(int-str[eg-request.reqstatus], "x(10)") + "   " .



        CREATE tbrowse.
        ASSIGN tbrowse.desc1 = CHAR1
               tbrowse.desc2 = char2
               tbrowse.tflag = "1"
               tbrowse.reqno = STRING(eg-request.reqnr , "->>>>>>9")
               tbrowse.opend = string(a, "x(9)")
               tbrowse.processd = string(b,"x(9)") 
               tbrowse.doned =  string(c,"x(9)")
               tbrowse.subtask = string(char4, "x(30)") 
               tbrowse.reqstat = string(int-str[eg-request.reqstatus], "x(10)").

        FIND FIRST eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-queasy THEN
        DO:

            CREATE tbrowse.            
            ASSIGN tbrowse.desc1 = ""
                   tbrowse.desc2 = ""
                   tbrowse.tflag = "0". 

            CREATE tbrowse.                     
            ASSIGN tbrowse.desc1 = "        " + "           Art No.    Stock Article                  "
                   tbrowse.desc2 = "     QTY        Price              TOTAL          "
                   tbrowse.tflag = "0".
                                             
            CREATE tbrowse.        
            ASSIGN tbrowse.desc1 = "        " + "           -----------------------------------------------------------------------" 
                   tbrowse.desc2 = "--------------------------------------------------"
                   tbrowse.tflag = "0". 

            ASSIGN char2 = ""
                   char3 = "".
            FOR EACH eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = eg-request.reqnr NO-LOCK:
    
                FIND FIRST tbuff WHERE tbuff.artnr = eg-queasy.stock-nr NO-LOCK NO-ERROR.
                IF AVAILABLE tbuff THEN
                DO:
                    /*itotal  = eg-queasy.stock-qty * eg-queasy.price.*/
                    itotal  = eg-queasy.deci1 * eg-queasy.price.
    
                    char2 = "         " + "           " + string(eg-queasy.stock-nr, "9999999") + "    " + string(tbuff.bezeich ,"x(26)") + "   ".
                    /*char3 = STRING(eg-queasy.stock-qty ,"->>>>>>9") + "   " + STRING(eg-queasy.price, ">>>,>>>,>>9") + "   " +
                        STRING(itotal , ">>>,>>>,>>>,>>9") + "   " .*/

                    char3 = STRING(eg-queasy.deci1 ,"->>>>>>9") + "   " + STRING(eg-queasy.price, ">>>,>>>,>>9") + "   " +
                        STRING(itotal , ">>>,>>>,>>>,>>9") + "   " .
    
                    CREATE tbrowse.
                    ASSIGN tbrowse.desc1 = char2
                           tbrowse.desc2 = char3 
                           tbrowse.tflag = "1".
    
                    char2 = "".
                    char3 = "".
                END. 
                tot = tot + itotal.
            END.
        END.

        FIND FIRST eg-vperform WHERE eg-vperform.reqnr = eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-vperform THEN
        DO:
            CREATE tbrowse.            
            ASSIGN tbrowse.desc1 = ""
                   tbrowse.desc2 = "" 
                   tbrowse.tflag = "0".

            CREATE tbrowse.             
            ASSIGN tbrowse.desc1 = "        " + "           Outsource  Vendor                        "
                   tbrowse.desc2 = "Start Date      Finish Date        Price  "
                   tbrowse.tflag = "0".
                                             
            CREATE tbrowse.        
            ASSIGN tbrowse.desc1 = "        " + "           -----------------------------------------------------------------------" 
                   tbrowse.desc2 = "--------------------------------------------------" 
                   tbrowse.tflag = "0".

            ASSIGN char2 = ""
                   char3 = "".

            FOR EACH eg-vperform WHERE eg-vperform.reqnr = eg-request.reqnr NO-LOCK:
                FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr = eg-vperform.vendor-nr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-vendor THEN
                DO:
                    vendo-nm = eg-vendor.bezeich.
                END.
                ELSE
                DO:
                    vendo-nm = "Undefine".
                END.
                
                IF eg-vperform.startdate = ? THEN a = "    -    ".
                ELSE a = " " + STRING(eg-vperform.startdate , "99/99/99").
    
                IF eg-vperform.finishdate = ? THEN b = "      -     ".
                ELSE b = "    " + STRING(eg-vperform.finishdate , "99/99/99").
    
                CHAR2 = "         " + "           " +  string(eg-vperform.perform-nr, "9999999") + "    " + STRING(vendo-nm , "x(26)") + "  " .
                
                char3 =  a + "  " + 
                        b + "  " + STRING(eg-vperform.price , ">>>,>>>,>>>,>>9") + "  " .
    
                CREATE tbrowse.
                ASSIGN tbrowse.desc1 = CHAR2
                       tbrowse.desc2 = char3
                       tbrowse.tflag = "0".
    
                char2 = "".
                char3 = "".
                tot = tot + eg-vperform.price .
            END.
        END.
        
        IF tot NE 0 THEN
        DO:
            CREATE tbrowse.
            ASSIGN tbrowse.desc1 = "         -----------------------------------------------------------------------" /*"--------------------------------------------------------------------------------"*/
               tbrowse.desc2 = "--------------------------------------------------"
               tbrowse.tflag = "0".
            CREATE tbrowse.             
            ASSIGN tbrowse.desc1 = "                                                                "
                   tbrowse.desc2 = "                TOTAL     " + STRING(tot ,  ">>,>>>,>>>,>>9").
           CREATE tbrowse.             
            ASSIGN tbrowse.desc1 = "                                                                "
                   tbrowse.desc2 = "  ".
            btotal = btotal + tot .
            tot = 0.
        END.

     
    END.

    CREATE tbrowse.        
    ASSIGN tbrowse.desc1 = "==================================================================================" 
           tbrowse.desc2 = "==================================================" 
           tbrowse.tflag = "0".

    CREATE tbrowse.             
    ASSIGN tbrowse.desc1 = "                                                                "
           tbrowse.desc2 = "          GRAND TOTAL  " + STRING(btotal ,  ">,>>>,>>>,>>>,>>9").


    OPEN QUERY q3 FOR EACH tbrowse NO-LOCK.
END.
