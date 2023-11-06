
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



