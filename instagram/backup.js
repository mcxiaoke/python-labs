/* 
 * @Author: mcxiaoke
 * @Date:   2016-01-04 12:00:01
 * @Last Modified by:   mcxiaoke
 * @Last Modified time: 2016-01-04 12:11:57
 */

function print_url(tag) {
    console.log(tag.src);
}
var tags = document.getElementsByClassName("_icyx7");
[].slice.call(tags).map(print_url);
