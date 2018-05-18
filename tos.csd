
<CsoundSynthesizer>
<CsInstruments>
sr = 44100
kr = 44100
ksmps = 1
nchnls = 2
0dbfs = 1.0

gifadein = 1
gifadeout = 1
gifadepercent = 0.05

; Diskin Mono
instr 1
  idur = p3
  iamp = p4
  SFilename = p5
  istart_time = p6
  imix = p7

  cigoto (idur > gifadein + gifadeout), fade
  igoto fadepercent

fade:
  ifadein = gifadein
  ifadeout = gifadeout
  goto cont

fadepercent:
  ifadein = idur * gifadepercent
  ifadeout = idur * gifadepercent
  goto cont

cont:
  ;aline linseg 0, ifadein, 1, idur - ifadeout, 1, ifadeout, 0
  aline linseg 0, ifadein, 1, idur - (ifadeout + ifadein), 0

  a0 diskin SFilename, 1, istart_time, 1, 0, 32
  a0 *= iamp
  a0 = a0 * aline
  outs a0 * imix, a0 * imix

  chnmix a0 * (1 - imix), "left"
  chnmix a0 * (1 - imix), "right"
endin

; Diskin Stereo player
instr 2
  idur = p3
  iamp = p4
  SFilename = p5
  istart_time = p6
  imix = p7

  cigoto (idur > gifadein + gifadeout), fade
  igoto fadepercent

fade:
  ifadein = gifadein
  ifadeout = gifadeout
  goto cont

fadepercent:
  ifadein = idur * gifadepercent
  ifadeout = idur * gifadepercent
  goto cont

cont:
  ;aline linseg 0, ifadein, 1, idur - ifadeout, 1, ifadeout, 0
  aline linseg 0, ifadein, 1, idur - (ifadeout + ifadein), 0

  a0, a1 diskin SFilename, 1, istart_time, 1, 0, 32
  a0 *= iamp
  a1 *= iamp
  a0 = a0 * aline
  a1 = a1 * aline
  outs a0 * imix, a1 * imix

  chnmix a0 * (1 - imix), "left"
  chnmix a1 * (1 - imix), "right"
endin

instr 100
  iamp = p4
  idelay_left = p5
  idelay_right = p6
  iroom_size = p7
  iHFDamp = p8

  a1 chnget "left"
  a2 chnget "right"

  a1 delay a1, idelay_left
  a2 delay a2, idelay_right

  a1, a2 freeverb a2, a1, iroom_size, iHFDamp
  outs a1 * iamp, a2 * iamp

  chnclear "left"
  chnclear "right"
endin


</CsInstruments>
<CsScore bin="python">
execfile('tos_score.py')
</CsScore>
</CsoundSynthesizer>
