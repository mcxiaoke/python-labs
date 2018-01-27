/* @author:Net@lilybbs ( http://bianbian.org ) */
$s = function () {
    for (var a = 0; a < arguments.length; a += 2) {
        for (var b in arguments[a + 1]) {
            arguments[a][b] = arguments[a + 1][b]
        }
    }
};
$s(Object, {toJSON: function (c) {
    switch (typeof c) {
        case"undefined":
        case"function":
        case"unknown":
            return;
        case"number":
        case"boolean":
            return c.toString()
    }
    if (c === null) {
        return"null"
    }
    if (c.toJSON) {
        return c.toJSON()
    }
    if (Object.isElement(c)) {
        return
    }
    var a = [];
    for (var d in c) {
        var b = Object.toJSON(c[d]);
        if (b !== undefined) {
            a.push(d.toJSON() + ":" + b)
        }
    }
    return"{" + a.join(",") + "}"
}, isElement: function (a) {
    return a && a.nodeType == 1
}});
$s(String.prototype, {formatReg: [], format: function () {
    var b = this;
    for (var a = 0; a < arguments.length; a++) {
        if (!this.formatReg[a]) {
            this.formatReg[a] = new RegExp("\\{" + a + "\\}", "g")
        }
        b = b.replace(this.formatReg[a], arguments[a])
    }
    return b
}, CHINESE: /[^ -~\033\s]/g, chars: function () {
    var a = this.match(this.CHINESE);
    return a == null ? this.length : this.length + a.length
}, isChineseCharAt: function (a) {
    return this.CHINESE.test(this.charAt(a))
}, include: function (a) {
    return this.indexOf(a) > -1
}, stripTags: function () {
    return this.replace(/<\/?[^>]+>/gi, "")
}, stripScripts: function () {
    return this.replace(/<script[^>]*>([\S\s]*?)<\/script>/img, "")
}, trim: function (a) {
    return this.replace(/(^\s*)|(\s*$)/g, "")
}, startsWith: function (a) {
    return this.indexOf(a) === 0
}, endsWith: function (a) {
    var b = this.length - a.length;
    return b >= 0 && this.lastIndexOf(a) === b
}, times: function (c) {
    var a = "";
    for (var b = 0; b < c; b++) {
        a += this
    }
    return a
}, toJSON: function () {
    return'"' + this.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"'
}, evalJSON: function () {
    try {
        return eval("(" + this + ")")
    } catch (e) {
        throw new SyntaxError("JSON error: " + this)
    }
}});
CONST_ARRAY_EACH_BREAK = 7758521;
$s(Array.prototype, {each: function (c) {
    for (var b = 0, a = this.length; b < a; b++) {
        if (c(this[b], b) == CONST_ARRAY_EACH_BREAK) {
            break
        }
    }
}, clear: function () {
    this.length = 0;
    return this
}, indexOf: function (a) {
    for (var b = 0, c = this.length; b < c; b++) {
        if (this[b] == a) {
            return b
        }
    }
    return -1
}, max: function () {
    for (var a = this[0], b = 1; b < this.length; b++) {
        if (this[b] > a) {
            a = this[b]
        }
    }
    return a
}, toJSON: function () {
    var a = [];
    this.each(function (b) {
        var c = Object.toJSON(b);
        if (c !== undefined) {
            a.push(c)
        }
    });
    return"[" + a.join(",") + "]"
}});
Net = {Browser: {IE: !!(window.attachEvent && !window.opera), Opera: !!window.opera, WebKit: navigator.userAgent.indexOf("AppleWebKit/") > -1, Gecko: navigator.userAgent.indexOf("Gecko") > -1 && navigator.userAgent.indexOf("KHTML") == -1}, Cookie: {get: function (a) {
    var c = document.cookie.split("; ");
    for (var d = 0; d < c.length; d++) {
        var b = c[d].split("=");
        if (b[0] == a) {
            return unescape(b[1])
        }
    }
    return""
}, set: function (a, b) {
    if (b == "") {
        document.cookie = a + '=""; expires="Thu, 01 Jan 1970 00:00:01 GMT"'
    } else {
        document.cookie = a + "=" + escape(b)
    }
}}, Point: function (b, a) {
    this.x = this.left = b;
    this.y = this.top = a
}, Rect: function (c, b, a, d) {
    this.x = this.left = c;
    this.y = this.top = b;
    this.w = this.width = a;
    this.h = this.height = d;
    this.getLeftTop = function () {
        return(new Net.Point(this.x, this.y))
    }
}};
Net.Dom = {get: function (a) {
    return(typeof a == "string") ? document.getElementById(a) : a
}, getBody: function () {
    return(document.body) ? document.body : document.documentElement
}, getsByName: function (b, a) {
    if (!a) {
        a = document
    }
    return a.getElementsByName(b)
}, getsByTagName: function (b, a) {
    if (!a) {
        a = document
    }
    return a.getElementsByTagName(b)
}, getsByClassName: function (e, h, k) {
    var d = this.getsByTagName(e, k);
    var b = new Array();
    for (var g = 0; g < d.length; g++) {
        var c = d[g];
        var a = c.className.split(" ");
        for (var f = 0; f < a.length; f++) {
            if (a[f] == h) {
                b.push(c);
                break
            }
        }
    }
    return b
}, getFrame: function (b) {
    for (var a = 0; a < window.top.frames.length; a++) {
        if (window.top.frames[a].name == b) {
            return window.top.frames[a]
        }
    }
}, create: function (a, d, c) {
    var b = document.createElement(a);
    if (c) {
        $s(b, c)
    }
    if (d) {
        d.appendChild(b)
    }
    return(b)
}, insert: function (c, a, b) {
    a.parentNode.insertBefore(c, b ? a : a.nextSibling)
}, remove: function (a) {
    a.parentNode.removeChild(a)
}};
Net.Util = {copyToClip: function (a) {
    try {
        window.clipboardData.setData("text", a);
        alert("已经复制到剪贴板")
    } catch (b) {
        Net.Dialog.show("需要复制的内容如下: ", a)
    }
}, loadJs: function (e, a) {
    if (!a) {
        a = document
    }
    var f = Net.Dom.getsByTagName("script", a);
    for (var b = 0; b < f.length; b++) {
        if (f[b].src && f[b].src.indexOf(e) > -1) {
            return f[b]
        }
    }
    var d = a.createElement("script");
    $s(d, {type: "text/javascript", src: e});
    Net.Dom.getsByTagName("head", a)[0].appendChild(d);
    return d
}, loadCss: function (c, a) {
    if (!a) {
        a = document
    }
    var b = a.createElement("link");
    $s(b, {href: c, rel: "stylesheet", type: "text/css"});
    Net.Dom.getsByTagName("head", a)[0].appendChild(b);
    return b
}, saveAs: function () {
    if (!Net.Browser.IE) {
        alert("非IE浏览器请直接另存即可");
        return
    }
    var b = '<base href="' + Net.BBS.HOST + '">';
    var a = document.all.item(0, 0);
    while (a != null) {
        b += a.outerHTML;
        a = a.nextSibling
    }
    document.open("text/html", "gb2312");
    document.write(b);
    document.execCommand("SaveAs", true, "bbssave.htm")
}, toQuery: function (a, c) {
    var b = [];
    if (typeof c == "object") {
        for (var d in c) {
            b.push(d + "=" + (c[d] ? encodeURIComponent(c[d]) : ""))
        }
    }
    return a + "?" + b.join("&")
}, addFav: function (a, c) {
    a = Net.BBS.HOST + a;
    c = c || a;
    try {
        if (Net.Browser.IE) {
            external.AddFavorite(a, c)
        } else {
            sidebar.addPanel(c, a, "")
        }
    } catch (b) {
        alert("浏览器不支持!")
    }
}, urlencode: function (a) {
    return encodeURIComponent(a + "").replace(/!/g, "%21").replace(/'/g, "%27").replace(/\(/g, "%28").replace(/\)/g, "%29").replace(/\*/g, "%2A").replace(/%20/g, "+")
}};
Net.Event = {element: function (a) {
    return $(a.target || a.srcElement)
}, observers: false, _observeAndCache: function (c, b, a) {
    if (!this.observers) {
        this.observers = []
    }
    this.observers.push([c, b, a]);
    if (c.addEventListener) {
        c.addEventListener(b, a, false)
    } else {
        if (c.attachEvent) {
            c.attachEvent("on" + b, a)
        }
    }
}, unloadCache: function () {
    if (!this.observers) {
        return
    }
    for (var a = 0, b = this.observers.length; a < b; a++) {
        this.stopObserving.apply(this, this.observers[a]);
        this.observers[a][0] = null
    }
    this.observers = false
}, observe: function (c, b, a) {
    c = $(c);
    Net.Event._observeAndCache(c, b, a)
}, stopObserving: function (c, b, a) {
    c = $(c);
    if (c.removeEventListener) {
        c.removeEventListener(b, a, false)
    } else {
        if (c.detachEvent) {
            try {
                c.detachEvent("on" + b, a)
            } catch (d) {
            }
        }
    }
}};
if (!window.XMLHttpRequest) {
    window.XMLHttpRequest = function () {
        var a, b = ["Msxml2.XMLHTTP.3.0", "Msxml2.XMLHTTP", "Microsoft.XMLHTTP"];
        for (a = 0; a < b.length; a++) {
            try {
                return new ActiveXObject(b[a])
            } catch (c) {
            }
        }
        alert("建立XMLHttp对象失败，请升级浏览器")
    }
}
Net.Ajax = function (b, f, c, e, d) {
    var a = new XMLHttpRequest();
    a.onreadystatechange = function () {
        if (a.readyState == 4) {
            if (a.status == 200 || a.status == 0) {
                f(a)
            }
        }
    };
    if (d !== false) {
        d = true
    }
    if (c) {
        e = e || "";
        a.open("POST", b, d);
        a.setRequestHeader("Content-Length", e.length);
        a.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    } else {
        e = null;
        a.open("GET", b, d)
    }
    a.send(e)
};
$ = Net.Dom.get;
$b = Net.Dom.getBody;
$c = Net.Dom.create;
$dw = function (a) {
    document.write(a)
};
$f = Net.Dom.getFrame;
$n = Net.Dom.getsByName;
$o = Net.Event.observe;
$os = Net.Event.stopObserving;
$t = Net.Dom.getsByTagName;
if (Net.Browser.IE) {
    $o(window, "unload", Net.Event.unloadCache)
}
Net.User = {Option: {WHEEL: 0, FACE: 1, BACK: -1, FONT: 14}, init: function (b) {
    for (var a in b) {
        this.Option[a] = b[a]
    }
}};
Net.BBS = {HOST: ("http://" + (location.protocol == "http:" ? location.host : "bbs.nju.edu.cn")), hasLogin: function () {
    var a = Net.Cookie.get("\x5F\x55\x5F\x55\x49\x44");
    return(a.length > 1)
}, open: function (b) {
    var a = (b == "reg" ? "/bbsreg" : "/main.html");
    window.open(this.HOST + a)
}, frames: function () {
    if (top != self) {
        top.location = self.location
    }
    var b, a = location.href;
    if ((b = a.indexOf(".lilybbs.net")) > 0) {
        var e = a.substring(7, b);
        if (e != "www") {
            location = "http://lilybbs.net/bbsdoc?board=" + e;
            return
        }
    }
    if (a.indexOf("#") > 0) {
        var d, e = a.split("#")[1];
        if (e.indexOf(".blog") > 0) {
            d = "blogdoc?userid=" + e.split(".")[0]
        } else {
            if (e.indexOf(".paint") > 0) {
                d = "pntmy?userid=" + e.split(".")[0]
            } else {
                d = "bbsdoc?board=" + e
            }
        }
        if (d.match(/^[\w-=\?]+$/)) {
            location = this.HOST + "/" + d;
            return
        }
    }
    var c = this.hasLogin() ? "bbsmain" : "cache_bbsmain.htm";
    if (location.href.match(/main\.html\?(\S{4,})/i)) {
        c = unescape(RegExp.$1)
    }
    $dw('<frameset name="fmenu" id="fmenu" border=0 frameborder=0 framespacing=2 framemargin=0 cols="120,10,*">  <frameset rows="*,32">    <frame name=f2 id=f2 framespacing=2 src="' + (this.hasLogin() ? "bbsleft" : "cache_bbsleft.htm") + '">    <frame scrolling=no name=f2tty framespacing=2 src="' + (this.hasLogin() ? "bbstty0" : "cache_bbstty0.htm") + '">  </frameset>  <frame name=f5 id=f5 framespacing=0 src="" scrolling=no>  <frameset name=main rows="0, *, 16">    <frame scrolling=no marginwidth=4 marginheight=0 framespacing=0 name=fmsg src="' + (this.hasLogin() ? "bbsgetmsg" : "") + '">    <frame framespacing=2 name=f3 id=f3 src="' + c + '">    <frame scrolling=no marginwidth=4 marginheight=1 framespacing=1 name=f4 src="bbsfoot">  </frameset></frameset>')
}, framesBless: function () {
    if (top != self) {
        top.location = self.location
    }
    var b = Net.Cookie.get("bless").split("/");
    Net.Cookie.set("bless", "");
    var a = "/file/" + b[2].toUpperCase().charAt(0) + "/" + b[2] + "/" + b[3];
    $dw('<body style="overflow:hidden;background-color: #D0F0C0; text-align:center; FONT-SIZE: 12px; margin:3px" scroll=no oncontextmenu="return false;"><div align=left style="margin-bottom:2px;padding-bottom:5px; border-bottom:#000 1px solid">' + b[1] + ", 您所看到的是来自 " + b[2] + " 的祝福(还能显示" + b[0] + '次). <a href="main.html' + location.search + '">点此进入BBS&gt;</a></div><iframe src="' + a + '" width=100% id="fmain" border=0 frameborder=0 framespacing=2 framemargin=0></iframe><div align=right style="padding-top:3px">@' + (new Date().getFullYear()) + ' <a href="/blogcon?userid=Net&file=1165651620" target=_blank>Net</a></div></body>');
    $("fmain").height = $b().clientHeight - 44
}, getUri: function (b) {
    var a = b.location.pathname.replace(/(\/vd\d+\/)/, "/").substr(1);
    return(a.indexOf("bbsmain") == -1) ? escape(a + b.location.search) : ""
}, checkFrame: function () {
    if (top == self) {
        $dw("<a href='main.html?" + this.getUri(document) + "'>[添加边框]</a> ")
    }
}, showMsg: function () {
    if (!top.fmsg.inmsg) {
        top.fmsg.location = top.fmsg.location
    }
}, img: function (d, c) {
    try {
        if (c == 0) {
            if (d.width > $b().clientWidth - 35) {
                d.resized = true;
                d.width = $b().clientWidth - 35;
                d.title = "出于视觉效果考虑,此图片已缩小;点击图片打开原图";
                d.alt = d.title;
                d.style.cursor = "pointer"
            }
        } else {
            if (c == 1) {
                var a = parseInt(d.style.zoom, 10) || 100;
                a += event.wheelDelta / 12;
                if (a > 0) {
                    d.style.zoom = a + "%"
                }
            } else {
                if (c == 2) {
                    if (!d.resized) {
                        return true
                    } else {
                        window.open(d.src)
                    }
                }
            }
        }
    } catch (b) {
    }
}, size: function (b, a) {
    $(b).width *= (a == 1 ? 1.2 : 0.8);
    $(b).height *= (a == 1 ? 1.2 : 0.8)
}, clearCookie: function () {
    Net.Cookie.set("\x5F\x55\x5F\x4E\x55\x4D", "");
    Net.Cookie.set("\x5F\x55\x5F\x55\x49\x44", "");
    Net.Cookie.set("\x5F\x55\x5F\x4B\x45\x59", "");
    Net.Cookie.set("nexturl", "");
    Net.Cookie.set("FOOTKEY", "")
}, setCookie: function (a) {
    Net.Cookie.set("\x5F\x55\x5F\x4E\x55\x4D", parseInt(a, 10) + 2);
    Net.Cookie.set("\x5F\x55\x5F\x55\x49\x44", a.substring(((parseInt(a, 10) + 2).toString(10)).length + 1, a.indexOf("+")));
    Net.Cookie.set("\x5F\x55\x5F\x4B\x45\x59", parseInt(a.substring(a.indexOf("+") + 1), 10) - 2)
}};
Net.Left = {closebut: function (d, a) {
    var c;
    for (var b = 0; b < 10; b++) {
        c = $("img" + b);
        if (c) {
            c.src = "/images/folder.gif"
        }
        c = $("div" + b);
        if (c) {
            c.style.display = "none"
        }
    }
    d.style.display = "block";
    a.src = "/images/folder2.gif"
}, t: function (b) {
    var c = $("div" + b);
    var a = $("img" + b);
    if (c.style.display != "none") {
        c.style.display = "none";
        a.src = "/images/folder.gif"
    } else {
        this.closebut(c, a)
    }
}};
Net.Blog = {init: function (a) {
    this.ID = a
}, ID: "", showComm: function (d, c) {
    var e = $("NET_" + c);
    var a = $("NET-" + c).innerHTML.split("\n");
    var b = 1;
    for (var c = 1; c < a.length; c++) {
        if (a[c].match(/^\[Head\]([A-Za-z0-9]{2,12}) 于 ([A-Za-z]{3} [ 0-9]{1,2} [:0-9]{8} [0-9]{4}) 提到:/g)) {
            a[c] = "<a href='bbsqry?userid=" + RegExp.$1 + "'>" + RegExp.$1 + "</a> 于 <font color=green>" + RegExp.$2 + "</font> 提到: <a href='blogcomment?userid=" + this.ID + "&file=" + d + "&reid=" + RegExp.$1 + "'>回复</a>&nbsp;";
            if (this.ID == Net.Cookie.get("\x5F\x55\x5F\x55\x49\x44")) {
                a[c] += "<a href='blogcocon?action=delco&userid=" + this.ID + "&file=" + d + "&coid=" + b + "' title='删除评论' onclick='return confirm(\"确认删除吗?\")'>删除</a>"
            }
            b++
        } else {
            a[c] = Net.Html.txt2html(a[c])
        }
    }
    e.innerHTML = "<pre style='font-size:" + Net.User.Option.FONT + "px; line-height:1.3'>" + a.join("\n") + "</pre>"
}};
Net.Dialog = {dialogBox: null, backBox: null, close: function () {
    if (this.dialogBox != null) {
        Net.UI.hide(this.dialogBox, this.backBox);
        this.setContent("")
    }
}, show: function (b, a) {
    this.create();
    this.setTitle(b);
    this.setContent(a);
    Net.UI.show(this.dialogBox, this.backBox);
    this.center()
}, showUrl: function (b, a) {
    this.show(b, '<img src="/images/loading.gif"/>');
    Net.Ajax(a, function (c) {
        Net.Dialog.setContent(c.responseText);
        Net.Dialog.center()
    })
}, setContent: function (a) {
    $("dialogBoxContent").innerHTML = a
}, setTitle: function (a) {
    $("dialogBoxTitle").innerHTML = a
}, create: function () {
    if (this.dialogBox != null) {
        return
    }
    this.dialogBox = $c("DIV", document.body, {id: "dialogBox", innerHTML: '<div id="dialogBoxBox"> <div id="dialogBoxHead" onselectstart="return false"><h2 id="dialogBoxTitle"></h2><span onclick=Net.Dialog.close()></span></div> <div id="dialogBoxWrap">  <div id="dialogBoxContent"></div> </div></div>'});
    Net.Drag.init($("dialogBoxHead"), this.dialogBox);
    $o($("dialogBoxHead"), "dblclick", function () {
        Net.Dialog.close()
    });
    $o(window, "resize", function () {
        Net.Dialog.center()
    });
    $o(window, "scroll", function () {
        Net.Dialog.center()
    });
    this.backBox = $c("DIV", document.body, {id: "backBox"})
}, center: function () {
    if (!Net.UI.visible(this.dialogBox)) {
        return
    }
    var a, b, c = Net.UI.getBodyRect();
    a = (c.width - $("dialogBoxContent").offsetWidth) / 2 + c.left;
    b = (c.height - this.dialogBox.offsetHeight) / 2 + c.top;
    $s(this.dialogBox.style, {left: a, top: b});
    $s(this.backBox.style, {left: c.left, top: c.top, width: c.width, height: c.height})
}};
Net.Drag = {obj: null, init: function (g, h, f) {
    if (f == null) {
        g.onmousedown = Net.Drag.start
    }
    g.root = h;
    if (isNaN(parseInt(g.root.style.left))) {
        g.root.style.left = "0px"
    }
    if (isNaN(parseInt(g.root.style.top))) {
        g.root.style.top = "0px"
    }
    g.root.onDragStart = new Function();
    g.root.onDragEnd = new Function();
    g.root.onDrag = new Function();
    if (f != null) {
        var e = Net.Drag.obj = g;
        f = Net.Drag.fixE(f);
        var j = parseInt(e.root.style.top);
        var i = parseInt(e.root.style.left);
        e.root.onDragStart(i, j, f.clientX, f.clientY);
        e.lastMouseX = f.clientX;
        e.lastMouseY = f.clientY;
        document.onmousemove = Net.Drag.drag;
        document.onmouseup = Net.Drag.end
    }
}, start: function (f) {
    var e = Net.Drag.obj = this;
    f = Net.Drag.fixE(f);
    var h = parseInt(e.root.style.top);
    var g = parseInt(e.root.style.left);
    e.root.onDragStart(g, h, f.clientX, f.clientY);
    e.lastMouseX = f.clientX;
    e.lastMouseY = f.clientY;
    document.onmousemove = Net.Drag.drag;
    document.onmouseup = Net.Drag.end;
    return false
}, drag: function (j) {
    j = Net.Drag.fixE(j);
    var i = Net.Drag.obj;
    var p = j.clientY;
    var o = j.clientX;
    var n = parseInt(i.root.style.top);
    var m = parseInt(i.root.style.left);
    var k, l;
    k = m + o - i.lastMouseX;
    l = n + p - i.lastMouseY;
    i.root.style.left = k + "px";
    i.root.style.top = l + "px";
    i.lastMouseX = o;
    i.lastMouseY = p;
    i.root.onDrag(k, l, j.clientX, j.clientY);
    return false
}, end: function () {
    document.onmousemove = null;
    document.onmouseup = null;
    Net.Drag.obj.root.onDragEnd(parseInt(Net.Drag.obj.root.style.left), parseInt(Net.Drag.obj.root.style.top));
    Net.Drag.obj = null
}, fixE: function (b) {
    if (typeof b == "undefined") {
        b = window.event
    }
    if (typeof b.layerX == "undefined") {
        b.layerX = b.offsetX
    }
    if (typeof b.layerY == "undefined") {
        b.layerY = b.offsetY
    }
    return b
}};
Net.Form = {check: function (a, c) {
    if (c == "login") {
        if (!a.id.value.match(/[A-Za-z0-9]{2,12}/)) {
            alert("请输入正确的id");
            a.id.focus();
            return false
        }
        if (a.pw.value == "") {
            alert("请输入密码");
            a.pw.focus();
            return false
        }
        try {
            a.lasturl.value = Net.BBS.getUri($f("f3"))
        } catch (b) {
        }
        a.action = "/vd" + parseInt(Math.random() * 100000) + "/bbslogin?type=2"
    }
}, postPanel: function (b, a, g, e, f) {
    var j = (b == "td" ? "<tr><td>" : "<br>");
    var c = new Array("/editor/font.htm?ptext=" + a, "bbsupload?ptext=" + a + "&board=" + g, "/editor/face.htm?ptext=" + a, "/editor/ascii.htm?ptext=" + a);
    var h = "文字属性,上载附件,表情图标,ASCII图案生成".split(",");
    var k = j + "辅助面板: [ ";
    for (var d = 0; d < c.length; d++) {
        if (d > 0) {
            k += " - "
        }
        if (d != f) {
            k += "<a target=fontpanel href='" + c[d] + "'>" + h[d] + "</a>"
        }
    }
    k += " ]";
    k += j + "<iframe name=fontpanel frameborder=0 width=100% height=50 src='" + c[e] + "'></iframe>";
    $dw(k)
}, CLICKCNT: 0, clckcntr: function () {
    this.CLICKCNT++;
    if (this.CLICKCNT > 1) {
        if (this.CLICKCNT > 2) {
            return false
        }
        alert("贴子已经发出了......\n\n请等待片刻......\n\n不要重复按发表文章键，谢谢！");
        return false
    }
    return true
}, addText: function (area, v) {
    var t = eval("document.forms[0]." + area);
    t.focus();
    if (document.selection) {
        document.selection.createRange().text = v
    } else {
        if (t.selectionStart || t.selectionStart == "0") {
            var stt = t.selectionStart;
            var end = t.selectionEnd;
            t.value = t.value.substring(0, stt) + v + t.value.substring(end, t.value.length);
            t.selectionStart = t.selectionEnd = stt + v.length
        } else {
            t.value += v
        }
    }
}, MAXC: 78, format: function (a) {
    a = a.replace(/　/g, "  ").replace(/\r\n/g, "\n");
    var e, g, d = a.split("\n");
    for (e = 0; e < d.length; e++) {
        g = d[e];
        if (g.chars() > this.MAXC) {
            if ("bianbian" == Net.Cookie.get("\x5F\x55\x5F\x55\x49\x44")) {
                g = g.replace(/(^|[^\"\'\]])(http|ftp|mms|rstp|news|https)\:\/\/([^\s\033\[\]\"\'\(\)（）。，]+)/gi, function (j, i, m, l) {
                    var k = m + "://" + l;
                    if (k.chars() > Net.Form.MAXC) {
                        Net.Ajax("/go.net?m=create&url=" + Net.Util.urlencode(k), function (n) {
                            k = n.responseText
                        }, false, "", false)
                    } else {
                        k = "\n" + k
                    }
                    return i + k
                })
            }
            if (g.substring(0, 2) == ": ") {
                d[e] = g.substring(0, this.MAXC - 2 - g.chars() + g.length) + ".."
            } else {
                d[e] = "";
                var c = g, f = "Net";
                var b = wordLength = 0;
                for (var h = Math.floor(this.MAXC / 2); h <= g.length; h++) {
                    c = g.substring(b, h);
                    if (c.chars() >= this.MAXC) {
                        f = g.charAt(h);
                        if (f.match(/[a-z]/) && c.match(/([a-zA-Z]+)$/g)) {
                            wordLength = RegExp.$1.length;
                            if (wordLength >= 18) {
                                wordLength = 0
                            }
                        }
                        d[e] += g.substring(b, h - wordLength) + (f == "" ? "" : "\n");
                        b = h - wordLength;
                        wordLength = 0
                    }
                }
                if (f != "") {
                    d[e] += c
                }
            }
        }
    }
    return d.join("\n")
}, preview: function (b) {
    var g = "ifrPreview", e = 650, a = 500;
    var d = '<iframe id={0} width={1} height={2} framemargin=0 frameborder=0 src="about:blank"></iframe>'.format(g, e, a);
    Net.Dialog.show("内容预览", d);
    var c = $t("link", $t("head")[0])[0].href;
    if (!c.startsWith("http")) {
        c = Net.BBS.HOST + c
    }
    d = '<html><head><meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=gb2312">' + '<link rel="stylesheet" type="text/css" href="{0}">'.format(c) + "</head><body>" + Net.Html.toHtml(this.format(b.value)) + "</body></html>";
    $(g).onmouseover = function () {
        return false
    };
    var f = $(g).contentWindow.document;
    f.open();
    f.write(d);
    f.close()
}, serialize: function (g, b) {
    if (!b) {
        b = {}
    }
    var c, a = $t("input", $(g));
    for (c = 0; c < a.length; c++) {
        var e = a[c], d = e.type.toLowerCase();
        if (!e.name || d == "reset") {
            continue
        }
        if (b && b[e.name] != undefined) {
            if ("checkbox,radio".include(d)) {
                if (b[e.name] == e.value) {
                    e.checked = true
                }
            } else {
                e.value = b[e.name]
            }
        } else {
            if ("checkbox,radio".include(d)) {
                if (e.checked) {
                    b[e.name] = e.value
                }
            } else {
                b[e.name] = e.value
            }
        }
    }
    return Object.toJSON(b)
}};
Net.Html = {FACES: {TXT: ["[:T]", "[;P]", "[;-D]", "[:!]", "[:L]", "[:?]", "[:Q]", "[:@]", "[:-|]", "[:(]", "[:)]", "[:D]", "[:P]", "[:'(]", "[:O]", "[:s]", "[:|]", "[:$]", "[:X]", "[:U]", "[:K]", "[:C-]", "[;X]", "[:H]", "[;bye]", "[;cool]", "[:-b]", "[:-8]", "[;PT]", "[;-C]", "[:hx]", "[;K]", "[:E]", "[:-(]", "[;hx]", "[:B]", "[:-v]", "[;xx]"], REG: [/\[\:T\]/g, /\[;P\]/g, /\[;-D\]/g, /\[\:!\]/g, /\[\:L\]/g, /\[\:\?\]/g, /\[\:Q\]/g, /\[\:@\]/g, /\[\:-\|\]/g, /\[\:\(\]/g, /\[\:\)\]/g, /\[\:D\]/g, /\[\:\P\]/g, /\[\:\'\(\]/g, /\[\:O\]/g, /\[\:s\]/g, /\[\:\|\]/g, /\[\:\$\]/g, /\[\:X\]/g, /\[\:U\]/g, /\[\:K\]/g, /\[\:C-\]/g, /\[;X\]/g, /\[\:H\]/g, /\[;bye\]/gi, /\[;cool\]/gi, /\[\:-b\]/g, /\[\:-8\]/g, /\[;PT\]/gi, /\[;-C\]/g, /\[\:hx\]/g, /\[;K\]/g, /\[\:E\]/g, /\[\:-\(\]/g, /\[;hx\]/g, /\[\:B\]/g, /\[\:-v\]/g, /\[;xx\]/gi], PIC: [19, 20, 21, 26, 27, 32, 18, 11, 10, 15, 14, 13, 12, 9, 0, 2, 3, 6, 7, 16, 25, 29, 34, 36, 39, 4, 40, 41, 42, 43, 44, 47, 49, 50, 51, 52, 53, 54], _img: function (a) {
    return"<img src=/images/blank.gif width=1><img src='/images/face/" + this.PIC[a] + ".gif' alt='" + this.TXT[a] + "'><img src=/images/blank.gif width=1>"
}, toHtml: function (b) {
    if (Net.User.Option.FACE && b.match(/\[(\:|;).+?\]/g)) {
        for (var a = 0; a < this.REG.length; a++) {
            b = b.replace(this.REG[a], this._img(a))
        }
    }
    return b
}}, BACKS: {HEX: ["FFFFFF", "FAFBE6", "FFF2E2", "FDE6E0", "F3FFE1", "DAFAFE", "E9EBFE", "EAEAEF"], TIP: ["白色", "杏仁黄", "秋叶褐", "胭脂红", "芥末绿", "天蓝", "雪青", "灰色"], color: function () {
    var a = parseInt(Net.User.Option.BACK, 10);
    if (a == -1) {
        return""
    }
    if (a < 0 || a > 7) {
        a = 0
    }
    return"#" + this.HEX[a]
}, toHtml: function (a) {
    var c = "";
    for (var b = 0; b <= 7; b++) {
        c += "&nbsp;<img class=hand src=/images/color/color" + b + ".gif onClick='" + a + ".value=" + b + "' alt=" + this.TIP[b] + " width=10 height=10>"
    }
    $dw(c)
}}, UBB: 1, CODE: 0, txt2html: function (a) {
    if (!a || a.length < 3) {
        return a
    }
    if (a.substring(0, 2) == ": ") {
        return"<font color=808080>" + a + "</font>"
    }
    if (location.href.indexOf("bbstcon") > 0 && (a == "--\r" || a == "--\n")) {
        this.UBB = 0
    }
    if (a.match(/信人: ([0-9A-Za-z]{2,12}) \(/gi)) {
        a = a.replace("本篇人气:", "<a href=# onclick=Net.Dialog.asciiPlay('',1)>本篇人气:</a>");
        return a.replace(/信人: ([0-9A-Za-z]{2,12}) \(/gi, "信人: <a href='bbsqry?userid=$1'>$1</a> (")
    }
    if (a.indexOf("[!START]") > -1) {
        this.UBB = 1;
        a = a.split("[!START]").join("")
    }
    if (a.indexOf("[!STOP]") > -1) {
        this.UBB = 0;
        a = a.split("[!STOP]").join("")
    }
    if (this.UBB) {
        if (this.CODE) {
            if (a.indexOf("[/code]") > -1) {
                this.CODE = 0;
                return"</pre>"
            }
            return a
        } else {
            if (a.indexOf("[code]") > -1) {
                this.CODE = 1;
                return"<pre class='prettyprint'>"
            }
        }
    }
    if (this.UBB && a.indexOf("://") > 0) {
        a = a.replace(/(^|[^\"\'\]])(http|ftp|mms|rstp|news|https)\:\/\/([^\s\033\[\]\"\'\(\)（）。，]+)/gi, "$1[url]$2://$3[/url]");
        a = a.replace(/\[url\]http\:\/\/(\S+\.)(gif|jpg|png|jpeg|jp)\[\/url\]/gi, "[img]http://$1$2[/img]");
        a = a.replace(/\[url\]http\:\/\/album\.sina\.com\.cn\/pic\/(\w+)\[\/url\]/gi, "[img]http://album.sina.com.cn/pic/$1[/img]");
        a = a.replace(/\[(\w+)\](http\:\/\/)(bbs\.nju\S*\.cn|\S*lilybbs\.net)(\S+)\[\/\1\]/gi, "[$1]" + Net.BBS.HOST + "$4[/$1]")
    }
    if (this.UBB && a.match(/\[(\w+)([^\[\]\s]*)\].*\[\/\1\]/)) {
        var b = "_NET_" + Math.random();
        a = a.replace(/\[url\](.+?)\[\/url\]/gi, "<a href=$1 target=_blank>$1</a>");
        a = a.replace(/\[img\](.+?\.(?:gif|jpg|jpeg|jp|png)|http\:\/\/album\.sina\.com\.cn\/pic\/\w+)\[\/img\]/gi, function (d, c) {
            var e = c;
            if ((e.indexOf(".photo.163.com/") > 0 || e.indexOf(".blog.163.com") > 0) && e.indexOf("?") == -1) {
                e = "http://www.0668.cc/showpic.asp?url=" + e
            }
            return"<img src='" + e + "' alt='" + c + "' border=0 onload='try{Net.BBS.img(this,0)}catch(e){}' onMouseOver='try{Net.BBS.img(this,0)}catch(e){}' onclick='try{Net.BBS.img(this,2)}catch(e){}'" + (Net.User.Option.WHEEL ? " onMouseWheel='try{Net.BBS.img(this,1)}catch(e){}'" : "") + ">"
        });
        if (location.href.indexOf("=Flash") > 0 || location.href.indexOf("/blog") > 0) {
            a = a.replace(/\[flash\](.+?)\[\/flash\]/gi, "<iframe MARGINWIDTH=0 MARGINHEIGHT=0 FRAMEBORDER=0 SCROLLING=NO id=" + b + " height=300 width=400 onload=\"$('" + b + "').contentWindow.document.body.innerHTML='<embed src=$1 type=application/x-shockwave-flash quality=high wmode=transparent width=100% height=100%></embed>';\"></iframe><br> <span class=hand onclick=Net.BBS.size('" + b + "',1) title='大大'>[+]</span><span class=hand onclick=Net.BBS.size('" + b + "',0) title='小小'>[-]</span> FLASH: <a href='$1' target=_blank>$1</a><br>")
        }
        a = a.replace(/\[wmv\](.+?\.wmv)\[\/wmv\]/gi, "<iframe MARGINWIDTH=0 MARGINHEIGHT=0 FRAMEBORDER=0 SCROLLING=NO id=" + b + " height=256 width=314 onload=\"$('" + b + "').contentWindow.document.body.innerHTML='<embed src=$1 height=100% width=100% AutoStart=0 AutoSize=1></embed>';\"></iframe><br> <span class=hand onclick=Net.BBS.size('" + b + "',1) title='大大'>[+]</span><span class=hand onclick=Net.BBS.size('" + b + "',0) title='小小'>[-]</span> WMV: <a href='$1' target=_blank>$1</a><br>");
        a = a.replace(/\[wma\](.+?\.(?:wma|mp3))\[\/wma\]/gi, "<iframe MARGINWIDTH=0 MARGINHEIGHT=0 FRAMEBORDER=0 SCROLLING=NO id=" + b + " height=40 onload=\"$('" + b + "').contentWindow.document.body.innerHTML='<embed src=$1 height=40 width=100% AutoStart=0></embed>';\"></iframe><br> WMA: <a href='$1' target=_blank>$1</a><br>");
        a = a.replace(/\[(?:c|color)=([#0-9a-zA-Z]{1,10})\](.+?)\[\/(?:c|color)\]/gi, "<font color='$1'>$2</font>");
        a = a.replace(/\[b\](.+?)\[\/b\]/gi, "<b>$1</b>");
        a = a.replace(/\[brd\](.+?)\[\/brd\]/gi, "<a href='bbsdoc?board=$1'>$1</a>");
        a = a.replace(/\[uid\]([0-9a-zA-Z]{2,12})\[\/uid\]/gi, "<a href='bbsqry?userid=$1'>$1</a>");
        a = a.replace(/\[blog\]([0-9a-zA-Z]{2,12})\[\/blog\]/gi, "<a href='blogdoc?userid=$1'>$1</a>")
    }
    if (a.indexOf("\033[") > -1) {
        a = a.replace(/\033\[[\d;]*(3\d{1})[\d;]*(4\d{1})[\d;]*m/g, "<font class=c$1><font class=c$2>");
        a = a.replace(/\033\[[\d;]*(4\d{1})[\d;]*(3\d{1})[\d;]*m/g, "<font class=c$1><font class=c$2>");
        a = a.replace(/\033\[[\d;]*(3\d{1}|4\d{1})[\d;]*m/g, "<font class=c$1>");
        a = a.replace(/\033\[0*m/g, "<font class=c37 style='background-color: " + this.BACKS.color() + "'>");
        a = a.replace(/\033\[[\d;]*(I|u|s|H|m|A|B|C|D)/gi, "").replace(/\033/g, "")
    }
    return this.FACES.toHtml(a)
}, toHtml: function (c) {
    this.UBB = 1;
    var a = c.split("\n");
    for (var b = 0; b < a.length; b++) {
        a[b] = this.txt2html(a[b])
    }
    return"<pre style='line-height:1.3; font-size:" + Net.User.Option.FONT + "px; background-color: " + this.BACKS.color() + "'>" + a.join("\n") + "</pre>"
}, make: function (a) {
    $("NET_" + a).innerHTML = this.toHtml($("NET-" + a).innerHTML)
}};
Net.Pnt = {checkJVM: function () {
    if (!window.navigator.javaEnabled()) {
        Net.Dialog.show("Java虚拟机安装", "您的浏览器目前不支持Java虚拟机, <a href=/temp/msjavx86.exe>请先点击这里下载安装</a>");
        return false
    } else {
        return true
    }
}, view: function (d, e, c, a) {
    if (this.checkJVM()) {
        var b = "pntview?board=" + d + "&id=" + e;
        Net.Dialog.showUrl("涂鸦过程回放", b)
    }
}, repaint: function (b, c) {
    var a = "pntpaint?board=" + b + "&id=" + c;
    if (confirm("是否保留以前作画动画?\n\n注意: 如果动画文件已损坏, 只能选择'取消', 否则图片将损坏") == false) {
        a += "&png=1"
    }
    location = a
}, time: function (a) {
    $dw(a < 60 ? a + "秒" : (a < 3600 ? parseInt(a / 60, 10) + "分" + a % 60 + "秒" : parseInt(a / 3600, 10) + "时" + a % 60 + "分"))
}, timestamp: function (a) {
    var b = new Date(a * 1000);
    $dw(b.getFullYear() + "-" + (b.getMonth() + 1) + "-" + b.getDate() + " " + b.getHours() + ":" + b.getMinutes())
}, _page2start: function (b) {
    var a = G.c.Total - b * G.c.Per;
    return(a > 0) ? a : 0
}, gUrl: "", pages: function () {
    var c, g, f;
    if (Net.Pnt.gUrl == "") {
        Net.Pnt.gUrl = Net.Util.toQuery("pntdoc", {board: G.c.Brd, userid: G.c.User, day: G.c.Day, mark: G.c.Mark, order: G.c.Order, start: ""})
    }
    var a = Math.ceil(G.c.Total / G.c.Per);
    var e = Math.ceil((G.c.Total - G.c.Start) / G.c.Per);
    var d = "<table border=0 cellpadding=2><tr>";
    d += "<td><a href='javascript:location.reload()' title='刷新'>刷</a>";
    d += "<td>" + G.c.Total;
    d += "<td><input value=" + e + " size=2 style='border:1px solid' onKeyPress=\"if(event.keyCode==13) location='" + Net.Pnt.gUrl + "' + _page2start(this.value);\">/" + a;
    var b = 1;
    if (e > 2) {
        d += "<td><a href=" + Net.Pnt.gUrl + ">[&lt;&lt;]</a>"
    }
    if (e > 1) {
        d += "<td><a href=" + Net.Pnt.gUrl + Net.Pnt._page2start(e - 1) + ">[&lt;]</a>"
    }
    g = e > 3 ? e - 2 : 1;
    for (c = g; c > 0 && c < e; c++) {
        d += "<td><a href=" + Net.Pnt.gUrl + Net.Pnt._page2start(c) + ">[" + c + "]</a>";
        b++
    }
    d += "<td><b>" + e + "</b>";
    for (c = e + 1; c <= a && b < 5; c++) {
        d += "<td><a href=" + Net.Pnt.gUrl + Net.Pnt._page2start(c) + ">[" + c + "]</a>";
        b++
    }
    if (e < a) {
        d += "<td><a href=" + Net.Pnt.gUrl + Net.Pnt._page2start(e + 1) + ">[&gt;]</a>"
    }
    if (e < a - 2) {
        d += "<td><a href=" + Net.Pnt.gUrl + "0>[&gt;&gt;]</a>"
    }
    d += "</tr></table>";
    $dw(d)
}, showSearch: function () {
    var a = "<form action=pntdoc style='margin:0'>";
    a += "ID:<input name=userid value='" + G.c.User + "' size=5>";
    a += "最近<input name=day value='" + G.c.Day + "' size=1>天";
    a += "<input name=mark value=1 type=checkbox " + (G.c.Mark > 0 ? "checked" : "") + ">精华";
    a += "<input name=board type=hidden value=" + G.c.Brd + ">";
    a += "<select name=order><option value=''>发表<option value='1' " + (G.c.Order > 0 ? "selected" : "") + ">评论</select>序";
    a += "<input type=submit value=GO>";
    a += "</form>";
    $dw(a)
}, showForm: function (b) {
    var a = "<form action=pntpaint method=post onsubmit='return Net.Pnt.checkJVM()' style='margin:0'><select name='tool'><option value='oekakibbs'>oekakiBBS旧板<option value='oekakibbs2' selected>oekakiBBS新板<option value='Shi-Painter'>ShiPainterPRO</select><input type=hidden name=board value=" + (b ? b : G.c.Brd) + "><select name='width'><option value=500>500</option><option value=400>400</option><option value=300 Selected>300</option><option value=200>200</option><option value=100>100</option></select>X<select name='height'><option value=500>500</option><option value=400>400</option><option value=300 Selected>300</option><option value=200>200</option><option value=100>100</option></select><input type=submit value='涂'></form>";
    $dw(a)
}, htmlComm: function (b, e, c) {
    var d = $("pntcomm" + e);
    var a = "/paint/{0}/{1}_{2}.txt?{3}".format(G.c.Brd, b, e, c);
    Net.Ajax(a, function (h) {
        var f = h.responseText.split("[Head");
        var g = 1;
        for (var j = 1; j < f.length; j++) {
            if (f[j].match(/^\]([A-Za-z0-9]{2,12}) 于 ([A-Za-z]{3} [ 0-9]{1,2} [:0-9]{8} [0-9]{4}) 提到:/g)) {
                var k = f[j].substring(f[j].indexOf("提到:") + "提到:".length, f[j].length);
                f[j] = "<hr size=1 color=gray><a href='bbsqry?userid={0}'>{0}</a> 于 <font color=green>{1}</font>".format(RegExp.$1, RegExp.$2) + " 说<a href='pntcomm?board={0}&id={1}&do=del&coid={2}' title='删除评论' onclick='return confirm(\"确认删除吗?\")'>:</a><br>".format(G.c.Brd, e, g) + Net.Html.txt2html(k);
                g++
            }
        }
        d.innerHTML = f.join("") + "<hr size=1 color=gray>共 {0} 条评论. <a href='javascript:Net.Pnt.addComm({1})'>发表评论</a>".format(g - 1, e)
    })
}, htmlImg: function (b, c) {
    var a, d;
    if (c == "my") {
        a = b.split("/")[2];
        d = b.substring(b.indexOf("_") + 1, b.indexOf("."))
    }
    $dw('<div style="width:10px; display:table"><div style="border:2px solid #e1e1e1"><div style="border:1px solid #b2b2b2; padding:4px; background:#fff">' + ' <a href={0} title="{1}"><img {2} border=0 src="{3}"></a>'.format(c == "doc" ? '"javascript:;" onclick=Net.Util.copyToClip("' + Net.BBS.HOST + b + '")' : "pntdoc?board=" + a + "&id=" + d, c == "doc" ? "点击复制图片地址" : "查看原图", c == "doc" ? "" : "width=110", b) + "</div></div></div>")
}, addComm: function (d) {
    if (!Net.BBS.hasLogin()) {
        alert("请先登录再发表评论!");
        return
    }
    var b = $("pntcommfrm" + d);
    if (b) {
        b.text.focus();
        return
    }
    var a = Net.Util.toQuery("pntcomm", {board: G.c.Brd, id: d, "do": "add"});
    var c = $("pntcomm" + d);
    c.innerHTML = c.innerHTML + "<br><br><br><center><form action='" + a + "' method=post id=pntcommfrm" + d + "><textarea name=text cols=35 rows=3 onkeypress=\"if(event.keyCode==10 || (event.ctrlKey && event.keyCode==13)) document.getElementById('pntcommfrm" + d + "').submit();\"></textarea><br><input type=submit value='发表评论(最多200字符)'></form>";
    $("pntcommfrm" + d).text.focus()
}};
var _uid, _uexp;
function Tbbsmain(d, g) {
    var e, c, a;
    if (d == "logo") {
        e = '<textarea id=".p.channel__logo" style="display:none"><table width="100%"  border="0" cellpadding="0" cellspacing="1" class="TabBest"><tr class="TabBody1"><td align="center" class="TabBody2"><img src="/images/bbs.gif" width="120" height="60" align="absmiddle"></td><td width="468" height="60" align="right">';
        e += '<embed src="/file/LilyLinks/topbanner.swf?id=' + _uid + "&exp=" + _uexp + '" quality=high width=468 height=60></embed>';
        e += "</td></tr></table></textarea>"
    } else {
        if (d == "init") {
            _uid = g.id;
            _uexp = g.exp
        } else {
            if (d == "good") {
                e = '<textarea id=".p.channel__good" style="display:none"><table width="100%" border="0" cellpadding="0" cellspacing="1" class="TabBest"><tr><td width="6%" align="center" class="BestTop"><img src="/images/digest.gif" width="22" height="21"></td><td class="BestTop">　精 彩 推 荐 文 章</td><td width="6%" class="BestTop"><a href=/cache/good.xml>RSS</a></td></tr><tr><td colspan="3" class="TabBody2"> <table width="100%" cellpadding="0" cellspacing="0">';
                for (a = g.hot, c = 0; c < a.length; c++) {
                    if (c % 2 == 0) {
                        e += "<tr>"
                    }
                    e += '<td><a href="' + a[c].link + '" target="' + a[c].target + '"><span style="color:' + a[c].color + '">' + a[c].title + "</span></a></td>"
                }
                e += ' </table></td></tr><tr><td colspan="3" class="TabBody1"> <table width="100%" cellspacing="0" cellpadding="0">';
                for (a = g.good, c = 0; c < a.length; c++) {
                    if (c % 2 == 0) {
                        e += "<tr>"
                    }
                    e += ' 	<td width="50%"><img src="/images/arrow.gif" width="8" height="13"><a  	href="bbstcon?board=' + a[c].brd + "&file=" + a[c].file + '" class="home">' + a[c].title + '</a>[ <a  	href="board?board=' + a[c].brd + '" class="home">' + a[c].brd + "</a>]</td>"
                }
                e += ' </table></td></tr><tr align="right"><td colspan="3" class="TabBody2"><a href="board?board=Bless" class="home">→<span class="FontStyle2">百合祝福</span> </a><a href="board?board=Ourselves" class="home">→<span class="FontStyle2">百合原创</span> </a><a href="board?board=LilyDigest" class="home">→<span class="FontStyle2">百合精华</span> </a><a	href="bbsrec2?top=3" class="home">→更多推荐文章(共' + g.goodnum + "篇)← </a> </td></tr></table></textarea>"
            } else {
                if (d == "act") {
                    e = '<textarea id=".p.channel__act" style="display:none"><table width="100%" cellpadding="0" cellspacing="1" class="TabBest"><tr><td colspan="2" class="TabHead3"><img src="/images/boxnews_ico.gif" width="16" height="13" align=absmiddle>各 类 活 动 与 讲 座 预 告</td></tr>';
                    for (a = g.act, c = 0; c < a.length; c++) {
                        e += '<tr><td class="TabBody' + (c % 2 == 0 ? "1" : "2") + '"><img src="/images/qq_dot2.gif" width="13" height="16"><a href="bbstcon?board=' + a[c].brd + "&file=" + a[c].file + '" class="home" title="版面: ' + a[c].brd + '">' + a[c].title + "</a></td></tr>"
                    }
                    e += "</table></textarea>"
                } else {
                    if (d == "favbrd") {
                        e = '<textarea id=".p.channel__favBrd" style="display:none"><table width="100%" cellpadding="0" cellspacing="1" class="TabBest"><tr><td class="TabHead1"><img src="/images/boxnews_ico.gif" width="16" height="13" align="absmiddle">预 定 讨 论 区</td></tr>';
                        for (a = g.fav, c = 0; c < a.length; c++) {
                            e += '<tr><td class="TabBody' + (c % 2 == 0 ? "1" : "2") + '"><img src="/images/qq_dot2.gif" width="13" height="16"><a href="board?board=' + a[c].brd + '" class="home">' + a[c].brd + " (" + a[c].title + ") </a></td></tr>"
                        }
                        e += "</table></textarea>"
                    } else {
                        if (d == "forum") {
                            e = '<textarea id=".p.channel__forum" style="display:none"><table width="100%"  border="0" cellpadding="0" cellspacing="1" class="TabBest"><tr><td width="6%" align="center" class="TabHead1"><img src="/images/digest.gif" width="22" height="21"></td><td class="TabHead1">　分 类 精 彩 讨 论 区</td></tr>';
                            for (a = g.fm, c = 0; c < a.length; c++) {
                                e += '<tr><td colspan="2"><table width="100%"  border="0" cellpadding="0" cellspacing="1" class="TabBody1"><tr><td colspan="5"><a href="bbsboa?sec=' + a[c].d + '" class="home"><img src="/images/fb' + (a[c].d + 1) + '.gif" width="159" height="20" border="0" /></a></td><td width="17%"> <a href="bbsboa?sec=' + a[c].d + '" class="home">更多版面... </a> </td></tr><tr class="TabBody2">';
                                for (var f = a[c].s, b = 0; b < f.length; b += 2) {
                                    e += '<td width="16%"> <a href="board?board=' + f[b] + '" class="home">' + f[b + 1] + "</a> </td>"
                                }
                                e += '</tr><tr><td colspan="6" align="center"><img src="/images/line2.gif" width="493" height="11"> </td></tr></table></td></tr>'
                            }
                            e += "</table></textarea>"
                        } else {
                            if (d == "recbrd") {
                                e = '<textarea id=".p.channel__recBrd" style="display:none"><table width="100%" cellpadding="0" cellspacing="1" class="TabBest"><tr><td class="TabHead1"><img src="/images/boxnews_ico.gif" width="16" height="13" align="absmiddle">今 日 推 荐 讨 论 区';
                                for (a = g.rec, c = 0; c < a.length; c++) {
                                    e += '<tr><td class="TabBody' + (c % 2 == 0 ? "1" : "2") + '"><img src="/images/qq_dot2.gif" width="13" height="16"><a href="board?board=' + a[c].brd + '" class="home" title="' + a[c].brd + "版, 版主: " + a[c].bm + '">' + a[c].brd + " (" + a[c].title + ") </a></td></tr>"
                                }
                                e += "</table></textarea>"
                            } else {
                                if (d == "top10") {
                                    e = '<textarea id=".p.channel__top10" style="display:none"><table width="100%" cellpadding="0" cellspacing="1" class="TabBest"><tr><tr><td class="TabHead2"><img src="/images/boxnews_ico.gif" width="16" height="13" align="absmiddle">今 日 十 大 热 门 话 题</td></tr>';
                                    for (a = g.tp, c = 0; c < a.length; c++) {
                                        e += "<tr><td class=TabBody" + (c % 2 == 0 ? "1" : "2") + '><img src=/images/qq_dot2.gif width=13 height=16><a href="bbstcon?board=' + a[c].b + "&file=M." + a[c].f + '.A" class="home">' + a[c].t + "</a></td></tr>"
                                    }
                                    e += "</table></textarea>"
                                } else {
                                    if (d == "hotbrd") {
                                        e = '<textarea id=".p.channel__hotBrd" style="display:none"><table width="100%" cellpadding="0" cellspacing="1" class="TabBest"><tr><td colspan="2" class="TabHead3"><img src="/images/boxnews_ico.gif" width="16" height="13" align="absmiddle">今 日 热 门 讨 论 区</td></tr>';
                                        for (a = g.hb, c = 0; c < a.length; c++) {
                                            e += '<tr><td width="85%" class="TabBody' + (c % 2 == 0 ? "1" : "2") + '"><img src="/images/qq_dot2.gif" width="13" height="16"><a href="board?board=' + a[c].brd + '" class="home" title="' + a[c].brd + "版, 版主: " + a[c].bm + '">' + a[c].brd + " (" + a[c].n + ') </a></td><td width="15%" class="TabBody' + (c % 2 == 0 ? "1" : "2") + '"><span class=' + (a[c].on >= 99 ? "FontStyle2" : "") + "> " + a[c].on + "人</span></td></tr>"
                                        }
                                        e += "</table></textarea>"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    $dw(e)
}
Net.Tpl = {};
Net.Tpl.pntdoc = function (c) {
    var b, a = '<table width="99%" border="0" cellpadding="4" cellspacing="1" class="TabBest"><tr class="TabBody2"><td><script>Net.Pnt.pages()<\/script><td align=center><script>Net.Pnt.showSearch()<\/script><td align=right><script>Net.Pnt.showForm()<\/script></td></tr></table>';
    b = a + ('<table width="99%"  border="0" cellpadding="0" cellspacing="1" class="TabBest"><tr><td width="6%" align="center" class="TabHead1"><img src="/images/digest.gif" width="22" height="21"></td><td class="TabHead1">　涂 鸦 展 台: ${c.Brd}</td>' + '<td class="TabHead1" align="right">域名: {0}/p/${c.Brd} </td></tr></table>'.format(Net.BBS.HOST) + '{for p in a}<table width="99%" border=0 align=center cellpadding=0 cellspacing=1><tr><td valign=top><table width="100%" height="100%" border=0 cellspacing=0 cellpadding=5 class=TabBody${p.i % 2 + 1}><tr><td height=14> [No.${p.i}] [作者:<a href=bbsqry?userid=${p.userid}>${p.userid}</a>] [工具:${p.tool}] [耗时:<script>Net.Pnt.time(${p.used})<\/script>] [精华:{if p.mark}是{else}否{/if}] <script>Net.Pnt.timestamp(${p.save})<\/script></td></tr><tr><td align=center height="100%"><script>Net.Pnt.htmlImg("/paint/${c.Brd}/${p.tool}_${p.save}.png?${p.used}", "doc")<\/script></td></tr><tr><td height=14> [<a href=javascript:Net.Pnt.view("${c.Brd}",${p.save},${p.w},${p.h}) title="已观看${p.click}次">观看过程</a>] [<a href="pntdoc?board=${c.Brd}&userid=${p.userid}">作者作品</a>] [<a href="pntmy?userid=${p.userid}">个人画集</a>] | [<a href=javascript:Net.Pnt.repaint("${c.Brd}",${p.save})>继续作画</a>] [<a href="pntman?board=${c.Brd}&id=${p.save}&do=del" onclick="return confirm(\'确定删除?\')">删除</a>] [<a href="pntman?board=${c.Brd}&id=${p.save}&do=check" onclick="return confirm(\'确定举报(仅管理员有权限)?\')">举报</a>] [<a href="pntman?board=${c.Brd}&id=${p.save}&do=mark" onclick="return confirm(\'确定吗?\')">{if p.mark}去{else}加{/if}精华</a>] | [<a href="javascript:Net.Pnt.addComm(${p.save})">发表评论</a>]</td></tr></table></td><td valign=top width=250> <table width="100%" height="100%" border=0 cellspacing=0 cellpadding=5 class=TabBody${p.i % 2 + 1}><tr><td height=14> 标题: ${p.title} </td></tr> <tr><td valign=top height="100%"><div id="pntcomm${p.save}">Loading...</div></td></tr> </table><script>Net.Pnt.htmlComm("${p.tool}",${p.save},${p.co})<\/script></td></tr></table><br>{/for}').process(c) + a + '<table width="99%" border="0" cellpadding="4" cellspacing="1" class="TabBest"><tr><td colspan="2" class="TabBody2" align=center>[<a href="pnt2blog?board=beginner" onclick="return confirm(\'是否确定此操作?\')">导出我的涂鸦到blog</a>]</td></tr></table>';
    $dw(b)
};
Net.UI = {show: function () {
    for (var a = 0; a < arguments.length; a++) {
        arguments[a].style.display = "block"
    }
}, hide: function () {
    for (var a = 0; a < arguments.length; a++) {
        arguments[a].style.display = "none"
    }
}, visible: function (a) {
    return a.style.display != "none"
}, getOffset: function (c) {
    var b = 0, a = 0;
    while (c && c.offsetParent) {
        b += c.offsetTop || 0;
        a += c.offsetLeft || 0;
        c = c.offsetParent
    }
    return(new Net.Point(a, b))
}, getScrollOffset: function (c) {
    var b = this.getOffset(c);
    var a = this.getBodyRect();
    b.x -= a.x;
    b.y -= a.y;
    return(b)
}, getRect: function (b) {
    b = $(b);
    var a = this.getOffset(b);
    return(new Net.Rect(a.x, a.y, b.offsetWidth, b.offsetHeight))
}, getScrollRect: function (b) {
    b = $(b);
    var a = this.getScrollOffset(b);
    return(new Net.Rect(a.x, a.y, b.offsetWidth, b.offsetHeight))
}, getBodyRect: function () {
    if (window.pageXOffset) {
        return(new Net.Rect(pageXOffset, pageYOffset, innerWidth, innerHeight))
    } else {
        var a = Net.Dom.getBody();
        return(new Net.Rect(a.scrollLeft, a.scrollTop, a.clientWidth, a.clientHeight))
    }
}, pointIn: function (c, b) {
    var a = this.getRect($(b));
    return this.pointInRect(c, a)
}, pointInRect: function (b, a) {
    return(b.x >= a.x && b.y >= a.y && b.x < a.x + a.w && b.y < a.y + a.h)
}};
Net.CD = function (b, a, d, c) {
    this.pid = b;
    this.oldId = ".p.channel_" + b;
    this.newId = ".p.ncd_" + b;
    this.oldObj;
    this.newObj = $c("DIV", null, {id: this.newId});
    this.setXYZ(a, d, c)
};
Net.CD.prototype = {appendIn: function (a) {
    var b = $c("SPAN", this.newObj);
    b.appendChild(document.createTextNode("Loading..."));
    a.appendChild(this.newObj)
}, getDiv: function () {
    return this.newObj
}, getTd: function () {
    return this.newObj.parentNode
}, getHtml: function () {
    this.oldObj = $(this.oldId);
    try {
        return this.oldObj.value
    } catch (a) {
        return"内容缺失."
    }
}, setHtml: function (a) {
    this.newObj.innerHTML = a
}, getPosStr: function () {
    return this.pid + "," + this.X + "," + this.Y + "," + this.Z
}, getX: function () {
    return this.X
}, getY: function () {
    return this.Y
}, getZ: function () {
    return this.Z
}, setX: function (a) {
    this.X = parseInt(a)
}, setY: function (a) {
    this.Y = parseInt(a)
}, setZ: function (a) {
    this.Z = parseInt(a)
}, setXYZ: function (a, c, b) {
    this.setX(a);
    this.setY(c);
    this.setZ(b)
}};
Net.CC = {};
Net.CC.init = function (a, c, b) {
    this.widthStr = a || "100%";
    this.oldPosStr = c || "";
    this.newPosStr = c || "";
    this.isMoveMode = b || false;
    this.colCount = 0;
    this.maxY = [];
    this.maxZ = [];
    this.allCDs = [];
    this.allxEl = [];
    $dw('<table id=".p.tb"><tbody/></table>');
    this.mainTable = $(".p.tb");
    $s(this.mainTable, {width: "100%", border: 0, cellPadding: 0, cellSpacing: (this.isMoveMode ? 4 : 0)});
    this._init()
};
Net.CC._init = function () {
    var c = this.widthStr.split(",");
    this.colCount = c.length;
    var d = $c("TR", this.mainTable.firstChild);
    for (var e = 0; e < this.colCount; e++) {
        this.allxEl[e] = $c("TD", d, {id: ".p.x_" + e, width: c[e], vAlign: "top", height: "100%"});
        if (this.isMoveMode) {
            $s(this.allxEl[e].style, {border: "1px solid #9d9d9d"});
            $c("SPAN", this.allxEl[e], {innerHTML: "&nbsp;"})
        }
    }
    if (this.newPosStr == "" || this.newPosStr == "null") {
        return
    }
    var h = [], f = [];
    var g = this.newPosStr.split(";");
    g.each(function (p) {
        try {
            var i = p.split(",");
            h.push(parseInt(i[2]));
            f.push(parseInt(i[3]));
            Net.CC.appendCD(new Net.CD(i[0], i[1], i[2], i[3]))
        } catch (q) {
        }
    });
    if (this.allCDs.length == 0) {
        return
    }
    var m, l, k, a = h.max(), o = f.max();
    for (m = 0; m < this.colCount; m++) {
        this.maxY[m] = -1;
        this.maxZ[m] = [];
        for (l = 0; l <= a; l++) {
            if (this.getPidByXYZ(m, l, 0)) {
                this.maxY[m] = l
            } else {
                break
            }
            var n = $c("TABLE", null, {width: "100%", border: 0, cellSpacing: 1, cellPadding: 1});
            var j = $c("TR", $c("TBODY", n));
            for (k = 0; k <= o; k++) {
                var b = $c("TD", j, {vAlign: "top", align: "center"});
                this.getCDByXYZ(m, l, k).appendIn(b);
                if (!this.getPidByXYZ(m, l, k + 1)) {
                    this.maxZ[m][l] = k;
                    break
                }
            }
            this.allxEl[m].appendChild(n)
        }
    }
};
Net.CC.print = function () {
    this.allCDs.each(function (a) {
        a.setHtml(a.getHtml())
    })
};
Net.CC.getCD = function (a) {
    return(a < this.allCDs.length ? this.allCDs[a] : null)
};
Net.CC.getCDByXYZ = function (a, c, b) {
    return this.getCDById(this.getPidByXYZ(a, c, b))
};
Net.CC.getPidByXYZ = function (a, f, e) {
    var c = "," + a + "," + f + "," + e;
    var d = this.newPosStr.indexOf(c);
    if (d == -1) {
        return null
    }
    var b = this.newPosStr.substring(0, d);
    d = b.lastIndexOf(";") + 1;
    return b.substr(d)
};
Net.CC.getCDById = function (a) {
    for (var b = 0; a && b < this.allCDs.length; b++) {
        if (this.allCDs[b].pid == a || this.allCDs[b].newId == a) {
            return this.allCDs[b]
        }
    }
    return null
};
Net.CC.appendCD = function (a) {
    this.allCDs.push(a)
};
Net.CC.setCDHtml = function (a, b) {
    this.getCDById(a).setHtml(b)
};
var TrimPath;
(function () {
    if (TrimPath == null) {
        TrimPath = new Object()
    }
    if (TrimPath.evalEx == null) {
        TrimPath.evalEx = function (src) {
            return eval(src)
        }
    }
    var UNDEFINED;
    if (Array.prototype.pop == null) {
        Array.prototype.pop = function () {
            if (this.length === 0) {
                return UNDEFINED
            }
            return this[--this.length]
        }
    }
    if (Array.prototype.push == null) {
        Array.prototype.push = function () {
            for (var i = 0; i < arguments.length; ++i) {
                this[this.length] = arguments[i]
            }
            return this.length
        }
    }
    TrimPath.parseTemplate = function (tmplContent, optTmplName, optEtc) {
        if (optEtc == null) {
            optEtc = TrimPath.parseTemplate_etc
        }
        var funcSrc = parse(tmplContent, optTmplName, optEtc);
        var func = TrimPath.evalEx(funcSrc, optTmplName, 1);
        if (func != null) {
            return new optEtc.Template(optTmplName, tmplContent, funcSrc, func, optEtc)
        }
        return null
    };
    try {
        String.prototype.process = function (context, optFlags) {
            var template = TrimPath.parseTemplate(this, null);
            if (template != null) {
                return template.process(context, optFlags)
            }
            return this
        }
    } catch (e) {
    }
    TrimPath.parseTemplate_etc = {};
    TrimPath.parseTemplate_etc.statementTag = "forelse|for|if|elseif|else|var|macro";
    TrimPath.parseTemplate_etc.statementDef = {"if": {delta: 1, prefix: "if (", suffix: ") {", paramMin: 1}, "else": {delta: 0, prefix: "} else {"}, elseif: {delta: 0, prefix: "} else if (", suffix: ") {", paramDefault: "true"}, "/if": {delta: -1, prefix: "}"}, "for": {delta: 1, paramMin: 3, prefixFunc: function (stmtParts, state, tmplName, etc) {
        if (stmtParts[2] != "in") {
            throw new etc.ParseError(tmplName, state.line, "bad for loop statement: " + stmtParts.join(" "))
        }
        var iterVar = stmtParts[1];
        var listVar = "__LIST__" + iterVar;
        return["var ", listVar, " = ", stmtParts[3], ";", "var __LENGTH_STACK__;", "if (typeof(__LENGTH_STACK__) == 'undefined' || !__LENGTH_STACK__.length) __LENGTH_STACK__ = new Array();", "__LENGTH_STACK__[__LENGTH_STACK__.length] = 0;", "if ((", listVar, ") != null) { ", "var ", iterVar, "_ct = 0;", "for (var ", iterVar, "_index in ", listVar, ") { ", iterVar, "_ct++;", "if (typeof(", listVar, "[", iterVar, "_index]) == 'function') {continue;}", "__LENGTH_STACK__[__LENGTH_STACK__.length - 1]++;", "var ", iterVar, " = ", listVar, "[", iterVar, "_index];"].join("")
    }}, forelse: {delta: 0, prefix: "} } if (__LENGTH_STACK__[__LENGTH_STACK__.length - 1] == 0) { if (", suffix: ") {", paramDefault: "true"}, "/for": {delta: -1, prefix: "} }; delete __LENGTH_STACK__[__LENGTH_STACK__.length - 1];"}, "var": {delta: 0, prefix: "var ", suffix: ";"}, macro: {delta: 1, prefixFunc: function (stmtParts, state, tmplName, etc) {
        var macroName = stmtParts[1].split("(")[0];
        return["var ", macroName, " = function", stmtParts.slice(1).join(" ").substring(macroName.length), "{ var _OUT_arr = []; var _OUT = { write: function(m) { if (m) _OUT_arr.push(m); } }; "].join("")
    }}, "/macro": {delta: -1, prefix: " return _OUT_arr.join(''); };"}};
    TrimPath.parseTemplate_etc.modifierDef = {eat: function (v) {
        return""
    }, escape: function (s) {
        return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    }, capitalize: function (s) {
        return String(s).toUpperCase()
    }, "default": function (s, d) {
        return s != null ? s : d
    }};
    TrimPath.parseTemplate_etc.modifierDef.h = TrimPath.parseTemplate_etc.modifierDef.escape;
    TrimPath.parseTemplate_etc.Template = function (tmplName, tmplContent, funcSrc, func, etc) {
        this.process = function (context, flags) {
            if (context == null) {
                context = {}
            }
            if (context._MODIFIERS == null) {
                context._MODIFIERS = {}
            }
            if (context.defined == null) {
                context.defined = function (str) {
                    return(context[str] != undefined)
                }
            }
            for (var k in etc.modifierDef) {
                if (context._MODIFIERS[k] == null) {
                    context._MODIFIERS[k] = etc.modifierDef[k]
                }
            }
            if (flags == null) {
                flags = {}
            }
            var resultArr = [];
            var resultOut = {write: function (m) {
                resultArr.push(m)
            }};
            try {
                func(resultOut, context, flags)
            } catch (e) {
                if (flags.throwExceptions == true) {
                    throw e
                }
                var result = new String(resultArr.join("") + "[ERROR: " + e.toString() + (e.message ? "; " + e.message : "") + "]");
                result.exception = e;
                return result
            }
            return resultArr.join("")
        };
        this.name = tmplName;
        this.source = tmplContent;
        this.sourceFunc = funcSrc;
        this.toString = function () {
            return"TrimPath.Template [" + tmplName + "]"
        }
    };
    TrimPath.parseTemplate_etc.ParseError = function (name, line, message) {
        this.name = name;
        this.line = line;
        this.message = message
    };
    TrimPath.parseTemplate_etc.ParseError.prototype.toString = function () {
        return("TrimPath template ParseError in " + this.name + ": line " + this.line + ", " + this.message)
    };
    var parse = function (body, tmplName, etc) {
        body = cleanWhiteSpace(body);
        var funcText = ["var TrimPath_Template_TEMP = function(_OUT, _CONTEXT, _FLAGS) { with (_CONTEXT) {"];
        var state = {stack: [], line: 1};
        var endStmtPrev = -1;
        while (endStmtPrev + 1 < body.length) {
            var begStmt = endStmtPrev;
            begStmt = body.indexOf("{", begStmt + 1);
            while (begStmt >= 0) {
                var endStmt = body.indexOf("}", begStmt + 1);
                var stmt = body.substring(begStmt, endStmt);
                var blockrx = stmt.match(/^\{(cdata|minify|eval)/);
                if (blockrx) {
                    var blockType = blockrx[1];
                    var blockMarkerBeg = begStmt + blockType.length + 1;
                    var blockMarkerEnd = body.indexOf("}", blockMarkerBeg);
                    if (blockMarkerEnd >= 0) {
                        var blockMarker;
                        if (blockMarkerEnd - blockMarkerBeg <= 0) {
                            blockMarker = "{/" + blockType + "}"
                        } else {
                            blockMarker = body.substring(blockMarkerBeg + 1, blockMarkerEnd)
                        }
                        var blockEnd = body.indexOf(blockMarker, blockMarkerEnd + 1);
                        if (blockEnd >= 0) {
                            emitSectionText(body.substring(endStmtPrev + 1, begStmt), funcText);
                            var blockText = body.substring(blockMarkerEnd + 1, blockEnd);
                            if (blockType == "cdata") {
                                emitText(blockText, funcText)
                            } else {
                                if (blockType == "minify") {
                                    emitText(scrubWhiteSpace(blockText), funcText)
                                } else {
                                    if (blockType == "eval") {
                                        if (blockText != null && blockText.length > 0) {
                                            funcText.push("_OUT.write( (function() { " + blockText + " })() );")
                                        }
                                    }
                                }
                            }
                            begStmt = endStmtPrev = blockEnd + blockMarker.length - 1
                        }
                    }
                } else {
                    if (body.charAt(begStmt - 1) != "$" && body.charAt(begStmt - 1) != "\\") {
                        var offset = (body.charAt(begStmt + 1) == "/" ? 2 : 1);
                        if (body.substring(begStmt + offset, begStmt + 10 + offset).search(TrimPath.parseTemplate_etc.statementTag) == 0) {
                            break
                        }
                    }
                }
                begStmt = body.indexOf("{", begStmt + 1)
            }
            if (begStmt < 0) {
                break
            }
            var endStmt = body.indexOf("}", begStmt + 1);
            if (endStmt < 0) {
                break
            }
            emitSectionText(body.substring(endStmtPrev + 1, begStmt), funcText);
            emitStatement(body.substring(begStmt, endStmt + 1), state, funcText, tmplName, etc);
            endStmtPrev = endStmt
        }
        emitSectionText(body.substring(endStmtPrev + 1), funcText);
        if (state.stack.length != 0) {
            throw new etc.ParseError(tmplName, state.line, "unclosed, unmatched statement(s): " + state.stack.join(","))
        }
        funcText.push("}}; TrimPath_Template_TEMP");
        return funcText.join("")
    };
    var emitStatement = function (stmtStr, state, funcText, tmplName, etc) {
        var parts = stmtStr.slice(1, -1).split(" ");
        var stmt = etc.statementDef[parts[0]];
        if (stmt == null) {
            emitSectionText(stmtStr, funcText);
            return
        }
        if (stmt.delta < 0) {
            if (state.stack.length <= 0) {
                throw new etc.ParseError(tmplName, state.line, "close tag does not match any previous statement: " + stmtStr)
            }
            state.stack.pop()
        }
        if (stmt.delta > 0) {
            state.stack.push(stmtStr)
        }
        if (stmt.paramMin != null && stmt.paramMin >= parts.length) {
            throw new etc.ParseError(tmplName, state.line, "statement needs more parameters: " + stmtStr)
        }
        if (stmt.prefixFunc != null) {
            funcText.push(stmt.prefixFunc(parts, state, tmplName, etc))
        } else {
            funcText.push(stmt.prefix)
        }
        if (stmt.suffix != null) {
            if (parts.length <= 1) {
                if (stmt.paramDefault != null) {
                    funcText.push(stmt.paramDefault)
                }
            } else {
                for (var i = 1; i < parts.length; i++) {
                    if (i > 1) {
                        funcText.push(" ")
                    }
                    funcText.push(parts[i])
                }
            }
            funcText.push(stmt.suffix)
        }
    };
    var emitSectionText = function (text, funcText) {
        if (text.length <= 0) {
            return
        }
        var nlPrefix = 0;
        var nlSuffix = text.length - 1;
        while (nlPrefix < text.length && (text.charAt(nlPrefix) == "\n")) {
            nlPrefix++
        }
        while (nlSuffix >= 0 && (text.charAt(nlSuffix) == " " || text.charAt(nlSuffix) == "\t")) {
            nlSuffix--
        }
        if (nlSuffix < nlPrefix) {
            nlSuffix = nlPrefix
        }
        if (nlPrefix > 0) {
            funcText.push('if (_FLAGS.keepWhitespace == true) _OUT.write("');
            var s = text.substring(0, nlPrefix).replace("\n", "\\n");
            if (s.charAt(s.length - 1) == "\n") {
                s = s.substring(0, s.length - 1)
            }
            funcText.push(s);
            funcText.push('");')
        }
        var lines = text.substring(nlPrefix, nlSuffix + 1).split("\n");
        for (var i = 0; i < lines.length; i++) {
            emitSectionTextLine(lines[i], funcText);
            if (i < lines.length - 1) {
                funcText.push('_OUT.write("\\n");\n')
            }
        }
        if (nlSuffix + 1 < text.length) {
            funcText.push('if (_FLAGS.keepWhitespace == true) _OUT.write("');
            var s = text.substring(nlSuffix + 1).replace("\n", "\\n");
            if (s.charAt(s.length - 1) == "\n") {
                s = s.substring(0, s.length - 1)
            }
            funcText.push(s);
            funcText.push('");')
        }
    };
    var emitSectionTextLine = function (line, funcText) {
        var endMarkPrev = "}";
        var endExprPrev = -1;
        while (endExprPrev + endMarkPrev.length < line.length) {
            var begMark = "${",endMark="}";
            var begExpr = line.indexOf(begMark, endExprPrev + endMarkPrev.length);
            if (begExpr < 0) {
                break
            }
            if (line.charAt(begExpr + 2) == "%") {
                begMark = "${%";
                endMark = "%}"
            }
            var endExpr = line.indexOf(endMark, begExpr + begMark.length);
            if (endExpr < 0) {
                break
            }
            emitText(line.substring(endExprPrev + endMarkPrev.length, begExpr), funcText);
            var exprArr = line.substring(begExpr + begMark.length, endExpr).replace(/\|\|/g, "#@@#").split("|");
            for (var k in exprArr) {
                if (exprArr[k].replace) {
                    exprArr[k] = exprArr[k].replace(/#@@#/g, "||")
                }
            }
            funcText.push("_OUT.write(");
            emitExpression(exprArr, exprArr.length - 1, funcText);
            funcText.push(");");
            endExprPrev = endExpr;
            endMarkPrev = endMark
        }
        emitText(line.substring(endExprPrev + endMarkPrev.length), funcText)
    };
    var emitText = function (text, funcText) {
        if (text == null || text.length <= 0) {
            return
        }
        text = text.replace(/\\/g, "\\\\");
        text = text.replace(/\n/g, "\\n");
        text = text.replace(/"/g, '\\"');
        funcText.push('_OUT.write("');
        funcText.push(text);
        funcText.push('");')
    };
    var emitExpression = function (exprArr, index, funcText) {
        var expr = exprArr[index];
        if (index <= 0) {
            funcText.push(expr);
            return
        }
        var parts = expr.split(":");
        funcText.push('_MODIFIERS["');
        funcText.push(parts[0]);
        funcText.push('"](');
        emitExpression(exprArr, index - 1, funcText);
        if (parts.length > 1) {
            funcText.push(",");
            funcText.push(parts[1])
        }
        funcText.push(")")
    };
    var cleanWhiteSpace = function (result) {
        result = result.replace(/\t/g, "    ");
        result = result.replace(/\r\n/g, "\n");
        result = result.replace(/\r/g, "\n");
        result = result.replace(/^(\s*\S*(\s+\S+)*)\s*$/, "$1");
        return result
    };
    var scrubWhiteSpace = function (result) {
        result = result.replace(/^\s+/g, "");
        result = result.replace(/\s+$/g, "");
        result = result.replace(/\s+/g, " ");
        result = result.replace(/^(\s*\S*(\s+\S+)*)\s*$/, "$1");
        return result
    };
    TrimPath.parseDOMTemplate = function (elementId, optDocument, optEtc) {
        if (optDocument == null) {
            optDocument = document
        }
        var element = optDocument.getElementById(elementId);
        var content = element.value;
        if (content == null) {
            content = element.innerHTML
        }
        content = content.replace(/&lt;/g, "<").replace(/&gt;/g, ">");
        return TrimPath.parseTemplate(content, elementId, optEtc)
    };
    TrimPath.processDOMTemplate = function (elementId, context, optFlags, optDocument, optEtc) {
        return TrimPath.parseDOMTemplate(elementId, optDocument, optEtc).process(context, optFlags)
    }
})();
(function () {
    var aq = {};
    (function () {
        var t = ["abstract bool break case catch char class const const_cast continue default delete deprecated dllexport dllimport do double dynamic_cast else enum explicit extern false float for friend goto if inline int long mutable naked namespace new noinline noreturn nothrow novtable operator private property protected public register reinterpret_cast return selectany short signed sizeof static static_cast struct switch template this thread throw true try typedef typeid typename union unsigned using declaration, directive uuid virtual void volatile while typeof", "as base by byte checked decimal delegate descending event finally fixed foreach from group implicit in interface internal into is lock null object out override orderby params readonly ref sbyte sealed stackalloc string select uint ulong unchecked unsafe ushort var", "package synchronized boolean implements import throws instanceof transient extends final strictfp native super", "debugger export function with NaN Infinity", "require sub unless until use elsif BEGIN END", "and assert def del elif except exec global lambda not or pass print raise yield False True None", "then end begin rescue ensure module when undef next redo retry alias defined", "done fi"];
        for (var r = 0; r < t.length; r++) {
            var q = t[r].split(" ");
            for (var s = 0; s < q.length; s++) {
                if (q[s]) {
                    aq[q[s]] = true
                }
            }
        }
    }).call(this);
    function ab(q) {
        return q >= "a" && q <= "z" || q >= "A" && q <= "Z"
    }

    function ay(t, r, q, s) {
        t.unshift(q, s || 0);
        try {
            r.splice.apply(r, t)
        } finally {
            t.splice(0, 2)
        }
    }

    var i = (function () {
        var t = ["!", "!=", "!==", "#", "%", "%=", "&", "&&", "&&=", "&=", "(", "*", "*=", "+=", ",", "-=", "->", "/", "/=", ":", "::", ";", "<", "<<", "<<=", "<=", "=", "==", "===", ">", ">=", ">>", ">>=", ">>>", ">>>=", "?", "@", "[", "^", "^=", "^^", "^^=", "{", "|", "|=", "||", "||=", "~", "break", "case", "continue", "delete", "do", "else", "finally", "instanceof", "return", "throw", "try", "typeof"], r = "(?:(?:(?:^|[^0-9.])\\.{1,3})|(?:(?:^|[^\\+])\\+)|(?:(?:^|[^\\-])-)";
        for (var q = 0; q < t.length; ++q) {
            var s = t[q];
            if (ab(s.charAt(0))) {
                r += "|\\b" + s
            } else {
                r += "|" + s.replace(/([^=<>:&])/g, "\\$1")
            }
        }
        r += "|^)\\s*$";
        return new RegExp(r)
    })(), ap = /&/g, ak = /</g, ao = />/g, am = /\"/g;

    function at(q) {
        return q.replace(ap, "&amp;").replace(ak, "&lt;").replace(ao, "&gt;")
    }

    var a = /&lt;/g, b = /&gt;/g, g = /&apos;/g, al = /&quot;/g, h = /&amp;/g;

    function ac(v) {
        var r = v.indexOf("&");
        if (r < 0) {
            return v
        }
        for (--r; (r = v.indexOf("&#", r + 1)) >= 0;) {
            var q = v.indexOf(";", r);
            if (q >= 0) {
                var u = v.substring(r + 3, q), s = 10;
                if (u && u.charAt(0) == "x") {
                    u = u.substring(1);
                    s = 16
                }
                var t = parseInt(u, s);
                if (!isNaN(t)) {
                    v = v.substring(0, r) + String.fromCharCode(t) + v.substring(q + 1)
                }
            }
        }
        return v.replace(a, "<").replace(b, ">").replace(g, "'").replace(al, '"').replace(h, "&")
    }

    function ar(q) {
        return"XMP" == q.tagName
    }

    var av = null;

    function ad(u) {
        if (null === av) {
            var r = document.createElement("PRE");
            r.appendChild(document.createTextNode('<!DOCTYPE foo PUBLIC "foo bar">\n<foo />'));
            av = !/</.test(r.innerHTML)
        }
        if (av) {
            var q = u.innerHTML;
            if (ar(u)) {
                q = at(q)
            }
            return q
        }
        var t = [];
        for (var s = u.firstChild; s; s = s.nextSibling) {
            au(s, t)
        }
        return t.join("")
    }

    function au(v, r) {
        switch (v.nodeType) {
            case 1:
                var q = v.tagName.toLowerCase();
                r.push("<", q);
                for (var u = 0; u < v.attributes.length; ++u) {
                    var s = v.attributes[u];
                    if (!s.specified) {
                        continue
                    }
                    r.push(" ");
                    au(s, r)
                }
                r.push(">");
                for (var t = v.firstChild; t; t = t.nextSibling) {
                    au(t, r)
                }
                if (v.firstChild || !/^(?:br|link|img)$/.test(q)) {
                    r.push("</", q, ">")
                }
                break;
            case 2:
                r.push(v.name.toLowerCase(), '="', v.value.replace(ap, "&amp;").replace(ak, "&lt;").replace(ao, "&gt;").replace(am, "&quot;"), '"');
                break;
            case 3:
            case 4:
                r.push(at(v.nodeValue));
                break
        }
    }

    function k(r) {
        var q = 0;
        return function (s) {
            var y = null, v = 0;
            for (var x = 0, t = s.length; x < t; ++x) {
                var w = s.charAt(x);
                switch (w) {
                    case"\t":
                        if (!y) {
                            y = []
                        }
                        y.push(s.substring(v, x));
                        var u = r - q % r;
                        q += u;
                        for (; u >= 0; u -= "                ".length) {
                            y.push("                ".substring(0, u))
                        }
                        v = x + 1;
                        break;
                    case"\n":
                        q = 0;
                        break;
                    default:
                        ++q
                }
            }
            if (!y) {
                return s
            }
            y.push(s.substring(v));
            return y.join("")
        }
    }

    var d = /(?:[^<]+|<!--[\s\S]*?--\>|<!\[CDATA\[([\s\S]*?)\]\]>|<\/?[a-zA-Z][^>]*>|<)/g, c = /^<!--/, e = /^<\[CDATA\[/, f = /^<br\b/i;

    function ae(w) {
        var y = w.match(d), x = [], v = 0, s = [];
        if (y) {
            for (var u = 0, q = y.length; u < q; ++u) {
                var t = y[u];
                if (t.length > 1 && t.charAt(0) === "<") {
                    if (c.test(t)) {
                        continue
                    }
                    if (e.test(t)) {
                        x.push(t.substring(9, t.length - 3));
                        v += t.length - 12
                    } else {
                        if (f.test(t)) {
                            x.push("\n");
                            v += 1
                        } else {
                            s.push(v, t)
                        }
                    }
                } else {
                    var r = ac(t);
                    x.push(r);
                    v += r.length
                }
            }
        }
        return{source: x.join(""), tags: s}
    }

    function ax(t, r) {
        var q = {};
        (function () {
            var w = t.concat(r);
            for (var y = w.length; --y >= 0;) {
                var u = w[y], x = u[3];
                if (x) {
                    for (var v = x.length; --v >= 0;) {
                        q[x.charAt(v)] = u
                    }
                }
            }
        })();
        var s = r.length;
        return function (D, F) {
            F = F || 0;
            var B = [F, "pln"], E = "", C = 0, w = D;
            while (w.length) {
                var A, z = null, x = q[w.charAt(0)];
                if (x) {
                    var y = w.match(x[1]);
                    z = y[0];
                    A = x[0]
                } else {
                    for (var v = 0; v < s; ++v) {
                        x = r[v];
                        var u = x[2];
                        if (u && !u.test(E)) {
                            continue
                        }
                        var y = w.match(x[1]);
                        if (y) {
                            z = y[0];
                            A = x[0];
                            break
                        }
                    }
                    if (!z) {
                        A = "pln";
                        z = w.substring(0, 1)
                    }
                }
                B.push(F + C, A);
                C += z.length;
                w = w.substring(z.length);
                if (A !== "com" && /\S/.test(z)) {
                    E = z
                }
            }
            return B
        }
    }

    var ai = ax([
        ["str", /^\'(?:[^\\\']|\\[\s\S])*(?:\'|$)/, null, "'"],
        ["str", /^\"(?:[^\\\"]|\\[\s\S])*(?:\"|$)/, null, '"'],
        ["str", /^\`(?:[^\\\`]|\\[\s\S])*(?:\`|$)/, null, "`"]
    ], [
        ["pln", /^(?:[^\'\"\`\/\#]+)/, null, " \r\n"],
        ["com", /^#[^\r\n]*/, null, "#"],
        ["com", /^\/\/[^\r\n]*/, null],
        ["str", /^\/(?:[^\\\*\/]|\\[\s\S])+(?:\/|$)/, i],
        ["com", /^\/\*[\s\S]*?(?:\*\/|$)/, null]
    ]);
    var aj = ax([], [
        ["pln", /^\s+/, null, " \r\n"],
        ["pln", /^[a-z_$@][a-z_$@0-9]*/i, null],
        ["lit", /^0x[a-f0-9]+[a-z]/i, null],
        ["lit", /^(?:\d(?:_\d+)*\d*(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?[a-z]*/i, null, "123456789"],
        ["pun", /^[^\s\w\.$@]+/, null]
    ]);

    function o(B, D) {
        for (var C = 0; C < D.length; C += 2) {
            var A = D[C + 1];
            if (A === "pln") {
                var x = D[C], z = C + 2 < D.length ? D[C + 2] : B.length, v = B.substring(x, z), y = aj(v, x);
                for (var w = 0, q = y.length; w < q; w += 2) {
                    var u = y[w + 1];
                    if (u === "pln") {
                        var t = y[w], r = w + 2 < q ? y[w + 2] : v.length, s = B.substring(t, r);
                        if (s == ".") {
                            y[w + 1] = "pun"
                        } else {
                            if (s in aq) {
                                y[w + 1] = "kwd"
                            } else {
                                if (/^@?[A-Z][A-Z$]*[a-z][A-Za-z$]*$/.test(s)) {
                                    y[w + 1] = s.charAt(0) == "@" ? "lit" : "typ"
                                }
                            }
                        }
                    }
                }
                ay(y, D, C, 2);
                C += y.length - 2
            }
        }
        return D
    }

    var ah = ax([], [
        ["pln", /^[^<]+/, null],
        ["dec", /^<!\w[^>]*(?:>|$)/, null],
        ["com", /^<!--[\s\S]*?(?:--\>|$)/, null],
        ["src", /^<\?[\s\S]*?(?:\?>|$)/, null],
        ["src", /^<%[\s\S]*?(?:%>|$)/, null],
        ["src", /^<(script|style|xmp)\b[^>]*>[\s\S]*?<\/\1\b[^>]*>/i, null],
        ["tag", /^<\/?\w[^<>]*>/, null]
    ]);

    function j(w) {
        var r = ah(w);
        for (var q = 0; q < r.length; q += 2) {
            if (r[q + 1] === "src") {
                var v = r[q], t = q + 2 < r.length ? r[q + 2] : w.length, u = w.substring(v, t), s = u.match(/^(<[^>]*>)([\s\S]*)(<\/[^>]*>)$/);
                if (s) {
                    r.splice(q, 2, v, "tag", v + s[1].length, "src", v + s[1].length + (s[2] || "").length, "tag")
                }
            }
        }
        return r
    }

    var ag = ax([
        ["atv", /^\'[^\']*(?:\'|$)/, null, "'"],
        ["atv", /^\"[^\"]*(?:\"|$)/, null, '"'],
        ["pun", /^[<>\/=]+/, null, "<>/="]
    ], [
        ["tag", /^[\w-]+/, /^</],
        ["atv", /^[\w-]+/, /^=/],
        ["atn", /^[\w-]+/, null],
        ["pln", /^\s+/, null, " \r\n"]
    ]);

    function l(x, r) {
        for (var q = 0; q < r.length; q += 2) {
            var w = r[q + 1];
            if (w === "tag") {
                var t = r[q], v = q + 2 < r.length ? r[q + 2] : x.length, s = x.substring(t, v), u = ag(s, t);
                ay(u, r, q, 2);
                q += u.length - 2
            }
        }
        return r
    }

    function m(w, y) {
        for (var x = 0; x < y.length; x += 2) {
            var v = y[x + 1];
            if (v == "src") {
                var s = y[x], u = x + 2 < y.length ? y[x + 2] : w.length, q = aw(w.substring(s, u));
                for (var t = 0, r = q.length; t < r; t += 2) {
                    q[t] += s
                }
                ay(q, y, x, 2);
                x += q.length - 2
            }
        }
        return y
    }

    function n(D, F) {
        var E = false;
        for (var C = 0; C < F.length; C += 2) {
            var z = F[C + 1];
            if (z === "atn") {
                var B = F[C], x = C + 2 < F.length ? F[C + 2] : D.length;
                E = /^on|^style$/i.test(D.substring(B, x))
            } else {
                if (z == "atv") {
                    if (E) {
                        var B = F[C], x = C + 2 < F.length ? F[C + 2] : D.length, A = D.substring(B, x), y = A.length, s = y >= 2 && /^[\"\']/.test(A) && A.charAt(0) === A.charAt(y - 1), w, v, t;
                        if (s) {
                            v = B + 1;
                            t = x - 1;
                            w = A
                        } else {
                            v = B + 1;
                            t = x - 1;
                            w = A.substring(1, A.length - 1)
                        }
                        var u = aw(w);
                        for (var r = 0, q = u.length; r < q; r += 2) {
                            u[r] += v
                        }
                        if (s) {
                            u.push(t, "atv");
                            ay(u, F, C + 2, 0)
                        } else {
                            ay(u, F, C, 2)
                        }
                    }
                    E = false
                }
            }
        }
        return F
    }

    function aw(r) {
        var q = ai(r);
        q = o(r, q);
        return q
    }

    function af(r) {
        var q = j(r);
        q = l(r, q);
        q = m(r, q);
        q = n(r, q);
        return q
    }

    function p(z, B, A) {
        var y = [], v = 0, x = null, t = null, w = 0, u = 0, q = k(8);

        function s(C) {
            if (C > v) {
                if (x && x !== t) {
                    y.push("</span>");
                    x = null
                }
                if (!x && t) {
                    x = t;
                    y.push('<span class="', x, '">')
                }
                var D = at(q(z.substring(v, C))).replace(/(\r\n?|\n| ) /g, "$1&nbsp;").replace(/\r\n?|\n/g, "<br>");
                y.push(D);
                v = C
            }
        }

        while (true) {
            var r;
            if (w < B.length) {
                if (u < A.length) {
                    r = B[w] <= A[u]
                } else {
                    r = true
                }
            } else {
                r = false
            }
            if (r) {
                s(B[w]);
                if (x) {
                    y.push("</span>");
                    x = null
                }
                y.push(B[w + 1]);
                w += 2
            } else {
                if (u < A.length) {
                    s(A[u]);
                    t = A[u + 1];
                    u += 2
                } else {
                    break
                }
            }
        }
        s(z.length);
        if (x) {
            y.push("</span>")
        }
        return y.join("")
    }

    function an(w) {
        try {
            var r = ae(w), q = r.source, v = r.tags, t = /^\s*</.test(q) && />\s*$/.test(q), u = t ? af(q) : aw(q);
            return p(q, v, u)
        } catch (s) {
            if ("console" in window) {
                console.log(s);
                console.trace()
            }
            return w
        }
    }

    function az(w) {
        var r = [document.getElementsByTagName("pre"), document.getElementsByTagName("code"), document.getElementsByTagName("xmp")], q = [];
        for (var v = 0; v < r.length; ++v) {
            for (var t = 0; t < r[v].length; ++t) {
                q.push(r[v][t])
            }
        }
        r = null;
        var u = 0;

        function s() {
            var F = (new Date).getTime() + 250;
            for (; u < q.length && (new Date).getTime() < F; u++) {
                var E = q[u];
                if (E.className && E.className.indexOf("prettyprint") >= 0) {
                    var z = false;
                    for (var D = E.parentNode; D != null; D = D.parentNode) {
                        if ((D.tagName == "pre" || D.tagName == "code" || D.tagName == "xmp") && D.className && D.className.indexOf("prettyprint") >= 0) {
                            z = true;
                            break
                        }
                    }
                    if (!z) {
                        var C = ad(E);
                        C = C.replace(/(?:\r\n?|\n)$/, "");
                        var A = an(C);
                        if (!ar(E)) {
                            E.innerHTML = A
                        } else {
                            var B = document.createElement("PRE");
                            for (var y = 0; y < E.attributes.length; ++y) {
                                var x = E.attributes[y];
                                if (x.specified) {
                                    B.setAttribute(x.name, x.value)
                                }
                            }
                            B.innerHTML = A;
                            E.parentNode.replaceChild(B, E)
                        }
                    }
                }
            }
            if (u < q.length) {
                setTimeout(s, 250)
            } else {
                if (w) {
                    w()
                }
            }
        }

        s()
    }

    this.prettyPrint = az
})();
$o(window, "load", function () {
    prettyPrint();
    var f = $("FOCUS");
    if (f) {
        f.focus()
    }
    for (var b = 0; b < document.forms.length; b++) {
        var c = document.forms[b];
        for (var a = 0; a < c.length; a++) {
            var d = c.elements[a];
            if (!d.type) {
                continue
            }
            if (d.type == "textarea") {
                d.onkeydown = function (e) {
                    e = (e) ? e : ((event) ? event : null);
                    if (e.ctrlKey && e.keyCode == 13) {
                        if (this.form.onsubmit() != false) {
                            this.form.submit()
                        }
                    }
                }
            }
            if ("file,button,reset,submit".indexOf(d.type) > -1) {
                d.className = "button"
            }
        }
    }
    Net.Event.stopObserving(window, "load", arguments.callee)
});
$dw("<div id=DIVpopLayer style='position:absolute;z-index:9999;'></div>");
var g_sPop = "";
$o(document, "mouseover", function (i) {
    i = i ? i : event;
    var c = i.srcElement ? i.srcElement : i.target;
    if (!g_sPop || !c || c.tagName == "FORM") {
        return
    }
    if (c.alt && c.alt != "") {
        c.pop = c.alt;
        c.alt = ""
    }
    if (c.title && c.title != "") {
        c.pop = c.title;
        c.title = ""
    }
    if (c.pop != g_sPop) {
        g_sPop = c.pop;
        var b = $("DIVpopLayer");
        if (g_sPop == null || g_sPop == "") {
            b.style.visibility = "hidden"
        } else {
            b.style.visibility = "visible";
            b.className = (c._class != null) ? c._class : "cPopText";
            b.innerHTML = g_sPop.replace(/<(.*)>/g, "&lt;$1&gt;").replace(/\n/g, "<br>");
            var h = i.clientX;
            var g = i.clientY;
            var f = b.clientWidth;
            var e = b.clientHeight;
            var a = (h + 12 + f > document.body.clientWidth) ? -f - 24 : 0;
            var d = (g + 12 + e > document.body.clientHeight) ? -e - 24 : 0;
            b.style.left = h + 12 + document.body.scrollLeft + a;
            b.style.top = g + 12 + document.body.scrollTop + d
        }
    }
});
Net.Html.show = function (a) {
    if (a == "bbshead") {
        $dw('<style type="text/css"><!--body {margin-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; }tr {height:18px;}--></style><body><table width="100%"  border="0" cellspacing="3" cellpadding="0"><tr><td>	<table width="100%"  border="0" cellspacing="3" cellpadding="0" class="NavLine">	<tr align="center" class="NavTab">	<td><a href="http://www.nju.edu.cn/" class="nav" target="_blank">南京大学</a></td>	<td><a href="http://news.nju.edu.cn/" class="nav" target="_blank">南大新闻网</a></td>	<td><a href="http://oa.nju.edu.cn/" class="nav" target="_blank">信息平台</a></td>	<td><a href="http://p.nju.edu.cn/" class="nav" target="_blank">校园网接入认证</a></td>	<td><a href="http://njuef.nju.edu.cn/jjhweb/newsjzfs.aspx?type=zxjz" class="nav" target="_blank">在线捐赠</a></td>	<td><a href="http://lilystudio.org/" class="nav" target="_blank">百合工作室</a></td>	<td><a href="javascript:external.AddFavorite(\'http://bbs.nju.edu.cn/\',\'南京大学小百合BBS\')" class="nav">加入收藏夹</a></td>	<td><a href="#" class="nav" onClick="this.style.behavior=\'url(#default#homepage)\';this.setHomePage(\'http://bbs.nju.edu.cn/\')">设为首页</a></td>	</tr>	</table></td></tr></table>')
    } else {
        if (a == "pnthead") {
            $dw('<style type="text/css"><!--body {margin-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; }tr {height:18px;}--></style><body><table width="100%"  border="0" cellspacing="3" cellpadding="0"><tr><td>	<table width="100%"  border="0" cellspacing="3" cellpadding="0" class="NavLine">	<tr align="center" class="NavTab">	<td><a href="pntmain" class="nav">涂鸦区首页</a></td>	<td><a href="board?board=Paint" class="nav">涂鸦论坛</a></td>	<td><a href="bbsmain" class="nav">讨论区首页</a></td>	<td><a href="blogall" class="nav">blog首页</a></td>	<td><a href="http://info.nju.edu.cn/" class="nav" target="_blank">信息平台</a></td>	<td><a href="http://lilystudio.org/" class="nav" target="_blank">百合工作室</a></td>	<td><a href="http://sunnyclass.lilystudio.org/" class="nav" target="_blank">阳光教室</a></td>	<td><a href="javascript:external.AddFavorite(\'http://bbs.nju.edu.cn/\',\'南京大学小百合BBS\')" class="nav">加入收藏夹</a></td>	<td><a href="#" class="nav" onClick="this.style.behavior=\'url(#default#homepage)\';this.setHomePage(\'http://bbs.nju.edu.cn/\')">设为首页</a></td>	</tr>	</table></td></tr></table><center><br>')
        } else {
            if (a == "copyright") {
                var b = " - - - - - - - - - - - - - - - - - ";
                $dw("<br><br><center>" + b + "CopyRight(C) 1997-" + (new Date()).getFullYear() + ", NJU <span onclick='Net.Util.copyToClip(location.href)' class=hand>Li</span>ly B<span onclick='Net.Util.saveAs()' class=hand>BS</span>" + b + "<br><br>")
            }
        }
    }
};

