import re
import sys
from os import walk, path
import shutil


# Path to jBake blog (source)
JBAKE = None

# Path to Hugo blog (destination). Must contain `content/posts` directory
HUGO = None

def migrate_md(source, destination):
    destination.write("---\n")
    state = "prolog"
    for line in source:
        if state == "prolog":
            if line.startswith("~"):
                destination.write("---\n")
                state = "body"
            elif "=" in line:
                directive, value = line.rstrip("\n").split("=")
                if directive in ["author", "date"]:
                    destination.write(f"{directive}: {value}\n")
                elif directive == "title":
                    destination.write(f"{directive}: \"{value}\"\n")
                elif directive == "tags":
                    destination.write(f"tags: [{value}]\n")
        else:
            destination.write(line)


def migrate_adoc(source, destination):
    destination.write("---\n")
    state = "prolog"
    for line in source:
        if state == "prolog":
            if line.startswith("\n"):
                destination.write("---\n\n")
                state = "body"
            elif line.startswith("= "):
                title = line.lstrip("= ").rstrip("\n")
                destination.write(f"title: \"{title}\"\n")
            elif line.startswith(":"):
                directive, value = re.findall(":(.*): (.*)", line.rstrip("\n"))[0]
                if directive == "jbake-status":
                    draft = "true" if value == "draft" else "false"
                    destination.write(f"draft: {draft}\n")
                elif directive == "jbake-type":
                    pass
                elif directive == "jbake-tags":
                    destination.write(f"tags: [{value}]\n")
                else:
                    print(f"⚠️ Unknown jBake directive: {directive}")
            else:
                if re.match("\d{4}", line):
                    destination.write(f"date: {line}")
                else:
                    destination.write(f"author: {line}")
        else:
            destination.write(line)


def copy_static_dir(subdir):
    jbake_subdir = path.join(JBAKE, "assets", subdir)
    hugo_subdir = path.join(HUGO, "static", subdir)
    if path.exists(hugo_subdir) and path.isdir(hugo_subdir):
        shutil.rmtree(hugo_subdir)
    shutil.copytree(jbake_subdir, hugo_subdir)


def copy_static_files():
    print(f"🖨 Copy images")
    copy_static_dir("img")
    print(f"🖨 Copy media")
    copy_static_dir("media")


def outcome(errors):
    if errors:
        print(f"❌ There were errors")
    else:
        print(f"✨ Migration completed")


def migrate():
    errors = False
    print(f"➡️ {JBAKE} => {HUGO}")
    jbake_content = path.join(JBAKE, "content")
    hugo_posts = path.join(HUGO, "content", "posts")

    _, _, posts = next(walk(jbake_content))
    for post in posts:
        _, file_extension = path.splitext(post)
        with open(path.join(jbake_content, post), "r") as source:
            if file_extension in [".md", ".adoc"]:
                with open(path.join(hugo_posts, post), "w") as destination:
                    print(f"📝 {post}")
                    if file_extension == ".md":
                        migrate_md(source, destination)
                    elif file_extension == ".adoc":
                        migrate_adoc(source, destination)
            else:
                print(f"❌ {post} skipping file type [{file_extension}]")
                errors = True

    copy_static_files()

    outcome(errors)


if __name__ == '__main__':
    JBAKE = sys.argv[1]
    HUGO = sys.argv[2]

    migrate()
