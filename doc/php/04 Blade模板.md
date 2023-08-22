## Blade模板

参考手册 [Blade模板](https://learnku.com/docs/laravel/8.x/blade/9377)

Blade也就是MVC中的V层，我们可以之间在控制器中 `echo` 输出 html 代码，比如像下面：

```php
    public function index()
    {
    		echo '<h1>1</h1>';
    }		
```

但是复杂的逻辑中HTML和我们的业务逻辑混合一起，确实不是一个很好的做法，视图提供了一种方便的方法，可以将所有的 HTML 放在不同的文件中。视图将控制器 / 应用逻辑与显示逻辑分开，并存储在 `resources/views` 目录下。一个简单的视图如下所示：

```
<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

将上述代码存储到 `resources/views/user.blade.php` 后，我们可以使用全局辅助函数 `view` 将其返回，例如：

```

    return view('user', ['name' => '徐晓熊']);


```

如你所见， 传递给 `view` 辅助函数的第一个参数对应 `resources/views` 目录中视图文件的名称。第二个参数是应该可供视图使用的数据数组。在这种情况下，我们传递 `name` 变量，该变量将使用 [Blade syntax](https://learnku.com/docs/laravel/8.x/blade) 在视图中显示。

当然，视图文件也可以嵌套在 `resources/views` 目录的子目录中。「点」符号可以用来引用嵌套视图。例如，如果你的视图存储在 `resources/views/admin/profile.blade.php`，则可以这样引用它：

```
return view('admin.user', $data);
```

> 注意：视图目录名称中不能包含 `.` 字符。



Blade 是 Laravel 提供的一个简单而又强大的模板引擎。



## 视图优化

默认情况下，视图是按需编译的。当执行渲染视图的请求时，Laravel 将确定该视图的编译版本是否存在。如果已编译视图存在，Laravel 将比较未编译视图是否已被修改。如果已编译视图不存在，或者未编译视图已被修改，Laravel 将重新编译该视图。
在请求期间编译视图会对性能产生影响，因此 Laravel 提供了 `view：cache` Artisan 命令来预编译应用中使用的所有视图文件。为了提高性能，你可能希望在部署过程中运行以下命令：

```
php artisan view:cache
```

你可以使用 `view:clear` 命令清除视图缓存：

```
php artisan view:clear
```

编译的视图将会存在 `storage/framework/views/`目录下。

你可以看到，凡是写的有``{{}}``的地方都编译成了 `echo `,而且调用了 `e`函数，`e` 函数会使用   `htmlentities`函数来对 HTML 实体进行双重编码。讲HTML代码转成实体字符。函数自动转义以防范 XSS 攻击。

```
<script>
	alert(123123);
<script>
```



#### 展示非转义数据

如果不想您的数据被转义，那么您可使用如下的语法：

```
Hello, {!! $name !!}.
```



#### 模板变量

您不仅限于显示传递给视图的变量的内容。 您也可以回显任何 PHP 函数的结果。 实际上，您可以将所需的任何 PHP 代码放入 Blade echo 语句中：

```php
The current UNIX timestamp is {{ time() }}.
```



#### 渲染 JSON

有时，您可能会将数组传递给视图，以将其呈现为 JSON，以便初始化 JavaScript 变量。 例如：

```javascript
<script>    
var app = <?php echo json_encode($array); ?>; 
</script>
```



当然，您亦可使用 `@json` Blade 指令来代替手动调用 `json_encode` 方法。 `@json` 指令的参数和 PHP 的 `json_encode` 函数一致：

```
<script>
    var app = @json($array);

    var app = @json($array, JSON_PRETTY_PRINT);
</script>	
```



## 控制结构

除了模板继承和显示数据以外， Blade 还为常见的 PHP 控制结构提供了便捷的快捷方式，例如条件语句和循环。这些快捷方式为 PHP 控制结构提供了一个非常清晰、简洁的书写方式，同时，还与 PHP 中的控制结构保持了相似的语法特性。

### If 语句

您可以使用 `@if` ， `@elseif` ， `@else` 和 `@endif` 指令构造 `if` 语句。这些指令功能与它们所对应的 PHP 语句完全一致：

```
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

为了方便， Blade 还提供了一个 `@unless` 指令：

```
@unless (Auth::check())
    You are not signed in.
@endunless
```

除了已经讨论过了的条件指令外， `@isset` 和 `@empty` 指令亦可作为它们所对应的 PHP 函数的快捷方式：

```
@isset($records)
    // $records 已经定义但不为空
@endisset

@empty($records)
    // $records 为空……
@endempty
```

您可使用 `@switch` ， `@case` ， `@break` ， `@default` 和 `@endswitch` 语句来构造 Switch 语句

```
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```



### 循环

除了条件语句， Blade 还提供了与 PHP 循环结构功能相同的指令。同样，这些语句的功能和它们所对应的 PHP 语法一致

```
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

技巧：循环时，您可以使用 [循环变量](https://learnku.com/docs/laravel/8.x/blade/9377#the-loop-variable) 去获取有关循环的有价值的信息，例如，您处于循环的第一个迭代亦或是处于最后一个迭代。

在使用循环的时候，您可以终止循环或跳过当前迭代：

```
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```

### Loop 变量

循环时，循环内部可以使用 `$loop` 变量。该变量提供了访问一些诸如当前的循环索引和此次迭代是首次或是末次这样的信息的方式

```
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```

如果您在嵌套循环中，您可以使用循环的 `$loop` 的变量的 `parent` 属性访问父级循环：

```
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

### 注释

Blade 也允许您在视图中定义注释。但是，和 HTML 注释不同， Blade 注释不会被包含在应用返回的 HTML 中：

```
{{-- This comment will not be present in the rendered HTML --}}
```

### PHP

在许多情况下，嵌入 PHP 代码到您的视图中是很有用的。您可以在模板中使用 Blade 的 `@php` 指令执行原生的 PHP 代码块：

```
@php
    //
@endphp
```

## 表单

### CSRF 域

任何您在应用中定义 HTML 表单的时候，您都应该在表单中包含一个隐藏的 CSRF token 域，这样一来， [CSRF 保护](https://learnku.com/docs/laravel/laravel/8.x/csrf) 中间件便能校验请求。您可以使用 `@csrf` Blade 指令来生成一个 token 域：

```
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

### 方法域

由于 HTML 表单不能够构造 `PUT` ， `PATCH` 或 `DELETE` 请求，您需要添加隐藏的 `_method` 域来模拟这些 HTTP 动作。您亦可使用 `@method` Blade 指令来创建这个方法域：

```
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

## 引入子视图



Blade 的 `@include` 指令可用于从另一个视图包含一个 Blade 视图。子视图将继承父视图中所有可用的变量：

```
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

除了子视图继承父视图中所有可用的数据，您亦可通过数组将数据传递给子视图：

```
@include('view.name', ['some' => 'data'])
```



## 模板继承 



### 使用模板继承进行布局

布局也可以通过 「模板继承」 创建。在引入 [组件](https://learnku.com/docs/laravel/8.5/blade/10375#components) 之前，这是构建应用程序的主要方法。

模板继承是我们工作之中最常用的布局方式，他可以向PHP类的继承一样方便又灵活的应用。

在我们实际的项目开发中，不同的页面会有公共的头部和底部  共同的样式 接下来我们写个简单的例子。

```php+HTML
// resources/views/layouts/app.blade.php
<html>
<head>
    <title>大熊婚恋网- @yield('title','我是默认值')</title>
    <style>
        .header{
            width: 100%;
            height: 100px;
            background-color:#f90;
        }
        .main{
            display: flex;
            width: 100%;
            min-height:500px;
        }
        .ce{
            width: 300px;
            background-color:pink;
        }
        .content{
            width: 100%;
            background-color:#cbd5e0;
        }
        .alert{
            width:300px;
            height:60px;
            background-color: #437bde;
            border-radius:10px;
            text-align:center;
            line-height:60px;
        }
        .alert-error{
            background-color: red;
        }
    </style>
</head>
<body>
  <header class="header"></header>
    <div class="main">
        <div class="ce">
            我是侧边栏
        </div>
        <div class="content">
            @section('content')
                <h1>我是面包屑</h1>
            @show

{{--                @yield('content')--}}
        </div>
    </div>
</body>
</html>

```

```php
// resources/views/user.blade.php

@extends('layouts.app')

@section('title',"个人中心")

@section('content')
    @parent
        <div>
            <h1>我是个人中心</h1>
        </div>
    @endsection
```





## 组件

组件的使用可以让我们更加方便的使用模板，可以借鉴和很多的VUE组件的思想，你可以向使用Vue组件一样使用Blade组件。

我们可以使用下面命令来创建组件

```
php artisan make:component Alert
```

那个 `make:component` 命令还将为组件创建视图模板。视图将放在 `resources/views/components` 目录中。为自己的应用程序编写组件时，组件会在 `app/View/components` 目录和 `resources/views/components` 目录中自动发现，因此通常不需要进一步的组件注册。

也可以在子目录中创建组件：

```php
php artisan make:component Forms/Input
```

上面的命令将在 `App\View\Components\Forms` 目录中创建一个 `Input` 组件，该视图将放在 `resources/views/Components/Forms` 目录中。

### 渲染组件

要显示组件，可以在其中一个 Blade 模板中使用 Blade 组件标记。Blade 组件标记以字符串 `x-` 开头，后跟组件类的蛇形名称：

```
<x-alert/>

<x-user-profile/>
```

如果组件类嵌套在 `App\View\Components` 目录的更深处，则可以使用 `.` 字符表示目录嵌套。例如，如果我们假设一个组件位于 `App\View\Components\Inputs\Button.php` ，我们可以这样处理：

```
<x-inputs.button/>
```

### 给组件传递数据

你可以使用 HTML 属性将数据传递给 Blade 组件。硬编码、原始值可以使用简单的 HTML 属性字符串传递给组件。PHP 表达式和变量应通过使用 `:` 字符作为前缀的属性传递给组件：

```php
<x-alert type="error" :message="$message"/>
```

> 类似于 VUE 组件语法

你应该在组件类的构造函数中定义组件所需的数据。组件上的所有公共属性将自动提供给组件的视图。不必从组件的 `render` 方法将数据传递到视图：

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The alert type.
     *
     * @var string
     */
    public $type;

    /**
     * The alert message.
     *
     * @var string
     */
    public $message;

    /**
     * 创建组件实例
     *
     * @param  string  $type
     * @param  string  $message
     * @return void
     */
    public function __construct($type, $message)
    {
        $this->type = $type;
        $this->message = $message;
    }

    /**
     * 将一个视图或者字符串传递给组件用于渲染
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return view('components.alert');
    }
}
```

渲染组件时，可以通过按名称回显变量来显示组件公共变量的内容：

```

<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

#### 驼峰命名

应使用 `camelCase` 指定组件构造函数参数，而在 HTML 属性中引用参数名称时应使用 `kebab-case`。例如，给定以下组件构造函数：

```
/**
 * 创建组件实例
 *
 * @param  string  $alertType
 * @return void
 */
public function __construct($alertType)
{
    $this->alertType = $alertType;
}
```

`$alertType` 参数可以使用如下所示的方式接受数据：

```php
<x-alert alert-type="danger" />
```

#### 访问组件类中的属性和插槽

Blade 组件还允许你访问类的 render 方法中的组件名称、属性和插槽。但是，为了访问这些数据，应该从组件的 `render` 方法返回闭包。闭包将接收一个 `$data` 数组作为它的唯一参数。此数组将包含几个元素，这些元素提供有关组件的信息：

```
/**
 * 获取表示组件的视图/内容
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
{
    return function (array $data) {
        // $data['componentName'];
        // $data['attributes'];
        // $data['slot'];
			 	return 'components.alert';
	
        return '<div>Components content</div>';
        
        return <<<'blade'
                <div class="alert alert-danger">
                    {{ $message }}
                </div>
            blade;
    };
}
```

组件传递的数据无法修改,修改数据可以在构造函数中修改。

闭包应该返回一个字符串。如果返回的字符串与现有视图相对应，则将呈现该视图；否则，返回的字符串将作为内联 Blade 视图进行计算。

### 插槽

你通常需要通过 「插槽」 将其他内容传递给组件。通过回显 `$slot` 变量来呈现组件插槽。为了探索这个概念，我们假设 `alert` 组件具有以下内容： 类似VUE

```
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

我们可以通过向组件中注入内容将内容传递到 `slot` ：

```
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

有时，组件可能需要在组件内的不同位置渲染多个不同的插槽。让我们修改警报组件以允许注入 「标题」插槽：

```
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

可以使用 `x-slot` 标记定义命名插槽的内容。任何不在显式 `x-slot` 标记中的内容都将传递给 `$slot` 变量中的组件：

```
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

#### 作用域插槽

如果你使用过诸如 Vue 之类的 JavaScript 框架，那么你可能熟悉 「作用域插槽」，它允许你从插槽中的组件访问数据或方法。通过在组件上定义公共方法或属性，并通过 `$component` 变量访问插槽中的组件，可以在 Laravel 中实现类似的行为。在本例中，我们假设 `x-alert` 组件在其组件类上定义了一个公共的 `formatAlert` 方法：

```
<x-alert>
    <x-slot name="title">
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

### 内联组件视图

```
/**
 * 获取表示组件的视图/内容。
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```



### 使用组件布局 

之前我们使用模板继承的方式进行布局。现在我们学习了组件 接下来我们使用组件的方式的来进行布局。

```
// resources/views/components/layout.balde.php
<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
          <style>
        .header{
            width: 100%;
            height: 100px;
            background-color:#f90;
        }
        .main{
            display: flex;
            width: 100%;
            min-height:500px;
        }
        .ce{
            width: 300px;
            background-color:pink;
        }
        .content{
            width: 100%;
            background-color:#cbd5e0;
        }
    </style>
    </head>
    
    <body>
      <header class="header"></header>
    <div class="main">
        <div class="ce">
            我是侧边栏
        </div>
        <div class="content">
				        {{ $slot }}
        </div>
    </div>
    </body>
</html>
```

### 应用布局组件

一旦定义了 `layout` 组件，我们就可以创建一个使用该组件的 Blade 视图。在本例中，我们将定义一个显示任务列表的简单视图：

```
// resources/views/user.blade.php
<x-layout>
       <div>
        		<h1>我是个人中心</h1>
        </div>
</x-layout>
```

请记住，注入到组件中的内容将提供给 `layout` 组件中的默认 `$slot` 变量。正如你可能已经注意到的，如果提供了 `$title` 插槽，那么我们的 `layout` 也会尊从该插槽；否则，将显示默认的标题。我们可以使用 x-slot插入标题

```

<x-layout>
    <x-slot name="title">
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```



​	



**掌握内容**

- 模板继承
- 继承布局
- 显示数据
- if语句
- 鉴权指令
- Switch语句
- 循环
- Loop变量
- 注释
- PHP代码
- 引入子视图