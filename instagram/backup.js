/* 
 * @Author: mcxiaoke
 * @Date:   2016-01-04 12:00:01
 * @Last Modified by:   mcxiaoke
 * @Last Modified time: 2016-01-12 17:39:43
 */
// 打印Instagram个人页面所有大图的URL
[].slice.call(document.getElementsByClassName("_icyx7")).map(function pu(tag) {
    console.log(tag.src);
});


Array.prototype.map.call(document.querySelectorAll('._icyx7'), function(tag) {
    return tag.src.replace('s640x640/sh0.08/', '')
}).map(function(i) {
    var l = document.createElement('a');
    l.href = i;
    l.download = i;
    document.body.appendChild(l);
    l.click()
});
