

library(maps)
library(leaflet)
library(dplyr)
library(shiny)


UKCities <- read.csv("C:/Users/didan/Downloads/uk_cities.csv")

Jobs <- read.csv("C:/Users/didan/Downloads/bio-science_jobs.csv")

Jobs <- left_join(Jobs, UKCities, by="city")
View(Jobs)

Jobspercity <- Jobs %>%
  select(city)
  count(city)
  View(Jobspercity)
mytext <- paste(
  "Jobs in this city: ", count(filter(Jobs, city ==~Jobs$city )), sep="") %>%
  lapply(htmltools::HTML)

ui <- fluidPage(
  mainPanel(
    leafletOutput(outputId = "mymap")
  )
)

server <- function(input, output, session) {

  output$mymap <- renderLeaflet({
    
    leaflet(Jobs) %>%
            setView(lng = -2, lat = 53, zoom = 4) %>%
      addTiles() %>%
      addCircleMarkers(~lng, ~lat, 
                       fillColor = blues9, fillOpacity = 0.7, color="white", radius=8, stroke=FALSE,
                       label = mytext,
                       labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto")
      )
  })  
}


shinyApp(ui,server)
