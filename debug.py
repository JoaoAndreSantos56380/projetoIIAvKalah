from jogos import *
from kalah import *
from main import *
from tournament import *


eu = JogadorAlfaBeta("YO1", 4, won_seeds_diff)
eu2 = JogadorAlfaBeta("YO2", 4, won_seeds_diff2)
eu3 = JogadorAlfaBeta("YO3", 4, won_seeds_diff3)
ronaldo = JogadorAlfaBeta("roni", 4, teste)
broken = JogadorAlfaBeta("borken", 4, won_seeds_diff3)
chap = Chapiteau( "chap", 4)

jogo = Kalah(80)
print(joga11(jogo, ronaldo, broken, True))
#print(joga11(jogo, chap, ronaldo, True))

