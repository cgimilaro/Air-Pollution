{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "f163b08e",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/1329788323.py:5: DtypeWarning: Columns (23,26,205) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  df = pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113.8_preprocessed.csv', header=0)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "        Time   Conc Status       Date\n",
      "0   14:35:01  11600    NaN 2024-11-13\n",
      "1   14:35:02  11700    NaN 2024-11-13\n",
      "2   14:35:03  11600    NaN 2024-11-13\n",
      "3   14:35:04  11600    NaN 2024-11-13\n",
      "4   14:35:05  11400    NaN 2024-11-13\n",
      "5   14:35:06  11600    NaN 2024-11-13\n",
      "6   14:35:07  11500    NaN 2024-11-13\n",
      "7   14:35:08  11600    NaN 2024-11-13\n",
      "8   14:35:09  11600    NaN 2024-11-13\n",
      "9   14:35:10  11900    NaN 2024-11-13\n",
      "10  14:35:11  11800    NaN 2024-11-13\n",
      "11  14:35:12  11600    NaN 2024-11-13\n",
      "12  14:35:13  11800    NaN 2024-11-13\n",
      "13  14:35:14  11600    NaN 2024-11-13\n",
      "14  14:35:15  11600    NaN 2024-11-13\n",
      "15  14:35:16  11500    NaN 2024-11-13\n",
      "16  14:35:17  11600    NaN 2024-11-13\n",
      "17  14:35:18  11300    NaN 2024-11-13\n",
      "18  14:35:19  11300    NaN 2024-11-13\n",
      "19  14:35:20  11300    NaN 2024-11-13\n",
      "20  14:35:21  11700    NaN 2024-11-13\n",
      "21  14:35:22  12400    NaN 2024-11-13\n",
      "22  14:35:23  12800    NaN 2024-11-13\n",
      "23  14:35:24  13000    NaN 2024-11-13\n",
      "24  14:35:25  13200    NaN 2024-11-13\n",
      "25  14:35:26  13500    NaN 2024-11-13\n",
      "26  14:35:27  12800    NaN 2024-11-13\n",
      "27  14:35:28  12600    NaN 2024-11-13\n",
      "28  14:35:29  12400    NaN 2024-11-13\n",
      "29  14:35:30  12800    NaN 2024-11-13\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "# =============== STEP 1: Read your CSV file ===============\n",
    "# Modify the filename as needed:\n",
    "df = pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113.8_preprocessed.csv', header=0)\n",
    "\n",
    "# ------------------------------------------------------------\n",
    "# Suppose df has columns like:\n",
    "#   Time    Conc (#/cm³)    Instr Status   Time.1  Conc (#/cm³).1   Instr Status.1  ...\n",
    "# ------------------------------------------------------------\n",
    "\n",
    "\n",
    "# =============== STEP 2: Systematically rename columns ===============\n",
    "# We assume there are 3 columns per group: Time, Conc, Status.\n",
    "# We'll rename them to Time_1, Conc_1, Status_1, then Time_2, Conc_2, ...\n",
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
    "\n",
    "# The final group_index - 1 tells us how many groups we actually have\n",
    "num_groups = group_index - 1\n",
    "\n",
    "\n",
    "# =============== STEP 3: Reshape (stack) from wide to long ===============\n",
    "long_dfs = []\n",
    "\n",
    "for g in range(1, num_groups + 1):\n",
    "    subset = df[[f\"Time_{g}\", f\"Conc_{g}\", f\"Status_{g}\"]].copy()\n",
    "    subset.columns = [\"Time\", \"Conc\", \"Status\"]  # standard column names\n",
    "    \n",
    "    # =============== STEP 4: Remove empty or whitespace-only time rows ===============\n",
    "    # Strip whitespace from Time column\n",
    "    subset[\"Time\"] = subset[\"Time\"].astype(str).str.strip()\n",
    "    \n",
    "    # Drop rows where Time is empty after stripping\n",
    "    subset = subset[subset[\"Time\"] != \"\"]\n",
    "    \n",
    "    # Optionally: also drop rows if \"Conc\" or \"Status\" is empty if you need that\n",
    "    # subset = subset.dropna(how='any')  # or how='all' if you prefer\n",
    "    \n",
    "    long_dfs.append(subset)\n",
    "\n",
    "# Concatenate all the subset dataframes\n",
    "stacked = pd.concat(long_dfs, ignore_index=True)\n",
    "\n",
    "\n",
    "# =============== STEP 5: Convert valid time strings to time objects ===============\n",
    "# If some rows are still invalid format (like \"abc\"), use errors='coerce' → becomes NaT\n",
    "stacked[\"Time\"] = pd.to_datetime(\n",
    "    stacked[\"Time\"], \n",
    "    format=\"%H:%M:%S\", \n",
    "    errors='coerce'\n",
    ")\n",
    "\n",
    "# Drop rows where Time couldn't be parsed (NaT)\n",
    "stacked.dropna(subset=[\"Time\"], inplace=True)\n",
    "\n",
    "# Convert from datetime to just time (we only have HH:MM:SS)\n",
    "stacked[\"Time\"] = stacked[\"Time\"].dt.time\n",
    "\n",
    "\n",
    "# =============== STEP 6: Assign dates with rollover after midnight ===============\n",
    "# Choose a start date\n",
    "start_date = pd.to_datetime(\"2024/11/13\")\n",
    "\n",
    "# Add a new Date column\n",
    "stacked[\"Date\"] = pd.NaT\n",
    "\n",
    "# We'll keep track of the \"current date\" as we go down the rows\n",
    "current_date = start_date\n",
    "\n",
    "# Make sure we iterate in the order the rows appear (you can sort if needed)\n",
    "stacked.reset_index(drop=True, inplace=True)\n",
    "\n",
    "# Initialize the first row\n",
    "stacked.loc[0, \"Date\"] = current_date\n",
    "\n",
    "for i in range(1, len(stacked)):\n",
    "    prev_time = stacked.loc[i-1, \"Time\"]\n",
    "    this_time = stacked.loc[i, \"Time\"]\n",
    "    \n",
    "    # Normally, keep the same date as the previous row\n",
    "    stacked.loc[i, \"Date\"] = current_date\n",
    "    \n",
    "    # If the new time is strictly less than the previous time, we crossed midnight\n",
    "    if this_time < prev_time:\n",
    "        current_date = current_date + pd.Timedelta(days=1)\n",
    "        stacked.loc[i, \"Date\"] = current_date\n",
    "\n",
    "# If needed, you can now combine Date + Time into a single column\n",
    "# stacked[\"DateTime\"] = stacked.apply(\n",
    "#     lambda row: pd.to_datetime(str(row[\"Date\"].date()) + \" \" + row[\"Time\"].strftime(\"%H:%M:%S\")),\n",
    "#     axis=1\n",
    "# )\n",
    "\n",
    "# =============== STEP 7: (Optional) Sort by Date then Time ===============\n",
    "stacked.sort_values(by=[\"Date\", \"Time\"], inplace=True, ignore_index=True)\n",
    "\n",
    "# =============== STEP 8: Save or Print ===============\n",
    "stacked.to_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113_processed.csv', index=False)\n",
    "print(stacked.head(30))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "ed866ecc-531c-46c7-8a76-ec51a7ce5cde",
   "metadata": {},
   "outputs": [
    {
     "ename": "UnicodeDecodeError",
     "evalue": "'utf-8' codec can't decode byte 0xb3 in position 246729: invalid start byte",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mUnicodeDecodeError\u001b[0m                        Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[7], line 1\u001b[0m\n\u001b[0;32m----> 1\u001b[0m df\u001b[38;5;241m=\u001b[39m pd\u001b[38;5;241m.\u001b[39mread_csv(\u001b[38;5;124mr\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124m/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241030.csv\u001b[39m\u001b[38;5;124m'\u001b[39m, skiprows\u001b[38;5;241m=\u001b[39m \u001b[38;5;241m20\u001b[39m)\n\u001b[1;32m      2\u001b[0m \u001b[38;5;28mprint\u001b[39m(df\u001b[38;5;241m.\u001b[39mtail())\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1026\u001b[0m, in \u001b[0;36mread_csv\u001b[0;34m(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)\u001b[0m\n\u001b[1;32m   1013\u001b[0m kwds_defaults \u001b[38;5;241m=\u001b[39m _refine_defaults_read(\n\u001b[1;32m   1014\u001b[0m     dialect,\n\u001b[1;32m   1015\u001b[0m     delimiter,\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m   1022\u001b[0m     dtype_backend\u001b[38;5;241m=\u001b[39mdtype_backend,\n\u001b[1;32m   1023\u001b[0m )\n\u001b[1;32m   1024\u001b[0m kwds\u001b[38;5;241m.\u001b[39mupdate(kwds_defaults)\n\u001b[0;32m-> 1026\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m _read(filepath_or_buffer, kwds)\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:620\u001b[0m, in \u001b[0;36m_read\u001b[0;34m(filepath_or_buffer, kwds)\u001b[0m\n\u001b[1;32m    617\u001b[0m _validate_names(kwds\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mnames\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m))\n\u001b[1;32m    619\u001b[0m \u001b[38;5;66;03m# Create the parser.\u001b[39;00m\n\u001b[0;32m--> 620\u001b[0m parser \u001b[38;5;241m=\u001b[39m TextFileReader(filepath_or_buffer, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwds)\n\u001b[1;32m    622\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m chunksize \u001b[38;5;129;01mor\u001b[39;00m iterator:\n\u001b[1;32m    623\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m parser\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1620\u001b[0m, in \u001b[0;36mTextFileReader.__init__\u001b[0;34m(self, f, engine, **kwds)\u001b[0m\n\u001b[1;32m   1617\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions[\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mhas_index_names\u001b[39m\u001b[38;5;124m\"\u001b[39m] \u001b[38;5;241m=\u001b[39m kwds[\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mhas_index_names\u001b[39m\u001b[38;5;124m\"\u001b[39m]\n\u001b[1;32m   1619\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mhandles: IOHandles \u001b[38;5;241m|\u001b[39m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[0;32m-> 1620\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_engine \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_make_engine(f, \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mengine)\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1898\u001b[0m, in \u001b[0;36mTextFileReader._make_engine\u001b[0;34m(self, f, engine)\u001b[0m\n\u001b[1;32m   1895\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(msg)\n\u001b[1;32m   1897\u001b[0m \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[0;32m-> 1898\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m mapping[engine](f, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions)\n\u001b[1;32m   1899\u001b[0m \u001b[38;5;28;01mexcept\u001b[39;00m \u001b[38;5;167;01mException\u001b[39;00m:\n\u001b[1;32m   1900\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mhandles \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/c_parser_wrapper.py:93\u001b[0m, in \u001b[0;36mCParserWrapper.__init__\u001b[0;34m(self, src, **kwds)\u001b[0m\n\u001b[1;32m     90\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m kwds[\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mdtype_backend\u001b[39m\u001b[38;5;124m\"\u001b[39m] \u001b[38;5;241m==\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mpyarrow\u001b[39m\u001b[38;5;124m\"\u001b[39m:\n\u001b[1;32m     91\u001b[0m     \u001b[38;5;66;03m# Fail here loudly instead of in cython after reading\u001b[39;00m\n\u001b[1;32m     92\u001b[0m     import_optional_dependency(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mpyarrow\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m---> 93\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_reader \u001b[38;5;241m=\u001b[39m parsers\u001b[38;5;241m.\u001b[39mTextReader(src, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwds)\n\u001b[1;32m     95\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39munnamed_cols \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_reader\u001b[38;5;241m.\u001b[39munnamed_cols\n\u001b[1;32m     97\u001b[0m \u001b[38;5;66;03m# error: Cannot determine type of 'names'\u001b[39;00m\n",
      "File \u001b[0;32mparsers.pyx:574\u001b[0m, in \u001b[0;36mpandas._libs.parsers.TextReader.__cinit__\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32mparsers.pyx:663\u001b[0m, in \u001b[0;36mpandas._libs.parsers.TextReader._get_header\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32mparsers.pyx:874\u001b[0m, in \u001b[0;36mpandas._libs.parsers.TextReader._tokenize_rows\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32mparsers.pyx:891\u001b[0m, in \u001b[0;36mpandas._libs.parsers.TextReader._check_tokenize_status\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32mparsers.pyx:2053\u001b[0m, in \u001b[0;36mpandas._libs.parsers.raise_parser_error\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32m<frozen codecs>:322\u001b[0m, in \u001b[0;36mdecode\u001b[0;34m(self, input, final)\u001b[0m\n",
      "\u001b[0;31mUnicodeDecodeError\u001b[0m: 'utf-8' codec can't decode byte 0xb3 in position 246729: invalid start byte"
     ]
    }
   ],
   "source": [
    "df= pd.read_csv(r'/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241030.csv', skiprows= 20)\n",
    "print(df.tail())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "e9ae4d60",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/335034061.py:2: DtypeWarning: Columns (2) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  df1= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241030_processed.csv')\n",
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/335034061.py:5: DtypeWarning: Columns (2) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  df4= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113_processed.csv')\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "            Time    Conc Status      Date\n",
      "685002  12:53:56  5950.0    NaN  11/21/24\n",
      "685003  12:53:57  4720.0    NaN  11/21/24\n",
      "685004  12:53:58  4560.0    NaN  11/21/24\n",
      "685005  12:53:59  4260.0    NaN  11/21/24\n",
      "685006  12:54:00  4420.0    NaN  11/21/24\n"
     ]
    }
   ],
   "source": [
    "#Merge .csv files\n",
    "df1= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241030_processed.csv')\n",
    "df2= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241101_processed.csv')\n",
    "df3= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241107_processed.csv')\n",
    "df4= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EVT_CPC_20241113_processed.csv')\n",
    "#df5= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_processed_12032024.csv\")\n",
    "#df6= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_processed_12232024.csv\")\n",
    "#df7= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_processed_12302024.csv\")\n",
    "#df8= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_processed_01082025.csv\")\n",
    "#df9= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_processed_01232025.csv\")\n",
    "\n",
    "merge= pd.concat([df1,df2,df3,df4])\n",
    "merge[:10]\n",
    "print(merge.tail())\n",
    "merge.to_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /csvmergeno2.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "3e3b4764",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\cgimil01\\AppData\\Local\\Temp\\ipykernel_3004\\3452582008.py:2: DtypeWarning: Columns (2) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  merge= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Everett\\CPC out\\EV_allmerge4.DAT\")\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "merge= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Everett\\CPC out\\EV_allmerge4.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "08c060b1",
   "metadata": {},
   "outputs": [],
   "source": [
    "dat= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Everett\\CPC out\\Everett Additional columns.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "id": "724602f7",
   "metadata": {},
   "outputs": [],
   "source": [
    "add= pd.read_csv(r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\additionalfiles_corryear.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "b40491d2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "   10/16/2024 16:22:00  6.79e3  0\n",
      "0  10/16/2024 16:22:03  7230.0  0\n",
      "1  10/16/2024 16:22:06  7290.0  0\n",
      "2  10/16/2024 16:22:09  7360.0  0\n",
      "3  10/16/2024 16:22:12  7200.0  0\n",
      "4  10/16/2024 16:22:15  7050.0  0\n",
      "   Unnamed: 0     Conc Status            Date/Time\n",
      "0           0  41200.0      0  10/30/2024 12:17:27\n",
      "1           1  41300.0      0  10/30/2024 12:17:28\n",
      "2           2  40800.0      0  10/30/2024 12:17:29\n",
      "3           3  40700.0      0  10/30/2024 12:17:30\n",
      "4           4  40700.0      0  10/30/2024 12:17:31\n"
     ]
    }
   ],
   "source": [
    "print(dat.head())\n",
    "print(merge.head())\n",
    "#print(add.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "3671bd70",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\cgimil01\\AppData\\Local\\Temp\\ipykernel_24408\\2684455667.py:1: DtypeWarning: Columns (4) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  fix= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Everett\\CPC out\\columns.DAT\")\n"
     ]
    }
   ],
   "source": [
    "fix= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Everett\\CPC out\\columns.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "id": "22cab31f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "             Date/Time     Conc Status\n",
      "0  11/25/2024 14:34:12  10200.0      0\n",
      "1  11/25/2024 14:34:13  10400.0      0\n",
      "2  11/25/2024 14:34:14  10700.0      0\n",
      "3  11/25/2024 14:34:15  10500.0      0\n",
      "4  11/25/2024 14:34:16  10600.0      0\n"
     ]
    }
   ],
   "source": [
    "dat2= dat.iloc[:,[1,2,3]]\n",
    "print(dat2.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 78,
   "id": "9f2d2ef7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "             Date/Time     Conc  Status\n",
      "0  11/25/2024 14:34:12  10200.0       0\n",
      "1  11/25/2024 14:34:13  10400.0       0\n",
      "2  11/25/2024 14:34:14  10700.0       0\n",
      "3  11/25/2024 14:34:15  10500.0       0\n",
      "4  11/25/2024 14:34:16  10600.0       0\n"
     ]
    }
   ],
   "source": [
    "#print(fix.head())\n",
    "#print(fix.shape)\n",
    "new= merge.iloc[:,[0,1,3]]\n",
    "#print(new.head())\n",
    "#print(merge.head())\n",
    "new.columns = ['Date/Time', 'Conc', 'Status']\n",
    "print(new.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "id": "0f051817",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/179152526.py:1: UserWarning: Could not infer format, so each element will be parsed individually, falling back to `dateutil`. To ensure parsing is consistent and as-expected, please specify a format.\n",
      "  merge['Date/Time'] = pd.to_datetime(merge['Date'] + ' ' + merge['Time'])\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "            Time    Conc Status      Date           Date/Time\n",
      "685002  12:53:56  5950.0    NaN  11/21/24 2024-11-21 12:53:56\n",
      "685003  12:53:57  4720.0    NaN  11/21/24 2024-11-21 12:53:57\n",
      "685004  12:53:58  4560.0    NaN  11/21/24 2024-11-21 12:53:58\n",
      "685005  12:53:59  4260.0    NaN  11/21/24 2024-11-21 12:53:59\n",
      "685006  12:54:00  4420.0    NaN  11/21/24 2024-11-21 12:54:00\n",
      "          Conc Status            Date/Time\n",
      "685002  5950.0      0  11/21/2024 12:53:56\n",
      "685003  4720.0      0  11/21/2024 12:53:57\n",
      "685004  4560.0      0  11/21/2024 12:53:58\n",
      "685005  4260.0      0  11/21/2024 12:53:59\n",
      "685006  4420.0      0  11/21/2024 12:54:00\n"
     ]
    }
   ],
   "source": [
    "#merge['Date/Time'] = pd.to_datetime(merge['Date'] + ' ' + merge['Time'])\n",
    "print(merge.tail())\n",
    "merge['Date/Time'] = merge['Date/Time'].dt.strftime('%m/%d/%Y %H:%M:%S')\n",
    "merge1 = merge.drop(['Date', 'Time'], axis=1)\n",
    "merge1[\"Status\"] = merge1[\"Status\"].fillna(\"0\")\n",
    "print(merge1.tail())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "id": "3630ab18",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "             Date/Time     Conc Status\n",
      "0  11/25/2024 14:34:12  10200.0      0\n",
      "1  11/25/2024 14:34:13  10400.0      0\n",
      "2  11/25/2024 14:34:14  10700.0      0\n",
      "3  11/25/2024 14:34:15  10500.0      0\n",
      "4  11/25/2024 14:34:16  10600.0      0\n",
      "      Conc Status            Date/Time\n",
      "0  41200.0      0  10/30/2024 12:17:27\n",
      "1  41300.0      0  10/30/2024 12:17:28\n",
      "2  40800.0      0  10/30/2024 12:17:29\n",
      "3  40700.0      0  10/30/2024 12:17:30\n",
      "4  40700.0      0  10/30/2024 12:17:31\n"
     ]
    }
   ],
   "source": [
    "print(dat2.head())\n",
    "print(merge1.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "id": "f669e799",
   "metadata": {},
   "outputs": [],
   "source": [
    "csv_and_dat= pd.concat([merge1, dat2])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "id": "73934f01",
   "metadata": {},
   "outputs": [],
   "source": [
    "csv_and_dat.to_csv('/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_allmerge4.DAT')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "6edb7d62",
   "metadata": {},
   "outputs": [],
   "source": [
    "CH= r\"C:\\Users\\cgimil01\\Box\\Master'sThesis\\Temp\\CH_allmerge.DAT\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "d64907f3",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\cgimil01\\AppData\\Local\\Temp\\ipykernel_14252\\3433424977.py:2: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  CH_df= pd.read_csv(CH)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[400 '0' '140E' '40A' '408' '1C0F' '1C0E' '140C' '1408' '400' '2' '100'\n",
      " '102' 8 408 1 2001 2009 2409 2401 2101 '2101' '2105' '2107' '2100' '1'\n",
      " 2105 2107 2100 100 101 40 140 2 48 448 '140F' 4000 4100 80 20]\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "CH_df= pd.read_csv(CH)\n",
    "CH_errors= df.loc[df['Status'].notnull() & (df['Status'] != 0), 'Status'].unique()\n",
    "print(CH_errors)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "033a555e",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<>:2: SyntaxWarning: invalid escape sequence '\\P'\n",
      "<>:2: SyntaxWarning: invalid escape sequence '\\P'\n",
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/3807191373.py:2: SyntaxWarning: invalid escape sequence '\\P'\n",
      "  df= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_allCPCdata.csv\")\n",
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/3807191373.py:2: SyntaxWarning: invalid escape sequence '\\P'\n",
      "  df= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_allCPCdata.csv\")\n"
     ]
    },
    {
     "ename": "FileNotFoundError",
     "evalue": "[Errno 2] No such file or directory: 'R:\\\\Personal\\\\Camille Gimilaro\\\\G4_Camille\\\\G4_Camille\\\\Data (Camille.Gimilaro@tufts.edu)\\\\Malden\\\\Raw Data\\\\CPC out\\\\ML_allCPCdata.csv'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[21], line 2\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mpandas\u001b[39;00m \u001b[38;5;28;01mas\u001b[39;00m \u001b[38;5;21;01mpd\u001b[39;00m\n\u001b[0;32m----> 2\u001b[0m df\u001b[38;5;241m=\u001b[39m pd\u001b[38;5;241m.\u001b[39mread_csv(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mR:\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mPersonal\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mCamille Gimilaro\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mG4_Camille\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mG4_Camille\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mData (Camille.Gimilaro@tufts.edu)\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mMalden\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mRaw Data\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mCPC out\u001b[39m\u001b[38;5;124m\\\u001b[39m\u001b[38;5;124mML_allCPCdata.csv\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[1;32m      3\u001b[0m ML_errors\u001b[38;5;241m=\u001b[39m df\u001b[38;5;241m.\u001b[39mloc[df[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mStatus\u001b[39m\u001b[38;5;124m'\u001b[39m]\u001b[38;5;241m.\u001b[39mnotnull() \u001b[38;5;241m&\u001b[39m (df[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mStatus\u001b[39m\u001b[38;5;124m'\u001b[39m] \u001b[38;5;241m!=\u001b[39m \u001b[38;5;241m0\u001b[39m), \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mStatus\u001b[39m\u001b[38;5;124m'\u001b[39m]\u001b[38;5;241m.\u001b[39munique()\n\u001b[1;32m      4\u001b[0m \u001b[38;5;28mprint\u001b[39m(ML_errors)\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1026\u001b[0m, in \u001b[0;36mread_csv\u001b[0;34m(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)\u001b[0m\n\u001b[1;32m   1013\u001b[0m kwds_defaults \u001b[38;5;241m=\u001b[39m _refine_defaults_read(\n\u001b[1;32m   1014\u001b[0m     dialect,\n\u001b[1;32m   1015\u001b[0m     delimiter,\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m   1022\u001b[0m     dtype_backend\u001b[38;5;241m=\u001b[39mdtype_backend,\n\u001b[1;32m   1023\u001b[0m )\n\u001b[1;32m   1024\u001b[0m kwds\u001b[38;5;241m.\u001b[39mupdate(kwds_defaults)\n\u001b[0;32m-> 1026\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m _read(filepath_or_buffer, kwds)\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:620\u001b[0m, in \u001b[0;36m_read\u001b[0;34m(filepath_or_buffer, kwds)\u001b[0m\n\u001b[1;32m    617\u001b[0m _validate_names(kwds\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mnames\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m))\n\u001b[1;32m    619\u001b[0m \u001b[38;5;66;03m# Create the parser.\u001b[39;00m\n\u001b[0;32m--> 620\u001b[0m parser \u001b[38;5;241m=\u001b[39m TextFileReader(filepath_or_buffer, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwds)\n\u001b[1;32m    622\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m chunksize \u001b[38;5;129;01mor\u001b[39;00m iterator:\n\u001b[1;32m    623\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m parser\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1620\u001b[0m, in \u001b[0;36mTextFileReader.__init__\u001b[0;34m(self, f, engine, **kwds)\u001b[0m\n\u001b[1;32m   1617\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions[\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mhas_index_names\u001b[39m\u001b[38;5;124m\"\u001b[39m] \u001b[38;5;241m=\u001b[39m kwds[\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mhas_index_names\u001b[39m\u001b[38;5;124m\"\u001b[39m]\n\u001b[1;32m   1619\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mhandles: IOHandles \u001b[38;5;241m|\u001b[39m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[0;32m-> 1620\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_engine \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_make_engine(f, \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mengine)\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1880\u001b[0m, in \u001b[0;36mTextFileReader._make_engine\u001b[0;34m(self, f, engine)\u001b[0m\n\u001b[1;32m   1878\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mb\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m mode:\n\u001b[1;32m   1879\u001b[0m         mode \u001b[38;5;241m+\u001b[39m\u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mb\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[0;32m-> 1880\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mhandles \u001b[38;5;241m=\u001b[39m get_handle(\n\u001b[1;32m   1881\u001b[0m     f,\n\u001b[1;32m   1882\u001b[0m     mode,\n\u001b[1;32m   1883\u001b[0m     encoding\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mencoding\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m),\n\u001b[1;32m   1884\u001b[0m     compression\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mcompression\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m),\n\u001b[1;32m   1885\u001b[0m     memory_map\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mmemory_map\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mFalse\u001b[39;00m),\n\u001b[1;32m   1886\u001b[0m     is_text\u001b[38;5;241m=\u001b[39mis_text,\n\u001b[1;32m   1887\u001b[0m     errors\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mencoding_errors\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mstrict\u001b[39m\u001b[38;5;124m\"\u001b[39m),\n\u001b[1;32m   1888\u001b[0m     storage_options\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39moptions\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mstorage_options\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m),\n\u001b[1;32m   1889\u001b[0m )\n\u001b[1;32m   1890\u001b[0m \u001b[38;5;28;01massert\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mhandles \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[1;32m   1891\u001b[0m f \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mhandles\u001b[38;5;241m.\u001b[39mhandle\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/pandas/io/common.py:873\u001b[0m, in \u001b[0;36mget_handle\u001b[0;34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)\u001b[0m\n\u001b[1;32m    868\u001b[0m \u001b[38;5;28;01melif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(handle, \u001b[38;5;28mstr\u001b[39m):\n\u001b[1;32m    869\u001b[0m     \u001b[38;5;66;03m# Check whether the filename is to be opened in binary mode.\u001b[39;00m\n\u001b[1;32m    870\u001b[0m     \u001b[38;5;66;03m# Binary mode does not support 'encoding' and 'newline'.\u001b[39;00m\n\u001b[1;32m    871\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m ioargs\u001b[38;5;241m.\u001b[39mencoding \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mb\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m ioargs\u001b[38;5;241m.\u001b[39mmode:\n\u001b[1;32m    872\u001b[0m         \u001b[38;5;66;03m# Encoding\u001b[39;00m\n\u001b[0;32m--> 873\u001b[0m         handle \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mopen\u001b[39m(\n\u001b[1;32m    874\u001b[0m             handle,\n\u001b[1;32m    875\u001b[0m             ioargs\u001b[38;5;241m.\u001b[39mmode,\n\u001b[1;32m    876\u001b[0m             encoding\u001b[38;5;241m=\u001b[39mioargs\u001b[38;5;241m.\u001b[39mencoding,\n\u001b[1;32m    877\u001b[0m             errors\u001b[38;5;241m=\u001b[39merrors,\n\u001b[1;32m    878\u001b[0m             newline\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m\"\u001b[39m,\n\u001b[1;32m    879\u001b[0m         )\n\u001b[1;32m    880\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m    881\u001b[0m         \u001b[38;5;66;03m# Binary mode\u001b[39;00m\n\u001b[1;32m    882\u001b[0m         handle \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mopen\u001b[39m(handle, ioargs\u001b[38;5;241m.\u001b[39mmode)\n",
      "\u001b[0;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: 'R:\\\\Personal\\\\Camille Gimilaro\\\\G4_Camille\\\\G4_Camille\\\\Data (Camille.Gimilaro@tufts.edu)\\\\Malden\\\\Raw Data\\\\CPC out\\\\ML_allCPCdata.csv'"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "df= pd.read_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\CPC out\\ML_allCPCdata.csv\")\n",
    "ML_errors= df.loc[df['Status'].notnull() & (df['Status'] != 0), 'Status'].unique()\n",
    "print(ML_errors)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "edd1910e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(53,)"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ML_errors.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "id": "68a46afc",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['0' 'Conditioner Temperature Error;' 'Pulse Height Error;'\n",
      " 'Growth Tube Temperature Error;Pulse Height Error;' 'Vacuum Level Error;'\n",
      " 'Vacuum Level Error;Nozzle Flow Error;' 400 '140E' '40A' '408' '1C0F'\n",
      " '1C0E' '140C' '1408' '400' '2' '100' '102' 8 408 1 2001 2009 2409 2401\n",
      " 2101 '2101' '2105' '2107' '2100' '1' 2105 2107 2100 100 101 40 140 2 48\n",
      " 448 '140F' 4000 4100 80 20]\n"
     ]
    }
   ],
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
   "execution_count": 22,
   "id": "aabece64",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Malden</th>\n",
       "      <th>Everett</th>\n",
       "      <th>Charestown</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>140E</td>\n",
       "      <td>400</td>\n",
       "      <td>140E</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>140C</td>\n",
       "      <td>140E</td>\n",
       "      <td>408</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1408</td>\n",
       "      <td>408</td>\n",
       "      <td>400</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>408</td>\n",
       "      <td>140C</td>\n",
       "      <td>100</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>400</td>\n",
       "      <td>1408</td>\n",
       "      <td>500</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>140A</td>\n",
       "      <td>400</td>\n",
       "      <td>100</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>100</td>\n",
       "      <td>100</td>\n",
       "      <td>400</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>2900</td>\n",
       "      <td>102</td>\n",
       "      <td>900</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>900</td>\n",
       "      <td>408</td>\n",
       "      <td>4400</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>140B</td>\n",
       "      <td>900</td>\n",
       "      <td>Water Separator Error;</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10</th>\n",
       "      <td>140F</td>\n",
       "      <td>2409</td>\n",
       "      <td>Nozzle Flow Error;Water Separator Error;</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>11</th>\n",
       "      <td>402</td>\n",
       "      <td>2401</td>\n",
       "      <td>Pulse Height Error;</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>12</th>\n",
       "      <td>408</td>\n",
       "      <td>2101</td>\n",
       "      <td>Pulse Height Error;Water Separator Error;Inlet...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>13</th>\n",
       "      <td>400</td>\n",
       "      <td>2101</td>\n",
       "      <td>Pulse Height Error;Water Separator Error;</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>14</th>\n",
       "      <td>NaN</td>\n",
       "      <td>2105</td>\n",
       "      <td>Water Separator Error;Inlet Temperature Error;</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>15</th>\n",
       "      <td>5C0E</td>\n",
       "      <td>2107</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>16</th>\n",
       "      <td>5C0F</td>\n",
       "      <td>2100</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>17</th>\n",
       "      <td>540E</td>\n",
       "      <td>2105</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>18</th>\n",
       "      <td>540C</td>\n",
       "      <td>2107</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>19</th>\n",
       "      <td>5408</td>\n",
       "      <td>2100</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>20</th>\n",
       "      <td>4408</td>\n",
       "      <td>100</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21</th>\n",
       "      <td>4400</td>\n",
       "      <td>101</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>22</th>\n",
       "      <td>100</td>\n",
       "      <td>140</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23</th>\n",
       "      <td>Vacuum Level Error;Nozzle Flow Error;</td>\n",
       "      <td>448</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>24</th>\n",
       "      <td>Water Separator Error;Inlet Temperature Error;</td>\n",
       "      <td>140F</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25</th>\n",
       "      <td>Pulse Height Error;Water Separator Error;Inlet...</td>\n",
       "      <td>4100</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>26</th>\n",
       "      <td>Pulse Height Error;</td>\n",
       "      <td>20</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27</th>\n",
       "      <td>Pulse Height Error;Water Separator Error;</td>\n",
       "      <td>Pulse Height Error;</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>28</th>\n",
       "      <td>Nozzle Flow Error;Water Separator Error;</td>\n",
       "      <td>Growth Tube Temperature Error;Pulse Height Error;</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>29</th>\n",
       "      <td>Nozzle Flow Error;Water Separator Error;Inlet ...</td>\n",
       "      <td>Vacuum Level Error;Nozzle Flow Error;</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                               Malden  \\\n",
       "0                                                140E   \n",
       "1                                                140C   \n",
       "2                                                1408   \n",
       "3                                                 408   \n",
       "4                                                 400   \n",
       "5                                                140A   \n",
       "6                                                 100   \n",
       "7                                                2900   \n",
       "8                                                 900   \n",
       "9                                                140B   \n",
       "10                                               140F   \n",
       "11                                                402   \n",
       "12                                                408   \n",
       "13                                                400   \n",
       "14                                                NaN   \n",
       "15                                               5C0E   \n",
       "16                                               5C0F   \n",
       "17                                               540E   \n",
       "18                                               540C   \n",
       "19                                               5408   \n",
       "20                                               4408   \n",
       "21                                               4400   \n",
       "22                                                100   \n",
       "23              Vacuum Level Error;Nozzle Flow Error;   \n",
       "24     Water Separator Error;Inlet Temperature Error;   \n",
       "25  Pulse Height Error;Water Separator Error;Inlet...   \n",
       "26                                Pulse Height Error;   \n",
       "27          Pulse Height Error;Water Separator Error;   \n",
       "28           Nozzle Flow Error;Water Separator Error;   \n",
       "29  Nozzle Flow Error;Water Separator Error;Inlet ...   \n",
       "\n",
       "                                              Everett  \\\n",
       "0                                                 400   \n",
       "1                                                140E   \n",
       "2                                                 408   \n",
       "3                                                140C   \n",
       "4                                                1408   \n",
       "5                                                 400   \n",
       "6                                                 100   \n",
       "7                                                 102   \n",
       "8                                                 408   \n",
       "9                                                 900   \n",
       "10                                               2409   \n",
       "11                                               2401   \n",
       "12                                               2101   \n",
       "13                                               2101   \n",
       "14                                               2105   \n",
       "15                                               2107   \n",
       "16                                               2100   \n",
       "17                                               2105   \n",
       "18                                               2107   \n",
       "19                                               2100   \n",
       "20                                                100   \n",
       "21                                                101   \n",
       "22                                                140   \n",
       "23                                                448   \n",
       "24                                               140F   \n",
       "25                                               4100   \n",
       "26                                                 20   \n",
       "27                                Pulse Height Error;   \n",
       "28  Growth Tube Temperature Error;Pulse Height Error;   \n",
       "29              Vacuum Level Error;Nozzle Flow Error;   \n",
       "\n",
       "                                           Charestown  \n",
       "0                                                140E  \n",
       "1                                                 408  \n",
       "2                                                 400  \n",
       "3                                                 100  \n",
       "4                                                 500  \n",
       "5                                                 100  \n",
       "6                                                 400  \n",
       "7                                                 900  \n",
       "8                                                4400  \n",
       "9                              Water Separator Error;  \n",
       "10           Nozzle Flow Error;Water Separator Error;  \n",
       "11                                Pulse Height Error;  \n",
       "12  Pulse Height Error;Water Separator Error;Inlet...  \n",
       "13          Pulse Height Error;Water Separator Error;  \n",
       "14     Water Separator Error;Inlet Temperature Error;  \n",
       "15                                                NaN  \n",
       "16                                                NaN  \n",
       "17                                                NaN  \n",
       "18                                                NaN  \n",
       "19                                                NaN  \n",
       "20                                                NaN  \n",
       "21                                                NaN  \n",
       "22                                                NaN  \n",
       "23                                                NaN  \n",
       "24                                                NaN  \n",
       "25                                                NaN  \n",
       "26                                                NaN  \n",
       "27                                                NaN  \n",
       "28                                                NaN  \n",
       "29                                                NaN  "
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "fatal= pd.read_csv(\"/Users/camillegimilaro/Desktop/Temp/Fatal_errors.csv\")\n",
    "fatal[:30]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "id": "1581f2e8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0                                                   400\n",
      "1                                                  140E\n",
      "2                                                   408\n",
      "3                                                  140C\n",
      "4                                                  1408\n",
      "5                                                   400\n",
      "6                                                   100\n",
      "7                                                   102\n",
      "8                                                   408\n",
      "9                                                   900\n",
      "10                                                 2409\n",
      "11                                                 2401\n",
      "12                                                 2101\n",
      "13                                                 2101\n",
      "14                                                 2105\n",
      "15                                                 2107\n",
      "16                                                 2100\n",
      "17                                                 2105\n",
      "18                                                 2107\n",
      "19                                                 2100\n",
      "20                                                  100\n",
      "21                                                  101\n",
      "22                                                  140\n",
      "23                                                  448\n",
      "24                                                 140F\n",
      "25                                                 4100\n",
      "26                                                   20\n",
      "27                                  Pulse Height Error;\n",
      "28    Growth Tube Temperature Error;Pulse Height Error;\n",
      "29                Vacuum Level Error;Nozzle Flow Error;\n",
      "Name: Everett, dtype: object\n"
     ]
    }
   ],
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
   "execution_count": 24,
   "id": "df720ed3",
   "metadata": {},
   "outputs": [],
   "source": [
    "clean_ML = EV_df[~EV_df['Status'].isin(EV_fatal)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "f47a46ec",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(24606781, 3)"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "clean_ML.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "id": "945c6cf7",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(26812419, 3)"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "EV_df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "id": "44df17e8",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(25264352, 3)"
      ]
     },
     "execution_count": 62,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "no= EV_df.drop_duplicates(['Date/Time'])\n",
    "no.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "id": "55406a84-9229-40ec-91c9-625e0ade561a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "object object\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/1522707950.py:2: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  no['Status'] = no['Status'].astype(str)\n",
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/1522707950.py:4: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  no['Status'] = no['Status'].str.strip()\n"
     ]
    }
   ],
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
   "execution_count": 64,
   "id": "ad7aef87-8b9e-4a36-ba05-e47db575a03c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(23350091, 3)"
      ]
     },
     "execution_count": 64,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "clean_EV = no[~no['Status'].isin(EV_fatal)]\n",
    "clean_EV.shape                      "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "id": "f5b27341",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/4234695969.py:1: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  clean_EV['Date/Time'] = pd.to_datetime(clean_EV['Date/Time'])\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(23350091, 3)"
      ]
     },
     "execution_count": 65,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "clean_EV['Date/Time'] = pd.to_datetime(clean_EV['Date/Time'])\n",
    "sorted_EV = clean_EV.sort_values(by='Date/Time', ascending= True)\n",
    "sorted_EV.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "7d4046c1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(27369385, 4)"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "final_ML= sorted_ML.drop_duplicates(['Date/Time'])\n",
    "final_ML.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "ba48ce95",
   "metadata": {},
   "outputs": [],
   "source": [
    "final_ML.to_csv(\"R:\\Personal\\Camille Gimilaro\\G4_Camille\\G4_Camille\\Data (Camille.Gimilaro@tufts.edu)\\Malden\\Raw Data\\Cleaned CPC Data\\S25\\ML_secondly_CPC_nofatalerrors_noduplicates.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "1fb6121d",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(23344222, 3)"
      ]
     },
     "execution_count": 66,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "no_zeros= sorted_EV[sorted_EV['Conc'] >=300]\n",
    "no_zeros.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "id": "fa98b38c",
   "metadata": {},
   "outputs": [],
   "source": [
    "no_zeros.to_csv(\"/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_secondly_CPC_nofatalerrors_above300.DAT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "5b6394ae",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "         Unnamed: 0           Date/Time    Conc Status\n",
      "1174003     1174003 2023-11-14 12:44:07  7570.0      0\n",
      "1174004     1174004 2023-11-14 12:44:09  7770.0      0\n",
      "1174005     1174005 2023-11-14 12:44:10  7620.0      0\n",
      "1174006     1174006 2023-11-14 12:44:11  7500.0      0\n",
      "1174007     1174007 2023-11-14 12:44:12  7820.0      0\n"
     ]
    }
   ],
   "source": [
    "print(final_ML.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "id": "9a355e6e",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/600225531.py:10: FutureWarning: 'H' is deprecated and will be removed in a future version, please use 'h' instead.\n",
      "  hourly_data = final_ML['Conc'].resample('H').mean()\n"
     ]
    }
   ],
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
    "output_file = '/Users/camillegimilaro/Desktop/Temp/EV AIM /EV_hourly_CPC_nofatalerrors_above300.DAT'\n",
    "convert_to_hourly(no_zeros, output_file)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 83,
   "id": "16c22c36-c9be-4022-b055-68ccb544c0a8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          Date/Time      Conc\n",
      "0  10/26/2023 10:00  15431.79\n",
      "1  10/26/2023 11:00       NaN\n",
      "2  10/26/2023 12:00       NaN\n",
      "3  10/26/2023 13:00       NaN\n",
      "4  10/26/2023 14:00       NaN\n"
     ]
    }
   ],
   "source": [
    "df= pd.read_csv(output_file, names=['Date/Time', 'Conc'])\n",
    "print(df.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 97,
   "id": "e28a5427-783c-4843-9fe6-69fbb23e2205",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/var/folders/_j/73q2vkp102d5fvjsj2tnjzzh0000gn/T/ipykernel_1962/2776119675.py:1: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  no_zeros= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/CH_out/allmerge.DAT')\n"
     ]
    }
   ],
   "source": [
    "no_zeros= pd.read_csv('/Users/camillegimilaro/Desktop/Temp/CH_out/allmerge.DAT')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 100,
   "id": "c0014945",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Missing full days: [datetime.date(2024, 3, 5), datetime.date(2024, 3, 6), datetime.date(2024, 3, 7), datetime.date(2024, 3, 8), datetime.date(2024, 3, 9), datetime.date(2024, 5, 9), datetime.date(2024, 5, 10), datetime.date(2024, 5, 11), datetime.date(2024, 5, 12), datetime.date(2024, 5, 13), datetime.date(2024, 5, 14), datetime.date(2024, 5, 24), datetime.date(2024, 5, 25), datetime.date(2024, 5, 26), datetime.date(2024, 5, 27), datetime.date(2024, 6, 19), datetime.date(2024, 6, 20), datetime.date(2024, 6, 21), datetime.date(2024, 6, 22), datetime.date(2024, 6, 23), datetime.date(2024, 6, 24), datetime.date(2024, 6, 25), datetime.date(2024, 11, 22), datetime.date(2024, 11, 23), datetime.date(2024, 11, 24), datetime.date(2024, 12, 11), datetime.date(2024, 12, 12), datetime.date(2024, 12, 26), datetime.date(2024, 12, 27), datetime.date(2025, 1, 8), datetime.date(2025, 1, 16)]\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "no_zeros = no_zeros.drop(index=5849252)\n",
    "# Ensure 'Date/Time' is in datetime format\n",
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
  },
  {
   "cell_type": "markdown",
   "id": "860694e2-c665-469d-bd30-57c9d326b958",
   "metadata": {},
   "source": [
    "Malden: \n",
    "\n",
    "Dates in Jennifer's missing data list but not actually missing:\n",
    "\n",
    "November 21, 2023\n",
    "\n",
    "March 5, 2024\n",
    "\n",
    "July 18, 2024\n",
    "\n",
    "October 30, 2024\n",
    "\n",
    "\n",
    "Days of missing data but not in Jennifer's missing data list:\n",
    "\n",
    "March 31, 2024\n",
    "\n",
    "April 12, 2024\n",
    "\n",
    "July 25, 2024\n",
    "\n",
    "July 26, 2024\n",
    "\n",
    "July 27, 2024\n",
    "\n",
    "July 28, 2024\n",
    "\n",
    "July 29, 2024"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9bbe311e-237d-4c38-be7c-31f94f728d2f",
   "metadata": {},
   "source": [
    "Everett\n",
    "\n",
    "Dates in Jennifer's missing data list but not actually missing:\n",
    "\n",
    "November 21, 2023\n",
    "\n",
    "November 22, 2023\n",
    "\n",
    "November 28, 2023\n",
    "\n",
    "May 23, 2024\n",
    "\n",
    "November 7, 2024\n",
    "\n",
    "November 8, 2024\n",
    "\n",
    "November 9, 2024\n",
    "\n",
    "November 10, 2024\n",
    "\n",
    "November 11, 2024\n",
    "\n",
    "November 12, 2024\n",
    "\n",
    "November 13, 2024\n",
    "\n",
    "November 14, 2024\n",
    "\n",
    "November 15, 2024\n",
    "\n",
    "November 16, 2024\n",
    "\n",
    "November 17, 2024\n",
    "\n",
    "November 18, 2024\n",
    "\n",
    "November 19, 2024\n",
    "\n",
    "November 20, 2024\n",
    "\n",
    "November 21, 2024\n",
    "\n",
    "Dates missing in the data but not in Jennifer's missing data list:\n",
    "\n",
    "October 15, 2024\n",
    "\n",
    "October 16, 2024\n",
    "\n",
    "October 17, 2024\n",
    "\n",
    "October 18, 2024\n",
    "\n",
    "October 19, 2024\n",
    "\n",
    "October 20, 2024\n",
    "\n",
    "October 21, 2024\n",
    "\n",
    "October 22, 2024\n",
    "\n",
    "November 4, 2024"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7f310d13-6783-48a3-ba58-ab8dd46678af",
   "metadata": {},
   "source": [
    "Charlestown:\n",
    "\n",
    "Dates actually missing but not in Jennifer's missing data list:\n",
    "\n",
    "January 16, 2025\n",
    "\n",
    "Dates in Jennifer's missing data list but not actually missing:\n",
    "\n",
    "March 10, 2024\n",
    "\n",
    "May 23, 2024\n",
    "\n",
    "July 18, 2024"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fa6985e2-28ab-4e20-adf3-da7e51db20ba",
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
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
