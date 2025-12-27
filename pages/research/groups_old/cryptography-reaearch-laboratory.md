<!-- ---
layout: page_research
title: Cryptography Research Laboratory
code: crl
permalink: /research/cryptography-research-laboratory/
navbar_active: Research
page_banner: images/banners/cryptography-research-banner.jpg
---

### Distinguished Collaborators

- Dr. Chai Wen Chuah, Tun Hussein Onn University of Malaysia, Malaysia
- Professor C. Pandu Rangan, Indian Institute of Technology Madras, India
- Dr. Gyu Myoung Lee, Liverpool John Moores University, UK
- Dr. Taechan Kim, Seoul, South Korea
- Dr. Tatsuaki Okamoto, NTT Research, Inc., USA
- Dr. Qinyi Li, Griffith University, Australia

### Research Projects

##### CRL2021(P2)
- Project: On leakage-resilient quantum-safe cryptography
- Grant: N/A. Ongoing since 2021
- Investigators: Dr. Qinyi Li, Dr. Janaka Alawatugoda
- Abstract:

At present providing quantum-safe security for systems became a major requirement to realize as existing secured cryptosystems may not survive after 30 years when quantum computers become a reality. Even though the existing quantum-safe cryptosystems are provably secure in theory, their security against side-channel (leakage) attacks may be problematic. In this research, we aim to construct leakage-resilient and quantum-safe cryptographic constructions.

##### 21-021 RG/MATHS/AS_1-FR3240319461
- Project: On stronger authenticated key exchange over the Internet
- Grant: 2021 UNESCO-TWAS Research Grant for Individual Scientists (Grant No: 21-021 RG/MATHS/AS_I-FR3240319461), November 2021 to November 2023 (Ongoing).
- Investigators: Dr. Janaka Alawatugoda (PI), Dr. Taechan Kim (collaborator), Dr. Tatsuaki Okamoto (collaborator)
- Abstract:

Security models for two-party authenticated key exchange (AKE) protocols have been developed over the years to address various attack scenarios against AKE protocols. The extended Canetti–Krawczyk (eCK) security model is widely used to provide security arguments for AKE protocols because of its clear definitions of security as well as advanced adversarial capabilities. Most of the eCK-secure AKE protocols are proven to be secure in the random oracle model (ROM). The ROM is an ideal-world assumption, whereas the standard model captures the real-world assumptions. In this project, we investigate different security improvements on AKE protocols, such as leakage resiliency, secure pairing-based constructions, etc. Our aim is to come up with new provable-secure protocol constructions in the standard model.

##### E15-FYP (Gr13)
- Project: Design of surveillance and censorship-resistant communication mechanism over the internet
- Grant: N/A. Ongoing since 2020
- Investigators: Dr. Janaka Alawatugoda. The research idea is from E15 batch Computer Engineering students Rishikeshan Lavakumar, Pasan Tennakoon, and Supipi Karunathilaka.
- Abstract:

Surveillance and censorship-resistant communication have been interesting topics in online communication. In this research, we report the shortcomings of modern centralized architecture-based communication. Then we explore design techniques that protect users’ privacy. Under design techniques, we explain how distributed and decentralized systems provide the privacy that users envy along with NAT navigation techniques and methods of safeguarding privacy and anonymity in communication. Then we present our design of a hybrid decentralized communication system and utilize this to establish DTLS tunnels to maintain connectivity among devices behind NAT. Design covers explicit details of the communication protocols designed for connection establishment, communication, tunnel establishment, and connection termination. Then we present our experiments and results to measure the performance of the system in a real environment. Then we conclude the research along with the results and the shortcomings of the current design.

- Project Page: [Link](https://projects.ce.pdn.ac.lk/4yp/e15/anonymous-authentication)

##### H082
- Project: Analysing side-channel attacks on key exchange protocols
- Grant: Tier 01 Internal Research Grant of Research Management Centre, Tun Hussein Onn University of Malaysia (Grant No: H082), July 2018 to July 2020 (Completed).
- Investigators: Dr. Chai Wen Chuah (PI), Dr. P. Siva Shamala Palaniappan, Dr. Sofia Najwa Binti Ramli, and Dr. Janaka Alawatugoda (external researcher).
- Abstract:

Typically, secure channels are constructed from an authenticated key exchange (AKE) protocol, which authenticates the communicating parties based on long-term public keys and establishes secret session keys, and a secure data transmission layer that uses the secret session keys to encrypt transmitted data. Particularly, in the real-world scenario, the TLS/SSL protocol suite is used for this purpose. First, the TLS/SSL handshake protocol exchanges a secret key (session key). Thereafter the TLS/SSL record protocol uses that session key to encrypt data. During the handshake protocol, both parties agree on an algorithm to encrypt data in the TLS/SSL record layer. During the past two decades, side-channel attacks become a popular method of attacking various cryptographic implementations. Side-channel attacks use the leakage of secret parameters due to the execution of the real-world implementation, to break the underlying cryptographic primitive.

In this research, we aim to address the partial leakage of long-term secret keys, ephemeral secret keys, and session keys of protocol participants, due to various side-channel attacks. Partial leakage of long-term secret keys, ephemeral secret keys, and session keys can negatively affect the security of channel establishment and data transmission. Security models for two-party AKE protocols have developed over time to provide security, even when the adversary learns certain secret values. In this work, we will advance the modeling of security for AKE protocols by considering more granular partial leakage of long-term secret keys, ephemeral secret keys, and session keys of protocol participants. Then we will construct AKE protocols that can be proven secure in the advanced security models. Thus, our project will be helpful to construct leakage-resilient protocol suites for future communication.

- Project Page: [link](http://www.ce.pdn.ac.lk/2019/06/10/on-implementing-eck-secure-key-exchange-protocol-for-openssl/)


##### URG2018/19/E
- Project: Power analysis attacks on Trivium stream cipher
- Grant: 2018 University Research Grant of University of Peradeniya, Sri Lanka (Grant No: URG 2018/19/E), November 2018 to November 2019 (Completed).
- Investigators: Dr. Janaka Alawatugoda (PI) and Dr. Chai Wen Chuah (foreign collaborator).
- Abstract:

Power analysis attacks are a relatively new type of attack which measures and analyses the power consumption of electronic circuits to extract secret information. These attacks have become a huge threat to the security of embedded systems. Therefore, identifying ciphers which are vulnerable against these type of attacks and developing countermeasures is of paramount importance. Many studies have been done on this topic. However, most of them are on block ciphers. This research focuses on an attack done on Trivium, which is a stream cipher. Correlation power analysis (CPA) is used in this attack to analyze the power consumption of the cryptosystem and figure out the secret key.
- Github Page: [Link](https://github.com/MalithaDilshan/Power-Analysis-Attack-on-Trivium)
- Project Page: [Link](https://projects.ce.pdn.ac.lk/4yp/e13/power-analysis-attack-on-trivium-stream-cipher)

##### NRC 16-020
- Project: Implementing server/client-side countermeasures against compression-based side-channel attacks
- Grant: 2016 Investigator Driven Research Grant of National Research Council–Sri Lanka (Grant No: NRC 16-020), July 2016 to July 2017 (Completed).
- Investigators: Dr. Janaka Alawatugoda (PI) and Professor Roshan G. Ragel (mentor).
- Abstract:

As the Internet developed, more and more computers and private networks are connected to the Internet. Since the Internet is a public resource, the security of the information exchanges via the Internet is not guaranteed. Therefore, ensuring the security of the information becomes an important task. Cryptography is engaged with communication systems to enforce the security of the information by establishing a secure channel for communication. A secure channel ensures that no third party can see or modify the actual messages that are being transferred. In the real world, Transport Layer Security/Secure Socket Layer (TLS/SSL) protocol suites are used for this purpose. First, the “TLS/SSL handshake protocol” exchanges a secret session key. After that, the “TLS/SSL record protocol” uses a secret session key to encrypt the messages.

In the key exchange phase (handshake protocol), various secret keys of communicating parties can be leaked to the attacker, and in the message transmission phase (record protocol), the secret session keys, as well as the plaintext messages can be leaked to the attacker, due to various side-channel attacks. Much research has been carried out in analyzing the leakage of

(1)—various secret keys in the key exchange phase, and

(2)—secret session keys in the message transmission phase.

Relatively less research has been carried out in analyzing the leakage of plaintext messages in the message transmission phase. In this research, our aim is to address this research gap and deploy necessary server/client-side countermeasures to the TLS/SSL protocol suite, in order to protect the plaintext messages from side-channel attacks. Although compression is desirable for network applications as it saves bandwidth, when data is compressed before being encrypted, the amount of compression leaks information about the quantity of redundancy in the plaintext. This side-channel has led to successful CRIME and BREACH attacks on web traffic protected by the TLS/SSL protocols.

The obvious mitigation technique is to eliminate data compression before the encryption, which is not desirable as it will waste the communication bandwidth. There are a number of mitigation techniques proposed by Gluck et al. [GHP13], without formal security arguments. In 2015, Alawatugoda et al. [ASB15] formally proved the security of one mitigation technique proposed by Gluck et al, as well as proposed a new proven secure mitigation technique; separating secrets from user inputs and fixed-dictionary compression, respectively. Currently, it is an open research question to adopt the proven secure mitigation techniques against compression-based side-channel attacks with real-world security protocol suites such as TLS/SSL protocol suites.

- Project Page: [Link](https://projects.ce.pdn.ac.lk/4yp/e12/implementing-a-proven-secure-and-cost-effective-countermeasure) -->
