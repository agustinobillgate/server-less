
DEF INPUT PARAMETER lresnr AS INT.
DEF OUTPUT PARAMETER sorttype AS INT.

DEFINE BUFFER rline FOR res-line.     
FIND FIRST rline WHERE rline.resnr = lresnr AND rline.active-flag LE 1 
  NO-LOCK. 
sorttype = rline.active-flag + 1. 
