# Theory

## 1. Bitcoin

Bitcoin is a cryptocurrency that allows people to send value (in Bitcoin) to one another by recording transactions on a public distributed ledger called a blockchain. In this section, various aspects of Bitcoin technology will be explained including how Bitcoin uses public-private key cryptography to protect a users access to their funds, how Bitcoin transactions work, how they are verified and how a blockchain is used to store these transactions. This section will also include the details of how Bitcoin technology can be used to form payment channels between users and then how payment channels can be used to create a Lightning Network.

### 1.1 Elliptic Curve Cryptography
Elliptic curve cryptography makes use of maths on an elliptic curve using numbers defined over a finite field [2]. Figure \ref{fig:ecc_curve} shows the Bitcoin elliptic curve plotted over real-numbers. On such a curve, point scalar multiplication is easy to calculate but point scalar division is impossibly hard to calculate.

![Bitcoin Curve](figures/bitcoin_curve.png)

For example, if a publicly known generator point on the curve is $G=(g_x, g_y)$ and this point is then multiplied by a constant $k$ then another point on the curve can be found: $P=(p_x, p_y)$. Due to the fact that this maths is evaluated over a finite field, it is easy to find point $P$ if both $G$ and $k$ are known but it is not known how to calculate $k$ if $P$ and $G$ are known. This asymmetric property is illustrated in figure \ref{fig:asymmetry_eqn}.

![Public-private key asymmetric property](figures/ecc.jpg)



[1] Andreas M. Antonopoulos.Mastering Bitcoin. ISBN 9781491954386. O’ReillyMedia, 2017
[2] Jimmy Song.Programming Bitcoin. ISBN 9781492031499. O’Reilly Media, 2017
<!--stackedit_data:
eyJoaXN0b3J5IjpbNjgwNDg0OTU2XX0=
-->