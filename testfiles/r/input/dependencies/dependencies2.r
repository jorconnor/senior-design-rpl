#MIT License
#
#Copyright (c) 2017 Todd Schneider
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

boroughs = c("Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island")
yellow_hex = "#f7b731"
green_hex = "#3f9e4d"
uber_hex = "#222222"

if (all(c("Open Sans", "PT Sans") %in% fonts())) {
  font_family = "Open Sans"
  title_font_family = "PT Sans"
} else {
  font_family = "Arial"
  title_font_family = "Arial"
}

con = dbConnect(dbDriver("PostgreSQL"), dbname = "nyc-taxi-data", host = "localhost")
query = function(sql) { fetch(dbSendQuery(con, sql), n = 1e8) }

add_credits = function(fontsize = 12, color = "#777777", xpos = 0.99) {
  grid.text("toddwschneider.com",
            x = xpos,
            y = 0.02,
            just = "right",
            gp = gpar(fontsize = fontsize, col = color, fontfamily = font_family))
}

title_with_subtitle = function(title, subtitle = "") {
  ggtitle(bquote(atop(bold(.(title)), atop(.(subtitle)))))
}

to_slug = function(string) {
  gsub("-", "_", gsub(" ", "_", tolower(string)))
}

theme_tws = function(base_size = 12) {
  bg_color = "#f4f4f4"
  bg_rect = element_rect(fill = bg_color, color = bg_color)

  theme_bw(base_size) +
    theme(text = element_text(family = font_family),
          plot.title = element_text(family = title_font_family),
          plot.background = bg_rect,
          panel.background = bg_rect,
          legend.background = bg_rect,
          panel.grid.major = element_line(colour = "grey80", size = 0.25),
          panel.grid.minor = element_line(colour = "grey80", size = 0.25),
          legend.key.width = unit(1.5, "line"),
          legend.key = element_blank())
}

theme_dark_map = function(base_size = 12) {
  theme_bw(base_size) +
    theme(text = element_text(family = font_family, color = "#ffffff"),
          rect = element_rect(fill = "#000000", color = "#000000"),
          plot.background = element_rect(fill = "#000000", color = "#000000"),
          panel.background = element_rect(fill = "#000000", color = "#000000"),
          plot.title = element_text(family = title_font_family),
          panel.grid = element_blank(),
          panel.border = element_blank(),
          axis.text = element_blank(),
          axis.title = element_blank(),
          axis.ticks = element_blank())
}

theme_tws_map = function(...) {
  theme_tws(...) +
    theme(panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.border = element_blank(),
          axis.text = element_blank(),
          axis.title = element_blank(),
          axis.ticks.length = unit(0, "cm"),
          plot.margin = unit(c(1, 1, 1, 0.5), "lines"))
}

nta_display_name = function(ntacode) {
  c(BK33 = "Carroll Gardens-Red Hook",
    BK38 = "DUMBO-Downtown-Boerum Hill",
    BK73 = "Williamsburg",
    MN03 = "Central Harlem North",
    MN13 = "Chelsea-Flatiron-Union Square",
    MN17 = "Midtown",
    MN24 = "SoHo-TriBeCa-Little Italy",
    MN25 = "Battery Park-Lower Manhattan",
    MN40 = "Upper East Side",
    MN50 = "Stuyvesant Town",
    QN31 = "Hunters Point-Sunnyside",
    QN68 = "Long Island City")[ntacode]
}
