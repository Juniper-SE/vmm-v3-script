#!/bin/bash
for i in spine{1..2} sw{1..2} leaf{1..5}
do
  ssh ${i} "show configuration" > ${i}.conf
done

