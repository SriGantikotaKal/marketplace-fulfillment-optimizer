# Marketplace Fulfillment Optimizer

A Python optimizer that assigns orders to fulfillment nodes using capacity, delivery SLA, and distance. It targets marketplace, delivery, logistics, and commerce companies where backend systems need deterministic allocation behavior.

## Highlights

- Chooses the best fulfillment node without over-allocating capacity
- Prioritizes SLA-safe assignments and explains why nodes were skipped
- Supports deterministic behavior for tests and operations reviews

## Run

```powershell
python -m unittest discover -s tests
```

