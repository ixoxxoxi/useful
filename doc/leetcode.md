## 555. 分割连接字符串

给定一个字符串列表 strs，你可以将这些字符串连接成一个循环字符串，对于每个字符串，你可以选择是否翻转它。在所有可能的循环字符串中，你需要分割循环字符串（这将使循环字符串变成一个常规的字符串），然后找到字典序最大的字符串。

具体来说，要找到字典序最大的字符串，你需要经历两个阶段：

1. 将所有字符串连接成一个循环字符串，你可以选择是否翻转某些字符串，并按照给定的顺序连接它们。
2. 在循环字符串的某个位置分割它，这将使循环字符串从分割点变成一个常规的字符串。
   你的工作是在所有可能的常规字符串中找到字典序最大的一个。

**示例 1:**

```
输入: strs = ["abc","xyz"]
输出: "zyxcba"
解释: 你可以得到循环字符串 "-abcxyz-", "-abczyx-", "-cbaxyz-", "-cbazyx-"，其中 '-' 代表循环状态。
答案字符串来自第四个循环字符串， 你可以从中间字符 'a' 分割开然后得到 "zyxcba"。
```

**示例 2:**

```
输入: strs = ["abc"]
输出: "cba"
```

**提示:**

- `1 <= strs.length <= 1000`
- `1 <= strs[i].length <= 1000`
- `1 <= sum(strs[i].length) <= 1000`
- `strs[i]` 只包含小写英文字母

### 解法：

```js
/**
 * @param {string[]} strs
 * @return {string}
 */
var splitLoopedString = function (strs) {
	for (let i = 0, len = strs.length; i < len; i++) {
		let str = strs[i];
		let rev = reverse(str);
		if (rev > str) {
			strs[i] = rev;
		}
	}
	let ans = "";
	for (let i = 0, len = strs.length; i < len; i++) {
		let str = strs[i];
		let rev = reverse(str);
		let other = "";
		for (let j = i + 1, jlen = strs.length; j < jlen; j++) {
			other += strs[j];
		}
		for (let j = 0; j < i; j++) {
			other += strs[j];
		}
		for (let j = 0, jlen = str.length; j < jlen; j++) {
			let cur = str.substring(j) + other + str.substring(0, j);
			if (cur > ans) {
				ans = cur;
			}
		}
		for (let j = 0, jlen = str.length; j < jlen; j++) {
			let cur = rev.substring(j) + other + rev.substring(0, j);
			if (cur > ans) {
				ans = cur;
			}
		}
	}
	return ans;
};

function reverse(str) {
	let res = "";
	for (let i = 0, len = str.length; i < len; i++) {
		res += str[len - 1 - i];
	}
	return res;
}
```

## 1063. 有效子数组的数目

给定一个整数数组 nums ，返回满足下面条件的 非空、连续 子数组的数目：

- 子数组 是数组的 连续 部分。
- 子数组最左边的元素不大于子数组中的其他元素 。

**示例 1：**

```
输入：nums = [1,4,2,5,3]
输出：11
解释：有 11 个有效子数组，分别是：[1],[4],[2],[5],[3],[1,4],[2,5],[1,4,2],[2,5,3],[1,4,2,5],[1,4,2,5,3] 。
```

**示例 2：**

```
输入：nums = [3,2,1]
输出：3
解释：有 3 个有效子数组，分别是：[3],[2],[1] 。
```

**示例 3：**

```
输入：nums = [2,2,2]
输出：6
解释：有 6 个有效子数组，分别为是：[2],[2],[2],[2,2],[2,2],[2,2,2] 。
```

**提示：**

- 1 <= nums.length <= $5 \times$ $10^{4}$

- 0 <= nums[i] <= $10^{5}$

### 解法一：

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
var validSubarrays = function (nums) {
	const stack = [];
	let res = 0;
	for (let num of nums) {
		while (stack.length !== 0 && stack[stack.length - 1] > num) {
			stack.pop();
		}
		stack.push(num);
		res += stack.length;
	}
	return res;
};
```

### 解法二：

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
var validSubarrays = function (nums) {
	const stack = [];
	const len = nums.length;
	let ans = 0;
	for (let i = 0; i < len; i++) {
		while (stack.length && nums[stack[stack.length - 1]] > nums[i]) {
			ans += i - 1 - stack.pop() + 1;
		}
		stack.push(i);
	}
	while (stack.length) {
		ans += len - stack.pop();
	}
	return ans;
};
```
