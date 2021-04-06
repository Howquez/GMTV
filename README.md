[![Generic badge](https://img.shields.io/badge/Status:-WIP-yellow.svg)](https://shields.io/)
Made with [oTree](https://www.sciencedirect.com/science/article/pii/S2214635016000101) and ❤️

# 🤷‍ Cooperation in uncertain times


## 🧐 What the project is about
This experiment replicates Gächter et al.'s [(2017, Journal of Public Economics)](https://www.sciencedirect.com/science/article/pii/S0047272717300361)
dynamic public goods game -- the 10-period no punish treatment, to be precise.

The original game is a public goods game where each player's current endowment is the sum of her initial endowment and 
gains or losses from previous periods. Hence, period endowments are incomes of previous periods and both growth as well 
as inequality arise endogenously.

After replicating the experiment [online and remote](https://doi.org/10.1007/s10683-017-9527-2), we want to incorporate 
an exogenous risk of extreme weather events that cause an endogenous damage. The rationale behind that is quite
intuitive: extreme weather events cannot be prevented in the short run but their damage can be controlled -- the more
a society contributes to a public good the lower the damage if an extreme weather event occurs.

## 🚏 How you can access a demo
You can find the experiment's demo [here](https://cliccs.herokuapp.com/demo/). A click on _Dynamic Public Goods Game_ 
will open a new tab with several URLs. I'd advice you to click on the Hyperlink called _Play in split screen mode._
[![](figures/Decision_Screen.png)](https://cliccs.herokuapp.com/demo/)


## ✅ To do
A kanban board can be found [here](https://github.com/Howquez/coopUncertainty/projects/1). 

## 🛠 How we built it
The experiment is built in Python 3 using [oTree](https://www.sciencedirect.com/science/article/pii/S2214635016000101).
So far, one can consider the game as an MVP -- it therefore only contains constant and homogeneous shocks to the 
players' endowments. 

## 📖 Read the Docs
I am creating a wiki over [here](https://github.com/Howquez/coopUncertainty/wiki).