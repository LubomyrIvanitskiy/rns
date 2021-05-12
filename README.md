# Residual Number System Conversion (Python)

Given and integer number <b>X</b>, and a set of RNS moduli <img src="https://render.githubusercontent.com/render/math?math=P = {p_1, p_2, .., p_n}"> its RNS representation will be <img src="https://render.githubusercontent.com/render/math?math={x_1, x_2, ... x_n}"> where <img src="https://render.githubusercontent.com/render/math?math=x_i = X_i \mod p_i"> 

However there is no a trivial algoritm to convert the RNS representation back to the decimal
The most pipular methods are:
- Chinese Remainder Theorem
- Mixed Radix Convertion

Details can be found : https://www.semanticscholar.org/paper/The-Mixed-Radix-Chinese-Remainder-Theorem-and-Its-Bi-Gross/df77e4473f80fc9f9f7765f10d94df3328e58ccd

This repo suggest an alternative way of making RNS-Decimal convertion that works efficently for any given 'moduli' without any requirements to be co-prime.
Also it doesn't require the multiplicative inverse to exist

This algorithm is not yet documented, but it's in my TODO

More about RNS:
https://www.researchgate.net/publication/307174628_An_overview_of_Residue_Number_System

# Usage

```
import rns

n=14221 # an decimal number you want to convert to RNS
P=[21,19,18,11,10,8,7,5,4] #moduli
encoded = encode(n=n, P=P) # will return [4, 9, 1, 9, 1, 5, 4, 1, 1] which is equal to (n mod P) = [14221 % 21, 14221 % 19, ... 14221 % 4]
decoded = decode(code=encoded, P=P) # returns 14221
```

