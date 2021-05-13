# Residual Number System Conversion (Python)

Given and integer number <b>X</b>, and a set of RNS moduli <img src="https://render.githubusercontent.com/render/math?math=P = {p_1, p_2, .., p_n}"> its RNS representation will be <img src="https://render.githubusercontent.com/render/math?math={x_1, x_2, ... x_n}"> where <img src="https://render.githubusercontent.com/render/math?math=x_i = X_i \mod p_i"> 

However, there is no a trivial algoritm to convert the RNS representation back to the decimal

The most popular methods are:
- Chinese Remainder Theorem
- Mixed Radix Convertion

Details can be found : https://www.semanticscholar.org/paper/The-Mixed-Radix-Chinese-Remainder-Theorem-and-Its-Bi-Gross/df77e4473f80fc9f9f7765f10d94df3328e58ccd

However, this repo suggest an alternative recursion-based way of making RNS-Decimal convertion that works efficently <b>for any given 'moduli' without any requirements to be co-prime.</b>
Also it doesn't require the multiplicative inverse to exist

This algorithm is not yet documented, but it's in my TODO

More about RNS:
https://www.researchgate.net/publication/307174628_An_overview_of_Residue_Number_System


# Evaluation
Converting first 500 000 numbers forth and back (moduli = [3, 5, 11, 19, 23, 29]) :

- <b>Current Method: 3.15718150138855 sec </b>
- Chinese Reminder Theorem: 5.739054918289185 sec
# Usage

```
>>> from rns import encode, decode, get_dynamic_range, list_encodings
>>> P=[7,6,5]
>>> get_dynamic_range(P)
210
>>> n=78
>>> encode(n=n, P=P)
[1, 0, 3] # which is equal to (n mod P) = [78 % 7, 78 % 6, 78 % 5]
>>> decode(code=[1,0,3], P=P)
78
>>> for n, code in enumerate(list_encodings(P)):\
... print(n,'=',code)
...
0 = 000
1 = 111
2 = 222
3 = 333
4 = 444
5 = 550
6 = 601
7 = 012
8 = 123
9 = 234
10 = 340
11 = 451
12 = 502
13 = 613
14 = 024
15 = 130
16 = 241
17 = 352
18 = 403
19 = 514
20 = 620
21 = 031
22 = 142
...
```

