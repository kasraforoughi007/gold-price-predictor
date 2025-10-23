from django.shortcuts import render 
from django.urls import path



def gold_price_view(request):
    grafana_iframe = """
<iframe src="http://localhost:3000/d-solo/null?orgId=1&from=1738333334959&to=1767307842775&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
"""

    return render(request , 'gold-price.html' , {
	'grafana_iframe': grafana_iframe
    })
