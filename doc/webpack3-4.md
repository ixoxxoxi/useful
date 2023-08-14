## https://blog.51cto.com/u_15725382/5735158

### 修复大小限制的报错

```
AssetsOverSizeLimitWarning: asset size limit: The following asset(s) exceed the recommended size limit (244 KiB 250000Byte). This can impact web performance.
```

```js
// webpack.config.js
module.exports = {
	performance: {
		hints: "warning",
		maxEntrypointSize: 5000 * 1024,
		maxAssetSize: 5000 * 1024,
	},
};
```

### 生成 manifest.js，生成 vendors.js

```js
// https://webpack.js.org/configuration/optimization/#optimizationsplitchunks
// 生成manifest.js
optimization: {
    runtimeChunk: {
        name:'manifest'
```

```js
// https://webpack.js.org/plugins/split-chunks-plugin/#split-chunks-example-1
// 生成 vendors.js
optimization: {
  splitChunks: {
    cacheGroups: {
      commons: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all',
      },
    },
  },
}
```

```js
output: {
-   chunkFilename: utils.assetsPath('js/[id].[chunkhash].js'),
+   chunkFilename: utils.assetsPath('js/[name].[chunkhash].js'),
  },
```

### 文件可以更小一些吗？构建速度可以更快一些吗？

- 未使用 TerserPlugin 而是用 UglifyjsPlugin
- OptimizeCSSPlugin 位置放错
- 如果手动配置 splitChunks 的话，一定要把没有配置的参数也配置上
- devtool 由最慢的“source-map”改为 false

引入 TerserPlugin 的话，需要首先升级 node 到 v10.17.0+。

```js
const TerserPlugin = require("terser-webpack-plugin");
module.exports = {
	optimization: {
		minimize: true,
		minimizer: [
			// Compress extracted CSS. We are using this plugin so that possible
			// duplicated CSS from different presentation can be deduped.
			new OptimizeCSSPlugin({
				cssProcessorOptions: config.build.productionSourceMap ? { safe: true, map: { inline: false } } : { safe: true },
			}),
			new TerserPlugin({
				cache: true,
				parallel: true,
				sourceMap: Boolean(config.build.productionSourceMap),
			}),
		],
	},
};
```

增加下面的配置：

```js
optimization: {
  splitChunks: {
    chunks: 'async',
    minSize: 30000,
    maxSize: 0,
    minChunks: 1,
    maxAsyncRequests: 5,
    maxInitialRequests: 3,
    automaticNameDelimiter: '~',
    automaticNameMaxLength: 30,
  }
}
```

### webpack3 与 webpack4 开发依赖对比

```js
// webpack3
"webpack": "^3.6.0"
"webpack-dev-server": "^2.9.1"
"eslint-loader": "^1.7.1"
"vue-loader": "^13.3.0"
"happypack": "^5.0.0"
"html-webpack-plugin": "^2.30.1"
"extract-text-webpack-plugin": "^3.0.0"
"uglifyjs-webpack-plugin": "^1.1.1"
```

```js
// webpack4
"webpack": "^4.43.0"
"webpack-cli": "^3.3.11"
"webpack-dev-server": "^3.7.2"
"thread-loader": "^2.1.3"
"eslint-loader": "^4.0.2"
"vue-loader": "^15.9.2"
"html-webpack-plugin": "^4.3.0"
"mini-css-extract-plugin": "^0.9.0"
"terser-webpack-plugin": "^3.0.1"
"babel-plugin-transform-es2015-modules-commonjs": "^6.26.2"
```

## https://www.jianshu.com/p/ddc96ac48754

### 注释 extract-text-webpack-plugin 相关代码

[https://github.com/BothEyes1993/webpack4_demo](https://github.com/BothEyes1993/webpack4_demo)

```js
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
if (options.extract) {
	//   return ExtractTextPlugin.extract({
	//     use: loaders,
	//     fallback: 'vue-style-loader'
	//   })
	return [MiniCssExtractPlugin.loader].concat(loaders);
} else {
	return ["vue-style-loader"].concat(loaders);
}
```

```js
  const webpackConfig = merge(baseWebpackConfig, {
    ...,
   optimization: {
    //取代 new UglifyJsPlugin
    minimizer: [
      // 压缩代码
      new UglifyJsPlugin({
        uglifyOptions: {
          compress: {
            warnings: false,
            drop_debugger: true,//关闭debug
            drop_console: true,//关闭console
          }
        },
        sourceMap: config.build.productionSourceMap,
        parallel: true
      }),
      // 可自己配置，建议第一次升级先不配置
      new OptimizeCSSPlugin({
        // cssProcessorOptions: config.build.productionSourceMap
        //     ? {safe: true, map: {inline: false}, autoprefixer: false}
        //     : {safe: true}
      }),
    ],
    // 识别package.json中的sideEffects以剔除无用的模块，用来做tree-shake
    // 依赖于optimization.providedExports和optimization.usedExports
    sideEffects: true,
    // 取代 new webpack.optimize.ModuleConcatenationPlugin()
    concatenateModules: true,
    // 取代 new webpack.NoEmitOnErrorsPlugin()，编译错误时不打印输出资源。
    noEmitOnErrors: true,
    splitChunks: {
      cacheGroups: {
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          chunks: 'initial',
          name: 'vendors',
        },
        'async-vendors': {
          test: /[\\/]node_modules[\\/]/,
          minChunks: 2,
          chunks: 'async',
          name: 'async-vendors'
        }
      }
    },
    runtimeChunk: { name: 'runtime' }
    },
  })

```

## https://codeleading.com/article/2504860251/

### webpack.optimize.UglifyJsPlugin has been removed

webpack4.x 中已经没有 UglifyJsPlugin

- 1.把 webpack.prod.conf.js 中 UglifyJsPlugin 相关代码注释掉。
- 2.在 package.json 的 scripts 下的 build 命令添加一个参数，即可实现 js 的压缩 。
- –mode production 表示生产环境

```js
//webpack.prod.conf.js 文件 注释UglifyJsPlugin配置
// new webpack.optimize.UglifyJsPlugin({
//   compress: {
//     warnings: false
//   },
//   sourceMap: config.build.productionSourceMap,
//   parallel: true
// }),
```

```js
//package.json文件 添加 --mode production参数
"scripts": {
   "start": "npm run dev",
   "build": "node build/build.js --mode production",
   "analyz": "NODE_ENV=production npm_config_report=true npm run deploy:prod"
 },
```

### webpack.optimize.CommonsChunkPlugin has been removed

webpack4.x 中已经没有 CommonsChunkPlugin

- 1.把 webpack.prod.conf.js 中 CommonsChunkPlugin 相关代码注释掉。
- 2.在 webpack.prod.conf.js 中添加配置，与 plugins 同级的。

```js
//webpack.prod.conf.js 文件，注释CommonsChunkPlugin配置
// new webpack.optimize.CommonsChunkPlugin({
//   name: 'vendor',
//   minChunks: function (module) {
//     // any required modules inside node_modules are extracted to vendor
//     return (
//       module.resource &&
//       /\.js$/.test(module.resource) &&
//       module.resource.indexOf(
//         path.join(__dirname, '../node_modules')
//       ) === 0
//     )
//   }
// }),
// new webpack.optimize.CommonsChunkPlugin({
//   name: 'manifest',
//   minChunks: Infinity
// }),
// new webpack.optimize.CommonsChunkPlugin({
//   name: 'app',
//   async: 'vendor-async',
//   children: true,
//   minChunks: 3
// }),
```

```js
//新配置
  plugins：[...],
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all'
        },
        manifest: {
          name: 'manifest',
          minChunks: Infinity
        },
      }
    },
  }

```

### Error: Chunk.entrypoints: Use Chunks.groupsIterable and filter by instanceof Entrypoint instead

extract-text-webpack-plugin 不兼容 webpack4.x，2 种方案：

- 1.升级包到^4.0.0-beta.0，不过官方不推荐，而且我升级之后会出现问题 4。
- 2.使用 mini-css-extract-plugin 替代。

```js
//1.去掉package.json 中的 "extract-text-webpack-plugin": "^4.0.0-beta.0"

//2.安装 mini-css-extract-plugin
npm install --save-dev mini-css-extract-plugin

//3.修改webpack.prod.conf.js配置
//注释掉
 // const ExtractTextPlugin = require('extract-text-webpack-plugin')
 // new ExtractTextPlugin({
 //   filename: utils.assetsPath('css/[name].[contenthash].css'),
 //   allChunks: false,
 // }),
// 添加
 new MiniCssExtractPlugin({
      filename: utils.assetsPath('css/[name].[contenthash].css'),
      allChunks: false,
    }),

```

### vue-loader was used without the corresponding plugin. Make sure to include VueLoaderPlugin in your webpack config

```js
const { VueLoaderPlugin } = require('vue-loader');
plugins: [
	new VueLoaderPlugin(),
	...
]

```

```js
// plugins
const webpackConfig = merge(baseWebpackConfig, {
  module: {...},
  optimization: { // 增加此处代码
    // Setting optimization.runtimeChunk to true adds an additonal chunk to each entrypoint containing only the runtime.
    // The value single instead creates a runtime file to be shared for all generated chunks.
    runtimeChunk: 'single',
    minimize: env === 'production' ? true : false, //生产环境下才进行代码压缩。
    splitChunks:{
      //As it was mentioned before this plugin will affect dynamic imported modules. Setting the optimization.
      //splitChunks.chunks option to "all" initial chunks will get affected by it (even the ones not imported dynamically).
      //This way chunks can even be shared between entry points and on-demand loading.
      //This is the recommended configuration.
      //官方推荐使用all.
      chunks: 'all',
      minSize: 30000, //模块大于30k会被抽离到公共模块
      minChunks: 1, //模块出现1次就会被抽离到公共模块
      maxAsyncRequests: 5, //异步模块，一次最多只能被加载5个
      maxInitialRequests: 3, //入口模块最多只能加载3个
      name: true, // 拆分出来块的名字(Chunk Names)，默认由块名和hash值自动生成；设置为true则表示根据模块和缓存组秘钥自动生成。
      cacheGroups: {
        // 详情建议参看官网 http://webpack.html.cn/plugins/split-chunks-plugin.html
        default: {
          minChunks: 2,
          reuseExistingChunk: true,
        },
        //打包重复出现的代码
        vendor: {
            // chunks: 'initial',
            // 省略test默认选择所有的模块。
            chunks: 'all',
            minChunks: 2,
            name: 'vendor'
        },
        //打包第三方类库
        commons: {
            // chunks: "initial",
            chunks: "all",
            name: "commons",
            minChunks: Infinity
        }
      }
    }
  },
  plugins: [...]
})
```

```js
// utils.js
'use strict'
...
// const ExtractTextPlugin = require('extract-text-webpack-plugin') //删除或注释此段。
// 引入
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
...

// 修改此处的generateLoaders函数。
  // generate loader string to be used with extract text plugin
  function generateLoaders(loader, loaderOptions) {
    const loaders = options.usePostCSS ? [cssLoader, postcssLoader] : [cssLoader]

    if (loader) {
      loaders.push({
        loader: loader + '-loader',
        options: Object.assign({}, loaderOptions, {
          sourceMap: options.sourceMap
        })
      })
    }
    // Extract CSS when that option is specified
    // (which is the case during production build)
    if (options.extract) {
     /**注释或删除此处代码，开始 */
     // return ExtractTextPlugin.extract({
     //   use: loaders,
     //   publicPath: '../../',
     //   fallback: 'vue-style-loader'
     // })
     /**注释或删除此处代码，结束 */
     /**增加此处代码开始 */
     return [MiniCssExtractPlugin.loader].concat(loaders)
     /**增加此处代码结束 */
    } else {
      return ['vue-style-loader'].concat(loaders)
    }
  }
```

```js
output： {........},

optimization: {
    runtimeChunk: { name: 'manifest' },
    minimizer: [new UglifyJsPlugin({ cache: true, parallel: true, sourceMap:config.build.productionSourceMap, uglifyOptions: { warnings: false } }), new OptimizeCSSPlugin({ cssProcessorOptions: config.build.productionSourceMap ? { safe: true, map: { inline: false } } : { safe: true } }),], splitChunks: { chunks: 'async', minSize: 30000, minChunks: 1, maxAsyncRequests: 5, maxInitialRequests: 3, name: false, cacheGroups: { vendor: { name: 'vendor', chunks: 'initial', priority: -10, reuseExistingChunk: false, test: /node_modules\/(.*)\.js/ }, styles: { name: 'styles', test: /\.(scss|css)$/, chunks: 'all', minChunks: 1, reuseExistingChunk: true, enforce: true } } } },

plugins: [..........]
```

---

```js
注释调extract - text - webpack - plugin相关代码;
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
if (options.extract) {
	//   return ExtractTextPlugin.extract({
	//     use: loaders,
	//     fallback: 'vue-style-loader'
	//   })
	return [MiniCssExtractPlugin.loader].concat(loaders);
} else {
	return ["vue-style-loader"].concat(loaders);
}
```

```js
// const ExtractTextPlugin = require('extract-text-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
module.exports添加
    optimization: {
        splitChunks: {
          cacheGroups: {
            styles: {
              name: 'styles',
              test: /\.css$/,
              chunks: 'all',
              enforce: true
            }
          }
        }
    },

```

```js
const MiniCssExtractPlugin  = require('mini-css-extract-plugin');
module: {
        rules: [
        {
            test: /\.css$/,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'postcss-loader',
            ]
        },
        {
            test: /\.styl(us)?$/,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'postcss-loader',
                'stylus-loader'
            ]
        },
        {
            test: /\.less$/,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'postcss-loader',
                'less-loader'
            ]
        },
        {
            test: /\.(scss|sass)$/,
            use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'postcss-loader',
                'sass-loader'
            ]
        },
    ]
    },

plugins: [
    new MiniCssExtractPlugin({
        filename: utils.assetsPath('css/[name].[contenthash].css'),
    }), // 新增

]
```

```js
optimization: {
    splitChunks: {
        chunks: 'async',
        minSize: 20000,
        minChunks: 1,
        maxAsyncRequests: 30,
        maxInitialRequests: 30,
        cacheGroups: {
            vendors: { // 工程基础包 例如包括vue、vue-router、axios等常用不改变的包，可以做缓存
                test: /[\\/]node_modules[\\/]/,
                name: 'vendor',
                chunks: 'all',
                priority: -10,
                reuseExistingChunk: true,
            },
            app: { // 业务基础包大部分不是node_modules的模块，例如我们在common中存放的一些基础组件，其次是一些三方的组件库（这些是在node_modules中的，但是因为经常变动所以不适宜放在vendor中）
                minChunks: 3,
                name: 'app',
                priority: -20,
                reuseExistingChunk: true,
            },
        }
    }
  },
```

```js
//webpack.prod.conf.js

optimization: {

    //其他配置

    runtimeChunk: {

      name: 'manifest'

    },

    splitChunks:{

      chunks: 'async',

      minSize: 30000,

      minChunks: 1,

      maxAsyncRequests: 5,

      maxInitialRequests: 3,

      name: false,

      cacheGroups: {

        vendor: {

          name: 'vendor',

          chunks: 'initial',

          priority: -10,

          reuseExistingChunk: false,

          test: /node_modules\/(.*)\.js/

        },

        styles: {

          name: 'styles',

          test: /\.(scss|css)$/,

          chunks: 'all',

          minChunks: 1,

          reuseExistingChunk: true,

          enforce: true

        }

      }

    }

  },
```

```js
optimization: {

    minimizer: [

      new UglifyJsPlugin({

        cache: true,

        parallel: true,

        sourceMap: true // set to true if you want JS source maps

      }),

      new OptimizeCSSAssetsPlugin({})

    ],

}
```

```js

```
