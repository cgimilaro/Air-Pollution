{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "21bc2742",
   "metadata": {},
   "source": [
    "# 1. Combine all .DAT files together"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "96c71644",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "\n",
    "def join_dat_files(input_folder, output_file):\n",
    "    with open(output_file, 'wb') as outfile:  # Use 'wb' for binary files\n",
    "        for filename in os.listdir(input_folder):\n",
    "            if filename.endswith('.DAT'):\n",
    "                with open(os.path.join(input_folder, filename), 'rb') as infile:  # Use 'rb' for binary files\n",
    "                    lines = infile.readlines()[6:]  # Skip the first 6 lines\n",
    "                    outfile.writelines(lines)\n",
    "\n",
    "input_folder = \"R:/Personal/Kaustuv Ray/Dulles sites/Localizer/Feb\"\n",
    "output_file = \"R:/Personal/Kaustuv Ray/Dulles sites/Localizer/data analysis/Feb/file1.DAT\"\n",
    "\n",
    "\n",
    "join_dat_files(input_folder, output_file)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "39b86c65",
   "metadata": {},
   "source": [
    "# 2.  DATE-TIME Combination and Format changing + Column extraction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "47c3ce6b",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "input_file = \"/Users/camillegimilaro/Desktop/Temp/merged.DAT\"\n",
    "output_file = \"/Users/camillegimilaro/Desktop/Temp/CH_out/merge.DAT\"\n",
    "\n",
    "# Step 1: Change date format\n",
    "def change_date_format(date_str):\n",
    "    year, month, day = date_str.split('/')\n",
    "    return f'{month}/{day}/{year}'\n",
    "\n",
    "# Step 2: Combine date and time\n",
    "def combine_date_and_time(row):\n",
    "    return row[0] + ' ' + row[1]\n",
    "\n",
    "\n",
    "\n",
    "# Read the input file and process data\n",
    "with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:\n",
    "    for line in infile:\n",
    "        # Split the line into a list of values\n",
    "        row = line.strip().split(',')\n",
    "        \n",
    "        # Step 1: Change date format\n",
    "        row[0] = change_date_format(row[0])\n",
    "        \n",
    "        # Step 2: Combine date and time\n",
    "        row[1] = combine_date_and_time(row)\n",
    "        \n",
    "        # Step 3: Extract columns\n",
    "        new_row = [row[1], row[2]] + row[-3:]\n",
    "        \n",
    "        # Write the processed row to the output file\n",
    "        outfile.write(','.join(new_row) + '\\n')"
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
