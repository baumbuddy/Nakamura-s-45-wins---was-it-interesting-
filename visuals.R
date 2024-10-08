# import libraries
library(ggplot2)
library(extrafont)

# create custom plotting theme
blue_theme <- function() {
  theme(
    
    # add border 1)
    panel.border = element_rect(colour = "grey20", fill = NA, linetype = "solid"),
    
    # color background 2)
    panel.background = element_rect(fill = "grey99"),
    
    # modify grid 3)
    panel.grid.major.x = element_line(colour = "grey40", linetype = 3, size = 0.2),
    panel.grid.minor.x = element_blank(),
    panel.grid.major.y =  element_line(colour = "grey40", linetype = 3, size = 0.2),
    panel.grid.minor.y = element_blank(),
    
    # modify text, axis and colour 4) and 5)
    axis.text = element_text(color = "grey20", family = "CMU Serif"),
    axis.title = element_text(color = "grey20", family = "CMU Serif"),
    #axis.ticks = element_line(color = "grey20"),
    
    # legend at the bottom 6)
    legend.position = "bottom",
    
    # legend font
    legend.text = element_text(family = "CMU Serif"),
    legend.title = element_text(family = "CMU Serif")
  )
}

# color hues
proj_colors <- c("#dfaae7", "#9a66ba", "#4b2a91", "#81b64c")


#############################################################
####    streak overview of first sim    ####
#############################################################
# import data
data_generous_1sim = read.csv("results/data_generous_1sim.csv")
data_midway_1sim = read.csv("results/data_midway_1sim.csv")
data_sceptic_1sim = read.csv("results/data_sceptic_1sim.csv")
data_chesscom_1sim = read.csv("results/data_chesscom_1sim.csv")

# add tag
data_generous_1sim$tag <- "I"
data_midway_1sim$tag <- "II"
data_sceptic_1sim$tag <- "III"
data_chesscom_1sim$tag <- "IV"


data_sceptic_1sim$streakID <- 1:nrow(data_sceptic_1sim)
data_sceptic_1sim[data_sceptic_1sim$streakCount > 40,] 

# combine data
data_1sim <- rbind.data.frame(
  data_generous_1sim[data_generous_1sim$streakCount > 1, ],
  data_midway_1sim[data_midway_1sim$streakCount > 1, ],
  data_sceptic_1sim[data_sceptic_1sim$streakCount > 1, ],
  data_chesscom_1sim[data_chesscom_1sim$streakCount > 1, ]
)

# streak stats
length(data_1sim$streakCount[data_1sim$tag == "I" & data_1sim$streakCount > 200])

# create figure
ggplot(data = data_1sim, aes(x = tag, y = streakCount, fill = tag)) + 
  geom_point(position = "jitter", shape = 21, color = "grey30") +
  blue_theme() +
  theme(legend.position = "none", panel.grid.major.x = element_blank()) +
  ylab("\nStreak size") +
  xlab("Scenario") +
  scale_y_continuous(breaks = seq(0, 200, 40)) +
  scale_fill_manual(values = proj_colors)
  
ggsave(filename = "1simplot.pdf", plot = last_plot(), device = cairo_pdf, height = 7, width = 15, units = "cm")

#############################################################
####    streak overview of all sim    ####
############################################################
# import data
percentsimul_generous = read.csv("results/percentsimuloutcomes_generous.csv")
percentsimul_midway = read.csv("results/percentsimuloutcomes_midway.csv")
percentsimul_sceptic = read.csv("results/percentsimuloutcomes_sceptic.csv")
percentsimul_chesscom = read.csv("results/percentsimuloutcomes_chesscom.csv")

# combine data
percentsimul = rbind.data.frame(
  percentsimul_generous,
  percentsimul_midway,
  percentsimul_sceptic,
  percentsimul_chesscom
)
percentsimul$Scenario <- percentsimul$scenario

percentsimul$Scenario <- factor(percentsimul$Scenario, levels = unique(percentsimul$Scenario))
# plot
ggplot(data = percentsimul, aes(x = Streak, y = sum, color = Scenario)) +
  geom_vline(xintercept = 45, color = "red", linetype = "dashed") +
  geom_point() +
  geom_line() +
  blue_theme() +
  theme(legend.position = c(1,1),
        legend.justification = c(1,1),
        legend.background=element_blank(),
        legend.box.background = element_rect(),
        legend.title = element_blank()
        ) +
  xlab("x (streak size)") +
  ylab("% of simulations with \nat least one >x-sized streak") + 
  scale_x_continuous(breaks = seq(0, 260, 20), limits = c(0, 260)) +
  scale_color_manual(values = proj_colors, labels = c("Scenario I","Scenario II", "Scenario III", "Scenario IV")) +
  annotate(geom = "text", x = 40, y = 25, color = "red", label ="45-game win streak", angle = 90, size = 3)
  
ggsave(filename = "PctofSimvsStreaks.pdf", plot = last_plot(), device = cairo_pdf, height = 7, width = 15, units = "cm")
