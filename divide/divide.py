from fastecdsa import curve
from fastecdsa.point import Point
import bit

G = curve.secp256k1.G
N = curve.secp256k1.q

def pub2point(pub_hex):
    x = int(pub_hex[2:66], 16)
    if len(pub_hex) < 70:
        y = bit.format.x_to_y(x, int(pub_hex[:2], 16) % 2)
    else:
        y = int(pub_hex[66:], 16)
    return Point(x, y, curve=curve.secp256k1)



# This function makes all the downscaled pubkeys obtained from subtracting
# numbers between 0 and divisor, before dividing the pubkeys by divisor.
def shiftdown(pubkey, divisor, file, convert=True):
    Q = pub2point(pubkey) if convert else pubkey
    print(Q, 'QQ')
    # k = 1/divisor
    k = pow(divisor, N - 2, N)
    for i in range(divisor+1):
        P = Q - (i * G)
        P = k * P
        if (P.y % 2 == 0):
            prefix = "02"
        else:
            prefix = "03"
        hx = hex(P.x)[2:].zfill(64)
        hy = hex(P.y)[2:].zfill(64)
        file.write(prefix+hx+"\n") # Writes compressed key to file

factor = 256
inputfile = "input.txt"
outputfile = "output.txt"
f = open(inputfile, "r")
outf = open(outputfile, "w")
line = f.readline().strip()
while line != '':
    shiftdown(line, factor, outf)
    line = f.readline().strip()