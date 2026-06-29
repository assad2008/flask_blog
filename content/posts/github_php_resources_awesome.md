---
Title:  PHP资源汇总大全
Summary: 一个PHP资源列表，内容包括：库、框架、模板、安全、代码分析、日志、第三方库、配置工具、Web 工具、书籍、电子书、经典博文等等
Authors: Django Wong
Date:    2026-06-28
---

# PHP资源汇总大全

> 一个偏实用的 PHP 资源导航，适合 PHP 后端开发、接口开发、Web 项目、企业系统、Composer 包管理和日常工程化参考。

![PHP 资源汇总封面](https://www.php.net/images/logos/new-php-logo.svg)

## 目录

- [贡献](#贡献)
- [依赖管理 Dependency Management](#依赖管理-dependency-management)
- [其他的依赖管理 Dependency Management Extras](#其他的依赖管理-dependency-management-extras)
- [框架 Frameworks](#框架-frameworks)
- [微框架 Micro Frameworks](#微框架-micro-frameworks)
- [模板 Template Engines](#模板-template-engines)
- [数据库 Database](#数据库-database)
- [缓存 Cache](#缓存-cache)
- [日志 Logging](#日志-logging)
- [HTTP 客户端 HTTP Clients](#http-客户端-http-clients)
- [安全 Security](#安全-security)
- [代码质量 Code Quality](#代码质量-code-quality)
- [测试 Testing](#测试-testing)
- [配置 Configuration](#配置-configuration)
- [Web 工具 Web Tools](#web-工具-web-tools)
- [书籍 Books](#书籍-books)
- [经典博文 Classic Posts](#经典博文-classic-posts)
- [示例代码 Example Code](#示例代码-example-code)

## 贡献

详细内容请查看[贡献](https://github.com/ziadoz/awesome-php/blob/master/CONTRIBUTING.md)。

如果你想维护自己的资源列表，建议按以下原则整理：

* 资源名称尽量使用官方名称。
* 链接优先使用 GitHub、官网或官方文档。
* 每条资源后面用一句话说明用途。
* 不建议把已经长期不维护的库放到核心推荐区域。
* 可以按“入门、常用、进阶、企业级”分层整理。

## 依赖管理 Dependency Management

*依赖和包管理库*

* [Composer](https://getcomposer.org/) / [Packagist](https://packagist.org/) - PHP 最常用的包和依赖管理器。
* [Composer Installers](https://github.com/composer/installers) - 一个多框架 Composer 库安装器。
* [Pickle](https://github.com/FriendsOfPHP/pickle) - 一个 PHP 扩展安装器。
* [Private Packagist](https://packagist.com/) - Composer 私有包仓库服务，适合企业内部组件管理。
* [Prestissimo](https://github.com/hirak/prestissimo) - Composer 并行安装插件，老项目中可能会遇到。

## 其他的依赖管理 Dependency Management Extras

*依赖管理相关工具和实践*

* [Composer Normalize](https://github.com/ergebnis/composer-normalize) - 格式化 composer.json，便于团队统一规范。
* [Composer Patches](https://github.com/cweagans/composer-patches) - 给 Composer 依赖包打补丁。
* [Composer Require Checker](https://github.com/maglnet/ComposerRequireChecker) - 检查代码中是否使用了未声明的依赖。
* [Symfony Flex](https://github.com/symfony/flex) - Symfony 项目常用的 Composer 增强插件。

## 框架 Frameworks

*Web 开发框架和应用框架*

* [Laravel](https://laravel.com/) - 优雅、生态完整的现代 PHP Web 框架。
* [Symfony](https://symfony.com/) - 企业级 PHP 框架和组件集合。
* [Yii](https://www.yiiframework.com/) - 高性能 PHP 框架，适合中后台系统。
* [CodeIgniter](https://codeigniter.com/) - 轻量级 PHP 框架，入门简单。
* [CakePHP](https://cakephp.org/) - 约定优于配置的 PHP 框架。
* [Hyperf](https://hyperf.io/) - 基于 Swoole 的高性能协程框架。
* [ThinkPHP](https://www.thinkphp.cn/) - 国内使用较多的 PHP 框架。
* [Yaf](https://www.php.net/manual/zh/book.yaf.php) - PHP 扩展形式的高性能框架，适合性能敏感项目。

## 微框架 Micro Frameworks

*轻量级接口服务框架*

* [Slim](https://www.slimframework.com/) - 适合快速构建 REST API 的微框架。
* [Lumen](https://lumen.laravel.com/) - Laravel 官方微框架，适合轻量接口服务。
* [Flight](https://flightphp.com/) - 简单、快速的小型 PHP 框架。
* [Mezzio](https://docs.mezzio.dev/) - 基于 PSR 标准的中间件框架。

## 模板 Template Engines

*模板引擎和视图渲染工具*

* [Twig](https://twig.symfony.com/) - Symfony 生态常用模板引擎。
* [Blade](https://laravel.com/docs/blade) - Laravel 内置模板引擎。
* [Smarty](https://www.smarty.net/) - 经典 PHP 模板引擎。
* [Plates](https://platesphp.com/) - 原生 PHP 风格模板系统。

## 数据库 Database

*数据库抽象、ORM 和迁移工具*

* [Doctrine ORM](https://www.doctrine-project.org/) - PHP 生态中成熟的 ORM。
* [Eloquent ORM](https://laravel.com/docs/eloquent) - Laravel 默认 ORM，写法简洁。
* [Medoo](https://medoo.in/) - 轻量级数据库操作库。
* [Phinx](https://phinx.org/) - 数据库迁移工具。
* [Laravel Migrations](https://laravel.com/docs/migrations) - Laravel 数据库迁移方案。
* [Cycle ORM](https://cycle-orm.dev/) - 支持 DataMapper 模式的 ORM。

## 缓存 Cache

*缓存、队列和高性能数据访问工具*

* [Predis](https://github.com/predis/predis) - 纯 PHP Redis 客户端。
* [phpredis](https://github.com/phpredis/phpredis) - PHP Redis 扩展，性能较好。
* [Symfony Cache](https://symfony.com/doc/current/components/cache.html) - Symfony 缓存组件。
* [Laravel Cache](https://laravel.com/docs/cache) - Laravel 缓存系统。
* [phpfastcache](https://github.com/PHPSocialNetwork/phpfastcache) - 支持多种后端的缓存库。

## 日志 Logging

*日志记录和日志分析工具*

* [Monolog](https://github.com/Seldaek/monolog) - PHP 最常用的日志库之一。
* [Analog](https://github.com/jbroadway/analog) - 简单灵活的 PHP 日志库。
* [KLogger](https://github.com/katzgrau/KLogger) - PSR-3 兼容的轻量日志库。
* [Graylog](https://www.graylog.org/) - 集中化日志管理平台。
* [ELK Stack](https://www.elastic.co/elastic-stack) - Elasticsearch、Logstash、Kibana 组成的日志分析方案。

## HTTP 客户端 HTTP Clients

*请求接口、调用第三方服务常用工具*

* [Guzzle](https://github.com/guzzle/guzzle) - 功能强大的 PHP HTTP 客户端。
* [Symfony HttpClient](https://symfony.com/doc/current/http_client.html) - Symfony 官方 HTTP 客户端。
* [Requests](https://github.com/WordPress/Requests) - WordPress 生态使用的 HTTP 请求库。
* [Buzz](https://github.com/kriswallsmith/Buzz) - 轻量 HTTP 客户端。

## 安全 Security

*安全、加密、权限和防护工具*

* [PHP Security Advisories](https://github.com/FriendsOfPHP/security-advisories) - PHP 依赖安全漏洞数据库。
* [Roave Security Advisories](https://github.com/Roave/SecurityAdvisories) - 防止安装存在安全漏洞的 Composer 包。
* [Defuse PHP Encryption](https://github.com/defuse/php-encryption) - PHP 加密库。
* [PHP JWT](https://github.com/firebase/php-jwt) - JWT 生成和验证库。
* [Laravel Sanctum](https://laravel.com/docs/sanctum) - Laravel 轻量 API Token 认证方案。
* [Laravel Passport](https://laravel.com/docs/passport) - Laravel OAuth2 认证方案。
* [HTML Purifier](http://htmlpurifier.org/) - HTML 内容过滤，防止 XSS。

## 代码质量 Code Quality

*静态分析、代码规范和重构辅助工具*

* [PHPStan](https://phpstan.org/) - PHP 静态分析工具。
* [Psalm](https://psalm.dev/) - 静态分析和类型检查工具。
* [PHP_CodeSniffer](https://github.com/squizlabs/PHP_CodeSniffer) - PHP 代码规范检查工具。
* [PHP CS Fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer) - 自动修复 PHP 代码风格。
* [Rector](https://getrector.com/) - PHP 自动化重构和版本升级工具。
* [Deptrac](https://github.com/qossmic/deptrac) - 检查项目分层依赖是否合理。

## 测试 Testing

*单元测试、接口测试和行为测试工具*

* [PHPUnit](https://phpunit.de/) - PHP 单元测试事实标准。
* [Pest](https://pestphp.com/) - 语法更简洁的 PHP 测试框架。
* [Codeception](https://codeception.com/) - 支持单元测试、功能测试和验收测试。
* [Behat](https://behat.org/) - BDD 行为驱动测试框架。
* [Mockery](https://github.com/mockery/mockery) - Mock 对象测试库。
* [FakerPHP](https://fakerphp.github.io/) - 生成测试假数据。

## 配置 Configuration

*配置文件、环境变量和参数管理工具*

* [phpdotenv](https://github.com/vlucas/phpdotenv) - 从 `.env` 文件加载环境变量。
* [Symfony Config](https://symfony.com/doc/current/components/config.html) - Symfony 配置组件。
* [Noodlehaus Config](https://github.com/hassankhan/config) - 支持多种格式的配置读取库。
* [Laminas Config](https://docs.laminas.dev/laminas-config/) - Laminas 配置组件。

## Web 工具 Web Tools

*Web 调试、接口、队列和后台工具*

* [Laravel Horizon](https://laravel.com/docs/horizon) - Laravel Redis 队列监控面板。
* [Laravel Telescope](https://laravel.com/docs/telescope) - Laravel 调试和请求观察工具。
* [Symfony VarDumper](https://symfony.com/doc/current/components/var_dumper.html) - 变量调试工具。
* [Whoops](https://filp.github.io/whoops/) - PHP 错误页面美化工具。
* [Adminer](https://www.adminer.org/) - 单文件数据库管理工具。
* [phpMyAdmin](https://www.phpmyadmin.net/) - MySQL/MariaDB Web 管理工具。

## 书籍 Books

*PHP 和 Web 开发相关书籍*

* [PHP The Right Way](https://phptherightway.com/) - PHP 现代开发实践指南。
* [Modern PHP](https://www.oreilly.com/library/view/modern-php/9781491905173/) - 介绍现代 PHP 特性和工程实践。
* [PHP Objects, Patterns, and Practice](https://www.apress.com/gp/book/9781484219959) - PHP 面向对象、设计模式和实践。
* [Laravel Documentation](https://laravel.com/docs) - Laravel 官方文档，也是很好的系统学习材料。
* [Symfony Documentation](https://symfony.com/doc/current/index.html) - Symfony 官方文档。

## 经典博文 Classic Posts

*值得长期阅读的文章和教程*

* [PHP: The Right Way](https://phptherightway.com/) - 现代 PHP 编码规范、依赖管理和部署实践。
* [Composer Documentation](https://getcomposer.org/doc/) - Composer 官方文档。
* [PSR Standards](https://www.php-fig.org/psr/) - PHP-FIG 标准规范。
* [Laravel Best Practices](https://github.com/alexeymezenin/laravel-best-practices) - Laravel 最佳实践整理。
* [Symfony Best Practices](https://symfony.com/doc/current/best_practices.html) - Symfony 官方最佳实践。

## 示例代码 Example Code

### 安装 Composer 依赖

```bash
composer init
composer require monolog/monolog vlucas/phpdotenv guzzlehttp/guzzle
```

### 一个简单的日志示例

```php
<?php

require __DIR__ . '/vendor/autoload.php';

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

// 创建日志对象
$logger = new Logger('app');

// 日志写入到 storage/app.log
$logger->pushHandler(new StreamHandler(__DIR__ . '/storage/app.log', Logger::DEBUG));

// 记录不同级别的日志
$logger->info('用户登录成功', [
    'user_id' => 1001,
    'ip' => $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1',
]);

$logger->warning('接口响应较慢', [
    'api' => '/api/order/list',
    'cost_ms' => 1380,
]);

$logger->error('数据库连接失败', [
    'host' => '127.0.0.1',
    'database' => 'demo',
]);
```

### 一个简单的 Guzzle 请求示例

```php
<?php

require __DIR__ . '/vendor/autoload.php';

use GuzzleHttp\Client;

$client = new Client([
    'timeout' => 10,
]);

$response = $client->get('https://api.github.com/repos/php/php-src');

$data = json_decode((string) $response->getBody(), true);

echo '项目名称：' . $data['full_name'] . PHP_EOL;
echo 'Star 数：' . $data['stargazers_count'] . PHP_EOL;
```

### 推荐的项目目录结构

```text
project/
├── app/
│   ├── Controller/
│   ├── Service/
│   ├── Model/
│   └── Middleware/
├── config/
│   ├── app.php
│   └── database.php
├── public/
│   └── index.php
├── routes/
│   └── web.php
├── storage/
│   ├── logs/
│   └── cache/
├── tests/
├── vendor/
├── .env
├── composer.json
└── README.md
```

## 资源维护建议

* 每 1 到 3 个月检查一次链接是否失效。
* 给资源加上“推荐指数”或“适合场景”，方便团队选择。
* 企业项目优先选择维护活跃、文档完整、生态成熟的库。
* 对生产系统使用的依赖，建议配合安全扫描和版本锁定。
* 新项目优先使用 Composer、PSR 标准、自动化测试和静态分析工具。
