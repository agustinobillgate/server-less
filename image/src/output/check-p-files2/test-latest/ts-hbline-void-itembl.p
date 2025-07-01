
DEF INPUT  PARAMETER menu-list-artnr AS INT.
DEF INPUT  PARAMETER dept            AS INT.
DEF OUTPUT PARAMETER betriebsnr      AS INT.
 
DEFINE BUFFER h-art       FOR vhp.h-artikel. 

FIND FIRST h-art WHERE h-art.artnr = menu-list-artnr
    AND h-art.departement = dept NO-LOCK. 
betriebsnr = h-art.betriebsnr.
