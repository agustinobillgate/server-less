
DEFINE TEMP-TABLE r-list LIKE res-line
    FIELD select-flag AS LOGICAL INITIAL NO
.

DEFINE TEMP-TABLE tlist
    FIELD select-flag AS LOGICAL
    FIELD NAME        AS CHAR
    FIELD ankunft     AS DATE
    FIELD abreise     AS DATE
    FIELD zinr        AS CHAR
    FIELD kurzbez     AS CHAR
    FIELD zipreis     AS DECIMAL
    FIELD arrangement AS CHAR
    FIELD erwachs     AS INTEGER
    FIELD gratis      AS INTEGER
    FIELD kind1       AS INTEGER
    FIELD kind2       AS INTEGER
    FIELD resstatus   AS CHAR 
    FIELD zimmeranz   AS INTEGER
    FIELD anztage     AS INTEGER
.

DEFINE TEMP-TABLE t-zimkateg LIKE zimkateg.
DEFINE TEMP-TABLE buf-r-list LIKE r-list.


DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.  
DEFINE INPUT PARAMETER resNo        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sortType     AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR r-list.
DEFINE OUTPUT PARAMETER TABLE FOR tlist.


{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "move-resmember".

DEFINE VARIABLE stat-list AS CHAR EXTENT 14 FORMAT "x(9)" NO-UNDO. 
stat-list[1] = translateExtended ("Guaranted",lvCAREA,""). 
stat-list[2] = translateExtended ("6 PM",lvCAREA,""). 
stat-list[3] = translateExtended ("Tentative",lvCAREA,""). 
stat-list[4] = translateExtended ("WaitList",lvCAREA,""). 
stat-list[5] = translateExtended ("VerbalConfirm",lvCAREA,""). 
stat-list[6] = translateExtended ("Inhouse",lvCAREA,""). 
stat-list[7] = "". 
stat-list[8] = translateExtended ("Departed",lvCAREA,""). 
stat-list[9] = translateExtended ("Cancelled",lvCAREA,""). 
stat-list[10] = translateExtended ("NoShow",lvCAREA,""). 
stat-list[11] = translateExtended ("ShareRes",lvCAREA,""). 
stat-list[12] = translateExtended ("AccGuest",lvCAREA,""). 
stat-list[13] = translateExtended ("RmSharer",lvCAREA,""). 
stat-list[14] = translateExtended ("AccGuest",lvCAREA,""). 

DEFINE VARIABLE done AS LOGICAL NO-UNDO.


RUN move-resmemberbl.p(1, resNo, sortType, ?, INPUT TABLE buf-r-list, 
                       OUTPUT done, OUTPUT TABLE r-list).
RUN read-zimkategbl.p(4, ?, "", OUTPUT TABLE t-zimkateg).

FOR EACH r-list NO-LOCK,
  FIRST t-zimkateg WHERE t-zimkateg.zikatnr = r-list.zikatnr NO-LOCK
    BY r-list.zinr BY r-list.kontakt-nr BY r-list.resstatus:

    CREATE tlist.
    ASSIGN 
        tlist.select-flag   = r-list.select-flag
        tlist.NAME          = r-list.name
        tlist.ankunft       = r-list.ankunft
        tlist.abreise       = r-list.abreise 
        tlist.zinr          = r-list.zinr 
        tlist.kurzbez       = t-zimkateg.kurzbez
        tlist.zipreis       = r-list.zipreis
        tlist.arrangement   = r-list.arrangement
        tlist.erwachs       = r-list.erwachs
        tlist.gratis        = r-list.gratis 
        tlist.kind1         = r-list.kind1
        tlist.kind2         = r-list.kind2  
        tlist.resstatus     = stat-list[r-list.resstatus + r-list.l-zuordnung[3]]
        tlist.zimmeranz     = r-list.zimmeranz
        tlist.anztage       = r-list.anztage
      .
END.
