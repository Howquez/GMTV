[![Generic badge](https://img.shields.io/badge/Status:-WIP-yellow.svg)](https://shields.io/)
Made with [oTree](https://www.sciencedirect.com/science/article/pii/S2214635016000101) and ❤️

# 🤷‍ Cooperation in uncertain times

This repository contains a dynamic public goods game as well as a public bads game designed to investigate growth under 
uncertainty as well as so called climate clubs respectively.

Even though both experiments are quite different, they share many features and thus, the same architecture. 
More precisely, both experiments are built using [oTree Lite](https://otree.readthedocs.io/en/latest/misc/otreelite.html)
and [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/) together with some simple JavaScript
functions as well as [Highcharts](https://www.highcharts.com/) visualizations.

👉 [Click here](DPGG.md) if you want to learn more about the **dynamic public goods game**.

👉 [Click here](Clubs.md) if you want to learn more about the **public bads game with climate clubs**.

## 🚏 How you can access a demo
You can find the experiment's demo [here](https://labexp.herokuapp.com/demo/). A click on _GMTV_ or _Clubs_
will open a new tab with several URLs. I'd advice you to click on the Hyperlink called _Play in split screen mode._
[![](screenshots/DPGG.png)](https://labexp.herokuapp.com/demo/)


<!--
## ▶️ How to 
To replicate the analysis (once you have the necessary data), you have to follow these steps:

- [ ] Store the data file called `all_aps_wide.csv` in `data/replication/`. The data that is currently stored in that folder is simulated. I left it in there for demo purposes. If you do not have actual data that was generated after June 30th, feel free to contact me.
- [ ] Store the data file called `GMTV-questionnaire-data.dta` in `data/gaechteretal/`. You will have to request the data as it is not included in this repository. This is because the data was not (publicly) provided by Gächter et al. in the first place.
- [ ] Make sure that you do have `data/gaechteretal/GMTV-data.dta`.
- [ ] Open `analysis/analysis.Rproj`, navigate to `analysis/R/source.R` and run that script. It will first run the `config.R` file which loads the required packages. Subsequently, RMarkdown reports (stored in `analysis/reports/rmd/`) will be rendered into HTML and PDF files. If you encounter any problems during the rendering process, [try to restart R](https://github.com/r-lib/callr/issues/102#issuecomment-474453623). Note that the HTML outputs are more convenient to read.
- [ ] You should now find freshly generated reports in `analysis/reports/html/` and `analysis/reports/pdf/`. In addition, you should find processed data in `data/processed/`.

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

-->
