
# TODO word_wrap:
def word_wrap(words,widget_width,letter_width):
    num=int((widget_width-50)/letter_width)
    l=len(words)
    if l<=num :
        return words
    res=''
    cur=0
    while l-cur>num:
        res=res+words[cur:cur+num]+'\n'
        cur=cur+num
    if cur!=l-1:
        res+=words[cur:l]
    return res

# letter_width=10
# widget_width=300
# words='十六点九分连锁酒店房间十六点九分洛杉矶发了开始分解落实到房间里开始打飞机'
# res=word_wrap(words,widget_width,letter_width)
# print(res)