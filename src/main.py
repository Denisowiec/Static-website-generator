from textnode import *

def main():
    example = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(example)

if __name__=="__main__":
    main()