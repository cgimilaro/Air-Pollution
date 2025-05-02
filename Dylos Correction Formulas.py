{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0dffc4c4",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "PA_data= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/noaabackfill.csv')\n",
    "print(PA_data.head())\n",
    "RH= PA_data[['DateTime', 'HourlyRelativeHumidity']]\n",
    "print(RH.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "61618bee",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_38413/198681607.py:3: DtypeWarning: Columns (3,4) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  Dy= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV Dylos 1100/EV_1100_Cleaned.csv', skiprows=0)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "   Small >0.5  Big >2.5 Clean Small Clean Big          DateTime\n",
      "0       367.0      52.0       367.0      52.0  2024-06-26 12:32\n",
      "1       366.0      44.0       366.0      44.0  2024-06-26 12:33\n",
      "2       374.0      43.0       374.0      43.0  2024-06-26 12:34\n",
      "3       374.0      38.0       374.0      38.0  2024-06-26 12:35\n",
      "4       373.0      45.0       373.0      45.0  2024-06-26 12:36\n"
     ]
    },
    {
     "ename": "NameError",
     "evalue": "name 'RH' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[2], line 15\u001b[0m\n\u001b[1;32m     13\u001b[0m Dy \u001b[38;5;241m=\u001b[39m Dy\u001b[38;5;241m.\u001b[39mdrop(columns\u001b[38;5;241m=\u001b[39m[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mDate and Time\u001b[39m\u001b[38;5;124m'\u001b[39m])\n\u001b[1;32m     14\u001b[0m \u001b[38;5;28mprint\u001b[39m(Dy\u001b[38;5;241m.\u001b[39mhead())\n\u001b[0;32m---> 15\u001b[0m \u001b[38;5;28mprint\u001b[39m(RH\u001b[38;5;241m.\u001b[39mhead())\n",
      "\u001b[0;31mNameError\u001b[0m: name 'RH' is not defined"
     ]
    }
   ],
   "source": [
    "from datetime import datetime\n",
    "import pandas as pd\n",
    "Dy= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV Dylos 1100/EV_1100_Cleaned.csv', skiprows=0)\n",
    "\n",
    "# Convert both 'DateTime' and 'ESTDateTime' to the same datetime format\n",
    "Dy['DateTime'] = pd.to_datetime(Dy['Date and Time'], format=\"%m/%d/%y %H:%M\")\n",
    "#RH['DateTime'] = pd.to_datetime(RH['DateandTime'], format='%Y-%m-%dT%H:%M:%S')\n",
    "\n",
    "# If you want to display them in a specific string format (e.g., \"YYYY-MM-DD HH:MM\")\n",
    "Dy['DateTime'] = Dy['DateTime'].dt.strftime(\"%Y-%m-%d %H:%M\")\n",
    "#RH['DateTime'] = RH['DateTime'].dt.strftime(\"%Y-%m-%d %H:%M\")\n",
    "\n",
    "Dy = Dy.drop(columns=['Date and Time'])\n",
    "print(Dy.head())\n",
    "print(RH.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7ffb18dd",
   "metadata": {},
   "outputs": [],
   "source": [
    "Dylos= pd.merge(Dy, RH, on= 'DateTime', how= 'left')\n",
    "print(Dylos.tail())\n",
    "print(Dylos['PM 2.5'].max())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "59e8a1cd",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "def correct_pm(pm, rh):\n",
    "    if rh < 60:\n",
    "        return pm \n",
    "    \n",
    "    else:\n",
    "        return pm * ((60 / rh) ** 6)\n",
    "\n",
    "# Apply the correction to the DataFrame\n",
    "Dylos['Corrected_PM2.5'] = Dylos.apply(lambda row: correct_pm(row['PM 2.5'], row['HourlyRelativeHumidity']), axis=1)\n",
    "Dylos['Corrected_PM10'] = Dylos.apply(lambda row: correct_pm(row['PM 10'], row['HourlyRelativeHumidity']), axis=1)\n",
    "\n",
    "print(Dylos.head())\n",
    "print(Dylos['Corrected_PM2.5'].max())\n",
    "print(Dylos['Corrected_PM10'].max())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c12ebd20",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "def corr_high_pm(pm): \n",
    "    if pm< 300:\n",
    "        return pm\n",
    "    elif pm< 550: \n",
    "        return 56.494 * (np.exp(0.0057 * pm))\n",
    "    else:\n",
    "        return np.nan\n",
    "    \n",
    "Dylos['Corrected_PM2.5_2'] = Dylos.apply(lambda row: corr_high_pm(row['Corrected_PM2.5']), axis=1)\n",
    "Dylos['Corrected_PM10_2'] = Dylos.apply(lambda row: corr_high_pm(row['Corrected_PM10']), axis=1)\n",
    "print(Dylos.head())\n",
    "print(Dylos['Corrected_PM2.5_2'].max())\n",
    "print(Dylos['Corrected_PM10_2'].max())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b0608fba",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(Dy.head())\n",
    "print(Dy.tail())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "fe3b7d54-8852-4767-afc1-c3200fab45a8",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(252609, 5)"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "sorted_Dylos = Dy.sort_values(by='DateTime', ascending= True)\n",
    "sorted_Dylos.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "ec9c9fa9-f64e-4402-b52a-ce47cedada92",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(243073, 5)"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "final_Dylos= sorted_Dylos.drop_duplicates(['DateTime'])\n",
    "final_Dylos.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8e2c7478-927c-426c-a90f-2360e07a733d",
   "metadata": {},
   "outputs": [],
   "source": [
    "final_Dylos.head()\n",
    "print(final_Dylos['Corrected_PM2.5_2'].dropna().shape)\n",
    "print(final_Dylos['Corrected_PM10_2'].dropna().shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "df98610f-c09f-413a-bee9-828e66bc0ded",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "   Clean Small  Clean Big          DateTime\n",
      "0        367.0       52.0  2024-06-26 12:32\n",
      "1        366.0       44.0  2024-06-26 12:33\n",
      "2        374.0       43.0  2024-06-26 12:34\n",
      "3        374.0       38.0  2024-06-26 12:35\n",
      "4        373.0       45.0  2024-06-26 12:36\n",
      "Clean Small    float64\n",
      "Clean Big      float64\n",
      "DateTime        object\n",
      "dtype: object\n"
     ]
    }
   ],
   "source": [
    "final_Dylos = final_Dylos.drop(columns=['Small >0.5', 'Big >2.5'])\n",
    "\n",
    "final_Dylos['Clean Small'] = final_Dylos['Clean Small'].astype(float)\n",
    "final_Dylos['Clean Big'] = final_Dylos['Clean Big'].astype(float)\n",
    "\n",
    "print(final_Dylos.head())\n",
    "print(final_Dylos.dtypes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "58a7f869-d916-4db8-8b42-72e0b958e3ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "final_Dylos.to_csv('/Users/camillegimilaro/Desktop/Temp/EV Dylos 1100/EV_1100_Clean.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "6b629f1a-6fdb-48eb-9d83-20abb303e655",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_38413/2083059789.py:1: DtypeWarning: Columns (10,11,12,13,19,20,21,23,40,41,42,44,51,62,63,66,67,80,92,93,94,95,96,97,98,99,100,101,102,103) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  noaa_data= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/noaabackfill.csv')\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "float64\n"
     ]
    }
   ],
   "source": [
    "noaa_data= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/noaabackfill.csv')\n",
    "print(noaa_data['HourlyRelativeHumidity'].dtypes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "23cad973",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "def convert_to_hourly(final_ML, output_file):\n",
    "    # Ensure DateTime is in datetime format, dropping any invalid entries\n",
    "    #final_ML = final_ML.drop(columns=['Date and Time'])\n",
    "    final_ML['DateTime'] = pd.to_datetime(final_ML['DateTime'], errors='coerce')\n",
    "    final_ML = final_ML.dropna(subset=['DateTime'])\n",
    "\n",
    "    # Set DateTime as the index\n",
    "    final_ML = final_ML.set_index('DateTime')\n",
    "\n",
    "    float_columns = final_ML.select_dtypes(include=['float64'])\n",
    "\n",
    "    # Resample data to hourly frequency and calculate the mean for float columns only\n",
    "    hourly_data = float_columns.resample('h').mean()# Resample data to hourly frequency and calculate the mean for all columns\n",
    "\n",
    "    # Write the hourly data to the output file\n",
    "    hourly_data.to_csv(output_file, date_format='%m/%d/%Y %H:%M', float_format='%.2f')\n",
    "\n",
    "# Example usage\n",
    "output_file = \"/Users/camillegimilaro/Desktop/Temp/noaaavgs.csv\"\n",
    "convert_to_hourly(noaa_data, output_file)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0399bbe1-b433-4d1c-b8cb-236ad0155508",
   "metadata": {},
   "outputs": [],
   "source": [
    "final_Dylos.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d18572cf-b7b7-40a4-8963-29be3e3faf13",
   "metadata": {},
   "outputs": [],
   "source": []
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
