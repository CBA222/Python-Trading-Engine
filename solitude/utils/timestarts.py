# -*- coding: utf-8 -*-

def get_month_starts(index):
    starts = [index[0]]
    for i in range(len(index)):
        if index[i].month != starts[-1].month:
            starts.append(index[i])
    return set(starts)

def get_week_starts(index):
    starts = [index[0]]
    for i in range(len(index)):
        if index[i].week != starts[-1].week:
            starts.append(index[i])
    return set(starts)
