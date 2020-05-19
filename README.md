# jbake-to-hugo

Simple python script to migrate a JBake blog to Hugo 🐍 🖋 ➡️ 🖋

- [JBake](https://jbake.org/)
- [Hugo](https://gohugo.io/)
- [I switched from JBake to Hugo](https://blog.sugoi.be/posts/blogging-with-hugo/)

## Run

The Hugo blog must already exist before running the migration.

```
python migrate.py path/to/jbake/blog path/to/hugo/blog
```

## Caveats

- This is a simple script, nothing fancy, used it once, not battle tested. Make a backup copy of source/destination in case things go wrong.
- Multiple-levels are not handled

## License

[GNU General Public License v.3](LICENSE)
