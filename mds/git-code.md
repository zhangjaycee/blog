

* 怎么统计某人在某仓库中的代码行数
```shell
git log --author="YOURNAME" --pretty=tformat: --numstat \
| gawk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "added lines: %s removed lines : %s total lines: %s\n",add,subs,loc }'
```

