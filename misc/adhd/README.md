# Ruke Engine Brute Force

Present a rule engine interface with certain variables injected into it. Only comparisons are allowed in the rule engine, no data extraction. Bruteforce the flag by comparing each index of the flag.

## Application

- Golang TCP Server interface
- Use [expr](https://github.com/antonmedv/expr) to evaluate rules and inject variables into a evaluator context.
