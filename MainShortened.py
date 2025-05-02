{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9076e62a-a37f-40a4-ba31-6c9febc50e17",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "data= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/CleanDATA.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f0e545e4-cf21-4af1-85dc-bd1d89e1f175",
   "metadata": {},
   "outputs": [],
   "source": [
    "ML=data[data['Location']== 'Malden']\n",
    "EV=data[data['Location']== 'Everett']\n",
    "CH=data[data['Location']== 'Charlestown']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e5938de8-bc67-4a58-bf01-f6decad6ebc1",
   "metadata": {},
   "outputs": [],
   "source": [
    "CH.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "52a996e1-624e-488d-917d-227f4d03459b",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import random\n",
    "\n",
    "def plot_boxplot_with_mean(data, y_column, box_color, mean_color):\n",
    "    plt.figure(figsize=(6, 6))\n",
    "    sns.boxplot(data=data, y=y_column, color= box_color,linewidth=2.5, showfliers=False)\n",
    "\n",
    "    # Calculate the mean value of the selected column\n",
    "    mean_value = data[y_column].mean()\n",
    "\n",
    "    # Overlay the mean on the boxplot\n",
    "    plt.scatter(0, mean_value, color=mean_color, label=f'Mean', zorder=10)\n",
    "\n",
    "    # Add the legend and show the plot\n",
    "    plt.legend()\n",
    "    plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/CH_winter_plot.png')\n",
    "    plt.show()\n",
    "\n",
    "# Example usage:\n",
    "plot_boxplot_with_mean(winter_CH, y_column=\"UFP Concentration\",  box_color='blue', mean_color='lavender')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f297003e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd \n",
    "\n",
    "Dy_1100= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/CH_1100_clean_hourly.csv')\n",
    "Dy_counts = Dy_1100.copy()\n",
    "Dy_counts['DateTime'] = pd.to_datetime(Dy_counts['DateTime'], format=\"%m/%d/%y %H:%M\", errors='coerce')\n",
    "Dy_counts['DateTime'] = Dy_counts['DateTime'].dt.strftime(\"%m/%d/%y %H:%M\")\n",
    "Dy_counts= Dy_counts[['DateTime', 'Small (#/cm^3)', 'Large (#/cm^3)']]\n",
    "Dy_counts.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7f91a1fc",
   "metadata": {},
   "outputs": [],
   "source": [
    "p_1700= '/Users/camillegimilaro/Desktop/Temp/Cleaned Data/CH_1700_clean_hour_with_high_values.csv'\n",
    "Dy_1700= pd.read_csv(p_1700, names=['DateTime', 'PM 2.5', 'PM 10'], skiprows=1)\n",
    "dy_1700 = Dy_1700.copy()\n",
    "dy_1700['DateTime'] = pd.to_datetime(dy_1700['DateTime'], format=\"%m/%d/%y %H:%M\")\n",
    "dy_1700['DateTime'] = dy_1700['DateTime'].dt.strftime(\"%m/%d/%y %H:%M\")\n",
    "dy_1700.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8d43aa66",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(Dy_counts.tail())\n",
    "print(dy_1700.tail())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "82569d5a",
   "metadata": {},
   "outputs": [],
   "source": [
    "dylos= pd.merge(Dy_counts, dy_1700, on= 'DateTime', how= 'outer')\n",
    "print(dylos.head())\n",
    "dylos.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "860563a3",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "CPC_path= '/Users/camillegimilaro/Desktop/Temp/Cleaned Data/CH_hourly_CPC_nofatalerrors_above300.DAT'\n",
    "CPC = pd.read_csv(CPC_path,names=['DateTime', 'UFP Concentration'] )\n",
    "CPC['DateTime'] = pd.to_datetime(CPC['DateTime'], format=\"%m/%d/%Y %H:%M\")\n",
    "CPC['DateTime'] = CPC['DateTime'].dt.strftime(\"%m/%d/%y %H:%M\")\n",
    "print(CPC.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "71cc4885",
   "metadata": {},
   "outputs": [],
   "source": [
    "All_size= pd.merge(dylos, CPC, on= \"DateTime\", how= \"outer\")\n",
    "print(All_size.head())\n",
    "All_size.shape\n",
    "complete_data= All_size.dropna()\n",
    "QA_complete = complete_data.loc[~((complete_data.select_dtypes(include=['float']) == 0).any(axis=1))]\n",
    "QA_complete.head()\n",
    "print('Whole data shape:', All_size.shape)\n",
    "print('Dropped NaN shape:', complete_data.shape)\n",
    "print('QAd data shape:',QA_complete.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2263f03f",
   "metadata": {},
   "outputs": [],
   "source": [
    "weather_path= r'/Users/camillegimilaro/Desktop/Temp/Cleaned Data/noaabackfill.csv'\n",
    "weather= pd.read_csv(weather_path)\n",
    "weather['DateTime'] = pd.to_datetime(weather['DateTime'], errors='coerce')\n",
    "weather['DateTime']= weather['DateTime'].dt.strftime(\"%m/%d/%y %H:%M\")\n",
    "print(weather.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "69aa653d",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(weather.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bad0a012",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(weather.columns)\n",
    "need_weather= weather[['DateTime', 'HourlyDewPointTemperature', 'HourlyDryBulbTemperature', 'HourlyPrecipitation', 'HourlyPresentWeatherType',\n",
    "                     'HourlyPressureChange', 'HourlyPressureTendency', 'HourlyRelativeHumidity', 'HourlySkyConditions', 'HourlySeaLevelPressure','HourlyStationPressure','HourlyVisibility', 'HourlyWetBulbTemperature', 'HourlyWindDirection','HourlyWindGustSpeed', 'HourlyWindSpeed']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "11ec993f",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df= pd.merge(CPC, need_weather, on= \"DateTime\", how= \"inner\")\n",
    "print(key_df.shape)\n",
    "print(key_df.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f005ab80-7617-4824-b2ad-957c01835162",
   "metadata": {},
   "outputs": [],
   "source": [
    "def precise_season(date):\n",
    "    doy = date.timetuple().tm_yday  # Day of the year\n",
    "    if doy >= 355 or doy < 79:\n",
    "        return 'Winter'\n",
    "    elif doy >= 79 and doy < 172:\n",
    "        return 'Spring'\n",
    "    elif doy >= 172 and doy < 266:\n",
    "        return 'Summer'\n",
    "    else:\n",
    "        return 'Fall'\n",
    "key_df['DateTime'] = pd.to_datetime(key_df['DateTime'], errors='coerce')\n",
    "key_df['Season'] = key_df['DateTime'].apply(precise_season)\n",
    "\n",
    "summer_CH= key_df[key_df['Season'] == 'Summer']\n",
    "summer_CH= summer_CH.dropna()\n",
    "winter_CH= key_df[key_df['Season'] == 'Winter']\n",
    "winter_CH= winter_CH.dropna()\n",
    "fall_CH= key_df[key_df['Season'] == 'Fall']\n",
    "fall_CH= fall_CH.dropna()\n",
    "spring_CH= key_df[key_df['Season'] == 'Spring']\n",
    "spring_CH= spring_CH.dropna()\n",
    "\n",
    "spring_CH.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b2787ce9",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df['Location']= \"Charlestown\"\n",
    "key_df.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a4b381f8",
   "metadata": {},
   "outputs": [],
   "source": [
    "main_df= pd.concat([main_df, key_df])\n",
    "main_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "deb156a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "376565bc",
   "metadata": {},
   "outputs": [],
   "source": [
    "main_df.to_csv('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/cleanDATA.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "298135e5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import plotly.express as px\n",
    "fig= px.scatter_polar(key_df, theta=\"HourlyWindDirection\", color=\"UFP Concentration\", r= \"HourlyWindSpeed\",\n",
    "            color_continuous_scale=\"reds\") #plotting a windrose for ultrafine particle concentrations\n",
    "fig.update_traces(marker=dict(size=5))\n",
    "fig.show()\n",
    "\n",
    "fig.write_html(r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\Polar Plots\\ML_UFP\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "384d55d0",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(df['HourlyWindDirection'].dtype)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3143d33e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.colors as mcolors\n",
    "import numpy as np\n",
    "\n",
    "# Load the data\n",
    "df= spring_CH[['HourlyWindDirection',\"UFP Concentration\", 'HourlyWindSpeed']]\n",
    "df['HourlyWindDirection'] = pd.to_numeric(df['HourlyWindDirection'], errors='coerce')\n",
    "#df = df[(df['HourlyWindDirection'] < 360) & (df['HourlyWindSpeed'] > 0) & (df['HourlyWindSpeed'] <= 12)]\n",
    "#df = df[(df['WindDirection'] < 360) & (df['WindSpeed'] > 0)]\n",
    "\n",
    "# Convert wind direction to radians\n",
    "df['WindDirectionRad'] = np.radians(df['HourlyWindDirection'])\n",
    "\n",
    "# Sort DataFrame by 'Concentration' in descending order\n",
    "df = df.sort_values(by=\"UFP Concentration\", ascending=True)\n",
    "\n",
    "# Create polar scatter plot\n",
    "fig = plt.figure(figsize=(8, 8))\n",
    "ax = fig.add_subplot(111, polar=True)\n",
    "\n",
    "ax.set_theta_offset(np.pi/2)  # Rotates the circle by 90 degrees counterclockwise\n",
    "ax.set_theta_direction(-1)    # Reverses the direction of rotation (clockwise)\n",
    "\n",
    "# Scatter plot of concentration\n",
    "sc = ax.scatter(df['WindDirectionRad'], df['HourlyWindSpeed'], c=df['UFP Concentration'], cmap='YlOrRd', s=50, alpha=0.7, vmin= 40000, vmax= 150000)\n",
    "\n",
    "\n",
    "# Set polar plot settings\n",
    "ax.set_title('Spring')\n",
    "ax.set_xticks(np.linspace(0, 2*np.pi, 8, endpoint=False))\n",
    "ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])\n",
    "\n",
    "# Add colorbar\n",
    "cbar = fig.colorbar(sc)\n",
    "cbar.set_label('Concentration (#/cm\\u00b3)')\n",
    "\n",
    "# Display plot\n",
    "\n",
    "plt.savefig(r'/Users/camillegimilaro/Desktop/Temp/Cleaned Data/spring_CH.png', dpi=500)\n",
    "\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "243fb49e",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df['DateTime'] = pd.to_datetime(key_df['DateTime'], format='%m/%d/%y %H:%M')\n",
    "key_df['Month'] = key_df['DateTime'].dt.month"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "73d18e79",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(key_df['Month'].max())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "94dbb6f1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "plt.figure(figsize=(12, 6))\n",
    "\n",
    "# Create a boxplot for concentration data for each hour, separated by weekday and weekend\n",
    "sns.boxplot(x='Month', y='UFP Concentration', data= key_df, color= 'Blue', showfliers=False, whis= [10, 90])\n",
    "\n",
    "\n",
    "# Add horizontal lines connecting the medians\n",
    "medians_weekday = key_df.groupby('Month')['UFP Concentration'].median().values\n",
    "medians_weekend = key_df.groupby('Month')['UFP Concentration'].median().values\n",
    "plt.plot(range(len(medians_weekday)), medians_weekday, color='c', linestyle='-', linewidth=2, label='Hourly Median')\n",
    "\n",
    "plt.title('Everett UFP (#/cm\\u00b3)')\n",
    "plt.xlabel('Month of Year')\n",
    "plt.ylabel('Concentration (#/cm\\u00b3)')\n",
    "plt.legend()\n",
    "\n",
    "plt.ylim(0, 30000)  # Adjust the multiplier as needed to provide some space above the highest value\n",
    "\n",
    "# Add horizontal gridlines only\n",
    "plt.grid(axis='y')\n",
    "\n",
    "\n",
    "plt.tight_layout()\n",
    "\n",
    "# Save plot as JPEG file\n",
    "plt.savefig(r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\Monthly Trends\\EV_UFP.png\", dpi=500)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9f8875ad",
   "metadata": {},
   "outputs": [],
   "source": [
    "def corw(m):\n",
    "    if m < 4:\n",
    "        return 'Cold'\n",
    "    elif m > 9:\n",
    "        return 'Cold'\n",
    "    else:\n",
    "        return 'Warm'\n",
    "    \n",
    "# Apply the function to create a new column\n",
    "key_df['Cold or Warm Month'] = key_df['Month'].apply(corw)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7a8ec1f7",
   "metadata": {},
   "outputs": [],
   "source": [
    "Warm_months= key_df[key_df['coldorwarm']=='Warm']\n",
    "Cold_months= key_df[key_df['coldorwarm']=='Cold']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5b637e75",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f8e3d060",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.histplot(data= key_df, x= \"Large (#/cm^3)\", kde= True, element= \"step\", hue= \"Cold or Warm Month\")\n",
    "plt.savefig(r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\Monthly Trends\\ML_hist_large.png\", dpi=500)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5bed220e",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.scatterplot(data= key_df, x= \"HourlyDryBulbTemperature\", y=\"UFP Concentration\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "34f8bdc8",
   "metadata": {},
   "outputs": [],
   "source": [
    "sub_set= main_df[[\"UFP Concentration\", \"PM 2.5\", \"PM 10\", \"Large (#/cm^3)\", \"Small (#/cm^3)\", 'HourlySeaLevelPressure', 'HourlyPrecipitation', \"HourlyDryBulbTemperature\", \"Location\"]]\n",
    "sub_set = sub_set.apply(lambda col: pd.to_numeric(col, errors='coerce') if col.name != 'Location' else col)\n",
    "sub_set_clean = sub_set.dropna()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "90fe411c",
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(30, 30))\n",
    "sns.pairplot(sub_set_clean, hue= \"Location\", plot_kws=dict(marker=\"+\", linewidth=0.15), corner= True)\n",
    "plt.savefig(r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\pairplots_morevariables.png\", dpi=2000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0668d72c",
   "metadata": {},
   "outputs": [],
   "source": [
    "count_df= key_df.groupby('Month')['UFP Concentration'].count()\n",
    "count_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1650bd26",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df.shape\n",
    "key_df.to_csv(\"/Users/camillegimilaro/Desktop/Temp/ML_analysis/RelevantDATA.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "72b2a1a1-2796-439d-b00b-ce4ce83fcbe8",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/mergedinnerDATA.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6ce24b02-bf04-425e-bd5e-d99ac0385ed3",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3e0cdf45-24a3-49d0-a0ee-56a60886a274",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.mixture import GaussianMixture\n",
    "X = DATA[['UFP Concentration', 'PM 2.5', 'PM 10']]\n",
    "gmm = GaussianMixture(n_components=2, n_init=10)\n",
    "\n",
    "gmm.fit(X)\n",
    "\n",
    "y_gmm = gmm.predict(X)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "78affbb5-254a-46dd-969f-449c23c000e6",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.mixture import GaussianMixture\n",
    "from sklearn.metrics import silhouette_score, davies_bouldin_score\n",
    "\n",
    "gmm_list = []\n",
    "silhouette_coefficients = []\n",
    "davies_bouldin_scores = []\n",
    "k_list = []\n",
    "\n",
    "for k in range(2, 11):\n",
    "    print(k)\n",
    "    \n",
    "    # Define and fit GMM\n",
    "    gmm = GaussianMixture(n_components=k, n_init=10)\n",
    "    gmm.fit(X)\n",
    "    \n",
    "    # Predict cluster assignments\n",
    "    y_gmm = gmm.predict(X)\n",
    "    \n",
    "    # Store results\n",
    "    k_list.append(y_gmm)\n",
    "    gmm_list.append(gmm)\n",
    "    \n",
    "    # Compute evaluation metrics\n",
    "    silhouette_index = silhouette_score(X, y_gmm)\n",
    "    db_index = davies_bouldin_score(X, y_gmm)\n",
    "    \n",
    "    silhouette_coefficients.append(silhouette_index)\n",
    "    davies_bouldin_scores.append(db_index)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "51f1621f-627b-4721-9b1d-f4b1d6cde9bc",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns; sns.set()  # for plot styling\n",
    "import numpy as np\n",
    "\n",
    "plt.figure(figsize=(10,5))\n",
    "plt.plot(range(2, 11), silhouette_coefficients,'o-')\n",
    "plt.grid(linestyle='--')\n",
    "plt.xticks(range(2, 11))\n",
    "plt.xlabel(\"Number of Clusters\")\n",
    "plt.ylabel(\"Silhouette Coefficient\")\n",
    "plt.title(\"Silhouette Score\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4f96e9a0-ad8b-40d6-98fb-70282170a031",
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10,5)) \n",
    "plt.plot(range(2, 11), davies_bouldin_scores,'o-')\n",
    "plt.grid(linestyle='--')\n",
    "plt.xticks(range(2, 11))\n",
    "plt.xlabel(\"Number of clusters\")\n",
    "plt.ylabel(\"Davies-Bouldin Index\")\n",
    "plt.title(\"Davies-Bouldin Index\")\n",
    "\n",
    "#plt.savefig('/Users/camillegimilaro/Desktop/Temp/ML_analysis/GaussianSihlouette.png')\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ec58fbd8-c52c-4b99-a6d2-90b82989ce10",
   "metadata": {},
   "outputs": [],
   "source": [
    "centers = gmm_list[i].means_"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7c838a48-499a-49e1-93cd-3483e839b217",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "from mpl_toolkits.mplot3d import Axes3D\n",
    "\n",
    "# Assuming X is your data and k_list contains the cluster assignments for each point\n",
    "k = 4\n",
    "i = k - 2\n",
    "\n",
    "# Set up the 3D plot\n",
    "fig = plt.figure(figsize=(15, 15))\n",
    "ax = fig.add_subplot(111, projection='3d')\n",
    "\n",
    "# Plot the data\n",
    "ax.scatter(X.values[:, 0], X.values[:, 1], X.values[:, 2], c=k_list[i], s=50, cmap='viridis')\n",
    "\n",
    "# Plot the cluster centers (adjust based on your k-means result)\n",
    "centers = gmm_list[i].means_\n",
    "ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], c='red', s=500, alpha=0.5)\n",
    "\n",
    "# Labels\n",
    "ax.set_xlabel('UFP (# > 7 nm/ cm^3)')\n",
    "ax.set_ylabel('PM 2.5')\n",
    "ax.set_zlabel('PM 10') #'UFP Concentration','PM 2.5', 'PM 10']\n",
    "\n",
    "# Save the plot\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/gaussian.png')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "788635db-6b5e-454a-8300-fb20075d5768",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(key_df['UFP Concentration'].min())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b80f3a03-9d01-48a1-9414-6668d5e40028",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(DATA.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "194f69f9-9053-4d6b-b68a-ac900d21e281",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "630143f9-c8eb-4d82-85ae-76e955314e23",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(gmm_list[2].means_)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "316b6bf9-2424-41db-96b5-de42d39adfd8",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA['Cluster'] = gmm_list[2].predict(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1cff6d0b-b1cc-4ce7-9500-2565e451e995",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "00331f8a-6246-4bed-a549-16fd34eff70f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ensure numeric types before plotting\n",
    "cols_to_numeric = ['HourlyWindSpeed', 'HourlyWindDirection', 'HourlyPrecipitation', \n",
    "                   'HourlyRelativeHumidity', 'HourlyStationPressure']\n",
    "\n",
    "for col in cols_to_numeric:\n",
    "    DATA[col] = pd.to_numeric(DATA[col], errors='coerce')  # Convert to numeric, setting errors to NaN\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bf43b423-86af-4e6b-9c68-07cefb1430eb",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATA.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "86ebde95-6ac2-4df9-98a9-5596586d3bff",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set a MultiIndex with 'timestamp' and 'location'\n",
    "main_df = main_df.reset_index(['DateTime', 'Location', 'Cluster'])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7a08541a-1f2c-4e15-a9b7-a8e7d22748a5",
   "metadata": {},
   "outputs": [],
   "source": [
    "clust = {}\n",
    "fig, axes = plt.subplots(4, 5, figsize=(30, 15), constrained_layout=True)\n",
    "axes = np.array(axes)\n",
    "row_colors = [(0.267004, 0.004874, 0.329415, 1.0), (0.229739, 0.322361, 0.545706, 1.0), (0.369214, 0.788888, 0.382914, 1.0), (0.993248, 0.906157, 0.143936, 1.0)]\n",
    "for i in range(4):\n",
    "    clust[i] = DATA[DATA['Cluster'] == i]\n",
    "    \n",
    "    sns.violinplot(data=clust[i], x='HourlyWindSpeed', ax=axes[i, 0], hue= 'Cluster', palette=[row_colors[i]])\n",
    "    sns.violinplot(data=clust[i], x='HourlyWindDirection', ax=axes[i, 1], hue= 'Cluster',palette=[row_colors[i]])\n",
    "    sns.violinplot(data=clust[i], x='HourlyPrecipitation', ax=axes[i, 2], hue= 'Cluster',palette=[row_colors[i]])\n",
    "    sns.violinplot(data=clust[i], x='HourlyRelativeHumidity', ax=axes[i, 3], hue= 'Cluster',palette=[row_colors[i]])\n",
    "    sns.violinplot(data=clust[i], x='HourlyStationPressure', ax=axes[i, 4], hue= 'Cluster',palette=[row_colors[i]])\n",
    "\n",
    "    # Set x-axis limits\n",
    "    axes[i, 0].set_xlim(1, 15)   # Wind Speed (m/s)\n",
    "    axes[i, 1].set_xlim(0, 360)  # Wind Direction (Degrees)\n",
    "    axes[i, 2].set_xlim(0, 0.30)   # Precipitation (adjust based on actual range)\n",
    "    axes[i, 3].set_xlim(10, 100) # Relative Humidity %\n",
    "    axes[i, 4].set_xlim(29.25, 30.5) # Station Pressure (inHg)\n",
    "\n",
    "    # Remove x-axis labels for all but the last row\n",
    "    for j in range(5):\n",
    "        if i < 4:\n",
    "            axes[i, j].set_xlabel('')\n",
    "\n",
    "# Add final row x-labels\n",
    "axes[3, 0].set_xlabel(\"Wind Speed (m/s)\", fontsize=20)\n",
    "axes[3, 1].set_xlabel(\"Wind Direction (Degrees)\", fontsize=20)\n",
    "axes[3, 2].set_xlabel(\"Precipitation\", fontsize=20)\n",
    "axes[3, 3].set_xlabel(\"Relative Humidity %\", fontsize=20)\n",
    "axes[3, 4].set_xlabel(\"Station Pressure (inHg)\", fontsize=20)\n",
    "\n",
    "#plt.show()\n",
    "\n",
    "\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/violinplot.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b6ecdb10-e181-41ed-bb70-affc8635943e",
   "metadata": {},
   "outputs": [],
   "source": [
    "key_df['DateTime']= pd.to_datetime(key_df['DateTime'])\n",
    "key_df['DateTime'].dtype"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6c57e515-45be-48be-86e7-5cb4e5e8140f",
   "metadata": {},
   "outputs": [],
   "source": [
    "cluster1= pd.DataFrame(clust[1])\n",
    "print(cluster1.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b6718dbe-5753-497f-973b-9bbd5e6c567c",
   "metadata": {},
   "outputs": [],
   "source": [
    "ufp_95th_percentile = data['UFP Concentration'].quantile(0.95)\n",
    "\n",
    "# Step 2: Create a new column 'UFP_category' to categorize UFP values into \"Top 90%\" and \"Below 90%\"\n",
    "data['UFP_category'] = data['UFP Concentration'].apply(lambda x: 'Top 95%' if x >= ufp_95th_percentile else 'Below 95%')\n",
    "\n",
    "# Step 3: Create a new DataFrame with UFP values in the top 90%\n",
    "top_95_df = data[data['UFP_category'] == 'Top 95%']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0d9f79a0-abcc-4d1f-b694-918dddd1744a",
   "metadata": {},
   "outputs": [],
   "source": [
    "top_95_df.head()\n",
    "#top_95_df.shape\n",
    "top_95_df.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7847a8bd-87dd-40d8-9cd7-7be9579df82b",
   "metadata": {},
   "outputs": [],
   "source": [
    "data= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/CleanDATA.csv')\n",
    "data.head()\n",
    "print(data.shape)\n",
    "print(DATA.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b45d14fc-361d-4f05-8c52-fc102899974c",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.histplot(data=top_95_df, x=\"UFP Concentration\", hue= \"Location\")\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/highesthourly.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e16d7857-5469-4b2c-9c58-d3d4c92ebcd8",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.histplot(data=top_95_df, x=\"HourlyDryBulbTemperature\", hue= \"Location\")\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/hourlytemp.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eedd9d53-7a58-4c0d-b857-cd59f5ad2e71",
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(60, 8))\n",
    "sns.histplot(data=top_95_df, x='HourlyPresentWeatherType' ,hue= \"Location\")\n",
    "plt.xticks(fontsize=9)\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/weathertype.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a17cf793-85c1-49d5-aa5e-c67a7d8b66d1",
   "metadata": {},
   "outputs": [],
   "source": [
    "top_95_df['HourlySeaLevelPressure'] = pd.to_numeric(top_95_df['HourlySeaLevelPressure'], errors='coerce')\n",
    "sns.histplot(data=top_95_df, x='HourlySeaLevelPressure' ,hue= \"Location\")\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/pressure.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "500b5a0f-46f7-44f6-ad76-1e15874fc724",
   "metadata": {},
   "outputs": [],
   "source": [
    "top_95_df['DateTime'] = pd.to_datetime(top_95_df['DateTime'])\n",
    "top_95_df['hour'] = top_95_df['DateTime'].dt.hour\n",
    "top_95_df['dayofweek']=top_95_df['DateTime'].dt.dayofweek\n",
    "top_95_df['month']=top_95_df['DateTime'].dt.month\n",
    "top_95_df.head()\n",
    "#top_95_df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e87ad875-563e-49bb-8194-ad57ec807af5",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.histplot(data=top_95_df, x='dayofweek' ,hue= \"Location\")\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/day.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d025eeab-233f-47b3-bbfb-a87db5837bea",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.histplot(data=top_95_df, x='month' ,hue= \"Location\")\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/month.png')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "df1f4af2-7a8b-4511-bca4-29d853024410",
   "metadata": {},
   "outputs": [],
   "source": [
    "sns.histplot(data=top_95_df, x='hour' ,hue= \"Location\")\n",
    "plt.savefig('/Users/camillegimilaro/Desktop/Temp/Cleaned Data/hour.png')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
