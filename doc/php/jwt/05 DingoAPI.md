# Dingo API 

## 安装

```
composer require dingo/api
```

### Laravel

如果您想在配置文件中进行配置更改，您可以使用以下 Artisan 命令发布它（否则，不需要此步骤）：

```
php artisan vendor:publish --provider="Dingo\Api\Provider\LaravelServiceProvider"

```



#### 配置相应

```
<?php

namespace App\Http\Controllers;

use Dingo\Api\Routing\Helpers;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Bus\DispatchesJobs;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

class Controller extends BaseController
{
    use AuthorizesRequests, DispatchesJobs, ValidatesRequests;
    use Helpers;
}

```



#### 配置信息



```
API_STANDARDS_TREE=x
API_SUBTYPE=shop
API_PREFIX=api
API_VERSION=v1
API_NAME=shop
API_CONDITIONAL_REQUEST=false
API_STRICT=false
API_DEFAULT_FORMAT=json
API_DEBUG=true
```



#### 创建路由文件 

App\Providers\RouteServiceProvider



```
            // 用户认证相关路由
            Route::prefix('api')
                ->middleware('api')
                ->namespace($this->namespace)
                ->group(base_path('routes/auth.php'));

            // 前台路由
            Route::prefix('api')
                ->middleware('api')
                ->namespace($this->namespace)
                ->group(base_path('routes/api.php'));

            // 后台路由
            Route::prefix('api')
                ->middleware('api')
                ->namespace($this->namespace)
                ->group(base_path('routes/admin.php'));

```

#### 路由的使用

##### 版本组

为了避免与你主要的项目路由冲突，dingo/api 将会使用其专属的路由实例。要创建端点，我们首先需要获得一个 API 路由的实例：

```
$api = app('Dingo\Api\Routing\Router');
```

现在我们必须定义一个版本分组。这种定义方式有利于后续为相同端点新增多版本支持。

```php
$api->version('v1', function ($api) {

});
```

如果你想一个分组返回多个版本，只需要传递一个版本数组。

```php
$api->version(['v1', 'v2'], function ($api) {

});
```

通过在第二个参数上传递一个属性数组，你也可以将此组视为特定框架的标准组。

```php
$api->version('v1', ['middleware' => 'foo'], function ($api) {

});
```

你还可以嵌套常规组以进一步定制某些端点。

```php
$api->version('v1', function ($api) {
    $api->group(['middleware' => 'foo'], function ($api) {
      
    });
});
```



#### 创建路由

一旦你有了一个版本分组，你就可以在分组闭包的参数中，通过 `$api` 创建端点。

```
$api->version('v1', function ($api) {
    $api->get('users/{id}', 'App\Api\Controllers\UserController@show');
});
```

创建前台控制器

```
php artisan make:controller Api/UserController
```



#### 响应

#### 直接返回模型

```php
class UserController
{
    public function show()
    {
        return User::all();
    }
}
```

你可以返回一个单一的用户。

```php
class UserController
{
    public function show($id)
    {
        return User::findOrFail($id);
    }
}
```



## 响应生成器

响应生成器提供了一个流畅的接口去方便的建立一个更定制化的响应。响应的生成器通常是与 **transformer** 相结合。

要利用响应生成器，你的控制器需要使用 `Dingo\Api\Routing\Helpers` trait。为了在你的控制器里保持引入和使用这个 trait，你可以创建一个基础控制器，然后你的所有的 API 控制器都继承它。

```
use Dingo\Api\Routing\Helpers;
use Illuminate\Routing\Controller;

class BaseController extends Controller
{
    use Helpers;
}
```

现在你的控制器可以直接继承基础控制器。响应生成器可以在控制器里通过 `$response` 属性获取。

### 响应一个数组

```
class UserController extends BaseController
{
    public function show($id)
    {
        $user = User::findOrFail($id);

        return $this->response->array($user->toArray());
    }
}
```

### 响应一个元素

```
class UserController extends BaseController
{
    public function show($id)
    {
        $user = User::findOrFail($id);

        return $this->response->item($user, new UserTransformer);
    }
}
```

每个Transformer 可以对应一个模型，用来格式化响应的数据。`Transformers` 创建在APP目录下。Transformers 允许你便捷地、始终如一地将对象转换为一个数组。通过使用一个 transformer 你可以对整数和布尔值，包括分页结果和嵌套关系进行类型转换。	

```
<?php


namespace App\Transformers;


use App\Models\User;
use League\Fractal\TransformerAbstract;

class UserTransformer extends TransformerAbstract
{
    public function transform(User $user)
    {
        return [
            'id' => $user->id,
            'name' => $user->name,
            'email' => $user->email,
            'phone' => $user->phohe,
            'avatar' => $user->avatar,
            'openid' => $user->openid,
        ];
    }
}

```

### 响应一个元素集合

```
class UserController extends BaseController
{
    public function index()
    {
        $users = User::all();

        return $this->response->collection($users, new UserTransformer);
    }
}
```



### 分页响应

```
class UserController extends BaseController
{
    public function index()
    {
        $users = User::paginate(25);

        return $this->response->paginator($users, new UserTransformer);
    }
}
```

### 无内容响应

```
return $this->response->noContent();
```

### 创建了资源的响应

```
return $this->response->created();
```

### 错误响应

这有很多不同的方式创建错误响应，你可以快速的生成一个错误响应。

```
// 一个自定义消息和状态码的普通错误。
return $this->response->error('This is an error.', 404);

// 一个没有找到资源的错误，第一个参数可以传递自定义消息。
return $this->response->errorNotFound();

// 一个 bad request 错误，第一个参数可以传递自定义消息。
return $this->response->errorBadRequest();

// 一个服务器拒绝错误，第一个参数可以传递自定义消息。
return $this->response->errorForbidden();

// 一个内部错误，第一个参数可以传递自定义消息。
return $this->response->errorInternal();

// 一个未认证错误，第一个参数可以传递自定义消息。
return $this->response->errorUnauthorized();
```

### 添加 Meta 信息

```
return $this->response->item($user, new UserTransformer)->addMeta('foo', 'bar');

```



###  API 节流

节流限速 (throttling) 允许你限制客户端给定时间的访问次数。限制和过期时间是在限速器里定义的。 默认有两个限速器，验证通过限速器和未验证限速器。

##### 启用节流限制

要为路由或路由组启用节流限制，你必须启用 `api.throttle` 中间件。 一旦启用了节流限制，你必须已经配置过了一些限制或配置过了具体的路由限制。

#####  在所有的路由中启用节流限制

```
$api->version('v1', ['middleware' => 'api.throttle'], function ($api) {
    // 此版本组中的路由将需要身份认证.
});
```

##### 路由特定节流

如果只是想限制某些路由或者路由群组，可使用 `limit` 和 `expires` 选项。

```
$api->version('v1', function ($api) {
    $api->get('users', ['middleware' => 'api.throttle', 'limit' => 100, 'expires' => 5, function () {
        return User::all();
    }]);
});
```

以上为这个路由设置了请求限制 100 次，过期时间 5 分钟。如果你把它设置在路由群组上，那组内的每个路由具有 100 次请求的限制。

```
$api->version('v1', ['middleware' => 'api.throttle', 'limit' => 100, 'expires' => 5], function ($api) {
    $api->get('users', function () {
        return User::all();
    });

    $api->get('posts', function () {
        return Post::all();
    });
});
```



### 模型注入 

app/Http/Kernel.php

```
    protected $routeMiddleware = [
......
        'bindings' =>  \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ];
```

### 去除data 

https://packagist.org/packages/liyu/dingo-serializer-switch

```
$api->version('v1',
    ['middleware' => 'serializer:array'],
    function ($api) {
});
```

