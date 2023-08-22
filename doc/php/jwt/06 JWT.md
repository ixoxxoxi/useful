# Laravel API 认证：JWT 认证

* 为什么要用JWT
* JWT 是什么

[文档](https://jwt-auth.readthedocs.io/en/develop/laravel-installation/)



#### 什么是 jwt ?

JWT 全称叫 JSON Web Token, 是一个非常轻巧的规范。这个规范允许我们使用 JWT 在用户和服务器之间传递安全可靠的信息。





## 安装 jwt-auth

```
composer require tymon/jwt-auth:1.0.x-dev
```





#### 发布配置

运行以下命令以发布包配置文件：

```
php artisan vendor:publish --provider="Tymon\JWTAuth\Providers\LaravelServiceProvider"
```

您现在应该有一个`config/jwt.php`文件，允许您配置此包的基础知识。

#### 生成密钥

我已经包含了一个帮助命令来为你生成一个密钥：

```
php artisan jwt:secret
```



#### 更新您的用户模型

首先，您需要`Tymon\JWTAuth\Contracts\JWTSubject`在 User 模型上实现合同，这需要您实现 2 个方法`getJWTIdentifier()`和`getJWTCustomClaims()`.

下面的示例应该让您了解它的外观。显然，您应该根据自己的需要进行任何更改。

```
<?php

namespace App;

use Tymon\JWTAuth\Contracts\JWTSubject;
use Illuminate\Notifications\Notifiable;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements JWTSubject
{
    use Notifiable;

    // Rest omitted for brevity

    /**
     * Get the identifier that will be stored in the subject claim of the JWT.
     *
     * @return mixed
     */
    public function getJWTIdentifier()
    {
        return $this->getKey();
    }

    /**
     * Return a key value array, containing any custom claims to be added to the JWT.
     *
     * @return array
     */
    public function getJWTCustomClaims()
    {
        return [];
    }
}
```

### 配置身份验证保护

在该`config/auth.php`文件中，您需要进行一些更改以配置 Laravel 以使用`jwt`防护来支持您的应用程序身份验证。

对文件进行以下更改：

```
'defaults' => [
    'guard' => 'api',
    'passwords' => 'users',
],

...

'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

这里我们告诉`api`守卫使用`jwt`驱动程序，我们将`api`守卫设置为默认值。

我们现在可以使用 Laravel 内置的 Auth 系统，由 jwt-auth 在幕后完成工作！

因为我们用的dingoapi 我们还需要在 config/api.php 里面修改：

```
  'auth' => [
        'jwt' => 'Dingo\Api\Auth\Provider\JWT',
    ],
```

### 创建路由文件

```
<?php

use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\RegisterController;

$api = app('Dingo\Api\Routing\Router');
$api->version(['v1','v2'], ['middleware' => 'api.throttle', 'limit' => 100, 'expires' => 5],function ($api) {
    $api->group(['prefix' => 'auth'], function ($api) {
        // 注册
        $api->post('register', [RegisterController::class, 'store']);
        $api->post('login', [LoginController::class, 'login']);
    });
});

```

创建控制器

```
php artisan make:controller Auth/LoginController

php artisan make:controller Auth/RegisterController
```



### RegisterController

```
    /**
     * 用户注册
     */
    public function store(RegisterRequest $request)
    {
        $user = new User();
        $user->name = $request->input('name');
        $user->email = $request->input('email');
        $user->password = bcrypt($request->input('password'));
        if ($request->input('openid')) $user->openid = $request->input('openid');
        if ($request->input('avatar')) $user->avatar = $request->input('avatar');
        $user->save();
        return $this->response->created();
    }
```





#### RegisterRequest

创建数据注册数据验证

```
php artisan make:request Auth/RegisterRequest
```





``` 

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'name' => 'required|max:16',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:6|max:16|confirmed',
            'openid' => 'sometimes|required|unique:users,openid'
        ];
    }

    public function messages()
    {
        return [
            'name.required' => '昵称 不能为空',
            'name.max' => '昵称 不能超过16个字符',
            'openid.required' => 'openid 不能为空',
            'openid.unique' => 'openid 已绑定其他用户',
        ];
    }

```



### 完成登录

LoginController

[文档](https://jwt-auth.readthedocs.io/en/develop/quick-start/)

因为我们用户有禁用的功能 所以我们还需要调整一下 

```
    /**
     * 登录
     */
    public function login(LoginRequest $request)
    {
        $credentials = request(['email', 'password']);

        if (!$token = auth('api')->attempt($credentials)) {
            return $this->response->errorUnauthorized();
        }

        // 检查用户状态
        $user = auth('api')->user();
        if ($user->is_locked == 1) {
            return $this->response->errorForbidden('被锁定');
        }

        return $this->respondWithToken($token);
    }

```

LoginRequest

```
php artisan make:request Auth/LoginRequest
```

```
   /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'email' => 'required|email',
            'password' => 'required|min:6|max:16',
        ];
    }
```

### 退出登录

路由

```
    $api->group(['middleware' => 'api.auth'], function ($api) {
            $api->post('logout', [LoginController::class, 'logout']);
        });
```





```
 /**
     * 退出登录
     */
    public function logout()
    {
        auth('api')->logout();

        return $this->response->noContent();
    }
```

### 刷新TOKEN 

```
     // 刷新token
            $api->post('refresh', [LoginController::class, 'refresh']);
           
```

```
   /**
     * 刷新token
     */
    public function refresh()
    {
        return $this->respondWithToken(auth('api')->refresh());
    }
```

