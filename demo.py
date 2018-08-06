from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    from datetime import datetime
    from bokeh.plotting import figure, show, output_file
    import pandas as pd
    pd.core.common.is_list_like = pd.api.types.is_list_like
    from pandas_datareader import data as pdr
    import fix_yahoo_finance as yf 
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime(2016, 1, 1)
    #print(start)
    end = datetime(2018, 8, 1) 

    yf.pdr_override()  

    df = pdr.get_data_yahoo(tickers="TSLA", start=start, end=end)

    def inc_dec(open_prise, close_prise):
        if close_prise > open_prise:
            return "Increase"
        elif open_prise > close_prise:
            return "Decrease"
        else:
            return "Equal"
        
    df["Status"] = [inc_dec(o, c) for o, c in zip(df.Open, df.Close)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Open - df.Close)

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p.title.text = "Candlestick Chart"
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000
    p.segment(df.index, df.High, df.index, df.Low)

    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
        hours_12, df.Height[df.Status == "Increase"], fill_color="#CCFFFF", line_color="black")
    p.rect(df.index[df.Status == "Equal"], df.Middle[df.Status == "Equal"],
        hours_12, df.Height[df.Status == "Equal"], fill_color="#CCFFFF", line_color="black")
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
        hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF3333", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    return render_template("plot.html", script1=script1,
                            div1=div1, cdn_js=cdn_js, cdn_css=cdn_css)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
    