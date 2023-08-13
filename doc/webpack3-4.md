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

```

```js

```

```js

```
