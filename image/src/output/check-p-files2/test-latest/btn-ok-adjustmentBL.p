
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER passwd    AS CHAR.
DEF INPUT PARAMETER id-str    AS CHAR.

create queasy. 
queasy.key = 8. 
queasy.date1 = TODAY. 
queasy.number1 = TIME. 
queasy.char1 = user-init. 
IF passwd NE id-str THEN queasy.char2 = id-str. 
release queasy. 
