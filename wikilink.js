! function() {
	"use strict";
	window.$docsify ? window.$docsify.plugins = [].concat((function(n, e) {
		n.beforeEach((function(n) {
			return n
		})), n.afterEach((function(n, e) {
			var i = document.createElement("div");
			i.innerHTML = n;
			var t = location.hash.lastIndexOf("/"),
				o = location.hash.substring(0, t + 1);
			const r = [];
			r.push(...i.getElementsByTagName("p")), r.push(...i.getElementsByTagName("li"));
			for (var c = 0; c < r.length; c++) {
				const n = r[c].innerHTML.replace(/\[\[([^\[\]]+)\]\]/g, (function(n) {
					const e = n.replace("[[", "").replace("]]", ""),
						i = e.split("|"),
						t = 2 === i.length ? `${i[0].trim()}` : e;
					var r = t,
						c = "",
						a = e;
					if (-1 != t.indexOf("#")) {
						const n = t.split("#");
						r = n[0], c = `?id=${n[1]}`, a = `${i[1].trim()}`
					}
                    if (a.split("|").length==2){a=a.split("|")[1]}
					return 0 === r.indexOf("/") ? `<a href="#${r}${c}">${a}</a>` : `<a href="${o}${r}${c}">${a}</a>`
				}));
				r[c].innerHTML = n
			}
			e(i.innerHTML)
		}))
	}), window.$docsify.plugins) : console.error(" 这是一个 docsify 插件，请先引用 docsify 库！")
}();