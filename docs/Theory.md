# Theory

## 1. Bitcoin

Bitcoin is a cryptocurrency that allows people to send value (in Bitcoin) to one another by recording transactions on a public distributed ledger called a blockchain. In this section, various aspects of Bitcoin technology will be explained including how Bitcoin uses public-private key cryptography to protect a users access to their funds, how Bitcoin transactions work, how they are verified and how a blockchain is used to store these transactions. This section will also include the details of how Bitcoin technology can be used to form payment channels between users and then how payment channels can be used to create a Lightning Network.

### 1.1 Elliptic Curve Cryptography
Elliptic curve cryptography makes use of maths on an elliptic curve using numbers defined over a finite field [2]. Figure \ref{fig:ecc_curve} shows the Bitcoin elliptic curve plotted over real-numbers. On such a curve, point scalar multiplication is easy to calculate but point scalar division is impossibly hard to calculate.

![Bitcoin Curve](figures/bitcoin_curve.png)

For example, if a publicly known generator point on the curve is $G=(g_x, g_y)$ and this point is then multiplied by a constant $k$ then another point on the curve can be found: $P=(p_x, p_y)$. Due to the fact that this maths is evaluated over a finite field, it is easy to find point $P$ if both $G$ and $k$ are known but it is not known how to calculate $k$ if $P$ and $G$ are known. This asymmetric property is illustrated in figure \ref{fig:asymmetry_eqn}.

![Public-private key asymmetric property](figures/ecc.jpg)

Bitcoin uses public-private key cryptography based on this asymmetric property \parencite{programming_bitcoin}. Each Bitcoin user has a private-key, $k$, which they use to produce a public-key, $P$. The public-key can be shared without the risk of an attacker being able to determine the private-key, $k$.

Bitcoin users can use their private-key to sign and therefore spend the outputs of transactions that were addressed to their public-key and anyone can see this signature and verify that it was produced by the person with access to the private-key that generated the public-key, $P$, and they can do this verification without knowing the private-key, $k$.

### 1.2 Transactions

Bitcoin coins are chains of transactions that represent changes in ownership of the coins. Each transaction is made up of inputs and outputs. The inputs of a transaction point to previously unspent transaction outputs and include a signature to sign the spending of these outputs. The outputs of a transaction include the public-key addresses to which the inputs should be paid to. These outputs will only be spendable by an entity who owns the private-key that produces the public-key in the output and this is done by creating a valid signature \parencite{mastering_bitcoin}.

Figure \ref{fig:transactions} shows an example of the transactions involved if a user, Alice, wanted to pay another user, Bob. In this example Alice has private-key $k1$ with which she produced her public-key, $P1$ and Bob has private-key, $k2$, with which he produced public-key, $P2$. To pay Bob, Alice creates transaction TX2. TX2 has an input that references the output of transaction TX1 and Alice is able to sign this input due to the fact that the output in TX1 is addressed to her public key, $P1$. Since she owns the private-key that produced $P1$ she is able produce a valid signature which Bob can then verify. Alice constructs the output of TX2 so that it is spendable by anyone who has the private-key corresponding to public-key $P2$ which in this case would enable Bob to spend this output.

![Public-private key asymmetric property](figures/transactions.jpg)


[1] Andreas M. Antonopoulos.Mastering Bitcoin. ISBN 9781491954386. O’ReillyMedia, 2017
[2] Jimmy Song.Programming Bitcoin. ISBN 9781492031499. O’Reilly Media, 2017
<!--stackedit_data:
eyJoaXN0b3J5IjpbMzM2MDM4NDczXX0=
-->