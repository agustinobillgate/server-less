
DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEFINE TEMP-TABLE t-eg-location LIKE eg-location.

DEFINE TEMP-TABLE q1-list
    FIELD nr        LIKE eg-property.nr
    FIELD bezeich   LIKE eg-property.bezeich
    FIELD maintask  LIKE eg-property.maintask /*FD for web*/
    FIELD char3     LIKE eg-property.char3
    FIELD char2     LIKE eg-property.char2
    FIELD zinr      LIKE eg-property.zinr
    FIELD datum     LIKE eg-property.datum
    FIELD brand     LIKE eg-property.brand
    FIELD capacity  LIKE eg-property.capacity
    FIELD dimension LIKE eg-property.dimension
    FIELD TYPE      LIKE eg-property.TYPE
    FIELD price     /*LIKE eg-property.price*/ AS DECIMAL
    FIELD Spec      LIKE eg-property.Spec
    FIELD location  LIKE eg-property.location
    FIELD activeflag LIKE eg-property.activeflag.

DEF INPUT  PARAMETER user-init  AS CHAR. /*FD for web*/
DEF OUTPUT PARAMETER EngId      AS INT. /*FD for web*/
DEF OUTPUT PARAMETER GroupID    AS INT. /*FD for web*/
DEF OUTPUT PARAMETER store-number AS INT.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

RUN define-group.
RUN define-engineering.

FIND FIRST htparam WHERE paramnr = 1061 NO-LOCK.
IF htparam.finteger NE 0 THEN
DO:
  FIND FIRST l-lager WHERE l-lager.lager-nr = htparam.finteger NO-LOCK
    NO-ERROR.
  IF AVAILABLE l-lager THEN store-number = l-lager.lager-nr.
END.

/*modify by bernatd 2025 AC13FB */
/*FOR EACH eg-property NO-LOCK, 
    FIRST eg-Location WHERE eg-Location.nr = eg-property.location NO-LOCK, 
    FIRST queasy WHERE queasy.KEY = 133 
    AND queasy.number1 = eg-property.maintask NO-LOCK:
    CREATE q1-list.
    ASSIGN
    q1-list.nr        = eg-property.nr
    q1-list.bezeich   = eg-property.bezeich
    q1-list.maintask  = queasy.number1 /*FD for web*/
    q1-list.char3     = queasy.char1
    q1-list.char2     = eg-Location.bezeich
    q1-list.zinr      = eg-property.zinr
    q1-list.datum     = eg-property.datum
    q1-list.brand     = eg-property.brand
    q1-list.capacity  = eg-property.capacity
    q1-list.dimension = eg-property.dimension
    q1-list.TYPE      = eg-property.TYPE
    q1-list.price     = eg-property.price
    q1-list.Spec      = eg-property.spec /* Malik Serverless 686 change eg-property.Spec -> eg-property.spec */
    q1-list.location  = eg-property.location
    q1-list.activeflag = eg-property.activeflag.
END.
*/

FOR EACH eg-location:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.

FOR EACH queasy WHERE KEY = 133:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

/**************************************************************************************/
PROCEDURE define-group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END PROCEDURE.

PROCEDURE define-engineering:
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        ASSIGN EngID = 0.        
    END.
END PROCEDURE.
