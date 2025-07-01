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

DEF INPUT PARAMETER prop-nr AS INT.
DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR tbrowse.

DEF VAR atotal AS INTEGER.
DEF VAR btotal AS INTEGER.
DEF VAR tot AS INTEGER.
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

    char1 = " Req No.  Open       Process    Done       Object Task                           ".  
  /*char1 = " Req No.  Open       Process    Done       Sub task                              ".  */
    char2 = "Status ".

    FOR EACH tbrowse:
        DELETE tbrowse.
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

    /*FOR EACH eg-request WHERE eg-request.propertynr = prop-nr NO-LOCK BY eg-request.opened-date BY eg-request.reqnr :*/
    FOR EACH eg-request WHERE  eg-request.propertynr = prop-nr AND eg-request.opened-date >= fdate AND eg-request.opened-date <= tdate OR 
        eg-request.propertynr = prop-nr AND eg-request.closed-date >= fdate AND eg-request.closed-date <= tdate OR 
        eg-request.propertynr = prop-nr AND eg-request.process-date >= fdate AND eg-request.process-date <= tdate NO-LOCK:
        
        IF eg-request.opened-date = ? THEN  a = "    -     ".
        ELSE a = STRING(eg-request.opened-date ,"99/99/99").

        IF eg-request.closed-date = ? THEN  b = "   -     ".
        ELSE b = STRING(eg-request.closed-date ,"99/99/99").

        IF eg-request.done-date = ? THEN  c =   "    -    ".
        ELSE c = STRING(eg-request.done-date ,"99/99/99").

        FIND FIRST eg-subtask WHERE eg-subtask.sub-CODE = eg-request.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN char4 = STRING(eg-subtask.bezeich , "x(36)").
        ELSE    char4 = "".

        char1 =  STRING(eg-request.reqnr , "->>>>>>9") + "  " + string(a, "x(9)")  + "  " 
            + string(b,"x(9)")  + "  "  + string(c,"x(9)")  + "  "  + string(char4, "x(30)") + "   ". 
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
            ASSIGN tbrowse.desc1 = "           Art No.    Article                        "
                   tbrowse.desc2 = "     QTY        Price              TOTAL          "
                   tbrowse.tflag = "0".
                /*"QTY             Price              TOTAL"*/ .
                                             
            CREATE tbrowse.        
            ASSIGN tbrowse.desc1 = "           -----------------------------------------------------------------------" 
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
    
                    char2 = "           " + string(eg-queasy.stock-nr, "9999999") + "    " + string(tbuff.bezeich ,"x(36)") + "   ".
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
            ASSIGN tbrowse.desc1 = "           Outsource  Vendor                        "
                   tbrowse.desc2 = "Start Date      Finish Date        Price  "
                   tbrowse.tflag = "0".
                                             
            CREATE tbrowse.        
            ASSIGN tbrowse.desc1 = "           -----------------------------------------------------------------------" 
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
    
                CHAR2 = "           " +  string(eg-vperform.perform-nr, "9999999") + "    " + STRING(vendo-nm , "x(36)") + "  " .
                
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
        

        /*
        IF tot NE 0 THEN
            do:
                atotal = atotal + tot.
                DISP atotal tot .
            END.
        */
        IF tot NE 0 THEN
        DO:
            CREATE tbrowse.             
            ASSIGN tbrowse.desc1 = "                                                                "
                   tbrowse.desc2 = "                TOTAL     " + STRING(tot ,  ">>,>>>,>>>,>>9").

            btotal = btotal + tot .
            tot = 0.
        END.

     
    END.

        /*IF btotal NE 0 THEN
        DO:*/
            CREATE tbrowse.        
            ASSIGN tbrowse.desc1 = "==================================================================================" 
                   tbrowse.desc2 = "==================================================" 
                   tbrowse.tflag = "0".

            CREATE tbrowse.             
            ASSIGN tbrowse.desc1 = "                                                                "
                   tbrowse.desc2 = "          GRAND TOTAL  " + STRING(btotal ,  ">,>>>,>>>,>>>,>>9").

        /*END.    */

    OPEN QUERY q3 FOR EACH tbrowse NO-LOCK.
    /*ASSIGN fin1 = btotal .
    DISPLAY fin1 WITH FRAME frame1.*/
END.
