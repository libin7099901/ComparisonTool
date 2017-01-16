# -*- coding:utf-8 -*-

str = "tag\tvalue"

if __name__ == "__main__":
    tag = str.find("\t")
    with open("./~test", "w") as temp_file:
        temp_file.write("")