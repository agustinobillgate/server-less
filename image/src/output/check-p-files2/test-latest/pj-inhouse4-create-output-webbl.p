DEFINE TEMP-TABLE inhouse-guest-list 
    FIELD flag          AS INTEGER 
    FIELD karteityp     AS INTEGER 
    FIELD nr            AS INTEGER   FORMAT ">>>9" 
    FIELD vip           AS CHAR      FORMAT "x(5)" 
    FIELD resnr         AS INTEGER   FORMAT ">>>>>9" 
    FIELD firstname     AS CHAR      FORMAT "x(32)" 
    FIELD lastname      AS CHAR      FORMAT "x(32)" 
    FIELD birthdate     AS CHAR      FORMAT "x(10)"
    FIELD groupname     AS CHAR      FORMAT "x(24)" 
    FIELD rmno          AS CHAR	  
    FIELD qty           AS INTEGER   FORMAT ">>9" 
    FIELD arrive        AS DATE 
    FIELD depart        AS DATE 
    FIELD rmcat         AS CHAR      FORMAT "x(6)" 
    FIELD ratecode      AS CHAR      FORMAT "x(15)"
    FIELD zipreis       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"
    FIELD kurzbez       AS CHAR 
    FIELD bezeich       AS CHAR 
    FIELD a             AS INTEGER   FORMAT "9" 
    FIELD c             AS INTEGER   FORMAT "9" 
    FIELD co            AS INTEGER   FORMAT ">9" 
    FIELD pax           AS CHAR      FORMAT "x(6)" 
    FIELD nat           AS CHAR      FORMAT "x(3)" 
    FIELD nation        AS CHAR 
    FIELD argt          AS CHAR      FORMAT "x(6)" 
    FIELD company       AS CHAR      FORMAT "x(18)" 
    FIELD flight        AS CHAR      FORMAT "x(6)" 
    FIELD etd           AS CHAR      FORMAT "99:99" 
    FIELD paym          AS INTEGER   FORMAT ">>9" 
    FIELD segm          AS CHAR      FORMAT "x(12)"
    FIELD telefon       AS CHAR      FORMAT "x(24)" 
    FIELD mobil-tel     AS CHAR      FORMAT "x(16)" 
    FIELD created       AS DATE      FORMAT "99/99/99"
    FIELD createID      AS CHAR      FORMAT "x(4)"
    FIELD bemerk        AS CHAR      FORMAT "x(100)"
    FIELD bemerk1       AS CHAR      FORMAT "x(32)" 
    FIELD ci-time       AS CHAR
    FIELD curr          AS CHAR      FORMAT "x(4)"
    FIELD inhousedate   AS DATE
    FIELD sob           AS CHAR      FORMAT "x(25)" 
    FIELD gastnr        AS INTEGER
    FIELD lodging       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD breakfast     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD lunch         AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
    FIELD dinner        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
    FIELD otherev       AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"       
    FIELD rechnr        AS INT            
    FIELD memberno      AS CHAR      FORMAT "x(15)"     
    FIELD membertype    AS CHAR      FORMAT "x(20)"     
    FIELD email         AS CHAR      FORMAT "x(30)"  
    FIELD localreg      AS CHAR      FORMAT "x(20)"  
    FIELD c-zipreis     AS CHAR      FORMAT "x(18)"
    FIELD c-lodging     AS CHAR     FORMAT "x(18)"
    FIELD c-breakfast   AS CHAR     FORMAT "x(18)"     
    FIELD c-lunch       AS CHAR     FORMAT "x(18)"    
    FIELD c-dinner      AS CHAR     FORMAT "x(18)"    
    FIELD c-otherev     AS CHAR     FORMAT "x(18)"
    FIELD c-a           AS CHAR  
    FIELD c-c           AS CHAR  
    FIELD c-co          AS CHAR  
    FIELD c-rechnr      AS CHAR  
    FIELD c-resnr       AS CHAR  
    FIELD night         AS CHAR     FORMAT "x(5)"
    FIELD city          AS CHAR     FORMAT "x(32)" 
    FIELD keycard       AS CHAR     FORMAT "x(6)"  
    FIELD co-time       AS CHAR                                     
    FIELD pay-art       AS CHAR     FORMAT "x(20)"
    FIELD etage         AS INTEGER
    FIELD zinr-bez      AS CHAR     /*Gerald 7E2311*/
    FIELD flag-guest    AS INTEGER  /*Gerald 7E2311*/
    . 

DEFINE INPUT PARAMETER idFlag       AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag    AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR inhouse-guest-list.

DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE htl-no    AS CHAR NO-UNDO.
DEFINE VARIABLE temp-char AS CHAR NO-UNDO.
DEFINE STREAM s1.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.


FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
  RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 

FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "Inhouse List" 
    AND queasy.number2 = INT(idFlag) NO-LOCK BY queasy.number1:

        ASSIGN counter = counter + 1.
        IF counter GT 1000 THEN LEAVE.
        
        CREATE inhouse-guest-list.
        ASSIGN
            
            inhouse-guest-list.bezeich     = ENTRY(1, queasy.char3, "|")
            inhouse-guest-list.bemerk      = ENTRY(2, queasy.char3, "|")       
            inhouse-guest-list.bemerk1     = ENTRY(3, queasy.char3, "|")    

            inhouse-guest-list.flag        = INTEGER(ENTRY(1, queasy.char2, "|"))
            inhouse-guest-list.karteityp   = INTEGER(ENTRY(2, queasy.char2, "|"))
            inhouse-guest-list.nr          = INTEGER(ENTRY(3, queasy.char2, "|"))
            inhouse-guest-list.vip         = ENTRY(4, queasy.char2, "|")
            inhouse-guest-list.resnr       = INTEGER(ENTRY(5, queasy.char2, "|"))
            inhouse-guest-list.firstname   = ENTRY(6, queasy.char2, "|")
            inhouse-guest-list.lastname    = ENTRY(7, queasy.char2, "|")
            inhouse-guest-list.birthdate   = ENTRY(8, queasy.char2, "|")
            inhouse-guest-list.groupname   = ENTRY(9, queasy.char2, "|")
            inhouse-guest-list.rmno        = ENTRY(10, queasy.char2, "|")
            inhouse-guest-list.qty         = INTEGER(ENTRY(11, queasy.char2, "|"))
            inhouse-guest-list.arrive      = DATE(ENTRY(12, queasy.char2, "|"))
            inhouse-guest-list.depart      = DATE(ENTRY(13, queasy.char2, "|"))
            inhouse-guest-list.rmcat       = ENTRY(14, queasy.char2, "|")
            inhouse-guest-list.ratecode    = ENTRY(15, queasy.char2, "|")
            inhouse-guest-list.zipreis     = DECIMAL(ENTRY(16, queasy.char2, "|"))
            inhouse-guest-list.kurzbez     = ENTRY(17, queasy.char2, "|")
            inhouse-guest-list.a           = INTEGER(ENTRY(18, queasy.char2, "|"))
            inhouse-guest-list.c           = INTEGER(ENTRY(19, queasy.char2, "|"))
            inhouse-guest-list.co          = INTEGER(ENTRY(20, queasy.char2, "|"))
            inhouse-guest-list.pax         = ENTRY(21, queasy.char2, "|")
            inhouse-guest-list.nat         = ENTRY(22, queasy.char2, "|")
            inhouse-guest-list.nation      = ENTRY(23, queasy.char2, "|")
            inhouse-guest-list.argt        = ENTRY(24, queasy.char2, "|")
            inhouse-guest-list.company     = ENTRY(25, queasy.char2, "|")
            inhouse-guest-list.flight      = ENTRY(26, queasy.char2, "|")
            inhouse-guest-list.etd         = ENTRY(27, queasy.char2, "|")
            inhouse-guest-list.paym        = INTEGER(ENTRY(28, queasy.char2, "|"))
            inhouse-guest-list.segm        = ENTRY(29, queasy.char2, "|")
            inhouse-guest-list.telefon     = ENTRY(30, queasy.char2, "|")
            inhouse-guest-list.mobil-tel   = ENTRY(31, queasy.char2, "|")
            inhouse-guest-list.created     = DATE(ENTRY(32, queasy.char2, "|"))
            inhouse-guest-list.createID    = ENTRY(33, queasy.char2, "|")           
            inhouse-guest-list.ci-time     = ENTRY(34, queasy.char2, "|")       
            inhouse-guest-list.curr        = ENTRY(35, queasy.char2, "|")       
            inhouse-guest-list.inhousedate = DATE(ENTRY(36, queasy.char2, "|"))
            inhouse-guest-list.sob         = ENTRY(37, queasy.char2, "|")       
            inhouse-guest-list.gastnr      = INTEGER(ENTRY(38, queasy.char2, "|"))
            inhouse-guest-list.lodging     = DECIMAL(ENTRY(39, queasy.char2, "|"))
            inhouse-guest-list.breakfast   = DECIMAL(ENTRY(40, queasy.char2, "|"))
            inhouse-guest-list.lunch       = DECIMAL(ENTRY(41, queasy.char2, "|"))
            inhouse-guest-list.dinner      = DECIMAL(ENTRY(42, queasy.char2, "|"))
            inhouse-guest-list.otherev     = DECIMAL(ENTRY(43, queasy.char2, "|"))
            inhouse-guest-list.rechnr      = INTEGER(ENTRY(44, queasy.char2, "|"))
            inhouse-guest-list.memberno    = ENTRY(45, queasy.char2, "|")       
            inhouse-guest-list.membertype  = ENTRY(46, queasy.char2, "|")       
            inhouse-guest-list.email       = ENTRY(47, queasy.char2, "|")       
            inhouse-guest-list.localreg    = ENTRY(48, queasy.char2, "|")       
            inhouse-guest-list.c-zipreis   = ENTRY(49, queasy.char2, "|")      
            inhouse-guest-list.c-lodging   = ENTRY(50, queasy.char2, "|")       
            inhouse-guest-list.c-breakfast = ENTRY(51, queasy.char2, "|")       
            inhouse-guest-list.c-lunch     = ENTRY(52, queasy.char2, "|")       
            inhouse-guest-list.c-dinner    = ENTRY(53, queasy.char2, "|")       
            inhouse-guest-list.c-otherev   = ENTRY(54, queasy.char2, "|")       
            inhouse-guest-list.c-a         = ENTRY(55, queasy.char2, "|")       
            inhouse-guest-list.c-c         = ENTRY(56, queasy.char2, "|")       
            inhouse-guest-list.c-co        = ENTRY(57, queasy.char2, "|")       
            inhouse-guest-list.c-rechnr    = ENTRY(58, queasy.char2, "|")       
            inhouse-guest-list.c-resnr     = ENTRY(59, queasy.char2, "|")       
            inhouse-guest-list.night       = ENTRY(60, queasy.char2, "|")       
            inhouse-guest-list.city        = ENTRY(61, queasy.char2, "|")       
            inhouse-guest-list.keycard     = ENTRY(62, queasy.char2, "|")       
            inhouse-guest-list.co-time     = ENTRY(63, queasy.char2, "|")       
            inhouse-guest-list.pay-art     = ENTRY(64, queasy.char2, "|")       
            inhouse-guest-list.etage       = INTEGER(ENTRY(65, queasy.char2, "|"))
            inhouse-guest-list.zinr-bez    = ENTRY(66, queasy.char2, "|")       
            inhouse-guest-list.flag-guest  = INTEGER(ENTRY(67, queasy.char2, "|"))
        .
        
        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE bqueasy.
        RELEASE bqueasy.
END.

FIND FIRST pqueasy WHERE pqueasy.KEY = 280 
    AND pqueasy.char1 = "Inhouse List"
    AND pqueasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN doneFlag = NO.
    /*MESSAGE "1" doneFlag VIEW-AS ALERT-BOX INFO.*/
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
        AND tqueasy.char1 = "Inhouse List" 
        AND tqueasy.number1 = 1
        AND tqueasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN doneFlag = NO.
        /*MESSAGE "2" doneFlag VIEW-AS ALERT-BOX INFO.*/
    END.
    ELSE DO: 
        ASSIGN doneFlag = YES.
        /*MESSAGE "3" doneFlag VIEW-AS ALERT-BOX INFO.*/
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
      AND tqueasy.char1 = "Inhouse List" 
      AND tqueasy.number1 = 0
      AND tqueasy.number2 = INT(idFlag) NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.

 


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 

