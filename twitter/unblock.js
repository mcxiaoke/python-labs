/* 
* @Author: mcxiaoke
* @Date:   2016-01-07 16:28:22
* @Last Modified by:   mcxiaoke
* @Last Modified time: 2016-01-07 16:30:11
*/
// 移除所有被屏蔽的帐号 https://twitter.com/settings/blocked
[].slice.call(document.getElementsByClassName("blocked-text")).map(function ub(e){e.click();});
