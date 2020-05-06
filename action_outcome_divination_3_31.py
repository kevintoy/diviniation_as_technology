# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:06:38 2020

@author: kevin
"""

import matplotlib.pyplot as plt
import random
import numpy as np
n=1000
a=1 #prior beliefs
b=1 #prior beliefs

z=100 #benefit of performing action if action yields positive results
c=1 #perceived cost of performing the action 

r=0.2#determines the relative amount of positive outcome
prob_freq=0.9 #probablity that "problem event" occurs during individual's lifetime (determines the amount of action)

unknown_rate=0.3 #in food taboo related false belief, should always be 0
subset_rate=0.1


wo_pos=1
wo_neg=1
wa=0.1#weight of action
w_noa=0.1 #weight of inaction
wp=10 #weight of personal experiences

npe=1 #number of "problem event"
neg_under=0.0 #percent of negative instances missed.
#note: even when neg_under is 0.9, meaning 90% of the negative instance is missed, when r=0.1 the mean belief
#is still 0.5. (0.1 vs. 0.9*0.9). This suggests that when true frequency r is small, negative under-reporting isn't much of a problem. 
#and the associated weight doesn't matter much

generation=20
def mean_belief(i):
    return i[0]/float(i[0]+i[1])


#create the initial population
pop=[]
for i in range(n):
    pop.append([a,b]) #each individual is a beta distribution with initial parameter a,b

#if a problem event occurs, each agent "act" if expected benefit is larger than cost
for gen in range(generation):

    action_pop=[]
    for i in pop:
        if prob_freq>random.random(): #if problem event occurs:
            #add some uncertainty regarding subjective perception of cost/benefit 
            z_uncertain=np.random.normal(loc=z,scale=5,size=None)
            c_uncertain=np.random.normal(loc=c,scale=5,size=None)
            if mean_belief(i)*z_uncertain>c_uncertain: #expected benefit larger than cost, action happens
                #in the case of food-taboo related false belief, this means very few individuals with perform the action
                
                
                if r>random.random():#positive outcome, rabbit meat indeed followed by deformed baby
                    action_pop.append(1)
                else:
                    action_pop.append(0) #negative outcome
            else: #expected benefit smaller than cost, no action (here means act in accordance with the transmitted belief)
                action_pop.append("no_action")
        else: #problem event doesn't occur
            pass
    #create a new list, randomly changing a portion action with outcomes into "unknown_outcome" (this means someone consumed rabbit meat but people weren't aware of the outcome)
    indx=0
    for i in action_pop:
        if i!="no_action": #if i is not "no_action"
            if unknown_rate>random.random(): #with propability,
                action_pop[indx]=-1 # -1 means action but unknown outcome
        indx=indx+1
    #under-reporting of negative evidence
    indx1=0
    for i in action_pop:
        if i==0: #if the outcome is negative (means someone consumed rabbit meat but had a healthy baby)
            if neg_under>random.random():
                action_pop[indx1]="under reported negative instance"
        indx1=indx1+1
    
    
    
    #create offspring generation
    pop_offspring=[]
    for i in range(n):
        pop_offspring.append([a,b])
    
    #now agent in the offspring generation starts to acquire their belief
    indx2=0
    for i in pop_offspring:
        #each naive offspring experiences a proportion of the total "action_pop".
        #this means need to construct a subset of the total "action_pop"
        action_subset=random.choices(action_pop,k=int(len(action_pop)*subset_rate))
        pop_offspring[indx2][0]=a+pop_offspring[indx2][0]+wo_pos*action_subset.count(1)+wa*action_subset.count(-1)
        pop_offspring[indx2][1]=b+pop_offspring[indx2][1]+wo_neg*action_subset.count(0)+w_noa*action_subset.count("no_action")
        
        #now agents "personallly experience" the action probabalistically
        for times in range(npe):
            #fun fact: if npe is too large, the first few negative experience may
            #drastically decrease agents belief and thus leads to inaction.
            #because they don't act anymore, they have not chance to update their belief.
            #their belief thus remains low.(close to zero)
            if prob_freq>random.random(): #problem event happened
                

                if mean_belief(i)*np.random.normal(loc=z,scale=5,size=None)>np.random.normal(loc=c,scale=5,size=None): #add uncertainty in benefit and cost perception
                    if r>random.random(): #positive outcome

                        pop_offspring[indx2][0]=pop_offspring[indx2][0]+wp
                        
                    else:
                        pop_offspring[indx2][1]=pop_offspring[indx2][1]+wp
                        
                else: #agent doesn't personally experience (action too costly)
                    pass
            else: #problem event doesn't occur
                pass
        indx2=indx2+1
    print (np.array(pop_offspring).mean(axis=0))
    if action_pop!=[]:
        print ("action_rate=", (len(action_pop)-action_pop.count("no_action"))/len(action_pop))
    else: 
        print ("no action")
    pop=pop_offspring
    
#create a list with mean beliefs values for individuals in pop

mean_belief_list=[]
for j in pop:
    mean_belief_list.append(mean_belief(j))
plt.style.use('ggplot')
plt.hist(mean_belief_list, bins = 100, range=(0,1))
plt.ylim(0,130)
plt.savefig("ind belief distribution.png", dpi=300)
#plt.title("distribution of belief p")
plt.axvline(x=r,color='k', linestyle='--')
plt.ylabel("Frequency")
#plt.text(0.9, 0, str((len(action_pop)-action_pop.count("no_action"))/len(action_pop))) #print action_rate on graph


print("mean=",np.array(pop_offspring).mean(axis=0)[0]/(np.array(pop_offspring).mean(axis=0)[0]+np.array(pop_offspring).mean(axis=0)[1]))
print("variance=",np.var(mean_belief_list))

#when high weight is placed on personal experience and personal experience is rare, people have a tendency to polerize (because some people will
#get positive evidence by chance)
#weight of action is pretty important. If people take "simply because other people are doing it, it must be effective,
#then the efficacy will be over-estimated

his_theta0=mean_belief_list
his_theta03=mean_belief_list
his_theta06=mean_belief_list

plt.hist(his_theta0, bins = 100, range=(0,1), label=r'$w_o$ = 0.1', alpha=0.8)
plt.hist(his_theta03, bins = 100, range=(0,1),label=r'$w_o$ = 0.5', alpha=0.8)
plt.hist(his_theta06, bins = 100, range=(0,1),label=r'$w_o$ = 1.0', alpha=0.8)
plt.axvline(x=r,color='k', linestyle='--')
plt.legend(loc="best")
plt.xlabel(r'individual mean belief $\bar{p}$', fontsize=14)
plt.ylabel("Frequency")
plt.style.use('ggplot')
plt.show()



#create a plot for the relationship betweeen belief and action
def func(c_over_b,p):
    if p<c_over_b:
        return 0
    else:
        return 1

vfunc=np.vectorize(func)

p=np.linspace(0,1,1000)
y=vfunc(0.01,p)
plt.yticks(np.arange(2),['0 (no action)', '1 (action)'],rotation=90)
plt.plot(p,y,"-",linewidth=1,ls=" ",ms=1, marker=".")
plt.xlim(-0.1,1)
plt.ylim(-0.1,1.1)
plt.xlabel(r"$\bar{p}$" " (belief)")
plt.ylabel(r"$f (\bar{p})$" " (Action decision)")
plt.axvline(x=0.01,color='k', linestyle='--', linewidth=0.5)
plt.text(0.02, 0.1, r'$\frac{c}{b}=0.01$', fontsize=20)
plt.style.use('classic')
plt.show()

