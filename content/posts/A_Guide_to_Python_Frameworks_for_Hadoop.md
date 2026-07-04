---
Title: Hadoop的Python框架指南
Summary: 最近，我加入了Cloudera，在这之前，我在计算生物学/基因组学上已经工作了差不多10年。我的分析工作主要是利用Python语言和它很棒的科学计算栈来进行的。但Apache Hadoop的生态系统大部分都是用Java来实现的，也是为Java准备的，这让我很恼火。所以，我的头等大事变成了寻找一些Python可以用的Hadoop框架。
Authors: Django Wong
Date:    2014-04-28
---

最近，我加入了Cloudera，在这之前，我在计算生物学/基因组学上已经工作了差不多10年。我的分析工作主要是利用Python语言和它[很棒的科学计算栈](http://pydata.org/)来进行的。但Apache Hadoop的生态系统大部分都是用Java来实现的，也是为Java准备的，这让我很恼火。所以，我的头等大事变成了寻找一些Python可以用的Hadoop框架。

在这篇文章里，我会把我个人对这些框架的一些无关科学的看法写下来，这些框架包括:

- Hadoop流  
- mrjob  
- dumbo  
- hadoopy  
- pydoop  
- 其它 

最终，在我的看来，Hadoop的数据流(streaming)是最快也是最透明的选项，而且最适合于文本处理。mrjob最适合于在Amazon EMR上快速工作，但是会有显著的性能损失。dumbo 对于大多数复杂的工作都很方便(对象作为键名(key))，但是仍然比数据流(streaming)要慢。
请继续往下阅读，以了解实现细节，性能以及功能的比较。

## 一个有趣的问题

为了测试不同的框架，我们不会做“统计词数”的实验，转而去转化谷歌图书N-元数据。 N-元代表一个n个词构成的元组。这个n-元数据集提供了谷歌图书文集中以年份分组的所有1-，2-，3-，4-，5-元记录的统计数目。 在这个n-元数据集中的每行记录都由三个域构成：n-元，年份，观测次数。(您能够在[http://books.google.com/ngrams](http://books.google.com/ngrams)取得数据)。

我们希望去汇总数据以观测统计任何一对相互临近的词组合所出现的次数，并以年份分组。实验结果将使我们能够判断出是否有词组合在某一年中比正常情况出现的更为频繁。如果统计时，有两个词在四个词的距离内出现过，那么我们定义两个词是“临近”的。 或等价地，如果两个词在2-，3-或者5-元记录中出现过，那么我们也定义它们是”临近“的。 一次，实验的最终产物会包含一个2-元记录，年份和统计次数。

有一个微妙的地方必须强调。n-元数据集中每个数据的值都是通过整个谷歌图书语料库来计算的。从原理上来说，给定一个5-元数据集，我可以通过简单地聚合正确的n-元来计算出4-元、3-元和2-元数据集。例如，当5-元数据集包含

	(the, cat, in, the, hat)       1999     20
	(the, cat, is, on, youtube)    1999     13
	(how, are, you, doing, today)  1986   5000
	
时，我们可以将它聚合为2-元数据集以得出如下记录

	(the, cat)  1999    33      // 也就是, 20 + 13
	
然而，实际应用中，只有在整个语料库中出现了40次以上的n元组才会被统计进来。所以，如果某个5元组达不到40次的阈值，那么Google也提供组成这个5元组的2元组数据，这其中有一些或许能够达到阈值。出于这个原因，我们用相邻词的二元数据，隔一个词的三元组，隔两个词的四元组，以此类推。换句话说，与给定二元组相比，三元组多的只是最外层的词。除了对可能的稀疏n元数据更敏感，只用n元组最外层的词还有助于避免重复计算。总的来说，我们将在2元、3元、4元和5元数据集上进行计算。

MapReduce的伪代码来实现这个解决方案类似这样：

	def map(record):
		(ngram, year, count) = unpack(record)
		// 确保word1为字典第一个字
		(word1, word2) = sorted(ngram[first], ngram[last])
		key = (word1, word2, year)
		emit(key, count)

	def reduce(key, values):
		emit(key, sum(values))
		
## 硬件

这些MapReduce组件在一个大约20GB的随机数据子集上执行。完整的数据集涵盖1500个文件；我们用这个脚本选取一个随机子集。文件名保持完整，这一点相当重要，因为文件名确定了数据块的n-元中n的值。
Hadoop集群包含5个使用CentOS 6.2 x64的虚拟节点，每个都有4个CPU，10GB RAM，100GB硬盘容量，并且运行CDH4。集群每次能够执行20个并行运算，每个组件能够执行10个减速器。


集群上运行的软件版本如下：

- Hadoop:2.0.0-cdh4.1.2  
- Python:2.6.6  
- mrjob:0.4-dev  
- dumbo:0.21.36  
- hadoopy:0.6.0  
- pydoop:0.7(PyPI)库中包含最新版本  
- java:1.6  

## 实现

大多数Python框架都封装了 [Hadoop Streaming](http://hadoop.apache.org/docs/r0.15.2/streaming.html)，还有一些封装了 [Hadoop Pipes](http://hadoop.apache.org/docs/r0.20.1/api/org/apache/hadoop/mapred/pipes/package-summary.html)，也有些是基于自己的实现。下面我会分享一些我使用各种Python工具来写Hadoop jobs的经验，并会附上一份性能和特点的比较。我比较感兴趣的特点是易于上手和运行，我不会去优化某个单独的软件的性能。

在处理每一个数据集的时候，都会有一些损坏的记录。对于每一条记录，我们要检查是否有错并识别错误的种类，包括缺少字段以及错误的N元大小。对于后一种情况，我们必须知道记录所在的文件名以便确定该有的N元大小。
所有代码可以从[GitHub](https://github.com/cloudera/python-ngrams)获得。

## Hadoop Streaming

[Hadoop Streaming ](http://hadoop.apache.org/docs/r0.15.2/streaming.html)提供了使用其他可执行程序来作为Hadoop的mapper或者reduce的方式，包括标准Unix工具和Python脚本。这个程序必须使用规定的语义从标准输入读取数据，然后将结果输出到标准输出。直接使用Streaming 的一个缺点是当reduce的输入是按key分组的时候，仍然是一行行迭代的，必须由用户来辨识key与key之间的界限。

下面是mapper的代码:

	#! /usr/bin/env python

	import os
	import re
	import sys

	# determine value of n in the current block of ngrams by parsing the filename
	input_file = os.environ['map_input_file']
	expected_tokens = int(re.findall(r'([\d]+)gram', os.path.basename(input_file))[0])

	for line in sys.stdin:
		data = line.split('\t')

		# perform some error checking
		if len(data) < 3:
			continue

		# unpack data
		ngram = data[0].split()
		year = data[1]
		count = data[2]

		# more error checking
		if len(ngram) != expected_tokens:
			continue

		# build key and emit
		pair = sorted([ngram[0], ngram[expected_tokens - 1]])
		print >>sys.stdout, "%s\t%s\t%s\t%s" % (pair[0], pair[1], year, count)
		
下面是reducer:

	#! /usr/bin/env python

	import sys

	total = 0
	prev_key = False
	for line in sys.stdin:
		data = line.split('\t')
		curr_key = '\t'.join(data[:3])
		count = int(data[3])

		# found a boundary; emit current sum
		if prev_key and curr_key != prev_key:
			print >>sys.stdout, "%s\t%i" % (prev_key, total)
			prev_key = curr_key
			total = count
		# same key; accumulate sum
		else:
			prev_key = curr_key
			total += count

	# emit last key
	if prev_key:
		print >>sys.stdout, "%s\t%i" % (prev_key, total)
		
Hadoop流(Streaming)默认用一个tab字符分割健(key)和值(value)。因为我们也用tab字符分割了各个域(field)，所以我们必须通过传递给Hadoop下面三个选项来告诉它我们数据的健(key)由前三个域构成。

	-jobconf stream.num.map.output.key.fields=3
	-jobconf stream.num.reduce.output.key.fields=3
	
要执行Hadoop任务命令

	hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.2.jar \
			-input /ngrams \
			-output /output-streaming \
			-mapper mapper.py \
			-combiner reducer.py \
			-reducer reducer.py \
			-jobconf stream.num.map.output.key.fields=3 \
			-jobconf stream.num.reduce.output.key.fields=3 \
			-jobconf mapred.reduce.tasks=10 \
			-file mapper.py \
			-file reducer.py
			
注意，mapper.py和reducer.py在命令中出现了两次，第一次是告诉Hadoop要执行着两个文件，第二次是告诉Hadoop把这两个文件分发给集群的所有节点。

Hadoop Streaming 的底层机制很简单清晰。与此相反，Python以一种不透明的方式执行他们自己的序列化/反序列化，而这要消耗更多的资源。 而且，如果Hadoop软件已经存在，Streaming就能运行，而不需要再在上面配置其他的软件。更不用说还能传递Unix 命令或者Java类名称作 mappers/reducers了。

Streaming缺点是必须要手工操作。用户必须自己决定如何将对象转化为为成键值对（比如JSON 对象）。对于二进制数据的支持也不好。而且如上面说过的，必须在reducer手工监控key的边界，这很容易出错。

## mrjob

[mrjob](https://github.com/Yelp/mrjob)是一个开放源码的Python框架，封装Hadoop的数据流，并积极开发Yelp的。，由于Yelp的运作完全在亚马逊网络服务，mrjob的整合与EMR是令人难以置信的光滑和容易（使用[boto](https://github.com/boto/boto)包）。

mrjob提供了一个Python的API与Hadoop的数据流，并允许用户使用任何对象作为键和映射器。默认情况下，这些对象被序列化为[JSON对象](http://en.wikipedia.org/wiki/JSON)的内部，但也有支持[pickle](http://docs.python.org/2/library/pickle.html)的对象。有没有其他的二进制I / O格式的开箱即用，但有一个机制来实现自定义序列化。

值得注意的是，mrjob似乎发展的非常快，并有很好的文档。  
所有的Python框架，看起来像伪代码实现：

	#! /usr/bin/env python

	import os
	import re

	from mrjob.job import MRJob
	from mrjob.protocol import RawProtocol, ReprProtocol

	class NgramNeighbors(MRJob):

		# mrjob allows you to specify input/intermediate/output serialization
		# default output protocol is JSON; here we set it to text
		OUTPUT_PROTOCOL = RawProtocol

		def mapper_init(self):
			# determine value of n in the current block of ngrams by parsing filename
			input_file = os.environ['map_input_file']
			self.expected_tokens = int(re.findall(r'([\d]+)gram', os.path.basename(input_file))[0])

		def mapper(self, key, line):
			data = line.split('\t')

			# error checking
			if len(data) < 3:
				return

			# unpack data
			ngram = data[0].split()
			year = data[1]
			count = int(data[2])

			# more error checking
			if len(ngram) != self.expected_tokens:
				return

			# generate key
			pair = sorted([ngram[0], ngram[self.expected_tokens - 1]])
			k = pair + [year]

			# note that the key is an object (a list in this case)
			# that mrjob will serialize as JSON text
			yield (k, count)

		def combiner(self, key, counts):
			# the combiner must be separate from the reducer because the input
			# and output must both be JSON
			yield (key, sum(counts))

		def reducer(self, key, counts):
			# the final output is encoded as text
			yield "%s\t%s\t%s" % tuple(key), str(sum(counts))

	if __name__ == '__main__':
		# sets up a runner, based on command line options
		NgramNeighbors.run()

mrjob只需要安装在客户机上，其中在作业的时候提交。下面是要运行的命令：

	export HADOOP_HOME="/usr/lib/hadoop-0.20-mapreduce"
	./ngrams.py -r hadoop --hadoop-bin /usr/bin/hadoop --jobconf mapred.reduce.tasks=10 -o hdfs:///output-mrjob hdfs:///ngrams
	
编写MapReduce的工作是非常直观和简单的。然而，有一个重大的内部序列化计划所产生的成本。最有可能的二进制计划将需要实现的用户（例如，为了支持typedbytes）。也有一些内置的实用程序日志文件的解析。最后，mrjob允许用户写多步骤的MapReduce的工作流程，在那里从一个MapReduce作业的中间输出被自动用作输入到另一个MapReduce工作。

***（注：其余的实现都非常相似，除了包具体的实现，他们都能被找到[here](http://github.com/cloudera/python-ngrams)。）***

## dumbo

[dumbo](https://github.com/klbostee/dumbo/wiki) 是另外一个使用Hadoop流包装的框架。dumbo出现的较早，本应该被许多人使用，但由于缺少文档，造成开发困难。这也是不如mcjob的一点。

dumbo通过typedbytes执行序列化，能允许更简洁的数据传输，也可以更自然的通过指定JavaInputFormat读取SequenceFiles或者其他格式的文件，比如，dumbo也可以执行Python的egg和Java的JAR文件。

在我的印象中， 我必须要手动安装dumbo中的每一个节点， 它只有在typedbytes和dumbo以eggs形式创建的时候才能运行。 就像他会因为onMemoryErrors终止一样，他也会因为使用组合器停止。

运行dumbo任务的代码是：

	dumbo start ngrams.py \
			-hadoop /usr \
			-hadooplib /usr/lib/hadoop-0.20-mapreduce/contrib/streaming \
			-numreducetasks 10 \
			-input hdfs:///ngrams \
			-output hdfs:///output-dumbo \
			-outputformat text \
			-inputformat text
			
## hadoopy

[hadoopy](https://github.com/bwhite/hadoopy)是另外一个兼容dumbo的Streaming封装。同样，它也使用typedbytes序列化数据，并直接把 typedbytes 数据写到HDFS。

它有一个很棒的调试机制， 在这种机制下它可以直接把消息写到标准输出而不会干扰Streaming过程。它和dumbo很相似，但文档要好得多。文档中还提供了与[Apache HBase](http://hbase.apache.org/)整合的内容。

用hadoopy的时候有两种发发来启动jobs：

1. launch 需要每个节点都已经安装了Python/hadoopy ，但是在这之后的负载就小了。  
2. launch_frozen 不要求节点上已经安装了Python，它会在运行的时候安装，但这会带来15秒左右的额外时间消耗（据说通过某些优化和缓存技巧能够缩短这个时间）。

必须在Python程序中启动hadoopy job，它没有内置的命令行工具。  
我写了一个脚本通过launch_frozen的方式启动hadoopy

	python launch_hadoopy.py
	
用launch_frozen运行之后，我在每个节点上都安装了hadoopy然后用launch方法又运行了一遍，性能明显好得多。

## pydoop

与其他框架相比，[pydoop](http://pydoop.sourceforge.net/docs/)封装了Hadoop的管道（Pipes），这是Hadoop的C++ API。 正因为此，该项目声称他们能够提供更加丰富的Hadoop和HDFS接口，以及一样好的性能。我没有验证这个。但是，有一个好处是可以用Python实现一个Partitioner，RecordReader以及RecordWriter。所有的输入输出都必须是字符串。

最重要的是，我不能成功的从PIP或者源代码构建pydoop。

## 其他

- [happy](http://code.google.com/p/happy/) 是一个用[Jython](http://www.jython.org/)来写Hadoop job的框架，但是似乎已经挂了  
- [Disco](http://discoproject.org/)成熟的，非Hadoop 的 MapReduce.实现，它的核心使用Erlang写的，提供了Python的API，它由诺基亚开发，不如Hadoop应用广泛。  
- [octopy](http://code.google.com/p/octopy/)是一个纯Python的MapReduce实现，它只有一个源文件，并不适于“真正的”计算。  
- [Mortar](http://www.mortardata.com/)是另一个Python选择，它不久前才发布，用户可以通过一个网页应用提交Apache Pig 或者 Python jobs 处理放置在 Amazon S3上的数据。  
- 有一些更高层次的Hadoop生态体系中的接口，像[Apache Hive](http://hive.apache.org/)和Pig。Pig 可以让用户用Python来写自定义的功能，是通过Jython来运行。 Hive 也有一个Python封装叫做[hipy](http://code.google.com/a/apache-extras.org/p/hipy/)。  
- (Added Jan. 7 2013)[Luigi](https://github.com/spotify/luigi) 是一个用于管理多步作业流程的Python框架。它与[Apache Oozie ](http://oozie.apache.org/)有一点相似，但是它内置封装了Hadoop Streaming(轻量级的封装)。Luigi有一个非常好的功能是能够在job出错的时候抛出Python代码的错误堆栈，而且它的命令行界面也非常棒。它的README文件内容很多，但是却缺少详尽的参考文档。Luigi 由Spotify 开发并在其内部广泛使用。

## 关于计数器的特别说明

在我的MR jobs的最初实现里，我用计数器来跟踪监控不良记录。在Streaming里，需要把信息写到stderr。事实证明这会带来不容忽视的额外开销：Streaming job花的时间是原生java job的3.4倍。这个框架同样有此问题

## 性能比较

将用Java实现的MapReduce job作为性能基准。 Python框架的值是其相对于Java的性能指标的比率。

![](/static/attach/11141946_s0Wt.png)

Java明显最快,，Streaming要多花一半时间，Python框架花的时间更多。从mrjob mapper的profile数据来看，它在序列化/反序列化上花费了大量时间。dumbo和hadoopy在这方面要好一点。如果用了combiner 的话dumbo 还可以更快。

## 特点比较

大多来自各自软件包中的文档以及代码库。

![](/static/attach/11141948_bMgi.png)

## 结论

Streaming是最快的Python方案，这面面没有任何魔力。但是在用它来实现reduce逻辑的时候，以及有很多复杂对象的时候要特别小心。

所有的Python框架看起来都像是伪码，这非常棒。

mrjob更新快，成熟的易用，用它来组织多步MapReduce的工作流很容易，还可以方便地使用复杂对象。它还可以无缝使用EMR。但是它也是执行速度最慢的

---

还有一些不是很流行的 Python 框架，他们的主要优势是内置了对于二进制格式的支持，但如果有必要话，这个完全可以由用户代码来自己实现。
就目前来看：

- Hadoop Streaming是一般情况下的最佳选择，只要在使用reducer的时候多加小心，它还是很简单易用的。  
- 从计算开销方面考虑的话，选择mrjob，因为它与Amazon EMR结合最好。  
- 如果应用比较复杂，包含了复合键，要组合多步流程，dumbo 最合适。它比Streaming慢，但是比mrjob快。  

如果你在实践中有自己的认识，或是发现本文有错误，请在回复里提出。  

---
翻译：[http://www.oschina.net/translate/a-guide-to-python-frameworks-for-hadoop](http://www.oschina.net/translate/a-guide-to-python-frameworks-for-hadoop)  
原文：[A Guide to Python Frameworks for Hadoop](http://blog.cloudera.com/blog/2013/01/a-guide-to-python-frameworks-for-hadoop/)