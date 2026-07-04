---
Title: Python进阶
Summary: Python进阶的一些知识，生成器，装饰器，函数式编程
Authors: Django Wong
Date: 2017-01-06
---

## 生成器（Generators）

首先得了解三个概念

- 可迭代对象(Iterable)  
- 迭代器(Iterator)  
- 迭代(Iteration)  

#### 可迭代对象(Iterable) 

Python中任意的对象，只要它定义了可以返回一个迭代器的`__iter__`方法，或者定义了可以支持下标索引的`__getitem__`方法(这些双下划线方法会在其他章节中全面解释)，那么它就是一个可迭代对象。简单说，可迭代对象就是能提供迭代器的任意对象。

#### 迭代器(Iterator) 

任意对象，只要定义了`next`(Python2) 或者`__next__`方法，它就是一个迭代器。

#### 迭代(Iteration)

用简单的话讲，它就是从某个地方（比如一个列表）取出一个元素的过程。当我们使用一个循环来遍历某个东西时，这个过程本身就叫迭代。


### 生成器(Generators)

`生成器`也是一种`迭代器`，但是你只能对其迭代一次。这是因为它们并没有把所有的值存在内存中，而是在运行时生成值。你通过遍历来使用它们，要么用一个`for`循环，要么将它们传递给任意可以进行迭代的函数和结构。大多数时候生成器是以函数来实现的。然而，它们并不返回一个值，而是`yield`(暂且译作`生出`)一个值

	def generator_function():
		for i in xrange(10):
			yield i
		
	for i in generator_function():
		print i
		

许多Python2里的标准库函数都会返回列表，而Python3都修改成了返回生成器，因为生成器占用更少的资源。  

下面写一个斐波拉契的的函数，使用生成器。

	def fb(n):
		a,b = 0,1
		for i in xrange(n):
			yield a
			a,b = b, a + b
			
	print fb(10)
	
那么Python中的那些数据类型支持迭代呢？我们看一下str

	some_str = "hello world"
	next(some_str)
	
你就会发现直接报错，因为`str`不是一个迭代器，而是一个迭代对象。所以它支持迭代，但不支持迭代操作。有个内置函数：`iter`，可以式str变成一个迭代器。

	str_iter = iter(some_str)
	next(str_iter)
	
## 函数编程

### 高阶函数

在函数式编程中，我们可以将函数当作变量一样自由使用。一个函数接收另一个函数作为参数，这种函数称之为**高阶函数（Higher-order Functions）**。

	def func(f, arr):
		return [f(x) for x in arr]
		
上面的代码中，func 是一个高阶函数，它接收两个参数，第 1 个参数是函数，第 2 个参数是数组，func 的功能是将函数 g 逐个作用于数组 arr 上，并返回一个新的数组，比如，我们可以这样用：

	def double(x):
		return 2 * x

	def square(x):
		return x * x

	arr1 = func(double, [1, 2, 3, 4])
	arr2 = func(square, [1, 2, 3, 4])


### 匿名函数(lambda)

	lambda 参数: 表达式
	
关键字`lambda`说明它是一个匿名函数，冒号`:`前面的变量是该匿名函数的参数，冒号后面是函数的返回值，注意这里不需使用`return`关键字。

	square = lambda x:x*x
	print square(10)

lambda的使用场景，函数一般适用于创建一些临时性的，小巧的函数。

### map/reduce/filter

#### map函数

	map(function, sequence)
	
对`sequence`中的`item`依次执行`function(item)`，并将结果组成一个`List`返回，也就是：

	[function(item1), function(item2), function(item3), ...]
	
	def square(n):
		return n*n
		
	print map(square,[1,2,3,4])
	
#### reduce

	reduce(function, sequence[, initial])
	
先将`sequence`的前两个`item`传给`function`，即`function(item1, item2)`，函数的返回值和`sequence`的下一个`item`再传给`function`，即`function(function(item1, item2), item3)`，如此迭代，直到`sequence`没有元素，如果有`initial`，则作为初始值调用。

reduece(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

	reduce(lambda x, y: x * y, [1, 2, 3, 4])  # 相当于 ((1 * 2) * 3) * 4
	reduce(lambda x, y: x * y, [1, 2, 3, 4], 5) # ((((5 * 1) * 2) * 3)) * 4
	
#### filter

	filter(function, sequnce)
	
将`function`依次作用于`sequnce`的每个`item`，即`function(item)`，将返回值为`Tru` 的 item 组成一个`List/String/Tuple`(取决于`sequnce`的类型，`python3`统一返回迭代器) 返回。

	even_num = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))
	filter(lambda x: x < 'g', 'hijack')


## 装饰器(Decorator)

在Python中

- 函数可以被赋值给其他变量
- 函数可以被删除
- 可以在函数里面再定义函数
- 函数可以作为参数传递给另外一个函数
- 函数可以作为另一个函数的返回

***简而言之，函数就是一个对象。***

### 对一个简单的函数进行装饰

	def hello():
		return 'hello world'
		
	def makeitalic(func):
		def wrapped():
			return "<i>" + func() + "</i>"
		return wrapped
		
	hello = makeitalic(hello)
	print hello()
	
在上面，我们将`hello`函数传给`makeitalic`，再将返回赋给`hello`，此时调用`hello()`就得到了我们想要的结果。

事实上，makeitalic就是一个装饰器(decorator)，我们可以使用@来简化上面的写法。

	def makeitalic(func):
		def wrapped():
			return "<i>" + func() + "</i>"
		return wrapped

	@makeitalic
	def hello():
		return 'hello world'


像上面的情况，可以动态修改函数（或类）功能的函数就是装饰器。***本质上，它是一个高阶函数，以被装饰的函数（比如上面的 hello）为参数，并返回一个包装后的函数（比如上面的 wrapped）给被装饰函数（hello）***。


### 装饰器的副作用

使用装饰器有一个瑕疵，就是被装饰的函数，它的函数名称已经不是原来的名称了，回到最开始的例子：

	def makeitalic(func):
		def wrapped():
			return "<i>" + func() + "</i>"
		return wrapped

	@makeitalic
	def hello():
		return 'hello world'
		
函数`hello`被`makeitalic`装饰后，它的函数名称已经改变了：

	>>> hello.__name__
	'wrapped'
	
为了消除这样的副作用，Python 中的`functool`包提供了一个`wraps`的装饰器：

	from functools import wraps

	def makeitalic(func):
		@wraps(func)       # 加上 wraps 装饰器
		def wrapped():
			return "<i>" + func() + "</i>"
		return wrapped

	@makeitalic
	def hello():
		return 'hello world'

	>>> hello.__name__
	'hello'