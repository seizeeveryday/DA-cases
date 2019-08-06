import random
import numpy as np


#生成一个中奖随机数组
def gen_random(num = 100):
    #我们面前有三个门，大奖藏在某个门背后，我们给大奖所在的门编个号（1号，2号，3号），在1,2,3之间随机生成
    #要让你信服，我们会玩很多轮，所以这里默认是生成100轮的正确答案（也就是玩100次）
    lst = np.random.randint(1,4,size = num)
    
    return lst



#猜法一就是盲猜，我们从1,2,3个门中随机猜一个，且不会因为主持人的干扰而改变想法，所以开始猜什么最终也就是什么
def guess_one(num = 100):
    
    #生成正确的答案
    lst = gen_random(num)
    
    #猜的轮数和前面生成的轮数一致，这里默认玩100次（生成100次正确答案，对应猜100次）
    guess = np.random.randint(1,4,size = len(lst))

    #计算有多少个正确的，相等即为正确，最终返回FALSE和TRUE的序列
    judge = (lst == guess)
    
    #因为TRUE默认是1，FALSE默认是0，我们直接求和，来计算正确率是多少
    correct_rate = judge.sum() / len(judge)

    print('Bro，这次我们玩%d轮~' % num)
    print('在第二次改变选择的策略下，你最终的中奖率是:%.2f' % (correct_rate * 100))



#猜法二，从1，2，3个门中随机猜一个，当主持人打开一个空门，改变最初的选择
def guess_two(num = 100):

    #和上面一样，随机生成100次正确答案
    lst = gen_random(num)

    #第一步，依然是随机猜100次
    guess = np.random.randint(1,4,size = len(lst))

    #因为第二次我们会改变选择，这里创建一个列表来存储我们改变后的最终选择
    guess_change = []

    for i,j in zip(lst,guess):

        #无论是否中奖，在主持人第一次打开门阶段，我们选择的门不会被打开，背后是大奖的门也不会被打开（有时候可能是同一个）
        #举个栗子：当我们选择的是A门，大奖藏在B门，那主持人帮我们打开的空门一定是C门，然后问我们是否改变选择
        #也就是说，当我们第一步猜的和正确答案不一致，改变选择之后一定会中奖

        #i是正确答案，j是我们第一步猜的
        if i != j:
            #如果正确答案和我们第一次猜的不一致，主持人排除掉一个门之后我们那改变选择，肯定选的是正确答案——i
            guess_change.append(i)

        else:
            #当我们猜的门和正确答案一致，主持人随机打开一扇门之后，我们会选择剩下的一扇未被打开的空门
            #继续举栗子：如果我们猜的A门，大奖就在A门，那么真理既然被我们选中，主持人在没有奖的B和C门中随机打开一扇都可以
            #然后问我们是否change，要是B门被打开，那么剩下A（我们第一步选择的）和C门，我们改变立场会转向C门，结果就是大奖飞走了

            anwser_range = [1,2,3]

            #我们选择的就是正确答案，先排除掉（因为最后我们会改变选择）
            anwser_range.remove(i)
            
            #主持人随机打开一个门
            anwser_range.remove(anwser_range[random.randint(0,1)])

            #剩下的一个就是我们最终选择的门
            guess_change.append(anwser_range[0])

    #到这一步，我们对刚才改变选择之后的结果进行汇总
    guess_change = np.array(guess_change)

    #看看猜对了多少轮
    judge = (lst == guess_change)
    
    #正确率是多少
    correct_rate = judge.sum() / len(judge)
    
    print('Bro，这次我们玩%d轮~' % num)
    print('在第二次改变选择的策略下，你最终的中奖率是:%.2f' % (correct_rate * 100))
    


def guess_two_type2(num = 100):
    
    #玩100轮，随机生成100个正确答案
    lst = gen_random(num)
    #先随机盲选，和正确答案数量对应，也是猜100个结果
    guess = np.random.randint(1,4,size = len(lst))
    guess == lst
    #1.如果第一次没有选对，例如大奖藏在A，而我们选的是C，接下来主持人会帮我们排除掉B（打开B门），再询问我们是否坚持最初的选择
    #如果我们改变选择，(排除掉B之后，如果改变选择，只能选C)，则必定会中大奖。
    #这个逻辑进一步延展我们会发现，只要第一次没有选中正确答案，在排除掉一个干扰项之后，我们改变选择，都一定会中奖
    #反之，如果第一次猜中了，后面更改了选择，就一定不会中奖
    #真相就在眼前了！现在已经有了100次的正确答案，我们也随机猜了100次
    #按照我们第二次改变选择的玩法，总结起来就一句话，如果第一次猜对，那不会中奖，如果没有猜对，那改就对了
    #口诀就是：“天对地，左对右，错对对，对对错，TRUE对FALSE，FALSE对TRUE”
    #求最终中标的概率，只需统计我们第一次猜错（FALSE）的次数即可。
    #先和正确答案比对，我们是否猜中
    judge = (lst == guess)

    #judge.sum()得到的是我们第一次就猜对的轮数
    #由于我们第二次会改变选择，所以，最终猜对的轮数，应该是第一次猜错的轮数(轮数 - 第一次猜对的轮数)
    correct_count = num - judge.sum()
    correct_rate = correct_count / len(judge)

    print('Bro，这次我们玩%d轮~' % num)
    print('在第二次改变选择的策略下，你最终的中奖率是:%.2f' % (correct_rate * 100))
    #return correct_rate
