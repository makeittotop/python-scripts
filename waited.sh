#! /bin/sh

n=5
while [ $n -gt 0 ]; do
    ns=`date +%N`
    p=`expr $ns % 10 + 10`
    sleep $p
    echo waited $p
    n=`expr $n - 1`
done
