"""Original schematic climate transformation figures; Python standard library only.
All temperatures and sequences are synthetic, not observed or projected data.
"""
from pathlib import Path
from html import escape
import math
OUT=Path(__file__).parent
BLUE, ORANGE, GREY = '#176b91', '#b34f16', '#697581'

def text(x,y,value,size=19,colour='#263746',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{colour}" text-anchor="{anchor}">{escape(value)}</text>'

def line(x1,y1,x2,y2,colour=GREY,dash='',width=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}" stroke-dasharray="{dash}"/>'

def box(x,y,w,h,fill='#f1f6f9'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#bdcbd5"/>'

def save(name,title,content,note,height=440,plain=False):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" role="img"><title>{escape(title)}</title><desc>{escape(note)}</desc><rect width="1000" height="{height}" fill="white"/><g font-family="Arial, sans-serif">'
    svg+=content if plain else text(26,34,title,25)+content+text(500,height-40,note,18,anchor='middle')+text(500,height-14,'Illustrative only: synthetic data and selected assumptions',16,GREY,'middle')
    (OUT/f'transformation_{name}.svg').write_text(svg+'</g></svg>\n',encoding='utf-8')

def plot(x,title,series,labels=('Day 1','Day 20'),ylim=(6,18)):
    left,top,w,h=x+40,110,360,155
    yy=lambda v:top+h-(v-ylim[0])/(ylim[1]-ylim[0])*h
    out=text(x,77,title,21)+text(left,101,'Temperature (°C)',16)
    out+=line(left,top,left,top+h)+line(left,top+h,left+w,top+h)
    for val in (ylim[0],sum(ylim)/2,ylim[1]):out+=text(left-9,yy(val)+5,f'{val:g}',16,anchor='end')
    out+=text(left,292,labels[0],17)+text(left+w,292,labels[1],17,anchor='end')
    for i,(name,values,colour,dash) in enumerate(series):
        pts=' '.join(f'{left+j/(len(values)-1)*w:.1f},{yy(v):.1f}' for j,v in enumerate(values))
        out+=f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="3" stroke-dasharray="{dash}"/>'
        y=324+i*27
        out+=line(x+40,y-6,x+70,y-6,colour,dash,3)+text(x+80,y,name,18)
    return out

def summary(x,title,items,calculation):
    out=text(x,77,title,21)
    for i,(label,value,colour) in enumerate(items):
        y=113+i*85
        out+=box(x+20,y,385,70)+text(x+38,y+28,label,19,colour)+text(x+38,y+55,value,22,colour)
    return out+text(x+212,330,calculation,23,ORANGE,'middle')

def main():
    fluctuations=[.8,-.3,.4,-1.1,.2,1.3,-.5,.5,-.8,.1,1,-.4,.6,-.6,.2,1.2,-.7,.3,-.2,.7]
    m=sum(fluctuations)/len(fluctuations)
    fluctuations=[v-m for v in fluctuations]
    base=[10+v for v in fluctuations]
    # Blue denotes source/input values; orange denotes a calculated result.
    content=box(35,85,260,95)+text(165,121,'Existing dataset',23,BLUE,'middle')+text(165,153,'10, 12, 9, ...',22,BLUE,'middle')
    content+=text(325,142,'→',34)+box(380,85,240,95)+text(500,123,'No further',23,anchor='middle')+text(500,153,'transformation',23,anchor='middle')
    content+=text(654,142,'→',34)+box(710,85,255,95)+text(837,121,'Next model / analysis',21,anchor='middle')+text(837,153,'10, 12, 9, ...',22,BLUE,'middle')
    save('direct','Direct use: pass the same dataset to the next step',content,'The input may already have been processed.',270)

    years=list(range(1981,2081))
    deviations=[.55*math.sin(i*2.15)+.3*math.cos(i*.79) for i in range(100)]
    hist_mean=sum(deviations[:30])/30
    simulation=[12+v-hist_mean+max(0,i-29)*.045 for i,v in enumerate(deviations)]
    ref_deviations=[.6*math.sin(i*1.77)+.25*math.cos(i*.61) for i in range(30)]
    ref_mean=sum(ref_deviations)/30
    reference=[10+v-ref_mean for v in ref_deviations]
    corrected=[v-2 for v in simulation]
    xx=lambda year:85+(year-1981)/99*855
    yy=lambda value:310-(value-8)/10*205
    content=f'<rect x="85" y="105" width="{xx(2010.5)-85}" height="205" fill="#edf3f7"/>'
    for value in [8,10,12,14,16,18]:
        content+=line(85,yy(value),940,yy(value),'#e0e6eb',width=1)+text(70,yy(value)+6,str(value),18,anchor='end')
    content+=line(85,105,85,310)+line(85,310,940,310)
    for values,colour,dash,width in [(simulation,BLUE,'',2.5),(corrected,ORANGE,'',2.5),(reference,'#263746','',2.5)]:
        pts=' '.join(f'{xx(1981+i):.1f},{yy(v):.1f}' for i,v in enumerate(values))
        content+=f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-dasharray="{dash}"/>'
    for value,col in [(12,BLUE),(10,'#263746')]:content+=line(85,yy(value),xx(2010),yy(value),col,'6 4',1.8)
    content+=text((85+xx(2010))/2,128,'Reference period',18,anchor='middle')
    content+=text(940,85,'Mean adjustment',20,anchor='end')
    # Show the difference between period means, not paired historical events.
    x=xx(2013)
    content+=line(x,yy(12),x,yy(10),GREY,width=2)
    for value in [10,12]:content+=line(x-5,yy(value),x+5,yy(value),GREY)
    content+=text(x+12,yy(11)+6,'\u22122\u00b0C',20)
    for year in [1981,2000,2020,2040,2060,2080]:content+=text(xx(year),340,str(year),18,anchor='middle')
    content+=text(500,375,'Year',20,anchor='middle')+text(85,85,'Annual mean temperature (\u00b0C)',20)
    for x,y,label,col in [(85,27,'Reference observations','#263746'),(540,27,'Unadjusted simulation',BLUE),(540,57,'Adjusted simulation',ORANGE)]:
        content+=line(x,y-6,x+35,y-6,col,width=3)+text(x+47,y,label,19)
    save('bias','Bias adjustment',content,'Mean adjustment estimated over the reference period and applied to the simulated series.',height=395,plain=True)

    # Model-derived period change applied to the historical baseline, in future years.
    annual_fluctuations=[fluctuations[i%len(fluctuations)] for i in range(30)]
    annual_mean=sum(annual_fluctuations)/30
    annual_baseline=[10+v-annual_mean for v in annual_fluctuations]
    years=list(range(1991,2066))
    simulated=[12+(year-2005.5)*2/45+.35*math.sin(i*2.03) for i,year in enumerate(years)]
    # Centre the simulated reference and future periods at the labelled means.
    for start,target in [(0,12),(45,14)]:
        correction=target-sum(simulated[start:start+30])/30
        for j in range(start,start+30):simulated[j]+=correction
    xx=lambda year:85+(year-1991)/74*855
    yy=lambda value:315-(value-7)/10*210
    content=''
    for start,end in [(1991,2020),(2036,2065)]:
        content+=f'<rect x="{xx(start)}" y="105" width="{xx(end)-xx(start)}" height="210" fill="#f2f6f9"/>'
    for value in [8,10,12,14,16]:
        content+=line(85,yy(value),940,yy(value),'#e0e6eb',width=1)+text(70,yy(value)+6,str(value),18,anchor='end')
    content+=line(85,105,85,315)+line(85,315,940,315)
    for yrs,vals,col in [(years,simulated,BLUE),(range(1991,2021),annual_baseline,'#263746'),(range(2036,2066),[v+2 for v in annual_baseline],ORANGE)]:
        pts=' '.join(f'{xx(year):.1f},{yy(v):.1f}' for year,v in zip(yrs,vals))
        content+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.7"/>'
    for start,end,value in [(1991,2020,12),(2036,2065,14)]:content+=line(xx(start),yy(value),xx(end),yy(value),BLUE,'7 5',2)
    content+=text(940,85,'Delta = 14 \u2212 12 = +2\u00b0C',21,ORANGE,'end')
    # Show how corresponding baseline values move into the future period.
    content+=f'<defs><marker id="delta-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{ORANGE}"/></marker></defs><path d="M {xx(2018)} {yy(9)} Q {xx(2029)} {yy(8.8)} {xx(2038)} {yy(11)}" fill="none" stroke="{ORANGE}" stroke-width="2.5" marker-end="url(#delta-arrow)"/>'

    for year in [1991,2000,2020,2036,2050,2065]:content+=text(xx(year),345,str(year),18,anchor='middle')
    content+=text(500,380,'Year',20,anchor='middle')+text(85,85,'Annual mean temperature (\u00b0C)',20)
    for x,y,label,col,dash in [(85,27,'Climate simulation',BLUE,''),(540,27,'Historical baseline','#263746',''),(85,57,'Simulated period means',BLUE,'7 5'),(540,57,'Future scenario: baseline +2\u00b0C',ORANGE,'')]:
        content+=line(x,y-6,x+35,y-6,col,dash,3)+text(x+47,y,label,19)
    save('delta','Delta method',content,'Simulated period changes applied to a baseline to construct a future scenario.',height=400,plain=True)

    # Original one-panel design: full record, selected period and their means.
    years=list(range(1961,2021))
    temperatures=[8.5+.025*i+.55*math.sin(i*2.1)+.35*math.cos(i*.83)+.18*math.sin(i*4.7) for i in range(60)]
    retained_start=1991
    whole_mean=sum(temperatures)/len(temperatures)
    retained_mean=sum(temperatures[30:])/30
    xx=lambda year:85+(year-1961)/59*855
    yy=lambda value:305-(value-7.5)/4*205
    content=f'<rect x="{xx(1990.5)}" y="100" width="{940-xx(1990.5)}" height="205" fill="#edf5fa"/>'
    for value in [8,9,10,11]:
        content+=line(85,yy(value),940,yy(value),'#e0e6eb',width=1)+text(70,yy(value)+6,str(value),18,anchor='end')
    content+=line(85,100,85,305)+line(85,305,940,305)
    for first,last,col in [(0,60,'#9ba5ad'),(30,60,BLUE)]:
        pts=' '.join(f'{xx(years[i]):.1f},{yy(temperatures[i]):.1f}' for i in range(first,last))
        content+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"/>'
    content+=line(85,yy(whole_mean),940,yy(whole_mean),GREY,'8 5',2)
    content+=line(xx(1991),yy(retained_mean),940,yy(retained_mean),ORANGE,'',3)
    content+=line(xx(1990.5),100,xx(1990.5),305,'#9eb3c0','4 5',1)
    for year in [1961,1970,1980,1990,2000,2010,2020]:content+=text(xx(year),335,str(year),18,anchor='middle')
    content+=text(85,84,'Annual mean temperature (\u00b0C)',20)
    content+=text(500,370,'Year',20,anchor='middle')
    for x,y,label,col,dash in [(85,27,'Full record: 1961-2020','#9ba5ad',''),(540,27,'Retained baseline: 1991-2020',BLUE,''),(85,57,'Full-record mean',GREY,'8 5'),(540,57,'Retained-period mean',ORANGE,'')]:
        content+=line(x,y-6,x+35,y-6,col,dash,3)+text(x+47,y,label,19)
    save('reduction','Reduction of a baseline record',content,'Full and retained records with their respective averages.',height=390,plain=True)

    trend=[9+.1*i for i in range(30)]
    raw=[v+fluctuations[i%len(fluctuations)] for i,v in enumerate(trend)]
    adjusted=[v+.1*(29-i) for i,v in enumerate(raw)]
    xx=lambda year:85+(year-1991)/29*855
    yy=lambda value:300-(value-7)/7*200
    content=''
    for value in [7,9,11,13]:
        content+=line(85,yy(value),940,yy(value),'#e0e6eb',width=1)+text(70,yy(value)+6,str(value),18,anchor='end')
    content+=line(85,100,85,300)+line(85,300,940,300)
    for values,col,dash,width in [(raw,BLUE,'',3),(adjusted,ORANGE,'',3),(trend,BLUE,'7 5',2),([11.9]*30,ORANGE,'7 5',2)]:
        pts=' '.join(f'{xx(1991+i):.1f},{yy(v):.1f}' for i,v in enumerate(values))
        content+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{width}" stroke-dasharray="{dash}"/>'
    for year in [1991,1995,2000,2005,2010,2015,2020]:content+=text(xx(year),330,str(year),18,anchor='middle')
    content+=text(500,365,'Year',20,anchor='middle')
    content+=text(85,85,'Annual mean temperature (\u00b0C)',20)
    for x,y,label,col,dash in [(85,27,'Original baseline',BLUE,''),(540,27,'Adjusted baseline',ORANGE,''),(85,57,'Selected baseline trend',BLUE,'7 5'),(540,57,'Reference level at 2020',ORANGE,'7 5')]:
        content+=line(x,y-6,x+35,y-6,col,dash,3)+text(x+47,y,label,19)
    save('adjustment','Trend adjustment',content,'Original and adjusted baselines with the selected trend and reference level.',height=390,plain=True)

    # A shared timeline makes explicit a 30-year shift and a linear-trend assumption.
    content=text(75,85,'Assumed trend: +0.1\u00b0C/year; corresponding years shifted forward by 30 years',21)
    xx=lambda year:80+(year-1991)/59*830
    yy=lambda value:285-(value-6)/10*165
    content+=text(80,109,'Temperature (°C)',16)+line(80,285,910,285)
    for val in [6,11,16]:content+=text(67,yy(val)+5,str(val),16,anchor='end')
    content+=f'<rect x="{xx(2020.5)}" y="115" width="{910-xx(2020.5)}" height="170" fill="#fff5ec"/>'
    for yrs,vals,col,dash in [(range(1991,2021),raw,BLUE,''),(range(2021,2051),[v+3 for v in raw],ORANGE,'')]:
        pts=' '.join(f'{xx(y):.1f},{yy(v):.1f}' for y,v in zip(yrs,vals))
        content+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="{dash}"/>'
    content+=line(xx(1991),yy(9),xx(2020),yy(11.9),GREY,'6 4')+line(xx(2021),yy(12),xx(2050),yy(14.9),GREY,'6 4')
    for year in [1991,2000,2010,2020,2021,2030,2040,2050]:
        anchor='end' if year==2020 else 'start' if year==2021 else 'middle'
        offset=-8 if year==2020 else 8 if year==2021 else 0
        content+=text(xx(year)+offset,310,str(year),17,anchor=anchor)
    content+=text(285,342,'Baseline sequence',21,BLUE,'middle')+text(710,342,'Reused sequence +3°C',21,ORANGE,'middle')
    content+=text(500,373,'Dashed line: selected trend and its extrapolation',18,GREY,'middle')
    save('extension','Extension: extrapolate a trend and reuse the baseline fluctuations',content,'A conditional construction, not a forecast of future weather or abrupt changes.',height=395,plain=True)

    def grid(x,y,n):
        out=''
        palette=['#e1eef4','#b8d6e4','#80b4ce','#488eaf']
        for r in range(n):
            for c in range(n):
                u,v=(c+.5)/n,(r+.5)/n
                level=min(3,int(4*(.6*u+.4*v)))
                out+=f'<rect x="{x+c*180/n}" y="{y+r*180/n}" width="{180/n}" height="{180/n}" fill="{palette[level]}" stroke="white" stroke-width=".8"/>'
        return out
    content=text(35,83,'Coarse Grid',22)+grid(35,130,3)
    content+=box(315,100,365,105)+text(330,130,'Statistical downscaling',22)+text(330,158,'Historical relationships',19)+text(330,184,'+ local reference observations',19)
    content+=box(315,230,365,105)+text(330,260,'Dynamical downscaling',22)+text(330,288,'Regional climate model',19)+text(330,314,'+ driving boundary conditions',19)
    for y in [153,282]:content+=line(235,220,285,y)+text(285,y+7,'→',28)+line(690,y,755,220)+text(747,227,'→',28)
    content+=text(780,83,'Finer grid',22)+grid(780,130,9)
    save('downscaling','Downscaling: two routes to finer-scale climate information',content,'Grid shading is schematic; finer resolution alone does not establish greater accuracy.',height=355,plain=True)

if __name__=='__main__':main()
