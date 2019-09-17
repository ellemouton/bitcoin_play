# Theory

## 1. Bitcoin

Bitcoin is a cryptocurrency that allows people to send value (in Bitcoin) to one another by recording transactions on a public distributed ledger called a blockchain. In this section, various aspects of Bitcoin technology will be explained including how Bitcoin uses public-private key cryptography to protect a users access to their funds, how Bitcoin transactions work, how they are verified and how a blockchain is used to store these transactions. This section will also include the details of how Bitcoin technology can be used to form payment channels between users and then how payment channels can be used to create a Lightning Network.

### 1.1 Elliptic Curve Cryptography
Elliptic curve cryptography makes use of maths on an elliptic curve using numbers defined over a finite field [2]. Figure \ref{fig:ecc_curve} shows the Bitcoin elliptic curve plotted over real-numbers. On such a curve, point scalar multiplication is easy to calculate but point scalar division is impossibly hard to calculate.

![Bitcoin Curve](figures/bitcoin_curve.png)

For example, if a publicly known generator point on the curve is $G=(g_x, g_y)$ and this point is then multiplied by a constant $k$ then another point on the curve can be found: $P=(p_x, p_y)$. Due to the fact that this maths is evaluated over a finite field, it is easy to find point $P$ if both $G$ and $k$ are known but it is not known how to calculate $k$ if $P$ and $G$ are known. This asymmetric property is illustrated in figure \ref{fig:asymmetry_eqn}.

![Public-private key asymmetric property](figures/eec.jpg)

Bitcoin uses public-private key cryptography based on this asymmetric property \parencite{programming_bitcoin}. Each Bitcoin user has a private-key, $k$, which they use to produce a public-key, $P$. The public-key can be shared without the risk of an attacker being able to determine the private-key, $k$.

Bitcoin users can use their private-key to sign and therefore spend the outputs of transactions that were addressed to their public-key and anyone can see this signature and verify that it was produced by the person with access to the private-key that generated the public-key, $P$, and they can do this verification without knowing the private-key, $k$.

### 1.2 Transactions

Bitcoin coins are chains of transactions that represent changes in ownership of the coins. Each transaction is made up of inputs and outputs. The inputs of a transaction point to previously unspent transaction outputs and include a signature to sign the spending of these outputs. The outputs of a transaction include the public-key addresses to which the inputs should be paid to. These outputs will only be spendable by an entity who owns the private-key that produces the public-key in the output and this is done by creating a valid signature \parencite{mastering_bitcoin}.

Figure \ref{fig:transactions} shows an example of the transactions involved if a user, Alice, wanted to pay another user, Bob. In this example Alice has private-key $k1$ with which she produced her public-key, $P1$ and Bob has private-key, $k2$, with which he produced public-key, $P2$. To pay Bob, Alice creates transaction TX2. TX2 has an input that references the output of transaction TX1 and Alice is able to sign this input due to the fact that the output in TX1 is addressed to her public key, $P1$. Since she owns the private-key that produced $P1$ she is able produce a valid signature which Bob can then verify. Alice constructs the output of TX2 so that it is spendable by anyone who has the private-key corresponding to public-key $P2$ which in this case would enable Bob to spend this output.

![Transactions](figures/transactions.jpg)

A different type of transaction called a multi-signature (multi-sig) transaction can also be formed. The output of such a transaction would require multiple signatures in order to be valid. Figure \ref{fig:multisig_tx} shows an example of such a transaction. In this example, the multi-sig transaction is transaction TX2 and the parties involved are Alice, with keys $P1$ and $k1$, and Bob, with keys $P2$ and $k2$. This transaction has two inputs, one of which references an output spendable by Alice and the other an output spendable by Bob. The output of the transaction is a 2-of-2 multi-sig script than is only spendable if the input that references it is signed by both Alice and Bob \parencite{mastering_bitcoin}\parencite{programming_bitcoin}. This type of transaction forms the basis of payment channels which are explained in section \ref{sec:pay_chan}.

![Multi-sig Transaction](figures/multisig_tx.png)

### 1.3 Blockchain

For a Bitcoin transaction to be valid, it must be broadcast to the entire Bitcoin network and this is done by including transactions in the blocks of a public blockchain. This enables any user of the system to validate any transaction and trace back the origins of the transaction inputs as can be seen in figure \ref{fig:blockchain}. For a transaction to be included into a block and mined,  it is necessary to incentives the miners by means of transaction fees. In the Bitcoin network, it takes approximately 10 minutes for a block to be mined and added to the blockchain. For these reasons publishing a transaction on the blockchain (an on-chain transaction) is both costly and slow. Using on-chain transactions for micropayment transactions is thus not feasible nor scalable \parencite{mastering_bitcoin}. Payment channels provide a way to perform fast and cheap off-chain transactions and these are discussed next.

![Blockchain](figures/blockchain.jpg)

### 1.4 Payment Channels
Payment channels provide a way for two parties to exchange an unlimited number of Bitcoin transactions and do so off-chain. In this section, the aim is to explain the basic setup and use of a payment channel. All details of these steps can be found in reference \parencite{mastering_bitcoin}.

#### Step 1 
Two parties, $A$ and $B$, decide to set up a payment channel and do this by each of them committing funds to a 2-of-2 multisig (see section \ref{sec:transactions}). Both parties sign this transaction and then broadcast it to the blockchain as an on-chain, funding transaction. This transaction and the future settlement transaction will be the only two transactions that need to be published to the blockchain. In the example in figure \ref{fig:pay_chan_1}, $A$ commits 10 satoshis and $B$ commits 5 satoshis to the channel.

![Payment channels step 1](figures/payment_channels/pay_chan_1.png)

#### Step 12
Two parties, $A$ and $B$, decide to set up a payment channel and do this by each of them committing funds to a 2-of-2 multisig (see section \ref{sec:transactions}). Both parties sign this transaction and then broadcast it to the blockchain as an on-chain, funding transaction. This transaction and the future settlement transaction will be the only two transactions that need to be published to the blockchain. In the example in figure \ref{fig:pay_chan_1}, $A$ commits 10 satoshis and $B$ commits 5 satoshis to the channel.

![Payment channels step 1](figures/payment_channels/pay_chan_1.png)

[1] Andreas M. Antonopoulos.Mastering Bitcoin. ISBN 9781491954386. O’ReillyMedia, 2017

[2] Jimmy Song.Programming Bitcoin. ISBN 9781492031499. O’Reilly Media, 2017
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg2NDQyNTA4MCwxODU1NzY5NTYzXX0=
-->