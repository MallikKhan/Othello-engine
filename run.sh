#!/bin/bash

# Assign the input file paths and initial time limits
file1=$1
file2=$2
output_file="results.txt"

# Clear the output file if it already exists
> $output_file

# Function to run othellostart and filter the results
run_othello() {
  file1=$1
  file2=$2
  for time_limit in {2..5}
  do
    echo "Running with $file1 vs $file2 and time limit $time_limit" | tee -a $output_file
    /home/leantan/Projects/5dv243ht24/Othello/test_code/othellostart $file1 $file2 $time_limit | grep -E '^\*{10,}|^Results|^(White|Black) won|^Average time' >> $output_file
  done
}

# Run the program with the original file order
run_othello $file1 $file2

# Swap the file paths
run_othello $file2 $file1
