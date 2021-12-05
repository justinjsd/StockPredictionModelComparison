>  **Methods and Techniques**

To see an indepth analysis of the methids and techniques used, click [here](https://docs.google.com/document/d/1WPYepVnIwnMPbQzC_hk2XCCSrdM4Hfqvo9R2DV06Hgo/edit?usp=sharing).

The Stock Price Predictor uses three models of Prediction to both analyse stock and determine the best possible model through the RMSE value. The models used were:

**1. LSTM**

**2. BI-LSTM**

**3. ARIMA**

We were able to plot the predicted stock graph against the actual price and were able to make conclusive results based on the Error values and resultant Graph.
 
data = pd.read_csv("GOOG1.csv")
 
This section of the code used pandas to read through the .csv file and extract important information from GOOG1.csv which is the main Dataset being used.


![Screenshot 2021-12-05 174922](https://user-images.githubusercontent.com/94802791/144749212-1e414639-2f98-4c44-99ff-d1b5b2315cd1.jpg)

In the above figure, we have LSTM model contained 9 layers  and is trained for 20 epochs.

![Screenshot 2021-12-05 175205](https://user-images.githubusercontent.com/94802791/144749359-d92de924-299f-4813-acc8-446ae20c1dd0.jpg)

In the above figure, we have a BI-LSTM model with 9 layers and is trained for 20 epochs.

![Screenshot 2021-12-05 175246](https://user-images.githubusercontent.com/94802791/144749430-4f1e6fdc-b84e-4437-b04b-05ec1980a795.jpg)

Here we have used a pre-trained ARIMA model to build our own prediction model.
