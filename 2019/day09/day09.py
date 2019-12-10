from intcode import Intcode
from pyrsistent import pvector

p1 = Intcode('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
#print(1, p1.run(pvector([])))

p2 = Intcode('1102,34915192,34915192,7,4,7,99,0')
print(2, p2.run(pvector([])))

p3 = Intcode('104,1125899906842624,99')
#print(3, p3.run(pvector([])))
