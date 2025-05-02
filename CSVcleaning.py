{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f163b08e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "df = pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113.8_preprocessed.csv', header=0)\n",
    "\n",
    "new_col_names = []\n",
    "group_index = 1\n",
    "for i, old_col in enumerate(df.columns, start=1):\n",
    "    col_mod = (i - 1) % 3  # cycle: 0 -> Time, 1 -> Conc, 2 -> Status\n",
    "    if col_mod == 0:\n",
    "        new_col_names.append(f\"Time_{group_index}\")\n",
    "    elif col_mod == 1:\n",
    "        new_col_names.append(f\"Conc_{group_index}\")\n",
    "    else:\n",
    "        new_col_names.append(f\"Status_{group_index}\")\n",
    "        group_index += 1\n",
    "\n",
    "df.columns = new_col_names\n",
    "num_groups = group_index - 1\n",
    "long_dfs = []\n",
    "\n",
    "for g in range(1, num_groups + 1):\n",
    "    subset = df[[f\"Time_{g}\", f\"Conc_{g}\", f\"Status_{g}\"]].copy()\n",
    "    subset.columns = [\"Time\", \"Conc\", \"Status\"]  # standard column names\n",
    "   \n",
    "    subset[\"Time\"] = subset[\"Time\"].astype(str).str.strip()\n",
    "    \n",
    "    subset = subset[subset[\"Time\"] != \"\"]\n",
    "   \n",
    "    long_dfs.append(subset)\n",
    "\n",
    "stacked = pd.concat(long_dfs, ignore_index=True)\n",
    "\n",
    "\n",
    "stacked[\"Time\"] = pd.to_datetime(\n",
    "    stacked[\"Time\"], \n",
    "    format=\"%H:%M:%S\", \n",
    "    errors='coerce'\n",
    ")\n",
    "\n",
    "stacked.dropna(subset=[\"Time\"], inplace=True)\n",
    "\n",
    "\n",
    "stacked[\"Time\"] = stacked[\"Time\"].dt.time\n",
    "\n",
    "start_date = pd.to_datetime(\"2024/11/13\")\n",
    "\n",
    "stacked[\"Date\"] = pd.NaT\n",
    "\n",
    "current_date = start_date\n",
    "\n",
    "stacked.reset_index(drop=True, inplace=True)\n",
    "\n",
    "stacked.loc[0, \"Date\"] = current_date\n",
    "\n",
    "for i in range(1, len(stacked)):\n",
    "    prev_time = stacked.loc[i-1, \"Time\"]\n",
    "    this_time = stacked.loc[i, \"Time\"]\n",
    "    \n",
    "    stacked.loc[i, \"Date\"] = current_date\n",
    "    \n",
    "    if this_time < prev_time:\n",
    "        current_date = current_date + pd.Timedelta(days=1)\n",
    "        stacked.loc[i, \"Date\"] = current_date\n",
    "stacked.sort_values(by=[\"Date\", \"Time\"], inplace=True, ignore_index=True)\n",
    "\n",
    "stacked.to_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113_processed.csv', index=False)\n",
    "print(stacked.head(30))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ed866ecc-531c-46c7-8a76-ec51a7ce5cde",
   "metadata": {},
   "outputs": [],
   "source": [
    "df= pd.read_csv(r'/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241030.csv', skiprows= 20)\n",
    "print(df.tail())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e9ae4d60",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Merge .csv files\n",
    "df1= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241030_processed.csv')\n",
    "df2= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241101_processed.csv')\n",
    "df3= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241107_processed.csv')\n",
    "df4= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113_processed.csv')\n",
    "\n",
    "merge= pd.concat([df1,df2,df3,df4])\n",
    "merge[:10]\n",
    "print(merge.tail())\n",
    "merge.to_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /csvmergeno2.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3e3b4764",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "merge= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /Everett Additional columns 2.DAT', names=['Date/Time', 'Conc', 'Status'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "08c060b1",
   "metadata": {},
   "outputs": [],
   "source": [
    "dat= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_allmerge4.DAT')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "724602f7",
   "metadata": {},
   "outputs": [],
   "source": [
    "add= merge"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b40491d2",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(dat.head())\n",
    "print(add.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3671bd70",
   "metadata": {},
   "outputs": [],
   "source": [
    "fix= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Everett\\CPC out\\columns.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "22cab31f",
   "metadata": {},
   "outputs": [],
   "source": [
    "dat2= dat.iloc[:,[1,2,3]]\n",
    "print(dat2.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9f2d2ef7",
   "metadata": {},
   "outputs": [],
   "source": [
    "#print(fix.head())\n",
    "#print(fix.shape)\n",
    "new= add.iloc[:,[0,1,3]]\n",
    "#print(new.head())\n",
    "#print(merge.head())\n",
    "new.columns = ['Date/Time', 'Conc', 'Status']\n",
    "print(new.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0f051817",
   "metadata": {},
   "outputs": [],
   "source": [
    "merge['Date/Time'] = pd.to_datetime(merge['Date'] + ' ' + merge['Time'])\n",
    "print(merge.tail())\n",
    "merge['Date/Time'] = merge['Date/Time'].dt.strftime('%m/%d/%Y %H:%M:%S')\n",
    "merge1 = merge.drop(['Date', 'Time'], axis=1)\n",
    "merge1[\"Status\"] = merge1[\"Status\"].fillna(\"0\")\n",
    "print(merge1.tail())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3630ab18",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(dat2.head())\n",
    "print(merge1.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f669e799",
   "metadata": {},
   "outputs": [],
   "source": [
    "csv_and_dat= pd.concat([dat2, add])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "73934f01",
   "metadata": {},
   "outputs": [],
   "source": [
    "csv_and_dat.to_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_allmerge5.DAT')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6edb7d62",
   "metadata": {},
   "outputs": [],
   "source": [
    "CH= r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\CH_allmerge.DAT\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d64907f3",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "CH_df= pd.read_csv(CH)\n",
    "CH_errors= df.loc[df['Status'].notnull() & (df['Status'] != 0), 'Status'].unique()\n",
    "print(CH_errors)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "033a555e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "df= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_allCPCdata.csv\")\n",
    "ML_errors= df.loc[df['Status'].notnull() & (df['Status'] != 0), 'Status'].unique()\n",
    "print(ML_errors)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "edd1910e",
   "metadata": {},
   "outputs": [],
   "source": [
    "ML_errors.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "68a46afc",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "EV_df= csv_and_dat\n",
    "EV_errors= EV_df.loc[EV_df['Status'].notnull() & (EV_df['Status'] != 0), 'Status'].unique()\n",
    "print(EV_errors)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "06263180",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "max_length = max(len(ML_errors), len(EV_errors), len(CH_errors))\n",
    "\n",
    "def pad_array(arr, length):\n",
    "    return np.pad(arr, (0, length - len(arr)), constant_values=np.nan)\n",
    "\n",
    "ML_errors = pad_array(ML_errors, max_length)\n",
    "EV_errors = pad_array(EV_errors, max_length)\n",
    "CH_errors = pad_array(CH_errors, max_length)\n",
    "\n",
    "errors = np.column_stack((ML_errors, EV_errors, CH_errors))\n",
    "error_df = pd.DataFrame(errors, columns=['Malden', 'Everett', 'Charlestown'])\n",
    "\n",
    "error= pd.DataFrame(errors, columns= ['Malden', 'Everett', 'Charestown'])\n",
    "#error.to_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Meta Data\\Errors.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "aabece64",
   "metadata": {},
   "outputs": [],
   "source": [
    "fatal= pd.read_csv(\"/Users/camillegimilaro/Desktop/Temp/Fatal_errors.csv\")\n",
    "fatal[:30]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1581f2e8",
   "metadata": {},
   "outputs": [],
   "source": [
    "ML_fatal= fatal.iloc[:,0]\n",
    "EV_fatal= fatal.iloc[:,1]\n",
    "CH_fatal= fatal.iloc[:,2]\n",
    "EV_fatal = EV_fatal.iloc[0:30]\n",
    "print(EV_fatal)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "df720ed3",
   "metadata": {},
   "outputs": [],
   "source": [
    "clean_ML = EV_df[~EV_df['Status'].isin(EV_fatal)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f47a46ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "clean_ML.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "945c6cf7",
   "metadata": {},
   "outputs": [],
   "source": [
    "EV_df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "44df17e8",
   "metadata": {},
   "outputs": [],
   "source": [
    "no= EV_df.drop_duplicates(['Date/Time'])\n",
    "no.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "55406a84-9229-40ec-91c9-625e0ade561a",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(no['Status'].dtype, EV_fatal.dtype)\n",
    "no['Status'] = no['Status'].astype(str)\n",
    "EV_fatal = EV_fatal.astype(str)\n",
    "no['Status'] = no['Status'].str.strip()\n",
    "EV_fatal = EV_fatal.str.strip()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ad7aef87-8b9e-4a36-ba05-e47db575a03c",
   "metadata": {},
   "outputs": [],
   "source": [
    "clean_EV = no[~no['Status'].isin(EV_fatal)]\n",
    "clean_EV.shape                      "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f5b27341",
   "metadata": {},
   "outputs": [],
   "source": [
    "clean_EV['Date/Time'] = pd.to_datetime(clean_EV['Date/Time'])\n",
    "sorted_EV = clean_EV.sort_values(by='Date/Time', ascending= True)\n",
    "sorted_EV.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7d4046c1",
   "metadata": {},
   "outputs": [],
   "source": [
    "final_ML= sorted_ML.drop_duplicates(['Date/Time'])\n",
    "final_ML.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ba48ce95",
   "metadata": {},
   "outputs": [],
   "source": [
    "final_ML.to_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\Cleaned CPC Data\\S25\\ML_secondly_CPC_nofatalerrors_noduplicates.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1fb6121d",
   "metadata": {},
   "outputs": [],
   "source": [
    "no_zeros= sorted_EV[sorted_EV['Conc'] >=300]\n",
    "no_zeros.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fa98b38c",
   "metadata": {},
   "outputs": [],
   "source": [
    "no_zeros.to_csv(\"/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_secondly_CPC_nofatalerrors_above300_updatedfeb25.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5b6394ae",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(final_ML.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9a355e6e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "def convert_to_hourly(final_ML, output_file):\n",
    "    # Read data from the input file into a dataframe\n",
    "\n",
    "    # Set the DateTime column as the index\n",
    "    final_ML = final_ML.set_index('Date/Time')\n",
    "\n",
    "    # Resample data to hourly frequency and calculate mean for each hour\n",
    "    hourly_data = final_ML['Conc'].resample('H').mean()\n",
    "\n",
    "    # Write the hourly data to the output file\n",
    "    hourly_data.to_csv(output_file, header=False, date_format='%m/%d/%Y %H:%M', float_format='%.2f')\n",
    "\n",
    "# Example usage\n",
    "output_file = '/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_hourly_CPC_nofatalerrors_above300_updatedfeb25.DAT'\n",
    "convert_to_hourly(no_zeros, output_file)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "16c22c36-c9be-4022-b055-68ccb544c0a8",
   "metadata": {},
   "outputs": [],
   "source": [
    "df= pd.read_csv(output_file, names=['Date/Time', 'Conc'])\n",
    "print(df.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e28a5427-783c-4843-9fe6-69fbb23e2205",
   "metadata": {},
   "outputs": [],
   "source": [
    "no_zeros= EV_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c0014945",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "no_zeros['Date/Time'] = pd.to_datetime(no_zeros['Date/Time'])\n",
    "\n",
    "# Create a daily count of records\n",
    "daily_counts = no_zeros.groupby(no_zeros['Date/Time'].dt.date).size()\n",
    "\n",
    "# Generate the full expected date range\n",
    "full_date_range = pd.date_range(no_zeros['Date/Time'].min(), no_zeros['Date/Time'].max(), freq='D').date\n",
    "\n",
    "# Find missing full days (days with zero records)\n",
    "missing_days = [day for day in full_date_range if day not in daily_counts.index]\n",
    "\n",
    "# Print only if there are fully missing days\n",
    "if missing_days:\n",
    "    print(\"Missing full days:\", missing_days)\n"
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
