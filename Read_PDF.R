# ================== Title: Function to read PDF files as bitmaps ================== #
ReadPDF <- function(pdf_file_location, page_no){
  library(pdftools)
  library(png)
  library(grid)
  img <- pdf_render_page(pdf_file_location, page = page_no)
  return(grid.raster(img))
}

ReadPDF("1403.2805.pdf", 1)
