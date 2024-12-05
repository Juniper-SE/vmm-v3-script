#!/bin/bash
for i in ce{1..2} p{1..4} 
do
	ssh ${i} "edit; load merge relative ${i}.conf; commit"
done
