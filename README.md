# RentCity
# Predicting NYC Rent Prices based on Apartment Features
### 
## Background
I recently had to find an apartment in NYC, which is a difficult process compared to most other cities.  High rents, broker fees, and being on the market for only days makes the process extremely difficult.  I decided it would be handy to know if an apartment is fairly priced by being able to predict the rent for an apartment based on features such as nighborhood, sqft, and amenities. 

## Data Collection
All data was scraped from <a href="https://streeteasy.com/for-rent/nyc">streeteasy.com</a>, widely considered the most robust apartment site for NYC. Data was collected June 28, 2019 thru June 30, 2019, on 7400 apartments.

Scraping proved to be extremely difficult for two reasons.  Firstly, the site does not allow headless requests, and it uses javascript.  Python's requests library can handle adding headers, however it can't handle JS pages because it doesnt wait for the JS to load before it collects the HTML.

Selenium proved to do the trick, allowing for the JS to load before completeing the get request.  However, a new problem appeared - CAPTCHA.  I am not a robot, however I wasn't able to figurew out a way around this, so for almost two days I had to reassure the site, and myself, that I am not a robot.

## EDA and Hygien
Total Apartments - 7408<br>
Average Rent - $4028<br>
Most Expensive Rent - $69500<br>
Least Expensive Rent - $950

<img src="rent_hist_lessthan10k.png"><br><br>
<img src="rent_hist_morethan10k.png"><br><br>
<div>
    <a href="https://plot.ly/~carlositoelperro/0/?share_key=rHMpAzpWEl5UfF9bpi1Mcd" target="_blank" title="boro_horz_bar_price_ranked.html" style="display: block; text-align: center;"><img src="https://plot.ly/~carlositoelperro/0.png?share_key=rHMpAzpWEl5UfF9bpi1Mcd" alt="boro_horz_bar_price_ranked.html" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="carlositoelperro:0" sharekey-plotly="rHMpAzpWEl5UfF9bpi1Mcd" src="https://plot.ly/embed.js" async></script>
</div><br><br>
<div>
    <a href="https://plot.ly/~carlositoelperro/4/?share_key=QbmSTqrwvrB3EfyjWxdCxp" target="_blank" title="hood_horz_bar_price_ranked.html" style="display: block; text-align: center;"><img src="https://plot.ly/~carlositoelperro/4.png?share_key=QbmSTqrwvrB3EfyjWxdCxp" alt="hood_horz_bar_price_ranked.html" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="carlositoelperro:4" sharekey-plotly="QbmSTqrwvrB3EfyjWxdCxp" src="https://plot.ly/embed.js" async></script>
</div><br>

I decided to remove outliers, since a 70k apartment should skew the data.  I ran a z-test on the price column and removed any apartments that scored more than a 3 on the z-test. Roughly 100 apartments were removed.  Below is the new histogram with no outliers.<br><br>
<img src="rent_hist_no_outliers.png">

I then removed all unneeded and junk columns, and combined redundant columns.  For example, there was a cats column and a dogs column, I combined them to be a pets colum.  Similarly I combined multiple parking columns.

I then imputed missing sqft values by filling them with the mean of apartments in the same neighborhood and having the same number of bedrooms.

After looking at the data, I believe the price is most closely related to sqft and neighborhood.  The below scatter plot comparing sqft to price, and color coding by borough seems to support this belief.<br>
<div>
    <a href="https://plot.ly/~carlositoelperro/6/?share_key=KsZkKrZSbpsq4cZ8jiHtIp" target="_blank" title="scatter_price_sqft_color_boro.html" style="display: block; text-align: center;"><img src="https://plot.ly/~carlositoelperro/6.png?share_key=KsZkKrZSbpsq4cZ8jiHtIp" alt="scatter_price_sqft_color_boro.html" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="carlositoelperro:6" sharekey-plotly="KsZkKrZSbpsq4cZ8jiHtIp" src="https://plot.ly/embed.js" async></script>
</div>


## Modeling
I started by using Lasso Regression to look for linear relationships.  I chose R2 as my error metric, and Lasso scored just  <b>.70</b> using the default alpha value.

I then decided to try Random Forest Regression, and scored much better right out of the gate, getting an R2 value of <b>.79</b> on the first run.  After adjusting N_estimators to 50, and max_depth to 8, I was able to manage a not great, but not terrible, R2 score of <b>.84</b>.  Random forest looks to be the better fit, probably because there are so many categorical amenities features (almost 200).

As you can see from plotting the residuals using random forest, my model worked much better on apartments priced below $5k.  <br>
<div>
    <a href="https://plot.ly/~carlositoelperro/8/?share_key=Irfd5LaUF9ojUcyVEgbSsq" target="_blank" title="rf_results.html" style="display: block; text-align: center;"><img src="https://plot.ly/~carlositoelperro/8.png?share_key=Irfd5LaUF9ojUcyVEgbSsq" alt="rf_results.html" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="carlositoelperro:8" sharekey-plotly="Irfd5LaUF9ojUcyVEgbSsq" src="https://plot.ly/embed.js" async></script>
</div>


As hypothesized, sqft and location has the most effect on pric, however borough was more important than nieghborhood, which suprised me.  I think we'd need more samples to see if neighborhood has more effect on the price.<br>
<div>
    <a href="https://plot.ly/~carlositoelperro/10/?share_key=yhUFOzx5YbaMQDEwkKJ3la" target="_blank" title="feature_importances.html" style="display: block; text-align: center;"><img src="https://plot.ly/~carlositoelperro/10.png?share_key=yhUFOzx5YbaMQDEwkKJ3la" alt="feature_importances.html" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="carlositoelperro:10" sharekey-plotly="yhUFOzx5YbaMQDEwkKJ3la" src="https://plot.ly/embed.js" async></script>
</div>


## Take Aways
I did well creating plots, doing EDA, and hypothesizing the feature importances.  All of those stages went smoothly and as expected.  I'd also like to rework the model or try new ones to try to get better prediction results.  Also, scraping could be done much more efficiently if I can find a way to get around CAPTCHA.  I am not a robot, but my scraper is.

Most importantly, more work needs to be done on the code to make it more readable and efficient.

