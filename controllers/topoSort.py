from models.Queue import *
from models import lnkGraph
import copy

UNVISITED=0
VISITED=1


# TODO 查bug！
def topoSort(lnkGraph:lnkGraph.lnkGraph,need_change=[],limit_term=0,limit_credit=17.5,mode='',base=[],chosen=[]):

    l=len(lnkGraph.graph)
    res=[]
    visited=[UNVISITED]*l
    indegree=lnkGraph.indegree[:]
    in0=Queue()
    next=Queue()
    temp=[]
    temp1=[]
    credit=0
    credits=[]
    partial=[]
    change=len(need_change)
    need_plan=[]
    flag = 0
    # TODO after的话从后面找，优先靠后的排，因为如果是后面的话可能不需要挪动
    wait=[]
    if mode=='credit':
        for index,term in enumerate(base):
            for course in term:
                credit += float(course.credit)
                if credit>limit_credit:
                    res.append(temp)
                    temp=[]
                    credit=0
                else:
                    num=lnkGraph.find_ver_num_by_name(course)
                    no=[lnkGraph.find_next_after(c.name)for c in temp]
                    if num not in no:
                        temp.append(course)
                    else:
                        wait.append(course)
            if wait:
                base[index+1]=wait+base[index+1]
                wait=[]
        return res

    if base!=[]:
        need_plan=[[c for c in t if lnkGraph.find_ver_num_by_name(c.name) in need_change] for t in base]
        base=[[c for c in x if lnkGraph.find_ver_num_by_name(c.name) not in need_change] for x in base]
        if not base[limit_term-1]:
            print("plan is too short! cant make it")
            return -1
    credits=[[float(c.credit) for c in term] for term in base]
    credits=[float(sum(term)) for term in credits]

    if mode:
        for e in range(l):
            if indegree[e]==0:
                in0.push(e)
        while not in0.is_empty() or not next.is_empty():
            if change:
                bl=True
                for index,a in enumerate(indegree):
                    if index not in need_change:
                        bl=bl and visited[index] and visited[need_change[0]]==0
                if bl:
                    print("the plan can't be made!!")
                    return False
            while not in0.is_empty():
                ver = in0.dequeue()
                course = lnkGraph.graph[ver].head.ele
                node = lnkGraph.graph[ver].head.next
                if ver in need_change:
                    if course.compulsory and mode=='before':
                        credit += float(course.credit)
                    if credit <= limit_credit/3 and mode=='before':
                        temp1.append(course)
                    elif mode=='before':
                        flag+=1
                        partial.append(temp1)
                        temp1 = [course]
                        credit = float(course.credit)
                    if course.compulsory and mode=='after':
                        if flag + limit_term >= len(credits):
                            credits.append(0.0)
                        credits[flag+limit_term] += float(course.credit)
                    if credits[flag+limit_term] <= limit_credit and mode=='after':
                        temp1.append(course)
                    elif mode=='after':
                        flag+=1
                        partial.append(temp1)
                        temp1 = [course]
                        if flag + limit_term >= len(credits):
                            credits.append(0.0)
                        credits[flag+limit_term] = float(course.credit)
                visited[ver] = VISITED
                while node:
                    name = lnkGraph.graph[node.ele].head.ele.name
                    indegree[node.ele] -= 1
                    if indegree[node.ele] == 0:
                        next.push(node.ele)
                    node = node.next
            no = []
            for c in temp1:
                num = lnkGraph.find_ver_num_by_name(c.name)
                af = lnkGraph.find_next_after(num)
                no += af
            later=[]
            while not next.is_empty():
                v=next.dequeue()
                if v in no:
                    later.append(v)
                    continue
                if not in0.is_in(v):
                    in0.push(v)
            for e in later:
                if not next.is_in(e):
                    next.push(e)
            if in0.is_empty() and not next.is_empty():
                if len(temp1)!=0:
                    flag+=1
                    partial.append(temp1)
                    temp1=[]
                    if flag+limit_term>=len(credits):
                        credits.append(0.0)
                    credits[flag+limit_term]=0.0
                t=next.dequeue()
                if not in0.is_in(t):
                    in0.push(t)
        partial.append(temp1)
    partial=[x for x in partial if x]
    if mode=='after':
        need_len=len(need_plan)
        par_len=len(partial)+limit_term
        if par_len>need_len:
            for j in range(par_len-need_len):
                need_plan.append(partial[par_len-limit_term-1-j])
                need_plan[:need_len+j]=[[c for c in x if c not in partial[par_len-limit_term-1-j]] for x in need_plan[:need_len+j]]
        elif par_len<need_len:
            for index in range(par_len,need_len):
                if not need_plan[index]:continue
                for ind, t in enumerate(partial):  # stay in need_plan; del it in partial
                    partial[ind] = [c for c in t if c not in need_plan[index]]
        m=min(need_len,par_len)
        for index in range(m-1,-1,-1):
            if index-limit_term<=0:break
            need_plan[index]+=[course for course in partial[index-limit_term] if course not in need_plan[index]]
            for ind,term in enumerate(need_plan): # put it in need_plan; del it in need_plan
                if ind==index: break
                if not need_plan[ind]: continue
                need_plan[ind]=[c for c in term if c not in need_plan[index]]
    elif mode=='before':
        if len(partial)>limit_term+1:
            print("too long! cant make it")
            return False
        need_len=len(need_plan)
        par_len=len(partial)
        gap=limit_term-par_len+1
        for i in range(need_len):
            if i>limit_term:
                break
            if i-gap<0:
                partial=[[c for c in t if c not in need_plan[i]] for t in partial]
                continue
            need_plan[i]+=[c for c in partial[i-gap] if c not in need_plan[i]]
            need_plan[i+1:]=[[cc for cc in t if cc not in need_plan[i]] for t in need_plan[i+1:]]

    if mode:
        res=base[:]
        for ii,t in enumerate(need_plan):
            if ii>=len(res):
                res.append(need_plan[ii])
            else:
                res[ii]+=list(need_plan[ii])
        return res

    indegree=lnkGraph.indegree[:]
    for e in range(l):
        if indegree[e]==0:
            in0.push(e)
    flag=0
    while not in0.is_empty() or not next.is_empty():
        while not in0.is_empty():
            ver = in0.dequeue()
            course = lnkGraph.graph[ver].head.ele
            node = lnkGraph.graph[ver].head.next
            if course.compulsory and not visited[ver]:
                if flag<len(credits):
                    credits[flag] += float(course.credit)
                else:
                    credits.append(float(course.credit))
            if credits[flag] <= limit_credit and not visited[ver]:
                temp.append(course)
            elif not visited[ver]:
                res.append(temp)
                temp = [course]
                flag+=1
                if flag<len(credits):
                    credits[flag] = float(course.credit)
                else:
                    credits.append(float(course.credit))
            visited[ver] = VISITED
            while node:
                indegree[node.ele] -= 1
                if indegree[node.ele] == 0:
                    next.push(node.ele)
                node = node.next
        no = []
        for c in temp:
            num = lnkGraph.find_ver_num_by_name(c.name)
            af = lnkGraph.find_next_after(num)
            no += af
        if flag>=limit_term and flag-limit_term<len(partial):
            for nn in partial[flag-limit_term]:
                no+=lnkGraph.find_next_after(lnkGraph.find_ver_num_by_name(nn.name))
        later=[]
        while not next.is_empty():
            v=next.dequeue()
            if v in no:
                later.append(v)
                continue
            if v in need_change and flag<limit_term:
                later.append(v)
                continue
            if not in0.is_in(v):
                in0.push(v)
        for e in later:
            if not next.is_in(e):
                next.push(e)
        if in0.is_empty() and not next.is_empty():
            if len(temp)!=0:
                res.append(temp)
                temp=[]
                flag+=1
                if flag<len(credits):
                    credits[flag] =0
                else:
                    credits.append(float(0))
            t=next.dequeue()
            if not in0.is_in(t):
                in0.push(t)
    res.append(temp)

    for ind in visited:
        if ind==UNVISITED:
            print("Error!!!")
            return False
    return res
