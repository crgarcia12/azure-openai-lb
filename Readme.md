# Kusto queries

```kql
search "oai state:"
| where timestamp > ago(10m)
| extend client1 = toint(substring(message,13,1))
| extend client2 = toint(substring(message,16,1))
| project timestamp, client1, client2
| summarize oai1=max(client1), oai2=max(client2) by bin(timestamp, 20s)
| render timechart

search "oai:"
| where timestamp > ago(10m)
| extend instance_used = extract(@"oai: (\d+)", 1, message)
| summarize count() by instance_used, bin(timestamp, 40s)
| project timestamp, instance_used, count_
| render timechart

union * 
| where timestamp > ago(10m)
| where * contains 'Duration:'
| extend duration = toint(extract(@"(\d+) msec", 1, message))
| summarize min(duration), avg(duration), max(duration) by bin(timestamp, 40s)
| render timechart

union * 
| where timestamp > ago(10m)
| where * contains 'Duration:'
| extend duration = toint(extract(@"(\d+) msec", 1, message))
| summarize count() by bin(timestamp, 40s)
| render timechart
```