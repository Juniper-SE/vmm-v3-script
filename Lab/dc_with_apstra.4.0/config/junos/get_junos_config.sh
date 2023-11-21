#!/bin/bash
for i in pe1 pe2 p1 ext1
do
  ssh ${i} "show configuration" > ${i}.conf
done

