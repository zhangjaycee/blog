# JciX~~~  我的博客  http://blog.jcix.top

模板手动fork自https://github.com/WakelessDragon/blog ， 原README保留在文档末尾。

适配jekyll 2.5.3

需要用pip安装代码高亮插件Pygments

---

##[点我查看中文说明](https://github.com/dubuyuye/blog/blob/gh-pages/README_zh_CN.md)

# Blog Address

<http://blog.rainyalley.com/>


# Must Modify

## 1.swiftype

This service provides the on-site search function.

Service address： <https://swiftype.com/>.

After the setup is complete， you need to modify the `swiftype_searchId` in `_config.yml`.

In your swiftype engine, go to `Setup and integration` -> `Install Search`, you could find the `swiftype_searchId`.

```html
<script type="text/javascript">
...
...
  _st('install','swiftype_searchId','2.0.0');
</script>
```

## 2.disqus

This service provides the comment function.

Service address： <https://disqus.com/>.

After the setup is complete， you need to modify the `disqus_shortname` in `_config.yml`.
