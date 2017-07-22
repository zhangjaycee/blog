---
layout: post
title: 美剧《硅谷》中的去中心化“全新互联网”现实中已经存在（翻译）
tags: 翻译 区块链 存储 去中心化 美剧
categories: Storage
---

原文：The technology to make 'Silicon Valley's' decentralized 'new internet' already exists( http://mashable.com/2017/04/24/is-silicon-valley-new-internet-possible-or-not/#6cEY_p263PqN )

作者：RAYMOND WONG
时间：APR 25, 2017

___


> “给你无限的时间和资源，你想用你的压缩算法做出什么都行……什么都行，说出来是什么，3，2，1……说！”美剧《硅谷第四季》中的“变态”亿万富翁Russ Hanneman对主角Richard Hendricks喊道。
>
> “一个全新的互联网”，可爱的程序猿Richard说。
>
>“我们曾用一台掌上电脑的计算能力把一个人放在月球上”，Richard继续说道，“我们现在手机上的计算能力要比那强几十万倍，但这些手机却都只是躺在口袋里什么都不做。所以我想到这个，有数十亿的手机在世界各地拥有相同的计算能力，只是闲在人们的口袋里。“
>
>“然后我想，如果我们使用这些手机来构建一个庞大的网络呢？使用我的压缩算法来使一切数据变得很小，高效，到处传播。如果我们能做到这一点，我们可以建立一个完全去中心化的网络，那将是没有防火墙，没有收费，没有政府监管，没有间谍的互联网。信息因此在各种意义下都将是完全自由的。“
>
>Russ不仅喜欢这个看似疯狂的想法，还答应投资。Russ还分解了Richard的数据压缩初创公司Pied Piper，迫使他退出，以便让他弄清楚如何将“新互联网”变成现实。
>
>“我不知道是否可行”，Richard承认，“我还没有仔细去想过。”


这正是观看剧集的粉丝们一直想知道的， Richard的“新互联网”到底是真的可能呢，还是只是电视上编造的？

当今的互联网是去中心化和中心化的混合体。 任何人都可以创建一个去中心化的点对点(P2P)网络，让设备间直接连接，比如BitTorrent。同时，任何人也可以去创建一个中心式网络，通过服务器传递数据，多数大型在线服务都是如此，如Google，Facebook和Twitter。

加密的、去中心化的网络的好处是显而易见的：安全性和隐私性。 由于数据在分散的网络节点上存储和传递，没有任何在线服务或者政府可以在你不知情的情况下窥探你的数据。

### Mesh Network

理论上，可以有几种方式来构建这个“新互联网”。 第一个是Mesh Network（网状网络），它是由任意数量的设备或节点组成，数据在节点之间传递。手机应用Firechat是使用mesh network的完美示例，它通过蓝牙让手机间相互连接。

事实上，一些狂热的reddit用户在《硅谷》下一集的预告视频中Richard的白板涂鸦上发现了一些线索，表明剧中他至少考虑了mesh network。使用mesh network并依赖蓝牙等无线协议的缺点当然是较小的覆盖范围和较慢的传输速度。你的设备与其他设备的连接质量要取决于各个设备的蓝牙规格。虽然你可以通过你和你要连接的设备的路径中间有其他节点“中继”来解决这个问题，但并无法保证每次都有中间节点。

另一方面，蓝牙4.0只有200英尺的范围，蓝牙5.0的新设备也能达到800英尺。此外，蓝牙5.0将带宽从4.0的25Mbps提高到50Mbps。虽然不如千兆的Wi-Fi或LTE，但嘿，隐私和安全更比速度更重要，对吧？ 也就是说，剧中Richard的能“使一切都变小，高效”的超级强大的压缩算法，将是使mesh network成为可能的特殊要素。

### Maidsafe & Storj

Richard实现他宏伟计划的另一种可行方式，是像Maidsafe的SAFE网络或Storj的P2P网络。虽然它们仅用于去中心化的文件存储，但我并不认为像Richard那样的代码狂人无法调整这些结构。SAFE网络自称为“新的去中心化互联网”，很大程度上承诺了Richard的想法，只不过它没有使用闲置的手机计算资源，而是使用的PC。

根据该公司的说明，用户可以无须验证地创建一个帐户，然后决定贡献分配给SAFE网络的空间。 然后，Maidsafe会向贡献存储空间的用户支付“Safecoins”（一种具有真实市场价值的加密虚拟货币）。用户向“vault”贡献越多的存储空间，就会得到越多的Safecoins。Maidsafe以此来进一步激励用户加入SAFE网络。

在文件被上传之前，它被先被加密，然后分解成较小的数据包并分散到网络中去。数据存储是存在冗余的，并且在计算机打开时，文件会在网络上自主移动。简单说，“新互联网”上所有的数据都是分块、加密存储在所有设备上的。在网络上所有设备上的碎片加密件中。 当你需要访问自己的数据时，只需从其他设备下载各部分就可以了，这基本上就和BitTorrent一样了。

SAFE网络现在只是在进行alpha测试，但是更接近公开发布。 虽然它只适用于Windows/Mac/Linux，但公司未来也会考虑移动平台。去年在TechCrunch上，Maidsafe创始人David Irvin曾表示，对于核心功能vault，“让人们只在手机上使用效果不够好”。另外，利用手机未使用的计算能力将是显著减少手机的续航时间，可能需要接入电源或连接充电宝才更好。

### IPFS

另外，Interplanetary File System（IPFS）P2P协议也可用于创建一个替代HTTP的新的去中心化互联网。 2015年Motherboard的这个理论，非常棒地说明了IPFS的优势，例如，视频会下载速度更快，从而带来更多的带宽节省，并且网站永远不会像在Yahoo!接管GeoCities网站后那样消失了。

创造“新互联网”的技术已经有了，并且已经开始在运行。 但要想全部实现在手机上，仍然有技术障碍要去克服，但这并非不可能。 更大的问题是，有多少人会加入一个全新的互联网？

## 参考（译者注）

[1] Maidsafe, http://maidsafe.net/

[2] Storj, https://storj.io/

[3] MaidSAFE vs Sia vs Storj, https://themerkle.com/maidsafe-vs-sia-vs-storj/

[4] Storj to Migrate Decentralized Storage Service to Ethereum Blockchain, http://www.coindesk.com/storj-migrate-decentralized-storage-service-ethereum-blockchain/

[5] Mesh Network, https://en.wikipedia.org/wiki/Mesh_networking
