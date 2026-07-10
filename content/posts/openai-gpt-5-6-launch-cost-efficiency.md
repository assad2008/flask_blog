---
authors:
- Assad
date: '2026-07-10'
seo_description: OpenAI 发布 GPT-5.6 系列，包含旗舰 Sol、均衡 Terra 和入门 Luna 三款模型，主打极致性价比，API
  价格大幅降低。新模型在编程智能体和长程任务评测中刷新纪录，设计品味和电脑操作能力显著提升。同时，Codex 独立应用下线，其能力全面整合进 ChatGPT，打造新的
  AI 超级应用。本文深度解读 GPT-5.6 的性能、价格优势及与 Claude 的竞争态势。
seo_keywords: GPT-5.6,OpenAI 新模型,AI 性价比,Codex 整合,ChatGPT 更新
summary: OpenAI 正式推出 GPT-5.6 系列模型，包含 Sol、Terra、Luna 三种型号，以极具竞争力的定价和性能提升为核心卖点。新模型在编程、设计及电脑操作任务上表现突出，同时
  Codex 功能被整合进 ChatGPT，旨在通过高性价比巩固其 AI 市场地位。
title: GPT-5.6 发布：OpenAI 新模型主打极致性价比
---

# 一夜之间，GPT-5.6来了，Codex没了，Claude急了

即便奥特曼瘫坐在椅子前的故事已经听过很多次，但每当 ChatGPT 发布新模型时，我们还是会下意识抱有一丝期待。

没有让我们等待太久，就在刚刚，GPT-5.6 系列正式登场，一口气发布三个型号：旗舰 Sol、均衡款 Terra，还有主打性价比的 Luna，名字分别取自拉丁语里的太阳、地球/大地和月亮。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/7dbc109a97ce4d7a01dab8b3.png)

价格上，Sol 每百万 token 输入 5 美元、输出 30 美元；Terra 直接减半，2.5 美元和 15 美元；Luna 最便宜，只要 1 美元和 6 美元。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/f6c1ac9f3853e9f20cb0bd8f.jpg)

API 价格🔗https://developers.openai.com/api/docs/pricing

相比于 Fable 5 的一波三折，今天起，三款模型将全量上线，24 小时内陆续覆盖 ChatGPT、Codex 和 API。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/b090f16dba9ff24e27bb091d.png)

上压力之后，Anthropic 都变懂事了，主动重置 Claude 额度

这还不是最大的更新，Codex 独立 App 今天也下线了，但它没有消失。Codex 能力整个并入 ChatGPT，造就了一个新的 AI 超级应用。GPT-5.6，就是驱动这个新入口的核心引擎。

![](https://n.sinaimg.cn/spider20260710/567/w1080h1087/20260710/fc7d-5fb1d24e0f40a56a1d39ee261c7e7b39.png)

GPT-5.6 的发布会，Claude 成了隐藏主角

打开 GPT-5.6 的官方博客，你会发现一件事：Claude 被 cue 的次数，多到像是给对家打广告。对比之下，谁菜谁尴尬。

![](https://n.sinaimg.cn/spider20260710/787/w905h682/20260710/9256-0a2814f0f50fb6e4098896bfe9ceeff1.jpg)

火药味最浓的是 Agents' Last Exam，一个横跨 55 个行业的长程智能体工作流评测。GPT-5.6 Sol 拿下 53.6 分创下新高，比 Claude Fable 5（自适应推理）高出 13.1 分。

![](https://n.sinaimg.cn/spider20260710/323/w1080h843/20260710/7aee-450a9e7d70a3b3e87ede1a01f2d792a6.png)

OpenAI 还嫌不够，补充说：就算只开中档推理，也比 Fable 5 高 11.4 分，成本只有对方四分之一左右。更小的 Terra 和 Luna 也超过 Fable 5，成本约为十六分之一。

在覆盖面更广的 Artificial Analysis 智能指数上，Sol 开满推理档，与 Fable 5 只差 1 分，但完成任务的耗时少 61%，成本约为一半。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/559b85ff46fc5d12f0497214.png)

看出来了吧，这次发布的核心叙事就一个词：性价比。同样的钱干更多活，或者同样的活花更少的钱。

奥特曼本人也第一时间在 X 上帮腔，说 OpenAI 听到了企业客户对 AI 成本的担忧，而 5.6 Sol 在“每个任务花多少钱”这件事上前进了一大步，Terra 和 Luna 同样如此。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/53e5c2c6e95dac070ad24cb7.png)

为了把省钱的故事讲圆，计费规则也做了配合：提示词缓存的写入按常规输入价的 1.25 倍收费，读取只收一折；开发者还可以手动设置缓存断点，缓存至少保留 30 分钟，账单变得更可预测了。

当然，嘴上说得很好听，但实际操作可能又是另一回事。

![](https://n.sinaimg.cn/spider20260710/374/w1080h894/20260710/2573-00a745ce024b2b3ad9048dec67a95d52.png)

编程是主战场。Sol 在 Artificial Analysis 编程智能体指数上拿到 80 分，创下新纪录，比 Fable 5 高 2.8 分，输出 token 不到一半，耗时不到一半，成本便宜约三分之一。Terminal-Bench 2.1 和 DeepSWE 上也刷新了最好成绩。

![](https://n.sinaimg.cn/spider20260710/330/w1080h850/20260710/04e5-0f6d52961f332a532771e0744394dab5.png)

Terra 和 Luna 同样能打：Terra 在该指数上略高于 Fable 5，Luna 超过 Opus 4.8，两者耗时都只有对手三分之一左右，成本约为四分之一。

已经上手的客户开始交口称赞。Lovable 联合创始人则表示，新模型让用户构建应用的步骤少了约 25%，工具调用少 35% 到 48%，卡死的任务减少 15%。

网友这边已经玩疯了。开发者 Matt Shumer 晒出 Sol 一次性搓出来的体素版曼哈顿，精度惊人，而且这活是模型完全自主跑了将近一周干完的。

![](https://n.sinaimg.cn/spider20260710/152/w640h312/20260710/aab7-gif7b4baa79507a0e31715dc820beb43fdf.gif)

一口气打造《我的世界》，也不在话下。

![](https://f.sinaimg.cn/spider20260710/654/w900h554/20260710/6a4f-gifc1b4fa49a451b33aa66893a4a2baea6f.gif)

🔗 https://x.com/preferredev\_/status/2075282363458982299

除了写代码，这次 OpenAI 反复强调的还有两个：设计品味和电脑操作。

官方说 GPT-5.6 在设计判断力上是跨越式进步，只给个大方向，它就能做出有审美、好上手的界面。

更关键的是，它会用增强后的电脑操作能力去检查自己渲染出来的成果，发现视觉和功能问题，收尾之后再交活。以前的模型是写完代码就完事，现在是写完还自己验收。

知识办公场景的提升同样显而易见。

BrowseComp 网页浏览评测上，Sol 拿下 92.2% 的新纪录；OSWorld 2.0 电脑操作评测 62.6%，超过 Opus 4.8 的同时输出 token 少了 85%。

![](https://n.sinaimg.cn/spider20260710/440/w1080h960/20260710/e0be-f0ad0d42e9e9abb037a4707d669e56ad.png)

做 PPT 这种打工人刚需，官方给了个对比案例：让模型照着参考文件更新数据，GPT-5.5 的输出丢失了母版里的关键元素，GPT-5.6 能推断出整套设计系统，然后原样套用到新内容上。

文档和表格也是同理，公式和财务模型的精度更高了。

![](https://n.sinaimg.cn/spider20260710/638/w1080h358/20260710/7607-a6cca8fe6c328deb347e073bcf3dd64d.png)

不过吃瓜要吃全套。翻到博客最底下的评测大表格，有几处数字挺微妙：

SWE-Bench Pro 上，Sol 是 64.6%，Claude Fable 5 是 80%，Anthropic 家更高档的 Mythos 5 是 80.3%。这项上 Claude 依然压着打。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/23387769a29c5e965547bbcd.png)

FrontierMath 最难的 Tier 4 数学题，Sol 65.9%，居然还不如自家上代 GPT-5.5 的 72.5%，而 Fable 5 是 87.8%。

GDPval-AA 专业工作评测上，Sol 的 1747.8 Elo 也还是略低于 Fable 5 的 1759.6。

![](https://n.sinaimg.cn/spider20260710/691/w1080h411/20260710/f30b-5bf93723ea3b990c2d66f5f9e52989a2.png)

生物评测 GeneBench Pro 那里还有个小心机：OpenAI 在图注里专门写了一句，Claude Fable 5 没被列进来，因为它不回答高阶生物问题，拒答了这项评测里的大多数题目。短短一条脚注，把阴阳怪气写得明明白白。

值得一提的是，GPT-5.6 这次带来一个新玩法：ultra 模式。

简单讲就是人多力量大。

![](https://n.sinaimg.cn/spider20260710/14/w570h244/20260710/4ff0-gif110c6dfda2e48054e76235fa673cfd4e.gif)

ultra 默认派出四个智能体并行开工，最多可以堆到十六个，用更多 token 换更强结果和更快出活。在 BrowseComp、SEC-Bench Pro、Terminal-Bench 2.1 三项评测里，加智能体都能抬升分数-耗时曲线。

![](https://n.sinaimg.cn/spider20260710/429/w1080h949/20260710/3877-2484a59196f303795729c44edcc78b1e.png)

发布会上研究员的说法是：这些智能体能像一支有经验的团队那样拆分工作。

除了 ultra，还有一档 max，给模型比 xhigh 更充裕的思考时间去推理、验算、换思路。API 侧则上了 Programmatic Tool Calling：模型可以自己写小程序来调度工具、过滤中间数据，省掉大量来回传输的 token。

简言之，以前是开发者手把手教模型每一步怎么走，现在模型自己会写调度脚本了。

ChatGPT+Codex=ChatGPT Work

模型之外，产品侧一口气三连发：ChatGPT Work、全新桌面 App、还有能直接分享的 Sites。

ChatGPT Work 是个啥？

官方定义是能跨应用和文件采取行动、项目执行持续好几个小时、能把目标变成成品的智能体。底层也应用到了 Codex 技术。

![](https://n.sinaimg.cn/spider20260710/88/w1080h608/20260710/1512-d6c1fdf57a19287275da514732e49795.png)

有意思的数据来了：Codex 每周有超过 500 万人在用，其中 100 多万人拿它干的活跟写代码没关系。OpenAI 一看，得，干脆做成通用产品。

ChatGPT Work 能做的事情，大致分三类。第一类是把分散在各系统中的资料整合成成品，借助 GPT-5.6 对模板和设计系统的理解，将分析、整理和生成工作一步完成。

第二类是连接企业工具，通过统一插件目录让 ChatGPT Work 能直接调用各类应用获取上下文，从而真正进入企业工作流。第三类是通过 Scheduled Tasks 自动执行重复任务，让 AI 持续处理监控、汇总和更新等工作，成为企业中的半自动员工。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/006a7e4cca1bf7d81cf5c0c2.jpg)

Sites 则是公测版，一句话把分析结果变成可分享的交互网站或 Web 应用，做仪表盘、项目追踪、产品原型都行。

![](https://n.sinaimg.cn/spider20260710/88/w1080h608/20260710/6130-146b68503c7a072cc679dd0336ec970a.jpg)

发布会现场， OpenAI 财务团队人员演示了一个月底对账的案例：

以前要在多个系统之间来回核对 Excel 预测模型，忙活好几天。现在一条指令，ChatGPT Work 跑完差异分析、更新 Excel 模型、顺手做好 PPT，还能生成一个可分享的交互网站，最后让它把链接发到 Slack 上。

![](https://n.sinaimg.cn/spider20260710/79/w1080h599/20260710/2588-fd26de7e36534c74bad83c632d5b6123.png)

哦对了，这次调整里还夹着一个不小的动作：Codex 独立 App 从今天起并入新版 ChatGPT 桌面 App，Chat、Work、Codex 三个模式装进同一个 App。

Codex 仍然保留编码能力，还新增了 diff 内联编辑、侧边栏 PR review、更快的 Computer Use，以及一个项目里支持多个代码仓库。

开发者如果不想被通用入口打扰，也可以把 Codex 设成桌面 App 的默认视图，甚至继续用 Codex 图标。原来的 ChatGPT 桌面 App 会改名叫 ChatGPT Classic。

![](https://n.sinaimg.cn/spider20260710/88/w1080h608/20260710/3a5f-b52c89375d52aec5c5830a55ae1adfea.jpg)

而独立的 Atlas 浏览器要被砍掉了，功能转进 Chrome 侧边栏插件。（Atlas：我才出生多久啊。）

![](https://n.sinaimg.cn/spider20260710/88/w1080h608/20260710/89b8-d28645bbce58958867303282e3ba8980.jpg)

OpenAI 内部据说已经全员上车，接近 100% 的团队在用 ChatGPT Work 和 Codex，包括财务和销售。销售团队拿它 24 小时内把客户需求变成定制化概念验证，以前这流程要几周。

![](https://n.sinaimg.cn/spider20260710/150/w1080h670/20260710/755b-6438a16f4bbc045d3e31bb576f089727.png)

AI 训练 AI，OpenAI 自己先被改造了

这次发布会最重要的信息，其实藏在研究员一句轻描淡写里：全家桶里最便宜的 Luna，后训练环节是旗舰 Sol 自己独立完成的。

研究员现场展示了那条 prompt：找到训练配置、找到空闲 GPU、启动脚本、确认跑通。就这么短短几句话，扔给 Codex，剩下的 Sol 自己搞定。

用 OpenAI 研究员的原话说：这活以前得一队资深研究员来干，现在感觉自动化研究员已经很近了。

![](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/10/75c1ea5e40cb49fb83e91123.jpg)

啧啧，AI 训练 AI 的时代真到来了。

而且不只这一处，OpenAI 给出了一组内部数据，挺震撼的。过去六个月，内部用于代码推理的研究算力份额涨了 100 倍，智能体 token 用量涨了约 22 倍。GPT-5.6 内测期间，研究员人均每日输出 token 量超过 GPT-5.5 时期最高水平的两倍。

为了量化这事，OpenAI 还专门搞了一套 RSI 指数（递归自我改进），涵盖调试研究系统、优化训练内核、跑机器学习实验、改进另一个模型等真实任务。GPT-5.6 Sol 比 GPT-5.5 高出 16.2 分。

![](https://n.sinaimg.cn/spider20260710/452/w1080h972/20260710/fd7b-10e690e8cb06277495c3fca5cea6ccd9.png)

网络安全这块进步同样猛：ExploitBench 从上代的 47.9% 干到 73.5%，把真实漏洞变成可用攻击的 ExploitGym 也接近翻倍。

能力太强，OpenAI 这次配套上了可信访问机制，个人要实名验证、开高级账户安全才能碰最强的网络安全能力，高风险地区直接限制。

![](https://n.sinaimg.cn/spider20260710/79/w1080h599/20260710/f8d9-0be232088dc811bbf8724b1767f839c2.png)

安全测试也是史上最苛刻的一轮：约 70 万 A100 等效 GPU 小时的自动化红队测试，新版安全系统拦截的潜在有害行为比之前多出约 10 倍。

当然误伤也难免，所以 ChatGPT 和 Codex 里加了个按钮，被拦了可以一键换低配模型重试。至于模型和产品的适用人群，我们也简单捋了一下，欢迎对号入座：

免费用户：在 ChatGPT Work 和 Codex 里可以用 Terra，新版桌面 App 也能直接下载，Chat、Work、Codex 三个入口都有

Plus / Business 用户：聊天里用上 Sol，在 Work 和 Codex 里三个模型随意切换，ChatGPT Work 几天内推送到位，Codex 里还能开 ultra

Pro / 企业版用户：待遇最全，多一个 Sol Pro 选项留给最难的任务，ChatGPT Work 当天可用，Work 里的 ultra 也直接解锁

开发者：API 开放全部三个模型，多智能体功能以 beta 形式提供

至于 max 模式，不挑档位，所有能用上 GPT-5.6 的 Work 和 Codex 用户，去设置里打开开关就行。

One More Thing

还记得 GPT-5.5 上线时那个著名的补丁吗？

当时 OpenAI 不得不在开发者消息里专门叮嘱模型：别老聊哥布林和小精灵。起因是训练阶段出了 reward hacking，模型钻了奖励机制的空子，学会了没事就往回答里塞哥布林，而且怎么劝都戒不掉。

![](https://n.sinaimg.cn/spider20260710/79/w1080h599/20260710/df88-f3d9ff717bd45822bf43b80e6fb31a77.png)

如今，这桩悬案终于迎来官方大结局。OpenAI 研究员宣布问题已在 GPT-5.6 中修复，今后模型只会在可爱或合适的场合，聊适量的哥布林。

注意措辞，是适量。也就是说，哥布林并没有被赶尽杀绝，只是从戒不掉的执念，降级成了偶尔拿出来把玩的小爱好。

恭喜 GPT 戒断依赖成功，也恭喜哥布林保住了 AI 编制（doge）。

> 本文转自 [一夜之间，GPT-5.6来了，Codex没了，Claude急了_新浪财经_新浪网](https://finance.sina.com.cn/roll/2026-07-10/doc-inihhkum8391902.shtml)