from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    from pandas_datareader import data,wb
    import datetime
    from bokeh.plotting import figure,show,output_file
    from bokeh.models import HoverTool,ColumnDataSource
    from bokeh.embed import components
    from bokeh.resources import CDN
    end=datetime.datetime.now()
    start=datetime.datetime(end.year,end.month-1,1)
    df=data.get_data_yahoo("TSLA",start=start,end=end)

    def status_find(a,b):
        if a>b:
            value='Decrease'
        elif a<b:
            value='Increase'
        else:
            value='Equal'
        return value
    df['Status']=[status_find(a,b) for a,b in zip(df.Open,df.Close)]


    df['Middle']=(df.Open+df.Close)/2

    df['Height']=(abs(df.Open-df.Close))
    hour_12=12*60*60*1000
    def find(ab):
        if ab=='Increase':
            val='#ccffff'
        else:
            val='#ffff33'
        return val
    df['Date']=df.index
    df['index']=[i for i in range(len(df))]
    df.set_index('index',inplace=True)
    df['color']=[find(i) for i in df.Status]
    df['st']=df['Date'].dt.strftime("%Y-%m-%d")
    cds=ColumnDataSource(df)
    f=figure(x_axis_type='datetime',width=1000,height=300,title="TESLA STOCK EXCHANGE CHART",sizing_mode='scale_width')
    f.grid.grid_line_alpha=0.5
    f.title.text_color="red"
    f.title.text_font="arial"
    f.title.text_font_style="bold"
    f.xaxis.axis_label="DATE"
    f.yaxis.axis_label="SENSEX"
    f.xaxis.axis_label_text_color="blue"
    f.yaxis.axis_label_text_color="blue"
    f.xaxis.axis_label_text_font_style="bold"
    f.yaxis.axis_label_text_font_style="bold"
    f.segment('Date','High','Date','Low',color='black',source=cds)
    f.rect('Date','Middle',hour_12,'Height',fill_color='color',line_color='black',source=cds)
    hover=HoverTool(tooltips=[('status','@Status'),('Date','@st')])
    f.add_tools(hover)

    #output_file("templates/stock.html")
    #show(f)
    source1,div1=components(f)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files
    return render(request,'plot.html',
    {'script1':source1,
    'div1':div1,
    'cdn_js':cdn_js})
    
