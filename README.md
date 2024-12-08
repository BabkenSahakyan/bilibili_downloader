# video_downloader
Downloading bilibili, TTC (TGC) plus (and not only) videos using youtube4kdownloader API. 

## TTC (TGC)
Extract titles from TTC (TGC) and TTC+ html page:  
$('.AccordionToggle').map((idx, val) => val.innerText)  
Object.assign({}, Array.from(document.querySelectorAll('span.title')).map(el => el.textContent))

> python --version  
Python 3.13.0
