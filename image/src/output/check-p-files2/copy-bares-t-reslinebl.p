
DEF TEMP-TABLE t-resline LIKE bk-reser
    FIELD vorbereit LIKE bk-raum.vorbereit.

DEF INPUT  PARAMETER frdate AS DATE.
DEF INPUT  PARAMETER todate AS DATE.
DEF INPUT  PARAMETER rraum  AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-resline.

DEF BUFFER bkraum    FOR bk-raum.
DEF BUFFER resline   FOR bk-reser. 

FOR EACH resline WHERE resline.datum GE frdate AND resline.datum LE todate,
    FIRST bkraum WHERE bkraum.raum = resline.raum AND
    bkraum.lu-raum EQ rraum NO-LOCK :
    CREATE t-resline.
    BUFFER-COPY resline TO t-resline.
    ASSIGN t-resline.vorbereit = bkraum.vorbereit.
END.
