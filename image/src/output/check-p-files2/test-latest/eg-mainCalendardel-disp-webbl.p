
/*FD Dec 13, 2020 => BL for vhpweb based move from ui to BL*/
DEFINE TEMP-TABLE t-zimmer LIKE zimmer.

DEFINE TEMP-TABLE maintain
    FIELD maintainnr    AS INTEGER      FORMAT ">>>>>>9"
    FIELD workdate      AS DATE
    FIELD estworkdate   AS DATE
    FIELD donedate      AS DATE
    FIELD TYPE          AS INTEGER
    FIELD maintask      AS INTEGER
    FIELD location      AS INTEGER
    FIELD zinr          AS CHAR
    FIELD propertynr    AS INTEGER
    FIELD pic           AS INTEGER
    FIELD cancel-date   AS DATE
    FIELD cancel-time   AS INTEGER
    FIELD cancel-str    AS CHAR     FORMAT "x(24)"
    FIELD cancel-by     AS CHAR
    FIELD categnr       AS INTEGER

    INDEX alldatum  estworkdate workdate.

DEFINE TEMP-TABLE smaintain
    FIELD maintainnr    AS INTEGER      FORMAT ">>>>>>9"
    FIELD workdate      AS DATE
    FIELD estworkdate   AS DATE
    FIELD stat-nr       AS INTEGER
    FIELD stat-nm       AS CHAR         FORMAT "x(24)"
    FIELD categ-nr      AS INTEGER
    FIELD categ-nm      AS CHAR         FORMAT "x(24)"
    FIELD main-nr       AS INTEGER
    FIELD main-nm       AS CHAR         FORMAT "x(24)"
    FIELD loc-nr        AS INTEGER
    FIELD loc-nm        AS CHAR         FORMAT "x(24)"
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR         FORMAT "x(40)"
    FIELD pzinr         AS CHAR         FORMAT "x(24)"
    FIELD pic-nr        AS INTEGER
    FIELD pic-nm        AS CHAR         FORMAT "x(24)"
    FIELD str           AS CHAR         FORMAT "x(2)" INITIAL ""
    FIELD rec           AS CHAR         FORMAT "x(2)" INITIAL ""
    FIELD cancel-date   AS DATE
    FIELD cancel-time   AS INTEGER
    FIELD cancel-str    AS CHAR         FORMAT "x(24)"
    FIELD cancel-by     AS CHAR

    INDEX alldatum  estworkdate workdate.

DEFINE TEMP-TABLE tproperty
    FIELD prop-nr AS INTEGER
    FIELD prop-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object Item"
    FIELD prop-selected AS LOGICAL INITIAL NO
    FIELD pcateg-nr AS INTEGER
    FIELD pcateg AS CHAR
    FIELD pmain-nr AS INTEGER
    FIELD pmain AS CHAR
    FIELD ploc-nr AS INTEGER
    FIELD ploc  AS CHAR
    FIELD pzinr    AS CHAR.

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tpic
    FIELD pic-nr AS INTEGER
    FIELD pic-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Pic"
    FIELD pic-selected AS LOGICAL INITIAL NO
    FIELD pic-Dept AS INTEGER.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr AS INTEGER
    FIELD stat-nm AS CHAR       FORMAT "x(24)"
    FIELD stat-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE dept-link 
    FIELD dept-nr AS INTEGER
    FIELD dept-nm AS CHAR.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest    AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR  FORMAT "x(24)"
    FIELD categ-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE t-eg-maintain LIKE eg-maintain.

DEFINE INPUT PARAMETER from-date AS DATE.   
DEFINE INPUT PARAMETER to-date   AS DATE.    
DEFINE INPUT PARAMETER user-init AS CHAR.   
DEFINE INPUT PARAMETER all-room  AS LOGICAL. 
DEFINE OUTPUT PARAMETER GroupID  AS INT.
DEFINE OUTPUT PARAMETER EngID    AS INT.
DEFINE OUTPUT PARAMETER p-992    AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR smaintain.
/*
DEFINE VARIABLE from-date AS DATE INIT 01/11/21.   
DEFINE VARIABLE to-date   AS DATE INIT 01/11/21.    
DEFINE VARIABLE user-init AS CHAR INIT "01".   
DEFINE VARIABLE all-room  AS LOGICAL INIT YES. 
DEFINE VARIABLE GroupID  AS INT.
DEFINE VARIABLE EngID    AS INT.
DEFINE VARIABLE p-992    AS LOGICAL.
*/
DEFINE VARIABLE selected-date as DATE NO-UNDO.

RUN eg-maincalendardel-gobl.p
    (from-date, to-date, user-init, all-room,
    OUTPUT GroupID, OUTPUT EngID, OUTPUT p-992,
    OUTPUT TABLE maintain, OUTPUT TABLE tproperty,
    OUTPUT TABLE troom, OUTPUT TABLE tMaintask,
    OUTPUT TABLE tpic, OUTPUT TABLE tStatus,
    OUTPUT TABLE dept-link, OUTPUT TABLE tLocation,
    OUTPUT TABLE tcategory, OUTPUT TABLE t-eg-maintain,
    OUTPUT TABLE t-zimmer).

RUN fill-maintain.
/***************************************************************************************/
PROCEDURE fill-maintain:    
    FOR EACH maintain USE-INDEX alldatum NO-LOCK,
        FIRST tStatus WHERE tStatus.stat-nr = maintain.TYPE NO-LOCK,
        FIRST tmaintask WHERE tmaintask.main-nr = maintain.maintask NO-LOCK,
        FIRST tlocation WHERE tlocation.loc-nr= maintain.location NO-LOCK,
        FIRST tproperty WHERE tproperty.prop-nr = maintain.propertynr NO-LOCK,
        FIRST tpic WHERE tpic.pic-nr = maintain.pic NO-LOCK,
        FIRST tcategory WHERE tcategory.categ-nr = maintain.categnr.

        RUN create-temp.
    END.      
END PROCEDURE.

PROCEDURE create-temp:
    CREATE smaintain.
    ASSIGN 
        smaintain.maintainnr     = maintain.maintainnr
        smaintain.workdate       = maintain.workdate
        smaintain.estworkdate    = maintain.estworkdate
        smaintain.stat-nr        = maintain.TYPE
        smaintain.stat-nm        = tStatus.stat-nm
        smaintain.main-nr        = maintain.maintask
        smaintain.main-nm        = tmaintask.main-nm
        smaintain.loc-nr         = maintain.location
        smaintain.loc-nm         = tlocation.loc-nm
        smaintain.prop-nr        = maintain.propertynr
        smaintain.prop-nm        = tproperty.prop-nm + "(" + trim(string(maintain.propertynr , ">>>>>>9")) + ")"
        smaintain.pzinr          = maintain.zinr 
        smaintain.pic-nr         = maintain.pic
        smaintain.pic-nm         = tpic.pic-nm 
        smaintain.cancel-date    = maintain.cancel-date
        smaintain.cancel-time    = maintain.cancel-time
        smaintain.cancel-str     = maintain.cancel-str
        smaintain.cancel-by      = maintain.cancel-by
        smaintain.categ-nr       = maintain.categnr
        smaintain.categ-nm       = tcategory.categ-nm
    .          
END PROCEDURE.

